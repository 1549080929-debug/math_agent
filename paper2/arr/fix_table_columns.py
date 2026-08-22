"""修复表格列格式：fix_latex 的 colspec 截断 bug，重新正确生成 tabular。

直接对 acl_submit.tex 处理：找到残缺的 tabular 列格式（@{），用正确列数重建。
"""
import re

BS = chr(92)
s = open('acl_submit.tex', encoding='utf-8').read()

# 从 paper_arr.tex 提取每个 longtable 的正确列数（p{ 出现次数）
arr = open('paper_arr.tex', encoding='utf-8').read()
col_counts = []
for m in re.finditer(re.escape(BS) + r'begin\{longtable\}\[\]', arr):
    # 找到这个 longtable 的列格式块（到 @{} } 结束）
    seg_start = m.end()
    # 数 p{ 次数（每列一个）
    seg = arr[seg_start:seg_start + 2000]
    # 找 \end{longtable} 前的列定义
    end = arr.find(BS + 'end{longtable}', seg_start)
    colspec_seg = arr[seg_start:end]
    n = colspec_seg.count('p{') + colspec_seg.count('>{\\raggedright')  # 数 p{ 或 >{ 前缀
    # 更准：数 >{\raggedright 前缀（pandoc 每列一个）
    n2 = colspec_seg.count(BS + '>{\\raggedright')
    col_counts.append(n2 if n2 > 0 else max(1, colspec_seg.count('p{')))

print('各 longtable 列数:', col_counts)

# 对 acl_submit.tex 里残缺的 tabular（列格式 @{）重建
# 顺序替换：每个 \begin{tabular}{@{ ... 残缺 → 正确列数
idx = 0
def fix_colspec(m):
    global idx
    n = col_counts[idx] if idx < len(col_counts) else 4
    idx += 1
    # 简单左对齐 l 列（等宽 p 更稳但 l 最可靠）
    return BS + 'begin{tabular}{' + 'l' * n + '}'

# 匹配 \begin{tabular}{@{...} （残缺列格式，以 @{ 开头）
pat = re.compile(re.escape(BS) + r'begin\{tabular\}\{@{[^}]*\}')
s2, n_rep = pat.subn(fix_colspec, s)
print(f'修复 tabular 列格式: {n_rep} 个')

open('acl_submit.tex', 'w', encoding='utf-8').write(s2)
print('完成')
