"""联网与证据类工具：新闻搜索、抓取正文、公告检索、证据链接。"""
from typing import Any

from .common import fetch_text, google_news_rss, text_response


def web_search_news(query: str, days: int = 7):
    """按关键词与时间窗口搜索在线新闻。"""
    return text_response(google_news_rss(query=query, days=days))


def web_fetch_article(url: str):
    """抓取文章正文并返回短摘要。"""
    try:
        text = fetch_text(url, timeout=10)
        return text_response({"url": url, "snippet": text[:1000]})
    except Exception as exc:
        return text_response({"url": url, "snippet": f"抓取失败: {exc}"})


def search_company_filings(symbol_or_cik: str):
    """返回 A 股/美股公告检索链接。"""
    if "." in symbol_or_cik:
        links = [f"https://www.cninfo.com.cn/new/fulltextSearch?keyWord={symbol_or_cik}"]
    else:
        links = [f"https://www.sec.gov/edgar/search/#/q={symbol_or_cik}"]
    return text_response({"symbol": symbol_or_cik, "filings": links})


def extract_evidence_links(claims: list[dict[str, Any]]):
    """从论断列表中收集不重复的证据链接。"""
    seen: set[str] = set()
    links: list[dict[str, str]] = []
    for c in claims:
        url = str(c.get("url", "")).strip()
        if not url or url in seen:
            continue
        seen.add(url)
        links.append({"claim": str(c.get("claim", "")), "url": url, "source": str(c.get("source", ""))})
    return text_response(links)
