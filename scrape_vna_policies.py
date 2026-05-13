from __future__ import annotations

import json
import re
import time
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE_URL = "https://www.vietnamairlines.com"
OUTPUT_DIR = Path("data")

SEED_URLS = [
    "/vn/vi/legal/privacy-policy",
    "/vn/vi/legal/terms-and-conditions",
    "/vn/vi/legal/conditions-of-carriage",
    "/vn/vi/legal/cookies-policy",
    "/vn/vi/legal/quy-che-hoat-dong-san-tmdt",
    "/vn/vi/legal/conditions-of-online-booking",
    "/vn/vi/legal/conditions-of-check-in-cancellation",
    "/vn/vi/support/customer-service-plan",
]

ALLOWED_PATH_PREFIXES = (
    "/vn/vi/legal/",
    "/vn/vi/support/customer-service-plan",
)

STOP_SECTION_TITLES = {
    "quý khách có hài lòng với thông tin đã tìm được?",
    "vietnam airlines",
    "hỗ trợ",
    "pháp lý",
    "thông tin hữu ích",
    "vận tải hàng hóa",
    "giải thưởng của vietnam airlines",
    "additional links",
}


@dataclass
class PolicyPage:
    url: str
    title: str
    slug: str
    depth: int
    parent_url: str | None
    body_markdown: str
    body_text: str
    links: list[dict[str, str]]
    word_count: int
    scraped_at: str


def create_session() -> requests.Session:
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset({"GET"}),
    )
    session = requests.Session()
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_html(session: requests.Session, url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout as e:
        print(f"⚠️  Timeout on {url}: {e}")
        # Retry once more with longer timeout
        time.sleep(2)
        return session.get(url, headers=headers, timeout=60).text
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        raise


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def html_filename_for_url(url: str) -> str:
    path = urlparse(url).path.strip("/") or "index"
    filename = re.sub(r"[^a-zA-Z0-9._-]+", "__", path)
    return f"{filename}.html"


def is_allowed_policy_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc != "www.vietnamairlines.com":
        return False
    if parsed.path.lower().endswith(".pdf"):
        return False
    return any(parsed.path.startswith(prefix) for prefix in ALLOWED_PATH_PREFIXES)


def is_stop_section(block_name: str | None, text: str) -> bool:
    normalized = clean_text(text).lower()
    if not normalized:
        return False
    if block_name in {"h2", "h3", "h4", "h5", "h6", "p", "div"}:
        return normalized in STOP_SECTION_TITLES
    return False


def slugify_url(url: str) -> str:
    path = urlparse(url).path.rstrip("/")
    slug = path.split("/")[-1] or "index"
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", slug).strip("-")
    return slug or "index"


def choose_content_container(soup: BeautifulSoup):
    return soup.find("div", class_="vna-main-content") or soup.find("main") or soup.body or soup


def iter_content_blocks(container):
    block_tags = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "th", "td", "blockquote", "figcaption"}
    started = False
    for element in container.find_all(block_tags):
        text = clean_text(element.get_text(" ", strip=True))
        if not text:
            continue
        if not started:
            if element.name == "h1":
                started = True
            else:
                continue
        if is_stop_section(element.name, text):
            break
        yield element, text


def extract_markdown(container) -> str:
    for tag in container.select("script, style, noscript"):
        tag.decompose()

    lines: list[str] = []
    seen: set[str] = set()

    for element, text in iter_content_blocks(container):

        key = text.lower()
        if key in seen:
            continue
        seen.add(key)

        if element.name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = min(int(element.name[1]), 6)
            prefix = "#" * level
            lines.append(f"{prefix} {text}")
        elif element.name == "li":
            lines.append(f"- {text}")
        else:
            lines.append(text)

    return "\n\n".join(lines).strip()


def extract_links(container, base_url: str) -> list[dict[str, str]]:
    links: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for block, _ in iter_content_blocks(container):
        for anchor in block.find_all("a", href=True):
            text = clean_text(anchor.get_text(" ", strip=True))
            href = urljoin(base_url, anchor["href"])
            key = (text.lower(), href)
            if not text or key in seen:
                continue
            seen.add(key)
            links.append({"text": text, "href": href})
    return links


def save_html_snapshot(url: str, html: str) -> None:
    html_dir = OUTPUT_DIR / "html"
    html_dir.mkdir(parents=True, exist_ok=True)
    (html_dir / html_filename_for_url(url)).write_text(html, encoding="utf-8")


def build_policy_page(session: requests.Session, url: str, depth: int = 0, parent_url: str | None = None) -> PolicyPage:
    html = fetch_html(session, url)
    save_html_snapshot(url, html)
    soup = BeautifulSoup(html, "lxml")
    title_node = soup.find("h1")
    title = clean_text(title_node.get_text(" ", strip=True)) if title_node else clean_text((soup.title.string if soup.title else ""))
    container = choose_content_container(soup)
    markdown = extract_markdown(container)
    links = extract_links(container, url)
    body_text = clean_text(BeautifulSoup(markdown.replace("\n", " "), "html.parser").get_text(" ", strip=True))
    return PolicyPage(
        url=url,
        title=title,
        slug=slugify_url(url),
        depth=depth,
        parent_url=parent_url,
        body_markdown=markdown,
        body_text=body_text,
        links=links,
        word_count=len(body_text.split()),
        scraped_at=datetime.now(timezone.utc).isoformat(),
    )


def crawl_policy_pages(seed_urls: list[str], max_depth: int = 4) -> list[PolicyPage]:
    session = create_session()
    queue = deque((canonicalize_url(url), 0, None) for url in seed_urls)
    visited: dict[str, PolicyPage] = {}

    while queue:
        url, depth, parent_url = queue.popleft()
        if url in visited:
            continue

        print(f"[{len(visited) + 1}] Fetching: {url}")
        try:
            page = build_policy_page(session, url, depth=depth, parent_url=parent_url)
        except Exception as exc:
            print(f"  ✗ Failed: {exc}")
            continue

        visited[url] = page
        print(f"  ✓ Success: {page.title} ({page.word_count} words)")

        if depth >= max_depth:
            continue

        for link in page.links:
            href = canonicalize_url(link["href"])
            if href in visited or not is_allowed_policy_url(href):
                continue
            queue.append((href, depth + 1, url))

        time.sleep(1.5)

    return list(visited.values())


def write_outputs(pages: list[PolicyPage]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = [asdict(page) for page in pages]
    (OUTPUT_DIR / "vietnamairlines_public_policies.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md_parts = ["# Vietnam Airlines public policy scrape", ""]
    for page in pages:
        md_parts.extend(
            [
                f"## {page.title}",
                f"URL: {page.url}",
                f"Slug: {page.slug}",
                f"Depth: {page.depth}",
                f"Parent URL: {page.parent_url or '(seed)'}",
                f"Word count: {page.word_count}",
                "",
                page.body_markdown or "(No body extracted)",
                "",
            ]
        )
    (OUTPUT_DIR / "vietnamairlines_public_policies.md").write_text("\n".join(md_parts).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    seed_urls = [urljoin(BASE_URL, relative_url) for relative_url in SEED_URLS]
    pages = crawl_policy_pages(seed_urls)

    if pages:
        write_outputs(pages)
        print(f"\n✓ Saved {len(pages)} policy pages to {OUTPUT_DIR.resolve()}")
    else:
        print("❌ No pages scraped.")


if __name__ == "__main__":
    main()
