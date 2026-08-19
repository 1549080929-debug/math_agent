# Paper / arXiv Preprint 状态清单

> 目标：将本项目（VAL 验证自主等级框架）写成 arXiv 预印本。
> 素材来源：docs/05（锚定层级）、docs/06（判级标准）、docs/07（文献评述 V1.3）、三章实验数据。

## 状态

| # | 任务 | 状态 |
|---|---|---|
| 1 | 6 篇锚定轴论文全文精读（docs/07 V1.3） | ✅ 完成 |
| 2 | **起草预印本骨架（paper/preprint.md）** | ✅ 完成（2026-08-18） |
| 3 | 画"金字塔 + 正交轴"图（Figure 1） | ⬜ 待做（可用 mermaid/figma） |
| 4 | docs/06 判级程序作附录（Appendix A） | ⬜ 待做（直接引用 val_standard.py） |
| 5 | val_standard.py 作可复现工具引用 | ✅ 已有（仓库根目录，10/10 自测） |
| 6 | 标题定稿 + 作者信息 + 许可（arXiv 需 CC-BY 4.0） | ⬜ 待做 |
| 7 | 全文 v1 草稿 | ⬜ 待做 |
| 8 | arXiv 提交（abstract 关键词、分类 cs.CL / cs.AI） | ⬜ 待做 |

## 关键写作决策（起草时已定）

1. **语言**：英文（arXiv 惯例）。
2. **定位**：概念/立场论文（concept/position paper），实证三章作 case study，不宣称"架构更准"。
3. **核心口号**：*"Others grade answers; we grade the graders."*（别人给答案分级，本项目给"分级"分级）
4. **最硬引文**：#4 Safe 原文 *"our formal verifier focuses on the correctness of each step"*——文献对完备性盲区最接近的正面承认。
5. **诚实负结果必须保留**：三章中数学章"架构准确率不优于 baseline（16→15→13 vs 20/20）"是论文可信度来源，不能美化。

## 文件

- `preprint.md` —— 骨架稿（标题/摘要/正文各节草稿 + [TODO] 标记）
- `docs/07-文献评述.md` —— 相关工作素材（17 篇 × VAL 判级，V1.3）
- `val_standard.py` —— 可复现判级工具
