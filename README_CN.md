<p align="center">
  <a href="README.md">🇺🇸 English Version</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v2.0-0f766e?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/platform-Claude%20Code%20%7C%20Codex%20%7C%20Cursor%20%7C%20DSH-202124?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/license-MIT-15803d?style=for-the-badge" alt="License">
</p>

<h1 align="center">Investment Analysis Skill（投资分析技能）</h1>
<p align="center">
  <b>AI 驱动的投资研究引擎</b><br>
  为一级市场和二级市场生成决策级投资报告<br>
  <sub>14 维度分析框架 · 自动化质量关卡 · 双格式输出（HTML + PDF）</sub>
</p>

---

## 这是什么？

一个专业级的 AI 技能，能将公司名称、股票代码或路演材料转化为**全面、有据可查的投资研究报告**。专为风险投资、私募股权和二级市场投资者设计，满足对深度、严谨性和可审计性的要求。

你可以把它想象成一位顶级投资分析师，以机器速度工作——阅读你的源文件，在中英文 5 个维度上进行网络搜索，对照一手来源交叉验证信息，最终生成一份排版精美的 HTML+PDF 报告，可以直接提交给投资决策委员会。

## 用途

| 场景 | 示例 |
|---|---|
| 🔍 **一级市场尽调** | 分析路演材料、商业计划书、财务模型 |
| 📊 **二级市场研究** | 基于年报、财报、行业数据进行深度分析 |
| 🏭 **行业研究** | 行业格局、竞争分析、价值链拆解 |
| 💰 **估值分析** | DCF、可比公司、先例交易分析 |
| 🌍 **政策/地缘分析** | 监管环境、地缘政治风险评估 |
| 📋 **竞争对手分析** | 对标分析、市场份额、差异化评估 |

## 快速开始

### Claude Code

```bash
# 安装技能
cp -r investment-analysis ~/.claude/skills/

# 使用
/投资分析 大疆无人机
# 或者
分析一下这家公司的路演材料 [拖放 PDF/PPT 文件]
```

### Codex / Cursor

将 `versions/codex/CODEX.md` 复制到 `.cursor/rules/`，然后：

```
@investment-analysis 分析 [公司名称]
```

### DeepSeek Harness (DSH)

安装到 DSH 用户技能目录，并使用 `dsh` profile：

```bash
# 安装技能（DSH 会自动发现 ~/.dsh/skills/ 下的目录式技能）
git clone https://github.com/BruceLZX/investment-analysis-skill.git ~/.dsh/skills/investment-analysis

# 使用 —— 编排器以 --profile dsh 运行
python scripts/run_analysis_harness.py init --profile dsh --output "[公司名]_[业务摘要]" --company "[公司名]"
```

### 任意 AI 工具

将 `prompt_universal.md` 复制为系统提示词，然后输入公司名称或上传文件即可。

## 输出内容

```
[公司名]_[业务摘要]/
├── sources/                         # 原始源文件
├── [公司名]_投资分析报告.html        # 交互式 HTML（约 50-130KB）
└── [公司名]_投资分析报告.pdf         # 打印就绪 PDF（约 400-800KB）
```

### 报告覆盖范围（14 个维度）

| # | 维度 | 核心问题 |
|---|---|---|
| 1 | 公司概览 | 做什么的？为什么现在关注？ |
| 2 | 团队与管理层 | 谁在做？有没有能力做成？ |
| 3 | 产品与技术 | 产品/技术是否真的有壁垒？ |
| 4 | 市场与行业 | 赛道有多大？增速如何？ |
| 5 | 竞争格局 | 谁能抢走份额？护城河到底多深？ |
| 6 | 商业模式 | 怎么赚钱？单位经济模型怎么样？ |
| 7 | 财务分析 | 数字健康吗？现金流能撑多久？ |
| 8 | 增长策略 | 下一步怎么长？天花板在哪里？ |
| 9 | 风险因素 | 什么事情能摧毁这家公司？ |
| 10 | 估值与退出 | 值多少钱？怎么退出？ |
| 11 | 监管与合规 | 政策风险大不大？合规成本多高？ |
| 12 | ESG 与可持续性 | 环境、社会、治理层面有无隐患？ |
| 13 | 地缘政治背景 | 宏观格局对业务有什么影响？ |
| 14 | 投资结论 | 投不投？多少钱？什么时候进？ |

### 投资者级深度

每个章节必须通过**强制证据关卡**：3-6 次定向搜索、≥2 个独立来源、≥1 个一手/权威来源验证、≥2 个量化事实或代理指标、≥1 个基准对比、≥1 条反面证据、投资者启示，以及 2-5 个尽调问题。

## 架构

