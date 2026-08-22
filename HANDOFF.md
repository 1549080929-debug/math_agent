# 项目交接文档（HANDOFF v3）

> 用途：压缩对话，转移新对话框。把本文件全文粘贴给新 AI 的第一条消息即可继续。
> 最后更新：2026-08-22。v2 交接于 2026-08-20（两篇论文 + AgentDojo 集成），本版覆盖至"构造实验（Z(α)/funnel）+ 方法论宣言 + 审计独立性 + 候选命题"。
> 阅读顺序建议：本文 → STATUS.md → docs/24（方法论宣言）→ agentsec/REPORT.md → paper2/paper.md

---

## 0. 一句话定位

**一个仓库、两篇论文、一本专著、一份方法论宣言**：
研究"LLM 验证/安全防御的失败模式"，核心框架 **VAL（验证自主等级 L0–L5）**。
元教训：**"裁判的裁判也需要裁判"**——已推广为更一般的候选不变量（docs/24）：**当系统内部不可直接获得时，找外部可作用面、可观测响应、证据锚点、失败边界**。

## 1. 论文（两条线）

| 论文 | 状态 | 内容 |
|---|---|---|
| **Grading the Graders**（arXiv:2608.19009） | ✅ v2 已公布，cs.CL | VAL 框架 + 四域实证 + 可复现性研究（κ≈0.8）+ 隐匿执行 TPR 0.60 天花板 |
| **The Same Zero**（paper2/，标题已改） | 📤 已提交 arXiv（08-20）待公布 | **标题从 "The Anchor Decides" 改为 "The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security"**（arXiv v2 预案） |

**The Same Zero 的 4 条贡献（当前版）**：
1. **Level map**：22 防御分级（L0-L5，盲评 κ≈0.8）
2. **Prediction validation**：10/10 + JADE 5/5（已降级为 falsifiability 证据，非 headline）
3. **Deployment-value comparison**：V 栈（D3+D4）0.000 ASR/1.000 良性 vs N 栈（D1+D2）0.000/0.000——same zero different guarantee
4. **Zero stability as measurable axis（Z(α)）**：failure morphology（abrupt collapse / progressive erosion / behavioral plateau / structural plateau）

**审稿演练沉淀的 8 项边界收紧**（全部落地）：数字统一（5400/4800→7000，370→380）、claim 软化（do-not-claim + "in the cases we can measure"）、VAL 客观性辩护（三重独立证据）、baseline 辩护（非 beats all）、D3/D4 分工、JADE 预测并入、三基准 ND 差异解释、VAL-selected→**VAL-guided**（不声称最优选择器）。

**关键数字（v3 口径，全部可追溯）**：
- 自建测试床：ND 0.333、D1 0.000、D2 **0.200**、D3 0.000、D4 **0.067**、V 0.000、N 0.000（v2 旧值 0.258/0.079 已废弃）
- AgentDojo：V 0.0% @ 82.6% utility vs tool_filter 0.0% @ 16.7%
- JADE 真实 MCP：ND 87.5%、N 6.2%（M6 词表盲区）、V 0%（模型被驱动 93.8% 仍全拦）
- LITMUS 互证：EH（EHR 7.98–17.97%）vs 我们的 covert execution（TPR 0.60）

## 2. 构造实验（2026-08-22 新增，第二篇的核心深化）

**Z(α)（7 轮，8 点梯度，30 例/点）**：

| cfg | 静态 | 轮1 | 轮2 | 轮4 | 轮7 |
|---|---|---|---|---|---|
| D1 behavioral | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| D2 surface rule | 0.200 | 0.233 | 0.467 | 0.733 | **0.833** |
| D3 authorization | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| D4 confinement | 0.067 | 0.067 | 0.300 | 0.300 | 0.300 |

- **D2 单调崩溃（3 轮 0.467 低估真实 0.833）、D4 轮 2 跳升后持平、D1/D3 8 点完全重合**
- **核心 claim**：Identical observed zero-stability profiles do not establish equivalent guarantees
- **D1 证伪攻击失败**（增强攻击者提示+7 轮）：0.000——读作"更强支持"，非"不能破"；合规 0.367 证明它仍是行为

**Execution Funnel（静态快照，与 Z(α) 分开报告）**：

| cfg | compliance | complete_args | authorized | 断开层 |
|---|---|---|---|---|
| D1 | 0.219 | **0.000** | 0.000 | 参数完整性（模型行为，无结构性 verifier） |
| D3 | 0.497 | 0.497 | **0.000** | 授权检查（平台记录） |

- **D3 的模型给了完整参数（49.7%）是授权门拦的；D1 的模型不给参数（0%）是半配合**——两个零在漏斗不同层级断开
- 机制确认：D1 下空参数 send_email 被执行且 state_changed=True（To: None 伪文件）——ASR 判定（args 非空）正确排除

**实验修复（审计驱动）**：发现论文 §6.1 混用 v2/v3 口径 → 重跑 v3 真效果 → 补 D1/D3 自适应+白盒（预测卡 5/6 和 4/6）→ forensic audit 通过（无 stale/duplicate，D2 突破分散 7 轮证明独立跑）。

## 3. 第三方验证（三个独立来源）

