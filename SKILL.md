---
name: ai-daily-report
description: >
  生成每日 AI/技术情报日报并发布到飞书知识库。从 Hacker News 和 HuggingFace Papers
  抓取高质量内容，按主题分类、评级，生成中文日报，最终导入飞书 Wiki。
  当用户说"生成日报"、"AI日报"、"今日技术资讯"、"每日情报"、"/ai-daily"、
  "tech daily"、"今天有什么新闻"、"抓一下今天的内容"时触发此技能。
  即使用户只是随口问"今天 HN 上有什么有意思的"，也应该触发。
---

# AI Daily Report

从 Hacker News 和 HuggingFace Papers 抓取当日高质量技术内容，按分类整理为中文日报，发布到飞书知识库。

## Workflow Overview

```
1. Check cache  -->  2. Crawl sources  -->  3. Deduplicate & filter
      |                    |                        |
      v                    v                        v
4. Score & categorize  -->  5. Generate Markdown  -->  6. Publish to Feishu Wiki
```

## Step 1: Check Cache

Before crawling, check what's already been collected today to avoid duplicate work.

```bash
python3 ~/.claude/skills/ai-daily-report/scripts/cache.py get --date $(date +%Y-%m-%d)
```

If entries exist for today, use them as a starting point. Only re-crawl sources that haven't been fetched yet.

## Step 2: Crawl Sources

Read `data/resource.json` (sibling to this SKILL.md) for source configuration. Each source has a `crawl_difficulty` that determines which tool to use:

### Easy sources (curl) -- Hacker News

HN has a clean Firebase API. Fetch top and best stories, then individual items:

```bash
# Get top 30 story IDs
curl -s 'https://hacker-news.firebaseio.com/v0/topstories.json' | python3 -c "
import json, sys
ids = json.load(sys.stdin)[:30]
print(json.dumps(ids))
"

# Fetch a single item
curl -s "https://hacker-news.firebaseio.com/v0/item/{id}.json"
```

Each item returns: `{id, title, url, score, by, time, descendants, type}`.

Filter: keep items with `score >= 50`.

For items that link to GitHub issues, blog posts, or other pages, use WebFetch to get a summary of the linked content. This is what turns a bare HN link into a useful report item.

### Medium sources (WebFetch) -- HuggingFace Papers

```
Use WebFetch on https://huggingface.co/papers with a prompt to extract:
- Paper title
- Authors / institution
- Upvote count
- One-line summary
- Paper URL
```

Filter: keep papers with `upvotes >= 10`.

### Hard sources (Playwright) -- reserved for future sources

If a source requires browser automation (JS rendering, login, infinite scroll), use the Playwright MCP tools to navigate, wait for render, and extract content.

## Step 3: Deduplicate & Cache

After crawling, write all new items to cache:

```bash
python3 ~/.claude/skills/ai-daily-report/scripts/cache.py put '{
  "url": "https://...",
  "title": "...",
  "source": "hackernews",
  "score": 150,
  "date": "2026-04-13",
  "summary": "..."
}'
```

The cache script automatically deduplicates by URL and title.

## Step 4: Score & Categorize

Separate the items into two independent tracks before categorizing:

**Track A -- Hacker News items**: Assign each to a topic category (see `references/format-guide.md` for the taxonomy). These become the main body of the report.

**Track B -- HuggingFace Papers**: Do NOT assign these to topic categories. They all go into one dedicated section: `AI 研究论文（HuggingFace Papers 今日精选）`. Keep them as a separate list throughout the pipeline.

For each item in both tracks, determine:

1. **Rating** -- pick the appropriate rating label (重要程度/有趣程度/实用程度/关注程度) and level (极高/高/中高/中)
2. **Summary** -- write a Chinese summary (2-5 sentences for HN items, 1-2 sentences for HF papers)

Rating guidelines:
- 极高: Paradigm shifts, critical security issues, >500 HN points, top HuggingFace paper
- 高: Significant tools/releases, notable research, 200-500 HN points
- 中高: Useful tools, interesting findings, 100-200 HN points
- 中: Worth knowing, 50-100 HN points

For HN items that link to substantial content (blog posts, papers, GitHub issues), use WebFetch to read the linked page and write a more informed summary. A bare title is not enough -- the value of the report is in the synthesis.

## Step 5: Generate Markdown

Read `references/format-guide.md` for the exact output format. Generate the full Markdown report following that template.

