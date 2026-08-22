"""审计论文中的重复修辞。"""
import re

s = open('paper.md', encoding='utf-8').read()

phrases = {
    'same zero': len(re.findall(r'same zero', s, re.I)),
    'anchor (全词)': len(re.findall(r'anchor', s, re.I)),
    'anchor decides': len(re.findall(r'anchor decides', s, re.I)),
    'structural|behavioral': len(re.findall(r'structural|behavioral', s, re.I)),
    'different guarantees': len(re.findall(r'different guarantees', s, re.I)),
    'zero is an outcome': len(re.findall(r'zero is an outcome', s, re.I)),
    'not a claim/does not claim': len(re.findall(r'not a claim|do not claim|does not claim|not our claim', s, re.I)),
    'determin*': len(re.findall(r'determin\w+', s, re.I)),
    'predict*': len(re.findall(r'predict\w+', s, re.I)),
    'guarantee': len(re.findall(r'guarantee', s, re.I)),
}
print('=== 修辞频率 ===')
for k, v in phrases.items():
    print(f'  {k}: {v}')

print()
print('=== "same zero" 出现位置 ===')
for m in re.finditer(r'same zero', s, re.I):
    start = max(0, m.start() - 70)
    print(f'  ...{s[start:m.end() + 40].strip()[:130]}')
    print()

print('=== "determin*" 出现位置（检查强表述） ===')
for m in re.finditer(r'determin\w+', s, re.I):
    start = max(0, m.start() - 50)
    print(f'  ...{s[start:m.end() + 30].strip()[:110]}')
