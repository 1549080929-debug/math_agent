"""删手写 References 节（citeproc 自动生成），保留 Appendix。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

ref_marker = '## References'
appendix_marker = '## Appendix'
if ref_marker in s:
    ri = s.find(ref_marker)
    ai = s.find(appendix_marker)
    # 删 References 到 Appendix 前（如果 Appendix 在 References 后）
    if ai > ri:
        s = s[:ri] + s[ai:]
    else:
        s = s[:ri].rstrip() + '\n'
    print('[ok] 删手写 References')
else:
    print('[warn] References 未找到')

open(p, 'w', encoding='utf-8').write(s)
