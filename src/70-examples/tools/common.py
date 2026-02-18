"""工具公共方法：统一响应格式、抓取与新闻 RSS。"""
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any

from agentscope.tool import ToolResponse


def text_response(payload: Any) -> ToolResponse:
    """将 payload 转为工具文本响应。"""
    if isinstance(payload, str):
        text = payload
    else:
        text = json.dumps(payload, ensure_ascii=False)
    return ToolResponse(content=[{"type": "text", "text": text}])


def fetch_text(url: str, timeout: int = 10) -> str:
    """根据 URL 抓取文本内容。"""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def google_news_rss(query: str, days: int = 7) -> list[dict[str, str]]:
    """按关键词与天数从 Google 新闻 RSS 获取条目列表。"""
    rss_url = (
        "https://news.google.com/rss/search?q="
        + urllib.parse.quote(query)
        + urllib.parse.quote(" when:")
        + urllib.parse.quote(f"{days}d")
        + "&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    )
    items: list[dict[str, str]] = []
    try:
        xml_text = fetch_text(rss_url, timeout=10)
        root = ET.fromstring(xml_text)
        for item in root.findall(".//item")[:8]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            if title and link:
                items.append({"title": title, "url": link})
    except Exception as exc:
        items = [{"title": f"搜索回退: {query}", "url": f"error://{exc}"}]
    return items
