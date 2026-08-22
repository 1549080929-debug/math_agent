# ARR 提交表单材料包（October 2026 Cycle → ACL 2027）

> 生成：2026-08-22 · 依据：aclrollingreview.org 官方页面（cfp / dates / authorchecklist / areas / responsibleNLPresearch，curl 直连核实）
> ⚠️ 交接文档/STATUS/docs17 中"ARR 2026-12"周期**不存在**——ARR 自 2025-05 起为 10 周一轮（一年 5 轮），最近可行窗口是 **2026-10-12**。本文档为权威版本。

---

## 0. 关键日期（官方核实，2026-08-22 抓取）

| 事项 | 日期 | 备注 |
|---|---|---|
| **October 2026 周期提交截止** | **2026-10-12** | 距今天约 7 周 |
| Reviewer 注册截止（所有作者） | 提交后 48h 内（约 10-14） | 不注册可能 desk reject |
| Reviews due | TBA（周期内） | |
| Author Response | TBA | |
| Meta-reviews 发布 / 周期结束 | **2026-12-20** | |
| ACL 2027 commitment | 2027-01（final ARR submission date = January 2027） | 承诺日期 TBA |
| 备选：NAACL 2027 & COLING 2027 | 承诺 2026-12-20 | 同一周期可投 |

**结论**：投 October 2026 周期（10-12 提交）→ 12-20 拿 meta-reviews → 2027-01 承诺 ACL 2027。若 7 周来不及，下一周期（约 2026-12/2027-01，TBA）仍可赶 ACL 2027。

---

## 1. Title（最终）

```
The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security
```

## 2. Abstract（199 words —— 同时满足 200/250 上限；论文内摘要已同步为此版）

```
LLM-agent security has produced a dense landscape of defenses—prompt hardening, content filters, permission gates, sandboxes—each claiming to make agents safe, lacking a pre-purchase question: what does a given defense actually guarantee, and where does that guarantee come from? We apply Verification Autonomy Levels (VAL), which grades verification schemes by the source of their specification (L0: LLM self-declaration; L1: deterministic rules; L2: objective ground truth; L3/L4: decidable completeness; L5: impossible), to 22 agent-security defenses. The taxonomy is falsifiable: a defense fails the way its anchor fails. We validate this with frozen prediction cards on a small published sample (10/10 hits, flagged), then run the first controlled deployment-value comparison: same budget, a VAL-guided stack (intent-anchored confirmation gate + schema sandbox) versus a mainstream intuition stack (prompt hardening + keyword filter), across 50 scenarios and 12 attack families under adaptive/white-box/PAIR escalation, three seeds (~7,000 calls). The VAL stack holds 0.000 attack success with 1.000 benign success; the intuition stack reaches 0.000 ASR but kills all benign actions, its security resting on model-behavior luck (compliance 0.235) rather than structure (the VAL stack tolerates 2.4x more compromise—0.567 compliance—and still blocks everything). The same zero, two different guarantees: zero is an outcome, not a guarantee.
```

## 3. Comments to Reviewers（草稿，可粘贴）

```
This paper asks a question the field has not asked explicitly: what does a given LLM-agent security defense actually guarantee, and where does that guarantee come from? It applies a published verification taxonomy (VAL) to agent security and validates it with (i) frozen prediction cards and (ii) the first controlled deployment-value comparison between a VAL-guided defense stack and a mainstream intuition stack, including a same-setting validation on the official AgentDojo benchmark.

Points we ask reviewers to note:

1. Prediction cards were frozen before outcome data and are reported with their status (10/10 hits on a small published sample, flagged as such). The falsifiability mechanism is the claim, not the hit count.
2. The deployment comparison is controlled (same budget, scenarios, attack families; real tool effects; three seeds) and includes AgentDojo's official defenses run in the identical harness/model/subset for a same-setting comparison.
3. We do not claim VAL is the unique correct ontology. It is offered as a falsifiable organizing principle, with honest boundaries (single victim model, self-built testbed, sample sizes) in the Limitations section.

The taxonomy we build on is cited anonymously in accordance with the ARR anonymization policy; the full reference will be restored in the camera-ready version.
```

