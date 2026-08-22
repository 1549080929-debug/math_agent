# 项目交接文档（HANDOFF v2）

> 用途：压缩对话，转移新对话框。把本文件全文粘贴给新 AI 的第一条消息即可继续。
> 最后更新：2026-08-20。v1 交接于 2026-08-18（三章实证时代），本版覆盖至"两篇论文 + AgentDojo 集成"。

---

## 0. 一句话定位

**一个仓库、三章实证、两条延伸线、两篇论文、一本专著**：
研究"LLM 验证/安全防御的失败模式"，核心框架 **VAL（验证自主等级 L0–L5）**——按"验证规格的来源"给验证方案分级。
元教训："裁判的裁判也需要裁判"（框架/实验/代码三层审计，均已实证上演）。

## 1. 论文（两条线）

| 论文 | 状态 | 内容 |
|---|---|---|
| **Grading the Graders**（arXiv:2608.19009） | ✅ v1（08-19）+ v2（08-20）**已公布**，cs.CL | VAL 框架 + 完备性盲区 + 四域实证 + 可复现性研究（κ≈0.8）+ PPMF 案例 + 锚语义 + 15+ 修正 |
| **The Same Zero**（paper2/，14 页） | 📤 **已提交 arXiv（08-20）待公布** | 22 防御等级图 + 预测验证 10/10 + 部署价值实验 + 2×2 + **AgentDojo 官方基准同设置对比** |

**第二篇论文的关键数字（投稿版）**：
- 部署价值实验（自研测试床，~5400 calls）：ND ASR 33.3% → **V 栈（确认门+参数沙箱）0.000/1.000 良性** vs N 栈（提示加固+关键词过滤）0.000/0.000——同一个 0，V 是结构（平台记录+schema，双受害者免疫），N 是模型运气（合规 0.235，半配合墙）
- **2×2 矩阵**（Llama 8B 第二受害者）：ND 0.253/0.328（Llama 更抗注入）、N 0.000/0.014、V 双受害者 0.000/1.000——结构跨受害者成立，运气跨受害者证实
- **跨家族尝试**：Kimi（kimi-k2.6/k2.7）与 Llama 8B **拒绝当攻击者**（显式拒答/中性改写消毒/消毒产物受害者侧无效）——"攻击者侧对齐约束跨家族红队招募"是可报告发现
- **AgentDojo 官方基准同设置对比**（banking，6 任务×6 注入×4 攻击=144 对/配置，DeepSeek）：**V 0.0% ASR [0, 2.6] @ 83.3% utility**；官方 tool_filter 0.0% @ **16.7%** utility；RP 8.3%、SL 6.2%、ND 6.2%、N 3.5%——V 与最强官方防御 ASR 持平、utility 5 倍
- **N 栈跨测试床漂移是运气主张的最强证据**：我们测试床 0.000 vs AgentDojo 3.5%——"N 的零是上下文相关的模型行为，换基准零就移动；V 的零不动"（论文 §6.5 原话）
- 审稿 8 项 P0/P1 修正 + 审查 7 条（CI/同设置对比/N 栈转正/四攻击族）**全部落地**

## 2. 三章实证（v1 时代，已封存）

- 数学：42/42 裁判、20 题 16/15/13 vs baseline 20/20（准确率窗口空，架构价值=错误可报告性）
- 行为观测：FPR 92%→30%，隐匿执行 0.60 是 L2 结构天花板
- 医疗诊断：教科书 10/10、硬病例 8/10、信息完整性裁判 3/3（含 #105 人工漏判发现）
- 代码生成（第四章）：164/164、6/6，反向验证 4/5 预测命中
- 失败模式分类学：9 模式（docs/02，含新增"来源洗白"）

## 3. 研究资产现状

- **可复现性研究**（方向 1，五轮收束）：协议 v2.3（R1–R15）· 70 条语料 · 评分者 A + B2–B7 · 两两 κ 0.77–0.93 · 安全子集 22 条 90.9% · 作者 6 处判级偏差定位
- **方向 3**（Agent 安全）：docs/12（PPMF 案例）· docs/13（锚语义 intent/truth/effect）· docs/14（VAL→ASR 预测协议）· docs/15（论文骨架→完整草稿）· docs/17（2027 投稿规划）
- **专著**：《给"分级"分级》127 页（book/，`py book/build_book.py` 重建）——待更新 2×2/跨家族/AgentDojo 新发现
- **演示**：`py demo/showcase.py [--batch]`（1 分钟 live：VAL 判级 + 智能体安全对比 + κ + 作品集）
- **工具链**：val_standard（11 自测）/val_raise（22）/val_interrogate（5）/val_chain（38）/verifier（42）

