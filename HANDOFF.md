# 项目交接文档（HANDOFF v7）

> 用途：压缩对话，转移新对话框。把本文件全文粘贴给新 AI 的第一条消息即可继续。
> 最后更新：2026-08-22（v7）。v6 交接于同日（表格修复/瘦身/坑总结）；本版新增：**主线 2 正式定义 = AI Research Capability Amplification（docs/27 研究母稿）——研究方法→可审计 protocol→AI 跨任务迁移→可量化科研能力；第二篇论文是实验场，主线 2 是研究能力基础设施**。
> 阅读顺序：本文 → docs/24（方法论宣言）→ STATUS.md → paper2/arr/README.md（ARR 管线）→ agentsec/REPORT.md → paper2/paper.md

---

## 0. 一句话定位

**一个仓库、两篇论文、一本专著、一份方法论宣言、一条研究主线**：
研究"LLM 验证/安全防御的失败模式"，核心框架 **VAL（验证自主等级 L0–L5）**。
**主线 2 = AI Research Capability Amplification**（docs/27 研究母稿）：Research Method → Protocol → AI Adaptation → Cross-task Transfer → Measurable Capability。
第二篇论文（The Same Zero）= 实验场；主线 2 = 研究能力基础设施（隐形杠杆）；第三篇 = 用升级后的 AI 研究全新领域。
元教训：**"裁判的裁判也需要裁判"** + **"经过验证的结果才有资格改变模型"**（docs/24 底层纪律）。

## 1. 论文状态（重要变化）

| 论文 | 状态 |
|---|---|
| **Grading the Graders**（arXiv:2608.19009） | ✅ v2 已公布，cs.CL |
| **The Same Zero**（paper2/） | ⚠️ **arXiv 退回**；**ARR October 2026 周期（10-12 提交）→ ACL 2027**。匿名化 PDF + 表单材料包就绪（v5） |

**The Same Zero 内容**：4 贡献（level map / prediction validation / deployment comparison + Z(α) zero stability）、8 项边界收紧（VAL-guided 等）、三第三方验证（AgentDojo/JADE/LITMUS）、funnel、可证伪预测（D1 运气零）。

## 2. ARR 投稿管线（本次对话核心成果）

**管线就绪，一条命令**：`python paper2/arr/rebuild_full.py`（map citations → pandoc → build_arr → fix_latex → fix_format → fix_natbib3 → xelatex）

- **源**：`paper2/arr/paper_arr.md`（ARR 压缩版，~5,540 words；完整版 `paper2/paper.md` 不动）
- **产物**：`paper2/arr/acl_submit.pdf`（**正文 8 页 + References + 附录**，格式全修）
- **环境**：TinyTeX（C:\TinyTeX，**ASCII 路径必须**——中文路径 kpathsea 不认）+ pandoc 3.9（pypandoc-binary）+ xelatex（Unicode 原生）
- **格式修复记录**：章节编号去重、行号禁用（xelatex+lineno 兼容）、表格列格式（fix_latex colspec 截断 bug 修复）、References→enumerate（绕开 natbib）、Appendix section*
- **流程文档**：`paper2/arr/README.md`（步骤/纪律/边界）
- **版本存档**：`paper2/arr/versions/`（v12 压缩前 + scripts_compression 压缩轨迹）

**下一步（ARR）**：见 `paper2/arr/submission_form.md`（权威材料包：title/199 词 abstract/comments/track=LLM agents/checklist 草稿/开放问题）。⚠️ **周期修正**：ARR 无 12 月周期（10 周一轮）；最近窗口 = **2026-10-12（October 2026）→ meta-review 12-20 → 2027-01 承诺 ACL 2027**。匿名化已做（build_arr.py \author Anonymous + paper_arr.md 去身份块 + refs.bib 自引匿名 + 摘要去 arXiv 号；命名版备份 versions/anon_prep_20260822/）。

## 3. C1a 实验完成（候选命题受控证据）

**C1**：规则制定者/执行者应处于规则 scope 内，或例外显式受限（有时限/可撤销/可追溯）
**C1a 已验证**：agent 自授权通道 → 规则漂移

- **结果**：对照（D3 平台记录）0.000 vs 实验（privileged）**0.717**（43/60，v2 trace-complete 独立重算）
- **审计**：`agentsec/c1a_set_audit.py`——S⊆A 验证（43/43 success 全经 self_authorize）、S∩A∩C=43 机制链完整、ctrl 52/60 尝试利用但被结构拦截
- **文件**：`agentsec/c1a_experiment_v2.py`（120 cases jsonl）、`c1a_summary.py`（独立 aggregator）、docs/25
- **诚实边界**：需强注入（A6/A8）+ exploit 包装；幅度 v1 0.533 vs v2 0.717（随机性，方向稳定）；早期-stop 的 round 是 time-to-success
- **下一步（C1 另一半）**：bounded exception 变体（有时限/可撤销）能否压回 0

