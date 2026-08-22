"""确认格式问题：章节编号、行号、AI 断词。"""
import re

BS = chr(92)
s = open('acl_submit.tex', encoding='utf-8').read()

# 1. 章节编号（section/subsection 标题里的手动编号）
print('=== section 标题 ===')
for m in re.finditer(re.escape(BS) + r'section\{([^}]*)\}', s):
    print(' ', m.group(1)[:60])
print('=== subsection 标题（前 8） ===')
for m in list(re.finditer(re.escape(BS) + r'subsection\{([^}]*)\}', s))[:8]:
    print(' ', m.group(1)[:60])

# 2. 行号相关（lineno / review 模式）
print()
print('lineno 使用:', 'lineno' in s)
print('review 模式:', 'review' in s[:500])
print('geometry:', 'geometry' in s)

# 3. AI 数学模式（\( ... \)）
print()
print('\\( 出现:', s.count(BS + '('))
print('theory of AI 上下文:', repr(s[max(0, s.find('theory of AI') - 40):s.find('theory of AI') + 50]))