## 4. 关键文件索引

| 路径 | 内容 |
|---|---|
| `paper/` | 论文 1 源稿+PDF（21 页 v2）+ 提交包 + figure1 |
| `paper2/` | 论文 2 源稿+PDF（14 页）+ 提交包 + 构建脚本 |
| `agentsec/` | 测试床（scenarios 50 场景/attacks 12+4 变体/defenses D1-D4/effects 真效果执行器/victim_client 双模型/adaptive 自适应+白盒+PAIR-lite/**agentdojo_integration.py**）+ REPORT.md（含 7.10 同设置对比） |
| `reliability/` | 判级语料/评分/分析/预测卡/arXiv 抓取/validation（含 AgentDojo 论文全文） |
| `docs/01–17` | 研究文档全集（17 篇） |
| `book/` | 专著 |
| `STATUS.md` | 状态总账（VAL 视角定级） |
| `CAPABILITIES.md` | 能力清单 |
| `promo/` | 知乎/推特/邮件/两篇 arXiv 走查 |
| `local_config.json` | API key（gitignored）——**DeepSeek key 当前有效** |

## 5. 环境配置

- Python：`C:\Users\殷雅杰\AppData\Local\Programs\Python\Python313\python.exe`（`py` 启动器）
- DeepSeek：api.deepseek.com / deepseek-chat（local_config.json，已验证）
- 本地 Ollama：llama3.1:8b（RTX 4050 6GB）——受害者切换：local_config 的 VICTIM_* 三字段
- 攻击者/受害者抽象：`agentsec/attacker_client.py` / `victim_client.py`（OpenAI 兼容，可接任意端点）
- git：SSH over 443 已配；命令用 `;` 分隔（PowerShell 5.1 不支持 &&）；**每步提交推送**
- 网络：arxiv/PyPI/GitHub 可直连；Google 被墙（WebSearch 类工具会超时，用 arxiv API/curl 代替）

## 6. 待办（按优先级）

1. **第二篇 arXiv ID 公布后**：更新 README/STATUS 链接（同第一篇流程）
2. **P2 实验扩展**（可选）：workspace/slack 套件 · Llama 受害者跑 AgentDojo · per-pair utility 明细
3. **ARR 2027 周期**（docs/17）：增强五杠杆（未对齐攻击者 Groq 70B / AgentDojo 已✅ / 2×2 多 seed / P02 SLR 对话节 / 良性扩样）→ 12 月 ARR 第一轮（目标 ACL 2027）→ 5-6 月 EMNLP 2027
4. **专著 v2**：吸收 2×2/跨家族/AgentDojo 结果
5. 可选：作者补判（N 系列，人机一致性）、第二篇 arXiv v2（若公布后还需修正）

## 7. 纪律与血泪教训（新 AI 必读）

1. **审计先行、测价值窗口、诚实负结果、每步提交推送**——项目的方法论本身
2. **裁判的裁判**：判级被盲评修正 6 处 · main.py 回退洗白面被关（LLM 规格 PASS→UNSURE）· 实验 3 个 bug（schema 正则/resume 假 seed/指标误读）被抓——**对数字永远做 trace 级验证**
3. **指标方向陷阱**：AgentDojo 的 security_results 平均 = ASR（True=攻击达成），曾误读为防御率导致"0.000 悖论"——跨库指标先查语义再解读
4. **API key 安全**：曾误入 git 的 `git add -A`（amend 清除、未推送）——local_config.json 已 gitignore，commit 前检查
5. **对齐模型不愿当攻击者**：跨家族红队需"愿意配合"的攻击者（Groq Llama 70B 候选），显式越狱框架会被拒答
6. **半配合墙**：模型在加固提示下对注入"提议工具但给空参数"——压制 ASR 但不构成结构保证（双受害者实测）

## 8. 给新 AI 的起点建议

1. 读 `STATUS.md`（级别总账）→ `agentsec/REPORT.md`（实验全史）→ `paper2/paper.md`（论文 2 现状）
2. 验证环境：`py agentsec/test_keys.py`（两端 OK 才算环境就绪）
3. 与用户确认走待办 1/2/3 哪条；执行纪律见 §7
