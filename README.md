# AI Daily Report

> Claude Code Skill — 每日 AI/技术情报日报生成器

从 Hacker News 和 HuggingFace Papers 自动抓取当日高质量技术内容，评分分类后生成中文日报，发布到飞书知识库。

## Quick Start

```bash
# 1. 安装：克隆到 Claude Code skills 目录
git clone https://github.com/AsterZephyr/ai-daily-report-skill.git
ln -s $(pwd)/ai-daily-report-skill ~/.claude/skills/ai-daily-report

# 2. 重启 Claude Code

# 3. 使用
> /ai-daily
> 生成今天的 AI 日报
> 今天 HN 上有什么有意思的
```

## 工作流程

```
数据源                  处理                    输出
─────────────────    ─────────────────    ─────────────────
HN Top Stories   ──┐
                   ├─→ 去重 → 评分 → 分类 ──→ Markdown 日报
HN Best Stories  ──┤                           │
                   │                           ├─→ 本地存档
HuggingFace      ──┘                           └─→ 飞书 Wiki
Papers
```

**并行抓取** — 通过 sub-agent 同时爬取 HN 和 HuggingFace，合并去重后统一处理。

## 日报示例

```markdown
# 每日技术情报日报 · 2026-04-18 · 共 22 条高质量精选内容

---

## AI 工具与开发

### Claude Code 2.0 发布
**重要程度：极高** · **来源：Hacker News（520+ 点）**

Anthropic 发布 Claude Code 2.0，新增 Skills 系统和多 Agent 编排，
支持自定义工作流和跨会话记忆...

[阅读原文](https://...)

---

## AI 研究论文（HuggingFace Papers 今日精选）

### Scaling Laws for Multimodal Models
**关注程度：高** · **MIT** · **HuggingFace（89 点）**

提出多模态模型的新 scaling law，发现视觉与语言模态的最优计算分配比例...

[论文链接](https://...)

---

本期共收录 22 条内容 · 信源：Hacker News, HuggingFace · 生成时间：2026-04-18
```

## 数据源与质量控制

### 信源配置

| 数据源 | 抓取方式 | 质量阈值 | 最大条目 |
|--------|---------|---------|---------|
| Hacker News Top Stories | Firebase API (`curl`) | score >= 50 | 30 |
| Hacker News Best Stories | Firebase API (`curl`) | score >= 80 | 20 |
| HuggingFace Daily Papers | REST API (`WebFetch`) | upvotes >= 10 | 15 |

每期目标 **15-25 条**。内容丰富时提高阈值精选，内容稀疏时适当降低。

信源配置存储在 `data/resource.json`，支持自定义 URL、阈值和抓取策略。

### 评分体系

每条内容按最匹配的维度评分，4 个等级（极高 / 高 / 中高 / 中）：

| 评分维度 | 适用场景 | 示例 |
|---------|---------|------|
| **重要程度** | 安全事件、重大变更、行业拐点 | Log4j 级漏洞、GPT-5 发布 |
| **有趣程度** | 历史发现、创意项目、冷知识 | 40年前的代码考古、奇葩 side project |
| **实用程度** | 工具、库、基础设施 | 新 CLI 工具、数据库性能优化方案 |
| **关注程度** | 论文、趋势、人物 | SOTA 论文、行业并购、CTO 离职 |

### 内容分类

| 分类 | 典型内容 |
|------|---------|
| AI 工具与开发 | AI 工具、框架、模型发布 |
| AI 研究论文 | HuggingFace 论文（独立章节，不混入其他分类） |
| 安全与密码学 | 安全漏洞、密码学、合规 |
| 基础设施与工具 | DevOps、云服务、数据库、CLI |
| 编程语言与框架 | 语言更新、新框架 |
| 开源项目 | 重要开源发布和里程碑 |
| 行业动态 | 商业新闻、收购、政策 |

## 飞书发布

日报自动发布到飞书知识库，按月归档：

```
知识库首页
  └── 2026年4月
       ├── 每日技术情报日报 · 2026-04-17
       ├── 每日技术情报日报 · 2026-04-18
       └── ...
```

使用前需在 `SKILL.md` Step 6 中配置你自己的 Wiki Space ID 和 Root Node Token。

## 项目结构

```
ai-daily-report-skill/
├── SKILL.md                  # 技能主文件（完整工作流定义）
├── data/
│   ├── resource.json         # 信源配置（URL、质量分、抓取策略）
│   └── cache.json            # 去重缓存（gitignored，自动创建）
├── references/
│   └── format-guide.md       # 日报输出格式规范
├── scripts/
│   └── cache.py              # 缓存管理器（90天TTL，URL+标题去重）
├── .gitignore
├── LICENSE
└── README.md
```

## 环境要求

| 依赖 | 用途 | 必需 |
|------|------|------|
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | 技能运行环境 | Yes |
| Python 3.10+ | 缓存脚本 | Yes |
| [feishu-cli](https://github.com/nicepkg/feishu-cli) | 飞书 Wiki 发布 | Yes |
| 飞书开放平台 App | Wiki 写入权限 | Yes |
| Playwright MCP Server | 未来扩展信源的浏览器自动化 | No |

## 安装

### 方式一：Symlink（推荐，方便更新）

```bash
git clone https://github.com/AsterZephyr/ai-daily-report-skill.git
ln -s $(pwd)/ai-daily-report-skill ~/.claude/skills/ai-daily-report
```

### 方式二：直接复制

```bash
git clone https://github.com/AsterZephyr/ai-daily-report-skill.git
cp -r ai-daily-report-skill ~/.claude/skills/ai-daily-report
```

安装后重启 Claude Code 即可。

## 什么是 Claude Code Skill

Skill 是基于 Markdown 的指令集，用于扩展 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 的能力：

- **YAML frontmatter**（`name` + `description`）始终在上下文中，用于触发匹配
- **SKILL.md 正文** 在技能触发时加载，包含完整工作流
- **references/** 按需加载，提供补充文档
- **scripts/** 直接执行，不占用上下文

详见 [Claude Code Skills 官方文档](https://docs.anthropic.com/en/docs/claude-code/skills)。

## License

[MIT](LICENSE)
