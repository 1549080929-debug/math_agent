# 能力清单：这个仓库能做什么

> 2026-08-20 定稿。演示：`python demo/showcase.py`（约 1 分钟，含 3 次真实 LLM 调用）。

---

## 一、判级与框架（VAL）

| 能力 | 入口 | 演示 |
|---|---|---|
| 给任意验证方案判 L0–L5 | `python val_standard.py` | 11 自测全过；输入 `anchor/guarantee/scope` 即判级 |
| 抬级处方（L2→L3 怎么走） | `python val_raise.py` | 22 自测 |
| 追问层（buzzword 不豁免） | `python val_interrogate.py` | 5 自测 |
| 一键全链（判级→抬级→审计） | `python val_chain.py` | 38/38 全仓库自测 |
| 判级协议 v2.3（15 条规则） | `reliability/protocol_v2.md` | 可复现性 κ≈0.8（4+ 盲评者） |

## 二、智能体安全（自研防御 + 实验）

| 能力 | 入口 | 数据 |
|---|---|---|
| 4 款自研防御（L0–L3） | `agentsec/defenses.py` | 提示加固/关键词/确认门禁/参数沙箱 |
| 40 场景 × 12 攻击测试床 | `agentsec/scenarios.json` + `attacks.py` | 含 AgentDojo 第三方载荷 |
| 真实效果执行器 | `agentsec/effects.py` | 真实账本/发件箱/文件删除 |
| 自适应攻击器（迭代 3 轮） | `agentsec/adaptive_attack.py` | PAIR 风格 + 白盒分层 |
| 完整实验结果 | `agentsec/REPORT.md` | ~4800 次调用；V 栈 0.000/1.000 vs N 栈 0.000/0.000 |

## 三、判级可复现性研究（裁判的裁判）

| 能力 | 入口 | 数据 |
|---|---|---|
| 70 条验证方案语料 | `reliability/corpus.json` | 文献/系统组件/Agent 防御 |
| 6 个盲评者档案 | `reliability/ratings/` | A + B–B5（LLM 盲评） |
| 一致性分析（κ/最弱锚双口径） | `reliability/analysis.py` | 评分者间 κ 0.77–0.93 |
| 预测卡（等级→行为，已冻结） | `reliability/prediction_cards.json` | 16 张，10/10 命中 |
| arXiv 文献抓取 | `reliability/fetch_abstracts.py` | 直连 export API |

## 四、数学验证器（第一章，9 种验证类型）

| 能力 | 入口 | 数据 |
|---|---|---|
| SymPy 确定性裁判 42/42 | `test_verifier.py` | 9 类型含 L3 解集等价 |
| 完备性锚（solveset） | `verifier.py` | 抓漏解/压缩篡改 |

## 五、方法论资产（可复用纪律）

- **审计先行**：标准答案 SymPy 审计（`audit_*.py`）制度化
- **测价值窗口**：baseline 对照（数学 16/15/13 vs 20/20、医疗 10/10、代码 164/164）
- **诚实负结果**：窗口为空如实报告（RESULTS.md）
- **版本化追踪**：docs/07 V1.0→V1.4、判级协议 v2.0→v2.3、五轮迭代
- **裁判的裁判**：可靠性研究审计出作者 6 处判级错误、main.py 回退洗白面

## 六、作品集（对外展示）

| 资产 | 位置 |
|---|---|
| 论文 v1（已上线） | arXiv:2608.19009 · v2 已提交 |
| 专著（127 页） | `book/book.pdf`（`py book/build_book.py` 重建） |
| 方向 3 论文草稿 | `docs/15`（三贡献：等级图/部署价值/锚语义） |
| 15+ 篇研究文档 | `docs/01–16` |
| 推广/申请材料 | `promo/` · `application/` |