Key rules:
- Title: `每日技术情报日报 · {date} · 共 {N} 条高质量精选内容`
- 15-25 items total (HN + HF combined). If you have more than 25, raise the HN score threshold or drop the lowest-rated items until you're within range. Prefer quality over quantity.
- Group HN items by topic category with `---` separators (these form the main body)
- After all HN topic sections, place HuggingFace papers in one dedicated section: `## AI 研究论文（HuggingFace Papers 今日精选）`. Papers must NOT appear inside the topic categories above -- they are always in this final section before the footer.
- Footer with source attribution and generation date

Save the Markdown to `~/notes/ai-report/ai-daily-{date}.md`.

## Step 6: Publish to Feishu Wiki

The report goes to a dedicated Feishu knowledge base, organized by month.

### Wiki Configuration

```
Space ID: 7627929211956645062
Root Node Token: AgWUwNcZwiext0kCozvcv7eOnlc
Wiki URL: https://bluefocus.feishu.cn/wiki/AgWUwNcZwiext0kCozvcv7eOnlc
```

### Monthly Organization

Reports are grouped under monthly parent documents. The hierarchy:

```
知识库首页 (AgWUwNcZwiext0kCozvcv7eOnlc)
  └── 2026年4月 (month node)
       ├── 每日技术情报日报 · 2026-04-07
       ├── 每日技术情报日报 · 2026-04-08
       └── ...
```

### Publishing Steps

#### 6a. Find or create the monthly node

List existing nodes under the root to check if a monthly node already exists:

```bash
feishu-cli wiki node list 7627929211956645062 --parent-node-token AgWUwNcZwiext0kCozvcv7eOnlc
```

Look for a node titled like `2026年4月`. If it doesn't exist, create it:

```bash
feishu-cli wiki node create 7627929211956645062 \
  --obj_type docx \
  --parent_node_token AgWUwNcZwiext0kCozvcv7eOnlc \
  --title "2026年4月"
```

Save the returned `node_token` for the monthly node.

#### 6b. Create the daily report document under the monthly node

```bash
feishu-cli wiki node create 7627929211956645062 \
  --obj_type docx \
  --parent_node_token {monthly_node_token} \
  --title "每日技术情报日报 · {date} · 共 {N} 条高质量精选内容"
```

This creates an empty document. Save the returned `obj_token` (this is the `document_id`).

#### 6c. Import the Markdown content

Use the feishu-cli-import skill pattern:

```bash
feishu-cli doc import ~/notes/ai-report/ai-daily-{date}.md \
  --document-id {obj_token} \
  --title "每日技术情报日报 · {date} · 共 {N} 条高质量精选内容"
```

Or write content directly:

```bash
feishu-cli doc add {obj_token} ~/notes/ai-report/ai-daily-{date}.md --content-type markdown
```

#### 6d. Return the URL

The final document URL follows this pattern:
```
https://bluefocus.feishu.cn/wiki/{node_token}
```

Print this URL so the user can open the report.

## Crawling Strategy: Use Sub-Agents for Parallelism

For best performance, dispatch source crawling in parallel:

1. **Agent 1**: Crawl Hacker News (top + best stories via curl, then WebFetch for interesting links)
2. **Agent 2**: Crawl HuggingFace Papers (WebFetch)

Each agent should return a JSON array of items with: `url, title, source, score, date, category_hint, summary`.

Then merge results, deduplicate, categorize, generate the report, and publish.

## Error Handling

- If feishu-cli fails with auth errors, suggest the user run the feishu-cli-auth skill
- If a source is unreachable, skip it and note in the report footer
- If cache.py fails, continue without caching (the report still works)
- If the monthly Wiki node creation fails with permission errors, fall back to creating the doc under the root node

## Command Reference

| Action | Command |
|--------|---------|
| Check cache | `python3 ~/.claude/skills/ai-daily-report/scripts/cache.py get --date YYYY-MM-DD` |
| Add to cache | `python3 ~/.claude/skills/ai-daily-report/scripts/cache.py put '<json>'` |
| List wiki nodes | `feishu-cli wiki node list 7627929211956645062` |
| Create wiki node | `feishu-cli wiki node create 7627929211956645062 --obj_type docx --parent_node_token <token> --title "..."` |
| Get node info | `feishu-cli wiki node get <node_token>` |
| Import markdown | `feishu-cli doc import /tmp/file.md --title "..."` |
| Write to doc | `feishu-cli doc add <doc_id> /tmp/file.md --content-type markdown` |
