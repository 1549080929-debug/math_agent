# math_agent — LLM 多步推理的失败模式与验证框架（VAL）

> **一句话**：一个仓库、三个章节、一条脉络——研究"LLM 多步推理的失败模式与验证框架"。
> 三章实验的元结论已升华为 **验证自主等级（VAL, L0–L5）**——给"验证方案"本身分级——
> 并沉淀为预印本 **Grading the Graders**。
>
> 核心主张（可原样引用）：
> **每一层都必须挂接可验证的裁判，而裁判必须理解"完备性"而不只是"正确性"。**
> LLM 只做翻译（拆解/声明/渲染），确定性代码做裁判；验证规格必须锚定在
> "不依赖 LLM 声明"的地面真值上。
>
> 贯穿三章的元教训：**"裁判的裁判也需要裁判"**（验证器自身也要被校准/审计）。

---

## 论文（arXiv 预印本）

**Grading the Graders: Verification Autonomy Levels (L0–L5) for LLM Reasoning**

- **一句话**：别人给答案分级，本项目给"分级"分级。
- **状态**：v1.0 草稿完成；提交包就绪（`paper/submission.md`）；待背书后投 arXiv（cs.AI）
- **文件**：`paper/preprint.md`（源稿）· `paper/preprint.pdf`（14 页，可上传版）· `paper/submission.md`（arXiv 表单提交包）

## VAL 验证自主等级（跨三章的元结论）

| 等级 | 锚定来源 | 保证 | 完备性 |
|---|---|---|---|
| **L0** | LLM 自证（"我检查过了"） | 无 | 无 |
| **L1** | 题面/代码确定性规则 | 确定性匹配 | 无 |
| **L2** | 客观真值 / oracle / 金标 | 正确性 | 无（**完备性盲区**） |
| **L3** | 可判定系统（解集等价 / 类型 / 决策规则） | **单性质完备** | 有（ODD 内） |
| **L4** | 领域级证明系统（类型系统 / 证明内核） | 领域完备 | 有（域内） |
| **L5** | 通用完备验证 | 任意性质 | **不可判定**（Rice 定理） |

- 判级工具：`val_standard.py`（判级三问的可运行版）
- 抬级工具：`val_raise.py`（L2→L3 重编码处方——框架从诊断走向生成）
- 追问层：`val_interrogate.py`（buzzword 不豁免，不清楚就不猜）
- 判级标准：`docs/06-判级标准.md` · 等级体系：`docs/05-锚定层级.md` · 文献对照：`docs/07-文献评述.md` · 抬级可行性：`docs/09-抬级器可行性.md`

## 工具链（一条命令）

```
声称 → [追问层 问] → [判级器 判] → [抬级器 开处方] → [审计报告 体检]
        不豁免buzzword   你在哪一级    怎么上去/上不去为什么    整条验证链健康
```

```bash
python val_chain.py    # 一条命令：33/33 自测 + 演示走查（全仓库含压力测试共 38/38）
```

| 工具 | 作用 | 自测 | 命令 |
|---|---|---|---|
| `val_interrogate.py` | 追问层：自由文本声称→判级参数，buzzword 穿透 | 5/5 | `python val_interrogate.py --auto`（交互：无参数运行） |
| `val_standard.py` | 判级器：L0–L5 分类（Q1 规格来源/Q2 保证/Q3 范围） | 10/10 | `python val_standard.py` |
| `val_raise.py` | 抬级器：六模式重编码处方 + 可判定域扫描 + 审计报告 | 18/18 | `python val_raise.py` |
| `val_demo.py` | 演示走查：判级→抬级→处方→体检四步 | — | `python val_demo.py` |
| `stress_test.py` | 压力测试：多智能体投票/SymPy 用法/主观性质/混合栈/区块链 buzzword | 5 题 | `python stress_test.py` |

诚实边界（工具会说的"不"）：性质不可编码 → 无法抬级；可判定性未知 → 要求人工确认；输入是声称（L0），工具不验证其真实性。

## 三章总览

