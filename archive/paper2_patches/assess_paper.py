"""评估 paper.md 结构，为 ARR 格式转换做准备。"""
import re

s = open('paper.md', encoding='utf-8').read()
sections = re.findall(r'^#{1,3} .*', s, re.M)
print('=== 章节结构 ===')
for sec in sections:
    print(' ', sec)
print()
words = len(re.sub(r'[#*|`>\-\n]', ' ', s).split())
print(f'总字数(含表格/代码块): ~{words}')
print(f'行数: {s.count(chr(10))}')
print(f'表格分隔行数: {s.count("|---")}')
# 每节字数
print()
print('=== 各主要节字数 ===')
for m in re.finditer(r'^## (.+)$', s, re.M):
    start = m.end()
    nxt = re.search(r'^## ', s[m.end():], re.M)
    end = m.end() + (nxt.start() if nxt else len(s) - m.end())
    body = s[start:end]
    w = len(re.sub(r'[#*|`>\-\n]', ' ', body).split())
    print(f'  {m.group(1)[:40]}: ~{w} words')
