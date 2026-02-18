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
    toolkit = Toolkit()
    toolkit.create_tool_group("core_tools", description="stock core analysis tools", active=True)
    toolkit.create_tool_group("web_tools", description="web search and evidence tools", active=True)
    toolkit.create_tool_group("mcp_tools", description="mcp service tools", active=True)

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
