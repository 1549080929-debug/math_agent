"""把 Appendix 移到 References 之后（ARR 惯例：正文 -> References -> Appendix）。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

ref_marker = '## References'
appendix_marker = '## Appendix'
if appendix_marker in s and ref_marker in s:
    ai = s.find(appendix_marker)
    ri = s.find(ref_marker)
    if ai < ri:
        # 提取 Appendix 块（到 References 前）
        appendix_block = s[ai:ri]
        s = s[:ai] + s[ri:]  # 删 Appendix 块（References 前）
        s = s.rstrip() + '\n\n' + appendix_block.rstrip() + '\n'
        print('[ok] Appendix 移到 References 后')
    else:
        print('[ok] Appendix 已在 References 后')
else:
    print('[warn] 锚点未找到')

open(p, 'w', encoding='utf-8').write(s)