## 4. Area / Track（ARR 2026-03 起的新 track 体系）

| 优先级 | Track | 理由 |
|---|---|---|
| **主** | **LLM agents**（tool use / agent evaluation / agent memory / environment interaction） | 论文核心是 LLM-agent 安全：防御、攻击、评估 |
| 备选 | Language Modeling（safety / security / adversarial attacks / red teaming / robustness） | 若表单单选且 LLM agents 不可用 |
| 不选 | NLP Applications（security/privacy） | 泛应用向，匹配度低 |

## 5. Keywords（表单若需，从官方 keyword 池选）

`LLM agents` · `agent security` · `prompt injection` · `adversarial attacks` · `safety` · `agent evaluation` · `tool use` · `robustness`

## 6. Preprint status（需用户决定）

论文（The Same Zero）未被 arXiv 接收（moderation 退回）→ 当前**无任何非匿名 preprint**，可选绑定选项：

- **选项 A（推荐）**：`We do not intend to release a non-anonymous preprint`（binding）——享有匿名激励（匿名奖 + borderline 优先），代价是 meta-review（约 12-20）前不能公开命名版
- **选项 B**：`We are considering...`——保留随时发布 arXiv 的自由，但失去绑定激励
- 注意：Grading the Graders（arXiv:2608.19009）是**先前工作**，不属于本文 preprint，不受此约束

## 7. Responsible NLP checklist（草稿答案，逐题）

### A. 通用
| # | 问题 | 答案 | 依据 |
|---|---|---|---|
| A1 | 描述局限性？ | **Yes** | §8 Limitations（4 条：单模型/自建测试床/覆盖率/评分者样本） |
| A2 | 讨论潜在风险？ | **Yes** | 安全研究双重用途：本文不引入新攻击技术，攻击族均来自公开基准（AgentDojo [4]）或简单手写注入；贡献是防御选型。详见 §6.5/§8 |

### B. 科学制品
| # | 问题 | 答案 | 依据 |
|---|---|---|---|
| B1 | 引用所用制品创建者？ | **Yes** | AgentDojo [4]、LITMUS [13]、PPMF [2] 等已引用；API 模型（DeepSeek-chat）以名称/版本标识（§3.3/§6.5） |
| B2 | 讨论许可证/使用条款？ | **No** | 论文未讨论许可证；代码/数据拟以 CC-BY 4.0 发布（camera-ready 补）；AgentDojo 许可证提交前需核实 |
| B3 | 使用与预期用途一致？ | **Yes** | AgentDojo 按官方评估用途使用；自制场景仅用于研究 |
| B4 | 检查 PII/冒犯内容？ | **Yes** | 全部数据为合成（注入文本/银行场景 fixture），无真人数据 |
| B5 | 制品文档（领域/语言等）？ | **Yes** | §3.3 描述 50 场景构成（30 恶意+20 良性）；AgentDojo banking 套件由官方文档覆盖 |
| B6 | 报告统计（例数/split）？ | **Yes** | 全篇报告：50 场景、12 攻击族、380 cases/config、144 对、3 seeds、CI |

### C. 计算实验
| # | 问题 | 答案 | 依据 |
|---|---|---|---|
| C1 | 参数数/计算预算/基础设施？ | **Yes** | Llama 3.1 8B（§6.4）；DeepSeek-chat 为闭源 API（参数未公开，如实说明）；~7,000 次 LLM 调用（§6）；本地 RTX 4050 |
| C2 | 实验设置/超参？ | **Yes** | temperature 0.2（§3.3）；无超参搜索（防御确定性）；攻击轮次 3/7（§6.2/附录） |
| C3 | 描述统计（误差棒/mean/max）？ | **Yes** | Wilson 95% CI、3 seed mean±std（§6.1/§6.3/§6.5） |
| C4 | 现有包/实现/参数设置？ | **Yes** | AgentDojo harness 0.1.35 [4]；Ollama 本地部署；DeepSeek API base_url（§6.5） |

