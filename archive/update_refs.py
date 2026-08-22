"""Update doc references after archiving (CRLF-safe, UTF-8)."""
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

# ---------- paper2/arr/README.md ----------
def r1(s):
    s = s.replace('| `acl_submit.tex` | 生成的 LaTeX |',
                  '| `acl_submit.tex` | 生成的 LaTeX（管线跑完自动归档 `archive/arr_intermediates/`） |')
    s = s.replace('| `versions/` | 版本存档（v12 压缩前 + scripts_compression 压缩轨迹） |',
                  '| `archive/arr_versions/` | 版本存档（v12 压缩前 + scripts_compression + anon_prep_20260822，已移出主目录） |')
    s = s.replace('3. 版本存档：压缩前版本在 `versions/v12_body10p_20260822/`',
                  '3. 版本存档：压缩前版本在 `archive/arr_versions/v12_body10p_20260822/`')
    s = s.replace('4. 修复轨迹脚本在 `versions/scripts_compression/`（可重放每步压缩）',
                  '4. 修复轨迹脚本在 `archive/arr_versions/scripts_compression/`（可重放每步压缩）')
    return s

# ---------- paper2/arr/submission_form.md ----------
def r2(s):
    s = s.replace('`paper2/arr/versions/anon_prep_20260822/fixed_pages/`',
                  '`archive/arr_versions/anon_prep_20260822/fixed_pages/`')
    s = s.replace('`final_pages.txt` 核实', '`archive/arr_intermediates/final_pages.txt` 核实')
    return s

# ---------- HANDOFF.md ----------
def r3(s):
    s = s.replace('> 最后更新：2026-08-22（v5）。v4 交接于同日（C1a/arXiv 退回/ARR 管线）；本版新增：**ARR 周期修正（10-12 提交，非 12 月）、匿名化投稿 PDF 就绪、表单材料包（submission_form.md）、ARR 官方要求核实（页数/匿名/checklist/Limitations 硬性）**。',
                  '> 最后更新：2026-08-22（v6）。v5 交接于同日（ARR 周期修正/匿名化/表单材料包）；本版新增：**表格溢出修复（tabularx）、Level map 列宽修复（p{1.2cm}）、项目瘦身（archive/ 归档）、坑总结 docs/26、按任务读文件工作流（token 优化）**。')
    s = s.replace('| `paper2/arr/` | ARR 管线（README.md 入口）；**`submission_form.md` = 提交表单材料包（权威）**；`versions/anon_prep_20260822/` = 匿名化前命名版备份 |',
                  '| `paper2/arr/` | ARR 管线（README.md 入口）；**`submission_form.md` = 提交表单材料包（权威）**；匿名化前命名版备份在 `archive/arr_versions/anon_prep_20260822/` |')
    s = s.replace('| `docs/25-C1a特权节点实验.md` | C1a 完整记录 |',
                  '| `docs/25-C1a特权节点实验.md` | C1a 完整记录 |\n| `docs/26-坑总结与工作流.md` | 表格/环境坑 + 按任务读文件清单（token 优化） |\n| `archive/` | 历史/中间/一次性产物（勿主动读，需要时取；arr_intermediates / paper2_patches / agentsec_results / agentsec_jade_assets / book_builds / arr_versions / logs） |')
    return s

# ---------- agentsec/REPORT.md ----------
def r4(s):
    s = s.replace('原始数据：`agentsec/results/*.json`（7 配置 × 250 用例 + adaptive_*.json），含每个用例的 LLM 提议与拦截原因',
                  '原始数据：`archive/agentsec_results/results/*.json`（7 配置 × 250 用例 + adaptive_*.json，已归档），含每个用例的 LLM 提议与拦截原因')
    return s

rw('paper2/arr/README.md', r1)
rw('paper2/arr/submission_form.md', r2)
rw('HANDOFF.md', r3)
rw('agentsec/REPORT.md', r4)
print('ALL OK')
