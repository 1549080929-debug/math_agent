# 项目状态总账（2026-08-22 更新）

> 用项目自己的框架（VAL）给每条研究线的**声称**定级——等级看锚，不看完成度。

---

## 一、研究线定级（VAL 视角）

| 研究线 / 声称 | VAL 级别 | 依据（锚） | 边界（诚实标注） |
|---|---|---|---|
| **判级程序可复现** | **L3**（实测可判定） | 4 独立盲评者两两 κ 0.77–0.93；协议 v2.3 冻结；安全子集 22 条 90.9% | 同族评分者；真人评分未测 |
| **V 栈主张**："VAL-guided 结构保证" | **L3**（构造性） | 双受害者 0.000/1.000；AgentDojo 0.0% @ 82.6% utility；JADE 真实 MCP 0%（模型被驱动 93.8% 仍全拦）；Z(α) 结构 plateau（合规随攻击升至 0.567 仍全拦） | ODD=测试床+两第三方基准；生产级实现未测 |
| **N 栈主张**："直觉选型=模型运气" | **L2**（正确性，本床成立） | 双受害者合规 >0 但 ASR 0；D2 单防 0.200→0.467（Z(α) 轮 2 跳崩）；跨基准漂移（0.000→3.5%→6.2%）；JADE M6 词表盲区真实漏 | 跨模型/更强攻击不可外推；GCG 无梯度不可测 |
| **预测协议**："等级预测失败方式" | **L2**（正确性，小样本） | 10/10（6 高置信+4 摘要级，已降级为 falsifiability 证据）+ JADE 5/5（含 M6 边界命中）+ 2 处机制修正 | 样本小；部分摘要级证据 |
| **Z(α) zero stability**："轨迹需 provenance 解释" | **L2**（本床成立） | 四种 failure morphology（跳崩/侵蚀/双 plateau）；D1/D3 轨迹重合但 provenance 不同（合规 0.333 vs 0.567） | 3 离散阶段×30 例；非连续 frontier；D1 运气零预测未测试 |
| **跨家族攻击者结论**："对齐攻击者拒绝参与" | **L2**（两家族实测） | Kimi 双模型 + Llama 8B：显式拒答、间接消毒、消毒产物受害者侧无效 | 未测未对齐/红队专用模型 |
| **LITMUS 互证**："语义层锚的结构盲区" | **L2**（独立文献复现） | LITMUS EH（EHR 7.98–17.97%）vs 我们 covert execution（TPR 0.60 天花板）——独立团队同结论 | 未跑其 Ubuntu+OpenClaw harness；互证在结构声称层面 |
| **专著/文档**（21 章 + docs/01-23） | L1/L2（自洽记录） | 全部实验/数据/修正轨迹存档 | 非正式出版物 |
| **主线 2：AI Research Capability Amplification**（docs/27 研究母稿） | **L1/L2**（声明 + 自洽记录） | protocol 已形成（audit/provenance/boundary/falsification）；within-conversation 行为适应已观察到；真实 failure cases 支撑规则必要性 | **跨任务 transfer / 可量化 capability gain 未证明——这是声明不是结论** |

## 二、数据与资产总账

- **LLM 调用**：主实验 ~5,400 + Llama 2×2 ~1,200 + 自适应/探针 ~300 + AgentDojo ~2,000 + JADE ~100 ≈ **~9,000 次**（DeepSeek + Ollama）
- **语料**：判级语料 70 条；JADE 公开实例 16 用例（8 变体 × 2 投毒型）
- **评分者**：A + B2–B7（6 个 LLM 盲评者）· 一致性报告 15+
- **工具链**：val_* 38 自测 · 数学裁判 42/42 · 判级协议 v2.3 · jade_integration.py（真实 MCP 协议）· Z(α) 提取脚本
- **论文**：① arXiv:2608.19009（v2 已公布）· ② The Same Zero（paper2/，arXiv 退回；ARR October 2026 周期投稿准备中，匿名化 PDF + 表单材料包就绪）
- **专著**：《给"分级"分级》21 章（book/，含新增第 19 章"论文 2 定位与证据链"）
- **主线 2 母稿**：docs/27（研究方法→AI 能力，核心备忘录）
- **第三方验证**：AgentDojo 官方基准 · 复旦 JADE 真实 MCP · LITMUS 行为层互证
- **审计记录**：v2/v3 口径混用修复（D2 0.258→0.200、D4 0.079→0.067）· 论文 8 项审稿边界收紧

## 三、环境配置（当前）

| 组件 | 端点 | 说明 |
|---|---|---|
| 受害者（默认） | api.deepseek.com / deepseek-chat | 全套件默认 |
| 攻击者 | api.deepseek.com / deepseek-chat | 异族接线保留（attacker_client） |
| 受害者（可选） | localhost:11434 / llama3.1:8b | 2×2 用；切 VICTIM_* 三字段即换 |
| MCP | mcp 2.0 + fastmcp（pip） | JADE 真实 server 验证用 |
| key | local_config.json（gitignore） | 已验证可用 |

## 四、待办（按优先级）

1. **第二篇论文投稿（ARR October 2026 周期，10-12 截止）**：✅ 匿名化投稿 PDF 就绪（无作者/邮箱/ORCID/GitHub/自引 arXiv 号，pypdf 全文扫描 clean）+ 表单材料包就绪（`paper2/arr/submission_form.md`：title/199 词 abstract/comments/track=LLM agents/checklist 草稿）。**待用户操作**：① 注册 OpenReview + 完善 profile（affiliation/semantic scholar/dblp/anthology）② 提交后 48h 内所有作者注册 reviewer ③ 决定 preprint binding 选项 ④ aclpubcheck 过稿 + acl.sty 对照官方最新模板 ⑤ 可选增强：C1 另一半（bounded exception）。⚠️ 周期修正：ARR 无 12 月周期（10 周一轮），最近窗口 2026-10-12
2. **沟通跟进**：复旦 JADE（docs/20 信）与南航 LITMUS（docs/22 信）邮件已发（08-22），**暂无回音**——待跟进
3. **C1a 扩展**（已完成首测 0.533 vs 0.000）：更大变体集、第二模型、bounded exception 变体（C1 另一半）、多轮 exploit
4. 可选：Groq Llama-3.3-70B 攻击者（跨家族最后开放变体）
5. 可选：作者补判（Rater A 补 N 系列）→ 人机一致性数据

## 五、方法论资产（不可量化部分）

审计先行 · 测价值窗口 · 诚实负结果 · 版本化追踪 · 裁判的裁判（对自身判级/实验/代码的三层审计）· 每步提交推送 · **claim 边界画在证据边界上（措辞比证据略窄）** · **"经过验证的结果才有资格改变模型"（docs/24 底层纪律）** · 审计独立性 v1（specs.py 判定规格单一化）

## 五、方法论资产（不可量化部分）

审计先行 · 测价值窗口 · 诚实负结果 · 版本化追踪 · 裁判的裁判（对自身判级/实验/代码的三层审计）· 每步提交推送 · **claim 边界画在证据边界上（措辞比证据略窄）**