### D. 人类标注者
| # | 问题 | 答案 | 依据 |
|---|---|---|---|
| D1–D5 | 人类被试/标注者？ | **No** | 无人类被试；论文评分者为 6 个盲评 LLM（§3.1/§4 已如实披露） |

### E. AI 助手
| # | 问题 | 答案 | 依据 |
|---|---|---|---|
| E1 | 使用 AI 助手？披露？ | **Yes** | 本项目为 AI-assisted research：AI 助手用于编码、实验编排与写作辅助。匿名版无致谢章节，故按政策在 checklist 中披露（本响应即披露声明）；符合 ACL 生成式 AI 政策（作者对内容负全责） |

## 8. 提交前检查清单（authorchecklist 逐项对照）

- [x] 长文页数：正文 8 页（不含 Limitations/References/附录）——`final_pages.txt` 核实
- [x] 有 "Limitations" 章节（§8），置于 References 前，只含局限讨论
- [x] PDF 匿名：无作者名/邮箱/ORCID/GitHub/arXiv 自引号（`pypdf` 提取全文扫描 clean，2026-08-22）
- [x] 自引匿名化：`[1]` → `(Anonymous 2026)`，bib 条目 `author={Anonymous}, note={Under review}`（官方示例格式）
- [x] 无致谢章节；无指向非匿名仓库/Dropbox 的链接
- [x] 无先前修订残留的 meta-text
- [ ] 附录双栏格式（ACL 模板自带；编译产物确认）
- [ ] 用官方 `aclpubcheck` 工具过一遍（提交前做，当前断网无法安装）
- [ ] OpenReview 账号 + 完整 profile（affiliation / semantic scholar / dblp / ACL anthology / email）
- [ ] Reviewer 注册表单（提交后 48h 内，所有作者）
- [ ] 提交时填写 preprint status（§6）
- [ ] 提交后 48h 内 metadata（含 checklist）仍可编辑

## 9. 开放问题（提交前需处理）

1. **acl.sty 版本**：当前模板为仓库自带（ACL 2024 系）。ACLPUB 指南 2025-01 更新过字体/表格/Limitations 位置。提交前对照最新官方模板（Overleaf ACL template）检查 `acl.sty`，必要时升级并重跑管线。
2. **AgentDojo 许可证**：B2 需在提交前核实（其 repo 许可证），在 checklist 或补充材料中注明。
3. **匿名仓库**：若提供代码/数据链接，需用 anonymous.4open.science（检查清单明确要求），不能用个人 GitHub。
4. **超页风险**：现在正文 8 页是"刚好"——若 reviewer 反馈后加内容，注意别超。附录 A.1–A.5 已吸收大部分细节，正文留有余量。
5. **abstract 上限**：OpenReview 表单未直接核实（需要登录）。199 词同时满足 200/250 两个可能上限，安全。
6. **DOI/会议版本**：camera-ready 时恢复作者信息 + 完整自引 + 致谢（含复旦 JADE / 南航 LITMUS 沟通致谢？——谨慎：致谢第三方需先征得同意）。

## 10. 时间线建议（距 10-12 的 7 周）

| 周 | 事项 |
|---|---|
| 1（本周） | ✅ 匿名化 PDF + 本材料包；提交 git；用户注册 OpenReview + 完善 profile |
| 2-3 | （可选）C1 另一半（bounded exception）增强实验，若做则插入 §6/附录并重跑管线 |
| 4 | acl.sty 对照官方模板检查；aclpubcheck 过稿 |
| 5-6 | 用户通读全文终审；Comments 定稿；checklist 定稿 |
| 7 | 10-12 提交 + 48h 内 reviewer 注册 |
