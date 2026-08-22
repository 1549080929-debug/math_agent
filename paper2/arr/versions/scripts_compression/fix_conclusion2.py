"""删 §8 与 ## 9. Conclusion 之间的残留 Conclusion 中段。"""
p = 'paper_arr.md'
s = open(p, encoding='utf-8').read()

# §8 Limitations 末尾（"not the hit count."）到 "## 9. Conclusion" 之间是残留
anchor = 'not the hit count.'
concl_marker = '## 9. Conclusion'
a = s.find(anchor)
c = s.find(concl_marker)
print('anchor@', a, 'concl@', c, '| 残留长度:', c - (a + len(anchor)))
if a > 0 and c > a:
    residual = s[a + len(anchor):c]
    print('残留内容:', repr(residual[:100]))
    # 删残留（保留 anchor 后直接接 Conclusion 标题）
    s = s[:a + len(anchor)] + '\n\n' + s[c:]
    print('[ok] 残留已删')

open(p, 'w', encoding='utf-8').write(s)
print('字数:', len(s.split()))
