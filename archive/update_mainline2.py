"""Update HANDOFF to v7 (主线2 definition) and STATUS."""
import io

def rw(path, fn):
    raw = io.open(path, 'rb').read()
    crlf = b'\r\n' in raw
    s = raw.decode('utf-8')
    s = fn(s)
    if crlf:
        s = s.replace('\n', '\r\n')
    io.open(path, 'w', encoding='utf-8', newline='').write(s)
    print('updated:', path)

# ---------- HANDOFF ----------
def hd(s):
    s = s.replace('# 项目交接文档（HANDOFF v4）', '# 项目交接文档（HANDOFF v7）')
    s = s.replace('> 最后更新：2026-08-22（v6）。v5 交接于同日（ARR 周期修正/匿名化/表单材料包）；本版新增：**表格溢出修复（tabularx）、Level map 列宽修复（p{1.2cm}）、项目瘦身（archive/ 归档）、坑总结 docs/26、按任务读文件工作流（token 优化）**。',
                  '> 最后更新：2026-08-22（v7）。v6 交接于同日（表格修复/瘦身/坑总结）；本版新增：**主线 2 正式定义 = AI Research Capability Amplification（docs/27 研究母稿）——研究方法→可审计 protocol→AI 跨任务迁移→可量化科研能力；第二篇论文是实验场，主线 2 是研究能力基础设施**。')
    s = s.replace('''**一个仓库、两篇论文、一本专著、一份方法论宣言**：
研究"LLM 验证/安全防御的失败模式"，核心框架 **VAL（验证自主等级 L0–L5）**。
元教训：**"裁判的裁判也需要裁判"** + **"经过验证的结果才有资格改变模型"**（docs/24 底层纪律）。''',
                  '''**一个仓库、两篇论文、一本专著、一份方法论宣言、一条研究主线**：
研究"LLM 验证/安全防御的失败模式"，核心框架 **VAL（验证自主等级 L0–L5）**。
**主线 2 = AI Research Capability Amplification**（docs/27 研究母稿）：Research Method → Protocol → AI Adaptation → Cross-task Transfer → Measurable Capability。
第二篇论文（The Same Zero）= 实验场；主线 2 = 研究能力基础设施（隐形杠杆）；第三篇 = 用升级后的 AI 研究全新领域。
元教训：**"裁判的裁判也需要裁判"** + **"经过验证的结果才有资格改变模型"**（docs/24 底层纪律）。''')
    s = s.replace('| `docs/26-坑总结与工作流.md` | 表格/环境坑 + 按任务读文件清单（token 优化） |',
                  '| `docs/26-坑总结与工作流.md` | 表格/环境坑 + 按任务读文件清单（token 优化） |\n| `docs/27-研究母稿-主线2-AI研究能力放大.md` | **主线 2 定义文档（核心备忘录）**：17 节完整母稿 |')
    return s

# ---------- STATUS ----------
def st(s):
    old = '| **专著/文档**（21 章 + docs/01-23） | L1/L2（自洽记录） | 全部实验/数据/修正轨迹存档 | 非正式出版物 |'
    new = ('| **专著/文档**（21 章 + docs/01-23） | L1/L2（自洽记录） | 全部实验/数据/修正轨迹存档 | 非正式出版物 |\n'
           '| **主线 2：AI Research Capability Amplification**（docs/27 研究母稿） | **L1/L2**（声明 + 自洽记录） | protocol 已形成（audit/provenance/boundary/falsification）；within-conversation 行为适应已观察到；真实 failure cases 支撑规则必要性 | **跨任务 transfer / 可量化 capability gain 未证明——这是声明不是结论** |')
    assert old in s, 'STATUS 研究线表'
    s = s.replace(old, new)
    old2 = '- **专著**：《给"分级"分级》21 章（book/，含新增第 19 章"论文 2 定位与证据链"）'
    new2 = old2 + '\n- **主线 2 母稿**：docs/27（研究方法→AI 能力，核心备忘录）'
    assert old2 in s, 'STATUS 资产'
    s = s.replace(old2, new2)
    return s

rw('HANDOFF.md', hd)
rw('STATUS.md', st)
print('ALL OK')