| 来源 | 结果 | 对论文的支撑 |
|---|---|---|
| AgentDojo 官方基准 | V 0.0% @ 82.6% vs tool_filter 0.0% @ 16.7% | utility 5 倍，同设置 |
| 复旦 JADE 真实 MCP | ND 87.5%（复现官方 83%）、N 6.2%（M6 漏）、V 0%（合规 93.8% 仍全拦） | 真实协议 + 预测卡 5/5 |
| LITMUS（南航）互证 | EH ≈ covert execution，独立复现语义层盲区 | 结构声称的外部支持（未跑其 harness） |

沟通信已备：docs/20（复旦张谧）、docs/22（南航周璐）。

## 4. 方法论沉淀（docs/24 + 候选命题）

**docs/24-方法论宣言**：不变量（黑盒→外部可作用面/锚/失败边界）+ 三精确化（有序打开/终极裁判不可达/VAL 锚即实例化）+ 失效边界 + 物理测量理论同构。

**候选命题（新，未实验）**：
- **C1**：Systems are more robust when rule-generating and rule-executing authorities remain within the scope of the rules they are subject to, **or when any exception is explicitly bounded (time-limited, revocable, traceable)**
- **C1a（可测，AI）**：agent 授予自授权通道 → 规则漂移概率高于无特权对照组（测试床可构造）
- **C1b（历史）**：例外受限的制度长期稳定性更高

**审计独立性（操作化方向）**：当前审计与实验共享作者（AI），交叉验证会"一致地错"的风险——外部基准提供真独立性；待做：判定 spec 单一化 + 独立实现者（L3）。

## 5. 关键文件索引

| 路径 | 内容 |
|---|---|
| `paper/` | 论文 1 源稿+PDF（21 页 v2）+ figure1 |
| `paper2/` | 论文 2（The Same Zero）+ PDF + submission + patch_*.py（修改轨迹） |
| `agentsec/` | 测试床 + REPORT.md（含 §7.13 构造实验）+ jade/（JADE 集成+Z(α)/funnel 图）+ PREDICTION_*.md（冻结预测卡）+ forensic_audit.py |
| `results/` | 实验 json（**注意 adaptivekimi_*=7 轮黑盒，adaptive_*=旧 3 轮**） |
| `docs/01-24` | 研究文档全集（**18-JADE 沟通准备、19-JADE 验证报告、20-复旦信、21-LITMUS 调查、22-南航信、23-论文 2 定位与证据链、24-方法论宣言**） |
| `book/` | 专著 21 章（含第 19 章论文 2 定位） |
| `STATUS.md` | 状态总账（2026-08-22 更新） |
| `HANDOFF.md` | 本文件（v3） |
| `promo/` | 推广材料 |

## 6. 环境配置

- Python：`py` 启动器（Python 3.13）
- DeepSeek：api.deepseek.com / deepseek-chat（local_config.json，gitignored）
- 本地 Ollama：llama3.1:8b（RTX 4050 6GB）
- MCP：`pip install mcp fastmcp`（JADE 真实 server 用）
- git：SSH over 443；PowerShell 用 `;` 分隔；**每步提交推送**
- 网络：arxiv/PyPI/GitHub 可直连；Google 被墙；**DeepSeek API 偶发 SSL 抖动（等待 15-25s 重试）**

## 7. 纪律与血泪教训（新 AI 必读）

1. **审计先行、测价值窗口、诚实负结果、每步提交推送**
2. **裁判的裁判**：判级/实验/代码三层审计；对数字做 trace 级验证（已抓：v2/v3 口径混用、resume 假 seed、指标误读、命名混乱）
3. **resume 坑**：adaptive_attack.py 会跳过已完成场景——改 rounds 后重跑**必须删旧文件**（本次 7 轮被旧 3 轮顶替过）
4. **文件命名**：黑盒自适应写 `adaptivekimi_*`（旧 `adaptive_*` 是 3 轮）——审计前先核对
5. **指标方向陷阱**：AgentDojo security_results 平均 = ASR（True=攻击达成）
6. **API key 安全**：local_config.json gitignored，commit 前检查
7. **对齐模型不愿当攻击者**：跨家族红队需愿意配合的攻击者
8. **claim 边界画在证据边界上**：措辞比证据略窄（VAL-selected→VAL-guided 等 8 项收紧）
9. **审计独立性**：审计脚本与实验共享作者——外部基准是真独立性；交叉验证会"一致地错"

## 8. 未测试预测清单（模型的保留条款，防止过拟合历史）

1. **D1 运气零**：在足以击败 DeepSeek 拒绝行为的攻击下（异族攻击者/GCG 级）应断裂；D3 不会（除非 substrate 被攻破）——未测试
2. **C1a privileged node**：agent 自授权通道 → 规则漂移概率更高——未实验（测试床可构造）
3. **连续 Z(α) frontier**：7 点离散梯度 → 连续失败前沿——未做
4. **LITMUS 真跑**：需 Ubuntu+OpenClaw——未做

## 9. 给新 AI 的起点建议

1. 读 `docs/24`（方法论宣言）→ `STATUS.md` → `agentsec/REPORT.md` → `paper2/paper.md`
2. 验证环境：`py agentsec/test_keys.py`
3. 与用户确认走哪条：arXiv v2 提交预案 / 构造实验继续（C1a 或连续 Z(α)）/ 专著收尾 / HANDOFF 本身
4. 执行纪律见 §7；未测试预测见 §8（**先测预测，别急着加新东西**）
