"""更新论文 §6.1/§6.2 为 v3 口径数据（真效果执行器重跑后）。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

# §6.1 表
repl = [
    # D1 行
    ('| D1 prompt hardening (L0) | 0.000 | 0.254 | 0.000 [0.00, 0.16] | 0.333, benign destroyed |',
     '| D1 prompt hardening (L0) | 0.000 | 0.219 | 0.000 [0.00, 0.16] | 0.333, benign destroyed |'),
    # D2 行
    ('| D2 keyword filter (L1) | 0.258 | 0.512 | 1.000 [0.84, 1.00] | 0.075 |',
     '| D2 keyword filter (L1) | 0.200 | 0.492 | 1.000 [0.84, 1.00] | 0.133 |'),
    # D3 行
    ('| D3 confirmation gate (L1/L2) | 0.000 | 0.512 | 1.000 [0.84, 1.00] | 0.333 |',
     '| D3 confirmation gate (L1/L2) | 0.000 | 0.497 | 1.000 [0.84, 1.00] | 0.333 |'),
    # D4 行
    ('| D4 parameter sandbox (L3) | 0.079 | 0.537 | 1.000 [0.84, 1.00] | 0.254 |',
     '| D4 parameter sandbox (L3) | 0.067 | 0.494 | 1.000 [0.84, 1.00] | 0.266 |'),
    # V 行
    ('| **V = D3+D4 (VAL)** | **0.000** | 0.512 | **1.000 [0.84, 1.00]** | **0.333, lossless** |',
     '| **V = D3+D4 (VAL)** | **0.000** | 0.497 | **1.000 [0.84, 1.00]** | **0.333, lossless** |'),
]

# §6.2 表（D2/D4 静态列）
repl += [
    ('| D2 | 0.258 | **0.467** | — | — | — |', '| D2 | 0.200 | **0.467** | — | — | — |'),
    ('| D4 | 0.079 | **0.200** | — | — | — |', '| D4 | 0.067 | **0.200** | — | — | — |'),
]

# 正文引用
repl += [
    ('D2 alone leaks 0.258 ASR: the keyword filter is bypassable by rewriting.',
     'D2 alone leaks 0.200 ASR: the keyword filter is bypassable by rewriting.'),
    ('D4 alone leaks 0.079 (schema-legal semantic attacks, e.g. a malicious comment posted to an allowed target).',
     'D4 alone leaks 0.067 (schema-legal semantic attacks, e.g. a malicious comment posted to an allowed target).'),
]

for old, new in repl:
    if old in s:
        s = s.replace(old, new)
        print(f'  [OK] {old[:60]}...')
    else:
        print(f'  [MISS] {old[:60]}...')

open(p, 'w', encoding='utf-8').write(s)
print('done')
