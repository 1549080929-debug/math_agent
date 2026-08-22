"""Anonymize build_arr.py author block + paper_arr.md title block (CRLF-safe)."""
import io

# 1) build_arr.py: hardcoded author -> Anonymous
p = r'paper2/arr/build_arr.py'
s = io.open(p, encoding='utf-8').read()
marker = '\\author{Yajie Yin'
i = s.find(marker)
assert i >= 0, 'author marker not found in build_arr.py'
j = s.find('}}', i) + 2
old = s[i:j]
print('REPLACING:', repr(old))
s = s[:i] + '\\author{Anonymous}' + s[j:]
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('build_arr.py OK')

# 2) paper_arr.md: remove title-page identity block
p2 = r'paper2/arr/paper_arr.md'
m = io.open(p2, encoding='utf-8').read()
start = m.find('**Yajie Yin**')
assert start >= 0, 'author line not found in paper_arr.md'
end = m.find('## Abstract', start)
assert end >= 0, 'Abstract heading not found'
block = m[start:end]
print('REMOVING:', repr(block[:120]))
m = m[:start] + m[end:]
io.open(p2, 'w', encoding='utf-8', newline='').write(m)
print('paper_arr.md OK')
