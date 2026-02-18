"""工具注册：构建 core / web / MCP 工具组并注册到 Toolkit。"""
from typing import Awaitable, Callable

from agentscope.message import ToolUseBlock
from agentscope.tool import ToolResponse, Toolkit

from .analysis_tools import (
    analyze_business_model_shift,
    analyze_core_technology,
    build_industry_chain,
    discover_hot_topics,
    generate_deep_dive_report,
    link_supply_chain,
    map_listed_companies,
    rank_investment_candidates,
)
from .mcp_mocks import FinanceMCPMock, SearchMCPMock
from .web_tools import extract_evidence_links, search_company_filings, web_fetch_article, web_search_news


PostprocessType = Callable[[ToolUseBlock, ToolResponse], ToolResponse | None] | Callable[
    [ToolUseBlock, ToolResponse],
    Awaitable[ToolResponse | None],
]


async def build_toolkit(postprocess_func: PostprocessType | None = None) -> Toolkit:
    """构建股票案例工具集：核心分析、联网与证据、MCP 模拟。"""
    toolkit = Toolkit()
    toolkit.create_tool_group("core_tools", description="股票核心分析工具", active=True)
    toolkit.create_tool_group("web_tools", description="联网搜索与证据工具", active=True)
    toolkit.create_tool_group("mcp_tools", description="MCP 服务工具", active=True)

    core = [
        discover_hot_topics,
        build_industry_chain,
        map_listed_companies,
        link_supply_chain,
        analyze_core_technology,
        analyze_business_model_shift,
        rank_investment_candidates,
        generate_deep_dive_report,
    ]
    web = [
        web_search_news,
        web_fetch_article,
        search_company_filings,
        extract_evidence_links,
    ]
    for func in core:
        toolkit.register_tool_function(
            func,
            group_name="core_tools",
            postprocess_func=postprocess_func,
        )
    for func in web:
        toolkit.register_tool_function(
            func,
            group_name="web_tools",
            postprocess_func=postprocess_func,
        )

    await toolkit.register_mcp_client(
        SearchMCPMock(),
        group_name="mcp_tools",
        postprocess_func=postprocess_func,
    )
    await toolkit.register_mcp_client(
        FinanceMCPMock(),
        group_name="mcp_tools",
        postprocess_func=postprocess_func,
    )
    return toolkit
