"""确认正文页数（References/附录节位置）。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
out = []
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    marks = []
    if 'References' in t:
        marks.append('Ref')
    if 'Appendix' in t and 'A.1 Defense' in t or 'A.1 Defense' in t:
        marks.append('APP(A.1)')
    if 'A.2 Victim' in t:
        marks.append('APP(A.2)')
    if 'Conclusion' in t:
        marks.append('Concl')
    if marks:
        out.append(f'页{i+1}: {marks}')
    head = t[:50].replace('\n', ' ')
    out.append(f'  页{i+1}开头: {head}')
open('body_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
