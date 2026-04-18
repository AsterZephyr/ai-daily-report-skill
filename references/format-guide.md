# AI Daily Report Format Guide

This document defines the output format for the daily tech intelligence report.

## Document Title Format

```
每日技术情报日报 · {YYYY-MM-DD} · 共 {N} 条高质量精选内容
```

Example: `每日技术情报日报 · 2026-04-13 · 共 18 条高质量精选内容`

## Overall Structure

The report is organized by topic categories. Each category is an H2 heading, and each item within it follows a consistent card format.

```markdown
# 每日技术情报日报 · {date} · 共 {N} 条高质量精选内容

---

## {Category Name}

### {Item Title}
**{Rating Label}：{Level}** · **来源：{Source}（{Points}+ 点）**

{2-5 sentence summary of the item. Focus on what matters to a senior engineer:
what changed, why it matters, what the implications are.}

{Optional: bullet points for key facts, data, or takeaways}

{Optional: table for before/after comparisons}

[阅读原文]({url})

---

## {Next Category}
...

---

本期共收录 {N} 条内容 · 信源：{comma-separated sources} · 生成时间：{date}
```

## Category Taxonomy

Assign each item to the most fitting category. Common categories:

| Category | Typical Content |
|----------|----------------|
| AI 工具与开发 | AI tools, frameworks, coding assistants, model releases |
| AI 研究论文 | Papers from HuggingFace, arXiv, conference proceedings |
| 安全与密码学 | Security vulnerabilities, cryptography, compliance |
| 基础设施与工具 | DevOps, cloud, CDN, monitoring, databases, CLI tools |
| 编程语言与框架 | Language updates, new frameworks, compiler news |
| 开源项目 | Notable open source releases and milestones |
| 行业动态 | Business news, acquisitions, policy, notable people |

If an item doesn't fit, create a new category. Keep categories to 3-6 per report for readability.

## Item Rating System

Each item gets a rating label and level. Use the dimension that best fits the content:

| Label | Levels | When to Use |
|-------|--------|-------------|
| 重要程度 | 极高 / 高 / 中高 / 中 | Security, breaking changes, industry shifts |
| 有趣程度 | 极高 / 高 / 中高 / 中 | Historical discoveries, creative projects |
| 实用程度 | 极高 / 高 / 中高 / 中 | Tools, libraries, infrastructure |
| 关注程度 | 极高 / 高 / 中高 / 中 | Papers, research, people, trends |

## Source Attribution

Always include the source and engagement metrics:

- **Hacker News**: `来源：Hacker News（{score}+ 点）` or `来源：GitHub Issue #{id}（Hacker News {score}+ 点）`
- **HuggingFace Papers**: `来源：HuggingFace（{upvotes} 点）` with optional institution: `· {University/Company}`
- **Cross-posted**: Include both: `来源：Hacker News（{score}+ 点）· 原始来源：{original}`

## HuggingFace Papers Section

Papers from HuggingFace ALWAYS go into their own dedicated section, separate from the topic categories above. This section appears after all HN-based topic categories and before the footer. Never merge papers into the topic categories (e.g., do not put a paper about security into the "安全与密码学" section).

Section title: `## AI 研究论文（HuggingFace Papers 今日精选）`

Paper items use a slightly different format -- shorter summaries, institution attribution:

```markdown
### {Paper Title}
**关注程度：{level}** · **{Institution}** · **HuggingFace（{upvotes} 点）**

{1-2 sentence description of what the paper does and why it matters.}

[论文链接]({url})
```

If a paper has the most upvotes, note it: `HuggingFace 今日最高票（{N} 点）`

## Quality Thresholds

Only include items that meet these minimums:

| Source | Minimum Metric |
|--------|---------------|
| Hacker News | score >= 50 |
| HuggingFace Papers | upvotes >= 10 |

Aim for 15-25 items total per report. If a day is sparse, lower thresholds slightly. If a day is rich, raise them and pick the best.

## Writing Style

- Chinese, concise and direct
- Technical audience: assume senior engineer reading level
- No marketing language, no hype
- Include concrete data: scores, numbers, benchmarks, comparisons
- Use tables for structured comparisons (e.g., before/after metrics)
- One blank line between items, `---` between categories
- Links at the end of each item, not inline

## Footer

```markdown
---

本期共收录 {N} 条内容 · 信源：{sources} · 生成时间：{YYYY-MM-DD}
```
