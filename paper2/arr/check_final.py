"""检查最终 PDF：附录表位置 + 正文页数。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
out = []
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    marks = []
    if 'References' in t:
        marks.append('Ref')
    if 'A.1 Defense' in t or 'A.2 Victim' in t:
        marks.append('APP_TABLE')
    if 'Conclusion' in t:
        marks.append('Concl')
    if marks:
        out.append(f'页{i+1}: {marks}')
    if i >= 9:
        head = t[:80].replace('\n', ' ')
        out.append(f'  页{i+1}开头: {head}')
open('pdf_final_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