## 4. 方法论沉淀

- **docs/24-方法论宣言**：不变量（黑盒→外部可作用面/锚/失败边界）+ 底层纪律（"经过验证的结果才有资格改变模型"+递归补充+硬币另一面）
- **审计独立性 v1**：`agentsec/specs.py`（ASR/compliance/funnel 判定规格单一化，source of truth）
- **候选命题**：C1/C1a（已测）、C1b（历史制度，未测）

## 5. 第三方验证与沟通

| 对象 | 状态 |
|---|---|
| 复旦 JADE（docs/18-20） | ✅ 真实 MCP 验证（ND 87.5%/N 6.2%/V 0%）+ 信已发（docs/20） |
| 南航 LITMUS（docs/21-22） | ✅ 论文整合（§7/§8 互证）+ 信已发（docs/22） |
| **沟通跟进** | ⚠️ **邮件已发无回音（08-22）**——待跟进 |

## 6. 关键文件索引（本次新增）

| 路径 | 内容 |
|---|---|
| `paper2/arr/` | ARR 管线（README.md 入口）；**`submission_form.md` = 提交表单材料包（权威）**；匿名化前命名版备份在 `archive/arr_versions/anon_prep_20260822/` |
| `paper2/arr/versions/` | 版本存档 |
| `agentsec/specs.py` | 审计独立性 v1（判定规格）|
| `agentsec/c1a_*.py` | C1a 实验 + 审计 |
| `docs/24-方法论宣言.md` | 底层纪律 |
| `docs/25-C1a特权节点实验.md` | C1a 完整记录 |
| `docs/26-坑总结与工作流.md` | 表格/环境坑 + 按任务读文件清单（token 优化） |
| `docs/27-研究母稿-主线2-AI研究能力放大.md` | **主线 2 定义文档（核心备忘录）**：17 节完整母稿 |
| `archive/` | 历史/中间/一次性产物（勿主动读，需要时取；arr_intermediates / paper2_patches / agentsec_results / agentsec_jade_assets / book_builds / arr_versions / logs） |
| `STATUS.md` | 状态总账（2026-08-22）|

## 7. 纪律与血泪教训（新 AI 必读）

1. **审计先行、测价值窗口、诚实负结果、每步提交推送**
2. **裁判的裁判**：对数字做 trace 级验证；**pypdf 提取文本 ≠ 视觉渲染**（表格乱要转图看，不能只看文本提取）
3. **改 md 必须重跑全管线**（rebuild_full.py），不能只跑下游——下游产物会 stale
4. **anchor 必须唯一**：'not the hit count.' 在 §1 和 §8 都有 → 误删过正文（git 恢复）
5. **TinyTeX 必须 ASCII 路径**（C:\TinyTeX；中文路径 kpathsea 不认）
6. **resume 坑**：adaptive_attack 跳过已完成场景，改 rounds 重跑需删旧文件
7. **指标方向陷阱**：AgentDojo security_results 平均 = ASR
8. **claim 边界画在证据边界上**（措辞比证据略窄）
9. **审计独立性**：审计与实验共享作者——外部基准是真独立性

## 8. 未测试预测清单（防过拟合）

1. **D1 运气零**：更强攻击（异族攻击者/GCG 级）下应断裂；D3 不会
2. **C1b**（历史制度）：例外受限的制度长期稳定性更高——未测
3. **连续 Z(α) frontier**：7 点离散 → 连续——未做
4. **LITMUS 真跑**：需 Ubuntu+OpenClaw——未做
5. **bounded exception 变体**（C1 另一半）：privileged 通道加"有时限/可撤销"能否压回 0——未做

## 9. 给新 AI 的起点建议

1. 读 `docs/24`（方法论）→ `paper2/arr/README.md`（ARR 管线）→ `STATUS.md` → `agentsec/REPORT.md`
2. 验证环境：`py agentsec/test_keys.py` + `py paper2/arr/rebuild_full.py`（重建 8 页 PDF）
3. 与用户确认走哪条：**ARR 提交准备**（表单/打磨）/ **C1 另一半**（bounded exception）/ **沟通跟进**（复旦/南航）/ **专著更新**
4. 执行纪律见 §7；未测试预测见 §8（先测预测，别急着加新东西）
