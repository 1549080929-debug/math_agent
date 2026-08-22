"""三个边界收紧：VAL-selected->VAL-guided、semantic caps at L2 软化、10/10 弱化。"""
p = 'paper2/paper.md'
s = open(p, encoding='utf-8').read()

# 1. VAL-selected -> VAL-guided（3 处）
n1 = s.count('VAL-selected')
s = s.replace('VAL-selected', 'VAL-guided')
print(f'  1. VAL-selected -> VAL-guided: {n1} 处')

# 2a. 摘要 caps at L2 软化
old_abs = 'not semantic safety, which caps at L2.'
new_abs = 'not unrestricted semantic safety, which caps at L2 (restricted semantic properties that can be formally encoded remain eligible for higher levels).'
assert old_abs in s, 'abstract caps anchor not found'
s = s.replace(old_abs, new_abs)
print('  2a. 摘要 caps at L2 软化')

# 2b. §5 open-world 绝对表述软化
old5 = '''*Semantic* safety ("is this action dangerous?") is an open-world property with no decidable fragment, and caps at L2.'''
new5 = '''*Semantic* safety ("is this action dangerous?") is an open-world property for which no decidable fragment is available in the unrestricted setting, and hence caps at L2; restricted semantic properties that can be formally encoded (e.g., a bounded action taxonomy) remain eligible for higher levels.'''
if old5 in s:
    s = s.replace(old5, new5)
    print('  2b. §5 open-world 软化')
else:
    # 尝试变体
    import re
    m = re.search(r'\*Semantic\* safety[^.]*\.', s)
    if m:
        print(f'  [变体] 找到: {m.group(0)[:80]}...')
        # 不自动替换，报告
    else:
        print('  [未找到] §5 open-world 表述')

# 3a. 摘要 10/10 弱化
old_10a = 'We validate this on published data (10/10 prediction hits) and then run'
new_10a = 'We validate this with frozen prediction cards on a small published sample (10/10 hits, flagged as such) and then run'
assert old_10a in s, 'abstract 10/10 anchor not found'
s = s.replace(old_10a, new_10a)
print('  3a. 摘要 10/10 弱化')

# 3b. 贡献 2 弱化
old_10b = '**Prediction validation.** We freeze level-to-behavior prediction cards and validate them: 10/10 hits on published data (PPMF\'s own numbers, abstract-level evidence), including two mechanism-driven classification corrections.'
new_10b = '**Prediction validation.** We freeze level-to-behavior prediction cards before outcome data and validate them on a small published sample: 10/10 hits (PPMF\'s own numbers, abstract-level evidence, flagged as such), including two mechanism-driven classification corrections—the point is falsifiability, not the hit count.'
assert old_10b in s, 'contribution 2 anchor not found'
s = s.replace(old_10b, new_10b)
print('  3b. 贡献 2 10/10 弱化')

open(p, 'w', encoding='utf-8').write(s)
print('boundary patch done')
