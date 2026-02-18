import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.append(str(Path(__file__).resolve().parents[1]))
from _bootstrap_agentscope_codebase import ensure_local_agentscope  # noqa: E402

ensure_local_agentscope()

import agentscope
from agentscope._logging import logger as log
from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.message import Msg, ToolUseBlock
from agentscope.model import OpenAIChatModel
from agentscope.tool import ToolResponse

from global_model_config import MODEL_NAME, get_openai_chat_model_kwargs
from tools.registry import build_toolkit


def extract_text_from_tool_resp(resp: ToolResponse) -> str:
    parts: list[str] = []
    for block in resp.content:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(str(block.get("text", "")))
    return " ".join(parts).strip()


def extract_msg_text(msg: Msg) -> str:
    content = msg.content if hasattr(msg, "content") else msg
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text" and item.get("text"):
                    parts.append(str(item["text"]))
            elif hasattr(item, "text"):
                text = getattr(item, "text")
                if text:
                    parts.append(str(text))
        return " ".join(parts).strip()
    return str(content)


def parse_json_from_text(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass

    matches = re.findall(r"\{[\s\S]*\}", text)
    for candidate in reversed(matches):
        try:
            return json.loads(candidate)
        except Exception:
            continue
    return {"raw_reply": text}


def register_skills(toolkit) -> list[str]:
    skills_root = Path(__file__).resolve().parent / "skills"
    skill_names: list[str] = []
    for skill_dir in sorted(skills_root.iterdir()):
        if skill_dir.is_dir():
            toolkit.register_agent_skill(str(skill_dir))
            skill_names.append(skill_dir.name)
    return skill_names


async def run_stock_hot_topic_case(topic: str, horizon: str, risk: str) -> dict[str, Any]:
    tool_trace: list[dict[str, Any]] = []

    def capture_tool_call(tool_call: ToolUseBlock, tool_resp: ToolResponse) -> ToolResponse:
        inp = dict(tool_call.get("input", {}))
        snippet = extract_text_from_tool_resp(tool_resp)[:200]
        tool_trace.append(
            {"tool": tool_call["name"], "input": inp, "result_snippet": snippet},
        )
        log.info(
            "[工具调用] name=%s input=%s result_snippet=%s",
            tool_call["name"],
            inp,
            snippet,
        )
        return tool_resp

    agentscope.init(
        project="agentscope-learning",
        name="70-examples-llm-driven",
        logging_level="DEBUG",
    )
    toolkit = await build_toolkit(postprocess_func=capture_tool_call)
    skill_names = register_skills(toolkit)

    model = OpenAIChatModel(**get_openai_chat_model_kwargs(MODEL_NAME))
    formatter = OpenAIChatFormatter()

    skill_prompt = toolkit.get_agent_skill_prompt()
    sys_prompt = (
        "你是一个热点驱动的产业链投资研究智能体。\n\n"
        "【语言要求，全程遵守】无论工具返回或上下文是否含英文，你的每一步都必须用中文：\n"
        "- 每一轮「思考」必须用中文写；\n"
        "- 对工具结果的解读、分析、总结必须用中文；\n"
        "- 中间结论和最终 JSON 内容（字段取值、说明文字）必须用中文。\n"
        "禁止在推理或回复中切换为英文。\n\n"
        "执行方式必须是 observe -> think -> tool act -> observe 的迭代。"
        "必须优先使用工具获取数据与证据，不允许凭空编造。\n\n"
        "工具调用预算不超过 12 次，避免重复调用同一工具。"
        "达到结论后必须立即输出 JSON，不要继续推理。\n\n"
        "你必须至少调用这些工具（可多次）: "
        "discover_hot_topics, build_industry_chain, map_listed_companies, "
        "link_supply_chain, analyze_core_technology, analyze_business_model_shift, "
        "rank_investment_candidates, generate_deep_dive_report, "
        "web_search_news, search_company_filings。\n\n"
        "最终输出必须是严格 JSON 对象，包含字段: "
        "hot_topic, industry_chain_map, candidate_pool, top_pick, "
        "top_pick_deep_dive, business_model_shift, key_risks, evidence, action_plan.\n\n"
        "以下是可用 skills 说明：\n"
        f"{skill_prompt}"
    )

    agent = ReActAgent(
        name="stock_hot_topic_agent",
        sys_prompt=sys_prompt,
        model=model,
        formatter=formatter,
        toolkit=toolkit,
        parallel_tool_calls=True,
        max_iters=10,
        print_hint_msg=False,
    )

    user_prompt = (
        "请基于热点概念做完整投资分析，全部使用中文作答。\n"
        f"主题偏好: {topic}; 投资期限: {horizon}; 风险偏好: {risk}。\n"
        "流程要求：热点发现 -> 产业链上下游 -> 相关企业和供应链 -> "
        "核心技术和商业模式变革 -> 标的筛选和深度分析。\n"
        "请输出严格 JSON，不要输出 markdown；JSON 内的说明、结论等文字均用中文。"
    )
    log.info("开始 Agent 调用 topic=%s horizon=%s risk=%s", topic, horizon, risk)
    response = await agent(Msg(name="user", role="user", content=user_prompt))
    log.info("Agent 调用结束，解析回复与报告")
    reply_text = extract_msg_text(response)
    report = parse_json_from_text(reply_text)

    report["meta"] = {
        "driver": "ReActAgent (LLM-driven)",
        "model": MODEL_NAME,
        "skills_loaded": skill_names,
        "skills_count": len(skill_names),
        "tools_count": len(toolkit.tools),
        "tools_used": sorted({x["tool"] for x in tool_trace}),
        "tool_calls_count": len(tool_trace),
        "tool_trace": tool_trace,
    }

    required_tools = {
        "discover_hot_topics",
        "build_industry_chain",
        "map_listed_companies",
        "link_supply_chain",
        "analyze_core_technology",
        "analyze_business_model_shift",
        "rank_investment_candidates",
        "generate_deep_dive_report",
        "web_search_news",
        "search_company_filings",
    }
    used = set(report["meta"]["tools_used"])
    missing = sorted(required_tools - used)
    report["meta"]["required_tools_missing"] = missing

    return report


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default="AI算力")
    parser.add_argument("--horizon", default="中期")
    parser.add_argument("--risk", default="中等")
    args = parser.parse_args()

    result = await run_stock_hot_topic_case(
        topic=args.topic,
        horizon=args.horizon,
        risk=args.risk,
    )

    out_dir = Path(__file__).resolve().parent / "output"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "latest_stock_hot_topic_report.json"
    out_file.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== Stock Hot Topic Case Completed (LLM-driven) ===")
    print(f"topic     : {result.get('hot_topic', args.topic)}")
    top_pick = result.get("top_pick")
    if isinstance(top_pick, dict):
        top_pick_str = top_pick.get("symbol", "N/A")
    else:
        top_pick_str = str(top_pick) if top_pick else "N/A"
    print(f"top_pick  : {top_pick_str}")
    print(f"tool_calls: {result.get('meta', {}).get('tool_calls_count', 0)}")
    print(f"report    : {out_file}")


if __name__ == "__main__":
    asyncio.run(main())