| 章 | 领域 | 状态 | 结论 |
|---|---|---|---|
| 一 | 数学验证（LLM+SymPy） | ✅ 封存 | 准确率窗口空（16/15/13 vs baseline 20/20）；价值=**错误可报告性**；L3 解集等价抓漏解 |
| 二 | 行为观测（prompt injection） | ✅ 封存 | 五轮迭代：FPR 92%→30%、强攻击 TPR 1.0、弱攻击 0.75；边界=隐匿执行 0.60（L2 天花板） |
| 三 | 医疗诊断 | 🔄 进行中 | LLM 教科书 10/10、硬病例 8/10；失败模式="信息不足仍下结论"；**信息完整性裁判 3/3**（含人工漏判 #105）；**L3 抬级成功：导入 Alvarado 决策规则**（阑尾炎 ODD，区间缺数据语义） |

## 快速开始

```bash
# 1. 配置密钥：local_config.json（不入 git）或环境变量 DEEPSEEK_API_KEY
pip install -r requirements.txt

# 2. 裁判单元测试（无需 API）
python test_verifier.py        # 42/42

# 3. VAL 判级工具自测
python val_standard.py         # 10/10

# 3b. VAL 抬级器自测
python val_raise.py            # 18/18

# 3c. VAL 追问层自测（buzzword 穿透）
python val_interrogate.py --auto   # 5/5

# 4. 跑一道数学题
python main.py -p "求函数 f(x)=x^2-4x+7 在区间 [1,4] 上的最小值"

# 5. 医疗裁判实跑（无需 API）
python medical/verify_diag.py
```

## 文档导航

| 文档 | 内容 |
|---|---|
| [docs/01-研究叙事.md](docs/01-研究叙事.md) | 项目故事主线（投名状第一页，四结论版） |
| [docs/02-失败模式分类学.md](docs/02-失败模式分类学.md) | 8 个失败模式，全部有数据实证 |
| [docs/03-架构设计备忘.md](docs/03-架构设计备忘.md) | 设计决策的"为什么" + 已知边界 |
| [docs/04-实验档案.md](docs/04-实验档案.md) | 8 轮实验全记录与数据索引 |
| [docs/05-锚定层级.md](docs/05-锚定层级.md) | **VAL 等级体系（可迁移结论）** |
| [docs/06-判级标准.md](docs/06-判级标准.md) | **判级三问 + 决策程序 + 使用清单** |
| [docs/07-文献评述.md](docs/07-文献评述.md) | **17 篇"分层验证"论文 × VAL 判级（V1.3，版本化追踪）** |
| [RESULTS.md](RESULTS.md) / [EVALUATION.md](EVALUATION.md) | 结果总账 / 早期评估 |
| [HANDOFF.md](HANDOFF.md) | 项目交接文档（新 AI 接手的全部上下文） |

## 目录结构

```
math_agent/
├── main.py                # 第一章主流程（分类→拆解→验证→纠错→组合→终局验证）
├── verifier.py            # 裁判：9 种验证类型（含 L3 solution_set），ANCHOR_LEVELS 标注等级
├── decomposer.py / solver.py / combiner.py / final_check_deriver.py
├── llm_client.py / config.py          # DeepSeek 客户端 / 配置（密钥外置）
├── test_verifier.py       # 裁判 42 用例
├── val_standard.py        # VAL 判级工具（10 用例）
├── behavior/              # 第二章：行为观测（5 轮迭代，REPORT.md 完整报告）
├── medical/               # 第三章：医疗诊断（cases*.json 病例 + verify_diag.py 裁判 + REPORT.md）
├── data/ logs/            # 全部实验数据 / 运行痕迹
├── docs/                  # 01-07 方法论文档（含 VAL 体系/判级标准/文献评述）
├── paper/                 # arXiv 预印本（preprint.md/pdf、submission.md 提交包）
└── README.md / HANDOFF.md / RESULTS.md / EVALUATION.md
```

## 已知边界（诚实版）

1. **完备性盲区**：代回/采样验证无法证明"没有遗漏"——原理性开放；L3 解集等价仅在 ODD（可判定域）内闭合；
2. **准确率窗口**：数学章架构不优于 baseline（16/15/13 vs 20/20）——价值在错误可报告性，不在准确率；
3. **行为章天花板**：隐匿执行攻击（输出层无痕迹）是 L2 结构性边界（TPR 0.60）；
4. **VAL 自身未验证**：判级程序是确定性的，但其 Q1/Q2 判断的可复现性（inter-rater）尚未在规模语料上检验——judge 的 judge 也需要 judge；
5. **医疗章伦理边界**：合成虚构病例、无真实患者数据、非诊断工具、不构成医疗建议。

---

*更多上下文见 [HANDOFF.md](HANDOFF.md)——新 AI 接手项目的完整交接文档。*