```
investment-analysis/
├── SKILL.md                          # 技能入口和工作流
├── agents/openai.yaml                # Codex agent 接口
├── references/                       # 分析师手册
│   ├── report_strategy_playbook.md   # 15+ 报告结构（二级市场、硬科技、生物医药等）
│   ├── analysis_core.md              # 证据关卡、写作规范、红队标准
│   ├── decision_framework.md         # 情景分析、非共识洞察、仓位建议
│   ├── section_deepening.md          # 各章节深度研究提示词
│   ├── geo_market_context_lens.md    # 区域市场体系分析
│   ├── policy_geopolitics_lens.md    # 政策/监管/地缘政治分析
│   └── public_equity_financials_lens.md  # 财务报表与估值框架
├── scripts/                          # Python 自动化脚本与质量检测
│   ├── run_analysis_harness.py       # 中央编排器（初始化/关卡/循环/清理）
│   ├── check_evidence.py             # 证据矩阵校验
│   ├── check_depth.py                # 章节深度 QA（防肤浅）
│   ├── check_report.py               # 报告完整性 QA
│   ├── check_citations.py            # 引用与来源可靠性检查
│   ├── check_source_register.py      # 来源登记簿校验
│   ├── check_workflow_docs.py        # 工作流文档关卡
│   ├── clean_output.py               # 最终输出规范执行
│   ├── generate_pdf.py               # HTML→PDF（WeasyPrint）
│   ├── inventory_sources.py          # 源文件清单与 SHA-256 校验
│   └── diagnose_report.py            # 报告诊断工具
├── templates/
│   └── report_template.html          # 专业报告模板（侧边栏、搜索、打印）
└── versions/                         # 平台特定配置
    ├── claude-code-claude/CLAUDE.md
    ├── claude-code-deepseek-ocr/CLAUDE.md
    ├── codex/CODEX.md
    └── dsh/DSH.md
```

## 分析框架（Analysis Spines）

本技能会根据公司类型自动调整分析视角：

| 公司类型 | 分析重点 |
|---|---|
| 🏢 **二级市场成熟企业** | 财务质量、估值倍数、资本回报率、管理层质量、资本配置 |
| 🔬 **深科技/硬科技** | 技术成熟度（TRL）、IP 壁垒、研发效率、工程团队深度 |
| 💊 **生物医药** | 管线分析、临床试验阶段、监管路径、市场独占期 |
| ☁️ **SaaS/软件** | 单位经济模型（CAC/LTV）、NDR、Rule of 40、产品驱动增长 |
| 🏭 **工业/制造** | 产能利用率、供应链韧性、自动化水平、订单积压 |
| 💰 **金融科技** | 监管许可、风险管理、资金成本、获客效率 |
| 🌍 **跨境/全球化** | 地缘风险敞口、汇率影响、各区域竞争格局 |

## 自动化工作流

这个技能不是一次性提示词——它是一个**带有自动化质量关卡的严谨工作流**：

```bash
# 1. 初始化工作区
python scripts/run_analysis_harness.py init \
  --output "公司名_业务摘要" \
  --company "公司名" \
  --sources 路演材料.pdf 股权结构表.xlsx

# 2. 撰写前关卡（必须通过才能开始写报告）
python scripts/run_analysis_harness.py gate --output "输出文件夹"

# 3. 使用 templates/report_template.html 模板撰写 HTML 报告

# 4. QA 循环（证据 + 深度 + 报告完整性）
python scripts/run_analysis_harness.py loop \
  --output "输出文件夹" --html "报告.html" --pdf "报告.pdf"

# 5. 清理与交付
python scripts/run_analysis_harness.py clean --output "输出文件夹"
```

## 核心设计原则

### 1. 证据优先于观点
每个论断必须追溯到具体来源。来源登记簿将 `[S1]...[SN]` 映射到 URL、文件页码、来源类型和置信度。没有任何事实可以没有出处。

### 2. 反面证据是强制要求
每个章节必须包含至少一条削弱性或矛盾性来源。红队质询的问题是：*"哪个事实如果错了，对投资论点的伤害最大？"*

### 3. 拒绝虚假精确
如果收入数据不可得，就标注"未公开"。如果某个指标会造成虚假精确，就解释为什么省略它，以及需要什么数据才能计算。绝不编造数字。

### 4. 决策导向，而非百科式
报告应该回答：*"投资者现在应该怎么做？"*——而不仅仅是描述公司是做什么的。每个段落都应该对投资决策有实质推进。

### 5. 多平台，统一标准
无论是在 Claude Code、Codex、Cursor 还是 DeepSeek Harness (DSH) 上运行，都适用同一套 14 维度框架和证据关卡。平台特定配置仅处理工具可用性和模型特性差异。

## 环境要求

- **Python 3.10+** 用于自动化脚本
- **WeasyPrint**（`pip install weasyprint`）用于 PDF 生成
- **Claude Code / Codex / Cursor / DeepSeek Harness (DSH)** 作为 AI 运行时

```bash
# macOS
pip install weasyprint
brew install pango

# Ubuntu/Debian
pip install weasyprint
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0
```

## 贡献指南

本技能设计为可扩展：

- **添加新的分析框架**：编辑 `references/report_strategy_playbook.md`
- **添加新的 QA 检查**：在 `scripts/` 中添加脚本并接入 `run_analysis_harness.py`
- **添加新的分析视角**：创建新的 reference 文件并在 `SKILL.md` 中引用
- **支持新平台**：在 `versions/` 中添加平台配置

## 免责声明

本技能基于公开信息生成投资分析报告。报告仅供研究参考，不构成投资建议。投资决策应结合专业判断，并咨询持牌顾问。

---

<p align="center">
  <sub>为追求深度的投资者而构建 · <a href="https://github.com/BruceLZX/investment-analysis-skill">GitHub</a></sub>
</p>
