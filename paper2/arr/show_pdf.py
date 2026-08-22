"""展示 acl_submit.pdf 内容结构：节标题 + 每节开头。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
full = []
for p in r.pages:
    full.append(p.extract_text() or '')

# 提取每页文本拼接
text = '\n'.join(full)

# 找关键节标题位置
import re
sections = ['Abstract', 'Introduction', 'Background', 'Method', 'Defense Level Map',
            'Prediction', 'Deployment-Value', 'Analysis', 'Limitations', 'Conclusion', 'References']
out = []
out.append('=== PDF 节结构（出现顺序） ===')
pos = []
for sec in sections:
    i = text.find(sec)
    pos.append((i, sec))
pos.sort()
for i, sec in pos:
    if i >= 0:
        snippet = text[i:i+120].replace('\n', ' ')
        out.append(f'  [{i:>6}] {sec}: ...{snippet}')

out.append('')
out.append('=== 各页头尾 60 字符 ===')
for idx, p in enumerate(full):
    tail = p[-60:].replace('\n', ' ')
    head = p[:60].replace('\n', ' ')
    out.append(f'页{idx+1}: 头[{head}] 尾[{tail}]')

open('pdf_structure.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written pdf_structure.txt')
