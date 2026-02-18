# 70-examples

用于放置综合案例（整合模型、工具、记忆、编排、运行时）。

## 案例主题：股票投资分析助手（完整用例）

目标：基于当前市场热点概念（而非先给股票代码）构建“主题投资研究链路”，从产业链上下游入手筛选企业与供应链关系，结合核心技术与商业收入模式变革，识别最有价值投资标的并输出深度分析报告。

> 说明：该案例用于研究和学习，不构成投资建议。

## 1) 端到端流程（热点驱动）

1. 热点识别：从新闻、政策、产业会议、资金流向中识别 Top 热点主题（如 AI 算力、机器人、低空经济）。
2. 产业链拆解：按上游（原材料/设备）、中游（核心部件/制造）、下游（应用场景）构建产业链图谱。
3. 企业映射：对每个环节映射相关上市公司，并标注其供应链上下游关系。
4. 技术壁垒分析：识别各环节核心技术、国产替代空间、专利/工艺壁垒。
5. 商业模式变革分析：判断热点驱动下收入结构、盈利模式、定价权与估值逻辑是否发生变化。
6. 候选池筛选：以“景气度 x 竞争力 x 估值性价比 x 风险暴露”进行多因子打分，得到候选标的池。
7. 深度个股分析：对候选 Top N 做财务、估值、事件催化、风险情景推演。
8. 输出报告：给出“最有价值标的 + 次优标的 + 风险对冲建议”，附证据链与跟踪指标。

## 2) Skills 规划（6 个）

1. `hot_topic_discovery_skill`
   - 用途：热点发现、热度排序、主题定义与边界划分。
2. `industry_chain_mapping_skill`
   - 用途：产业链上中下游拆解、环节归类、公司映射。
3. `supply_chain_linking_skill`
   - 用途：企业间供应关系、客户结构、依赖度识别。
4. `tech_moat_analysis_skill`
   - 用途：核心技术壁垒、替代路径、迭代节奏分析。
5. `business_model_shift_skill`
   - 用途：收入模式变革、利润池迁移、估值锚变化分析。
6. `investment_selection_reporting_skill`
   - 用途：候选筛选、打分排序、最终投资结论与报告生成。

## 3) Tools 规划（12 个）

### A. 热点与产业链分析工具（8 个）

1. `discover_hot_topics(window_days, market)`
2. `build_industry_chain(topic)`
3. `map_listed_companies(chain_node, market)`
4. `link_supply_chain(company)`
5. `analyze_core_technology(company_or_chain_node)`
6. `analyze_business_model_shift(company, topic)`
7. `rank_investment_candidates(candidates, scoring_config)`
8. `generate_deep_dive_report(symbol, context)`

### B. 联网检索与证据工具（4 个）

9. `web_search_news(query, days)`
10. `web_fetch_article(url)`
11. `search_company_filings(symbol_or_cik)`
12. `extract_evidence_links(claims)`

## 4) MCP 服务建议（常用，按职责）

下面给出常见且实用的 MCP 类型，实际可按你本地环境替换：

1. **搜索类 MCP**
   - 示例：`Tavily MCP` / `Brave Search MCP` / `SerpAPI MCP`
   - 用途：实时新闻、主题检索、站点限定检索（如 `site:sec.gov`）。

2. **网页抓取类 MCP**
   - 示例：`Fetch MCP` / 通用 HTTP MCP
   - 用途：拉取网页正文、公告详情、财报解读页面。

3. **金融数据类 MCP**
   - 示例：`Yahoo Finance MCP` / `Alpha Vantage MCP` / `FMP MCP`
   - 用途：K 线、估值指标、财务报表、分红回购数据。

4. **监管披露类 MCP**
   - 示例：`SEC EDGAR MCP`（美股）/ 交易所公告接口 MCP（A 股）
   - 用途：10-K/10-Q/8-K、临时公告、业绩预告。

5. **代码计算类 MCP**
   - 示例：`Python REPL MCP` / `Code Runner MCP`
   - 用途：DCF 计算、情景分析、敏感性分析、图表生成。

6. **文档存储与检索 MCP**
   - 示例：`Filesystem MCP` / `SQLite MCP` / `Postgres MCP`
   - 用途：缓存历史分析结果、记录结论与证据索引。

## 5) 推荐编排（Pipeline）

- `sequential`：热点识别 -> 产业链拆解 -> 企业映射
- `fanout(concurrent)`：技术壁垒分析 / 商业模式变革分析 / 财务估值分析 并行执行
- `sequential`：并行结果交叉验证 -> 候选打分排序 -> 深度报告输出

## 6) 输出结构（建议）

- `hot_topic`: 热点主题及热度来源
- `industry_chain_map`: 上中下游结构与关键节点
- `candidate_pool`: 候选公司与打分
- `top_pick`: 最有价值投资标的（含核心逻辑）
- `top_pick_deep_dive`: 技术壁垒、供应链地位、财务与估值、催化剂
- `business_model_shift`: 收入模式变革结论
- `key_risks`: 风险清单与触发条件
- `evidence`: `[{claim, source, url, timestamp}]`
- `action_plan`: 仓位建议、止损、跟踪指标

## 7) 最小可运行范围（MVP）

第一阶段只做：

- 3 个 skill：`market_research`、`fundamental_analysis`、`reporting`
- 5 个 tool：行情、财务、联网搜索、网页抓取、报告生成
- 2 个 MCP：搜索类 + 金融数据类

在 MVP 跑通后，再扩展估值与风险控制模块。
