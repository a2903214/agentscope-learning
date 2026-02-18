---
name: investment_selection_reporting_skill
description: 对候选标的排序并产出最终深度投资报告。
---

# 投资筛选与报告技能

先调用 `rank_investment_candidates`，再调用 `generate_deep_dive_report`。
输出严格 JSON，包含证据与风险控制建议。
