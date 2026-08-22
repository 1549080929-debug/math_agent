# 第二篇论文的定位与证据链（The Same Zero）

> 日期：2026-08-22 · 专著 v2 新增章 · 对应 paper2（arXiv 已提交待公布，标题已定为 *The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security*）

---

## 1. 论文定位：mid-level methodological claim

第二篇论文的站位在审稿演练中被反复打磨后钉死为一个**中尺度方法论声明**，既不是"AI 安全的普遍理论"，也不是"两个防御的比较实验"：

> **在 LLM-agent security 中，当不同防御给出同一个 security outcome（如 0 ASR）时，我们需要知道这个 outcome 是由什么 verification anchor 支撑的——这决定了它的 guarantee，并预测它的失败边界。**

论文显式声明**不 claim** 的部分：
- 不是 AI verification 的一般理论（robotics / formal methods / HITL / non-agentic LLM 均划出 scope）
- 不是完整的安全测评
- 不是按质量给防御排序
- 不是覆盖所有可能防御

**三层结构**（论文的 spine）：

```
现象层：  The Same Zero —— 两个防御可达到相同的 0 ASR，但 guarantee 相反
   ↓
机制层：  verification anchor —— 差异在于安全裁决 grounded 在哪里
   ↓
方法层：  VAL —— 识别最强实际 grounded 的 guarantee，并预测每级的失败边界
```

## 2. 核心现象：The Same Zero

**ASR 是结果，Anchor 是结果站在哪里。**

| | V 栈（确认门+参数沙箱） | N 栈（提示加固+关键词过滤） |
|---|---|---|
| ASR | 0.000 | 0.000 |
| 良性 | 1.000 | 0.000 |
| 合规率 | 0.567（被驱动仍全拦） | 0.235（模型半配合） |
| 零的性质 | 结构（平台记录+schema 枚举） | 运气（模型行为） |

证据链完整形态：**同一个数字 → 不同内部机制 → 不同 robustness → 不同 utility → 不同 guarantee**。这使"same zero"从哲学观察变成工程问题。

## 3. 机制：verification anchor

防御失败的方式 = 其锚失效的方式：
- L0（模型自述）：模型被注入驱动即失败
- L1（确定性规则）：改写绕过
- L2（客观真值）：ODD 外失败（伪造元数据、投毒数据）
- L3（可判定系统）：ODD 内构造性成立
- L5（通用完备）：不可证

## 4. 方法：VAL 是 guarantee provenance framework

VAL 不是"告诉你系统多安全"的安全分级系统，而是**"告诉你观察到的安全结果 grounded 在哪里"**的 guarantee provenance framework。归因（这个零站在哪里）+ 预测（因此它会在哪里失败）双价值。

## 5. 领域 insight：L3 frontier = confinement, not semantics

第二篇除了 "same zero" 现象外，第二个能留下来的领域结论：

> **在 agent security 中，L3 锚真正适合的是可被严格约束的 property——confinement、information flow、data/control separation；而"这个 action 语义上是否安全"仍封顶于 L2。**

"能不能做"可以编码成可判定系统（L3）；"该不该做"是语义判断（L2 封顶）。这是防御选型的可操作结论。

## 6. 证据链（五个独立来源）

| 来源 | 内容 | 对论文的支撑 |
|---|---|---|
| 自建测试床（~5400 调用） | V 0.000/1.000 vs N 0.000/0.000 | 现象 + 部署价值 |
| 2×2 矩阵（Llama 受害者） | V 双受害者 0.000/1.000；N 运气跨受害者证实 | 结构跨受害者成立 |
| AgentDojo 官方基准 | V 0.0% ASR @ 82.6% utility vs tool_filter 0.0% @ 16.7% | 第三方基准，utility 5 倍 |
| JADE 真实 MCP（复旦实例） | ND 87.5%（复现官方 83%）、N 6.2%（M6 词表盲区真实漏）、V 0%（模型被驱动 93.8% 仍全拦） | 第三方真实 MCP 协议 + 预测卡 5/5 |
| LITMUS 互证（南航） | EH（口头拒绝+OS 层静默执行，EHR 7.98–17.97%）vs 我们 covert execution（TPR 0.60 天花板） | 独立复现"语义层锚的结构盲区" |

