"""产业链与投资分析工具：热点、产业链、标的映射、打分与深度报告。"""
from typing import Any

from .common import google_news_rss, text_response


def discover_hot_topics(window_days: int = 7, market: str = "CN_US"):
    """根据近期新闻热度发现市场热点主题。"""
    topic_queries = {
        "AI算力": "AI 算力 芯片 数据中心 产业链",
        "人形机器人": "人形机器人 供应链 减速器 伺服",
        "低空经济": "低空经济 eVTOL 无人机 产业",
        "智能汽车": "智能驾驶 激光雷达 供应链",
    }
    ranking: list[dict[str, Any]] = []
    for topic, query in topic_queries.items():
        news = google_news_rss(query=query, days=window_days)
        ranking.append(
            {
                "topic": topic,
                "market": market,
                "heat": len(news),
                "sample_news": news[:3],
            },
        )
    ranking.sort(key=lambda x: x["heat"], reverse=True)
    return text_response(ranking)


def build_industry_chain(topic: str):
    """按热点主题构建上中下游产业链。"""
    mapping = {
        "AI算力": {
            "upstream": ["先进制程", "EDA/IP", "HBM/存储"],
            "midstream": ["GPU/ASIC", "服务器", "液冷"],
            "downstream": ["云服务", "行业AI应用"],
        },
        "人形机器人": {
            "upstream": ["稀土磁材", "高端轴承", "传感器"],
            "midstream": ["减速器", "伺服系统", "本体集成"],
            "downstream": ["工业制造", "物流服务", "家庭服务"],
        },
    }
    chain = mapping.get(topic, mapping["AI算力"])
    return text_response({"topic": topic, "chain": chain})


def map_listed_companies(chain_node: str, market: str = "CN_US"):
    """将上市公司映射到指定产业链环节。"""
    companies = {
        "GPU/ASIC": [
            {"symbol": "NVDA", "name": "NVIDIA", "market": "US"},
            {"symbol": "AMD", "name": "AMD", "market": "US"},
        ],
        "服务器": [
            {"symbol": "000063.SZ", "name": "中兴通讯", "market": "CN"},
            {"symbol": "000977.SZ", "name": "浪潮信息", "market": "CN"},
        ],
        "液冷": [
            {"symbol": "300308.SZ", "name": "中际旭创", "market": "CN"},
            {"symbol": "300763.SZ", "name": "锦浪科技", "market": "CN"},
        ],
        "云服务": [
            {"symbol": "BABA", "name": "阿里巴巴", "market": "US"},
            {"symbol": "MSFT", "name": "微软", "market": "US"},
        ],
    }
    return text_response(companies.get(chain_node, []))


def link_supply_chain(company: str):
    """返回某公司的简化供应商/客户关系。"""
    links = {
        "NVDA": {"suppliers": ["TSM", "SK hynix"], "customers": ["MSFT", "AMZN"]},
        "AMD": {"suppliers": ["TSM"], "customers": ["META", "ORCL"]},
        "000977.SZ": {"suppliers": ["CPU/GPU厂商"], "customers": ["云厂商", "运营商"]},
        "BABA": {"suppliers": ["服务器厂商"], "customers": ["企业客户", "开发者"]},
    }
    return text_response(links.get(company, {"suppliers": [], "customers": []}))


def analyze_core_technology(company_or_chain_node: str):
    """分析公司或产业链环节的技术壁垒。"""
    text = f"{company_or_chain_node} 核心技术壁垒：工艺良率、系统集成能力、生态兼容性。"
    moat = 80 if company_or_chain_node in {"NVDA", "MSFT", "BABA"} else 65
    return text_response({"summary": text, "moat_score": moat})


def analyze_business_model_shift(company: str, topic: str):
    """分析热点驱动下该公司的商业模式变革。"""
    shift = {
        "mode": "一次性硬件收入 -> 软硬一体 + 服务订阅",
        "impact": "毛利率与现金流质量提升",
        "score": 75 if topic == "AI算力" else 60,
    }
    return text_response(shift)


def rank_investment_candidates(
    candidates: list[dict[str, Any]],
    scoring_config: dict[str, float],
):
    """按加权因子对候选公司打分排序。"""
    ranked: list[dict[str, Any]] = []
    for c in candidates:
        score = (
            c.get("tech_moat", 0) * scoring_config.get("tech_moat", 0.35)
            + c.get("business_shift", 0) * scoring_config.get("business_shift", 0.25)
            + c.get("chain_position", 0) * scoring_config.get("chain_position", 0.2)
            + c.get("valuation", 0) * scoring_config.get("valuation", 0.2)
        )
        item = dict(c)
        item["score"] = round(score, 2)
        ranked.append(item)
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return text_response(ranked)


def generate_deep_dive_report(symbol: str, context: dict[str, Any]):
    """为选定标的生成深度分析报告。"""
    report = {
        "symbol": symbol,
        "thesis": context.get("thesis", ""),
        "core_technology": context.get("core_technology", ""),
        "business_model_shift": context.get("business_model_shift", ""),
        "supply_chain": context.get("supply_chain", {}),
        "risks": context.get("risks", []),
        "valuation_view": context.get("valuation_view", ""),
        "action_plan": context.get("action_plan", ""),
    }
    return text_response(report)
