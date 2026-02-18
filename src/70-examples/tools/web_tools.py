from typing import Any

from .common import fetch_text, google_news_rss, text_response


def web_search_news(query: str, days: int = 7):
    """Search online news by query and time window."""
    return text_response(google_news_rss(query=query, days=days))


def web_fetch_article(url: str):
    """Fetch article content and return a short snippet."""
    try:
        text = fetch_text(url, timeout=10)
        return text_response({"url": url, "snippet": text[:1000]})
    except Exception as exc:
        return text_response({"url": url, "snippet": f"fetch failed: {exc}"})


def search_company_filings(symbol_or_cik: str):
    """Return filing search links for CN/US markets."""
    if "." in symbol_or_cik:
        links = [f"https://www.cninfo.com.cn/new/fulltextSearch?keyWord={symbol_or_cik}"]
    else:
        links = [f"https://www.sec.gov/edgar/search/#/q={symbol_or_cik}"]
    return text_response({"symbol": symbol_or_cik, "filings": links})


def extract_evidence_links(claims: list[dict[str, Any]]):
    """Collect unique evidence links from claims."""
    seen: set[str] = set()
    links: list[dict[str, str]] = []
    for c in claims:
        url = str(c.get("url", "")).strip()
        if not url or url in seen:
            continue
        seen.add(url)
        links.append({"claim": str(c.get("claim", "")), "url": url, "source": str(c.get("source", ""))})
    return text_response(links)
