# AI Daily Report — Claude Code Skill

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that generates daily AI/tech intelligence reports from Hacker News and HuggingFace Papers, then publishes to a Feishu (Lark) knowledge base.

## What It Does

```
1. Check cache  -->  2. Crawl sources (parallel)  -->  3. Deduplicate & filter
      |                      |                              |
      v                      v                              v
4. Score & categorize  -->  5. Generate Markdown  -->  6. Publish to Feishu Wiki
```

1. **Crawls multiple sources** in parallel via sub-agents:
   - Hacker News Top + Best stories (Firebase API, `curl`)
   - HuggingFace Daily Papers (REST API, `WebFetch`)
2. **Deduplicates and caches** results (90-day TTL, URL + title matching)
3. **Scores and categorizes** each item with rating levels (极高 / 高 / 中高 / 中)
4. **Generates a Chinese report** with 15-25 curated items grouped by topic
5. **Publishes to Feishu Wiki** under a monthly hierarchy

## Usage

```bash
# Natural language
> 生成今天的 AI 日报
> 今天 HN 上有什么有意思的

# Slash command
> /ai-daily
```

## Report Example

```markdown
# 每日技术情报日报 · 2026-04-18 · 共 22 条高质量精选内容

---

## AI 工具与开发

### Claude Code 2.0 发布
**重要程度：极高** · **来源：Hacker News（520+ 点）**

Anthropic 发布 Claude Code 2.0，新增 Skills 系统和多 Agent 编排...

[阅读原文](https://...)

---

## AI 研究论文（HuggingFace Papers 今日精选）

### Scaling Laws for Multimodal Models
**关注程度：高** · **MIT** · **HuggingFace（89 点）**

提出多模态模型的新 scaling law...

[论文链接](https://...)

---
本期共收录 22 条内容 · 信源：Hacker News, HuggingFace · 生成时间：2026-04-18
```

## Category Taxonomy

| Category | Typical Content |
|----------|----------------|
| AI 工具与开发 | AI tools, frameworks, model releases |
| AI 研究论文 | Papers from HuggingFace (always a dedicated final section) |
| 安全与密码学 | Security vulnerabilities, cryptography |
| 基础设施与工具 | DevOps, cloud, databases, CLI tools |
| 编程语言与框架 | Language updates, new frameworks |
| 开源项目 | Notable open source releases |
| 行业动态 | Business news, acquisitions, policy |

## Quality Thresholds

| Source | Minimum | Max Items |
|--------|---------|-----------|
| Hacker News Top | score >= 50 | 30 |
| Hacker News Best | score >= 80 | 20 |
| HuggingFace Papers | upvotes >= 10 | 15 |

Target: 15-25 items per report. Raise thresholds on rich days, lower on sparse days.

## Rating System

| Label | When to Use |
|-------|-------------|
| 重要程度 | Security, breaking changes, industry shifts |
| 有趣程度 | Historical discoveries, creative projects |
| 实用程度 | Tools, libraries, infrastructure |
| 关注程度 | Papers, research, people, trends |

Each label has 4 levels: 极高 / 高 / 中高 / 中.

## Project Structure

```
ai-daily-report-skill/
├── SKILL.md                    # Main skill definition (workflow + instructions)
├── data/
│   ├── resource.json           # Source configuration (URLs, quality tiers, crawl methods)
│   └── cache.json              # Local dedup cache (gitignored, auto-created)
├── references/
│   └── format-guide.md         # Output format specification and template
├── scripts/
│   └── cache.py                # Cache manager (get/put, 90-day TTL, URL+title dedup)
├── LICENSE
└── README.md
```

## Installation

### Option 1: Copy

```bash
git clone https://github.com/YOUR_USERNAME/ai-daily-report-skill.git
cp -r ai-daily-report-skill ~/.claude/skills/ai-daily-report
```

### Option 2: Symlink (recommended for development)

```bash
git clone https://github.com/YOUR_USERNAME/ai-daily-report-skill.git
ln -s $(pwd)/ai-daily-report-skill ~/.claude/skills/ai-daily-report
```

Restart Claude Code after installation. The skill triggers on "生成日报", "AI日报", "/ai-daily", etc.

## Prerequisites

- **Claude Code** with WebFetch and Bash tools
- **Python 3.10+** for the cache script
- **[feishu-cli](https://github.com/nicepkg/feishu-cli)** for Feishu Wiki publishing
- **Feishu App** with Wiki write permissions (`wiki:wiki:create`, `wiki:wiki:manage`)
- Optional: **Playwright MCP server** for hard-to-crawl future sources

## Configuration

### Source Configuration

Edit `data/resource.json` to customize:

- Source URLs and API endpoints
- Quality scores (1-10) and crawl difficulty tiers (easy/medium/hard)
- Minimum score/upvote thresholds
- Maximum items per source

### Feishu Wiki

Update these values in `SKILL.md` Step 6 to point to your own Wiki:

```
Space ID: <your-wiki-space-id>
Root Node Token: <your-root-node-token>
```

### Cache

The cache auto-creates at `data/cache.json`. Entries older than 90 days are auto-pruned. No manual configuration needed.

## How Claude Code Skills Work

Skills are Markdown-based instruction sets that extend Claude Code:

1. **Metadata** (`name` + `description` in YAML frontmatter) is always in context — used for trigger matching
2. **SKILL.md body** loads when the skill triggers — contains the full workflow
3. **References** (`references/`) load on-demand when referenced by the skill
4. **Scripts** (`scripts/`) execute directly without loading into context

See [Claude Code Skills Documentation](https://docs.anthropic.com/en/docs/claude-code/skills) for details.

## License

[MIT](LICENSE)