五个来源无共享实现，收敛到同一结论——这是 VAL 分类有效性最强的外部辩护。

## 6b. Z(α)：zero stability 成为可测量轴（2026-08-22 新增）

构造实验把 "same zero" 从观察推进为可测量现象。固定 agent/task/attacker/ODD，构造四种 provenance 的零（D1 refusal / D2 keyword / D3 confirmation / D4 sandbox），在攻击增强下追踪每轮累计 ASR：

| cfg | α=静态 | 轮1 | 轮2 | 轮3 | failure morphology |
|---|---|---|---|---|---|
| D1 | 0.000 | 0.000 | 0.000 | 0.000 | **behavioral plateau** |
| D2 | 0.200 | 0.200 | 0.467 | 0.467 | **abrupt collapse**（轮 2） |
| D3 | 0.000 | 0.000 | 0.000 | 0.000 | **structural plateau** |
| D4 | 0.067 | 0.067 | 0.167 | 0.200 | **progressive erosion** |

**最关键的发现**：D1 与 D3 的 Z(α) 轨迹**完全重合**（都平在 0），但 provenance 不同——D3 白盒合规率 0.567（模型被驱动过半仍全拦，平台记录），D1 白盒合规率 0.333（零是 DeepSeek 的拒绝脾气）。**重合轨迹本身不能解释为什么稳定，必须引入 provenance。**

升级后的核心 claim：**Identical observed zero-stability profiles do not, by themselves, establish equivalent security guarantees.**

可证伪预测：D1 的平线会在足以击败 DeepSeek 拒绝行为的攻击下断裂；D3 不会（under an uncompromised authorization/audit substrate）。

Z(α) 已提升为论文贡献 4（Zero stability as a measurable axis）。诚实边界：3 离散阶段×30 例/点（proof-of-concept，非连续 frontier）；轮 1 = 静态 direct 变体注入（α 轴语义需准确表述）。

**实验修复（审计驱动）**：构造实验发现论文 §6.1 混用 v2/v3 口径（D1-D4 旧 stub 数据）→ 重跑 v3 真效果（D2 0.258→0.200、D4 0.079→0.067）→ 补跑 D1/D3 自适应+白盒（预测卡冻结，5/6 命中）→ Z(α) 从既有 adaptive rows 提取（零成本，rounds 字段即突破轮次）。

## 6c. 三项边界收紧（2026-08-22）

审稿演练沉淀的措辞原则——**claim 边界画在证据边界上，甚至略窄**：
1. **VAL-selected → VAL-guided**：不声称 VAL 是最优选择器（没和别家选择策略比过），只描述"按 VAL 指引"的动作
2. **semantic caps at L2 软化**："open-world property for which no decidable fragment is available **in the unrestricted setting**... restricted semantic properties that can be formally encoded remain eligible for higher levels"——防 formal methods reviewer 拿受限语义属性反例
3. **10/10 弱化**：从"验证准确率"降为"小样本上冻结预测的命中记录（已标注）"，核心价值是 falsifiability 和机制修正，不是 hit count

## 7. 与第一篇的关系：研究路线

- **第一篇**（Grading the Graders，arXiv:2608.19009）：建立 verification 的坐标系（VAL，元层面）
- **第二篇**（The Same Zero）：把这个坐标系放进 agent security，发现 deployment-level 现象

两篇合起来是研究路线而非两篇孤立 paper：第一篇建立语言，第二篇证明这门语言在 agent security 里有用，并发现了一个只有它能解释的现象。

## 8. 诚实边界（审稿演练沉淀）

- VAL 的分类范畴是作者提出的（盲评 κ≈0.8 + 样本外预测 + 跨基准收敛为操作有效性辩护，非外部 ground truth）
- 部署对比是结构防御 vs 最常见行为防御，非全谱系
- "the anchor decides" 是漂亮 slogan；正文用 "predicts"，且限定 "in the cases we can measure"
- 预测验证样本小（10 + JADE 5），核心 claim 是机制（anchor → failure mode）而非命中数
- L4/L5 是 upper-bound conceptual boundary，非实验 claim

## 9. 一句话

> **Zero is an outcome, not a guarantee——在 LLM-agent security 中，同一个 0 可以站在完全不同的 ground 上，VAL 是区分它们、并预测它们在哪里失败的工具。**
