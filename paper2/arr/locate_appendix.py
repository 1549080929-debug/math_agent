"""精确定位 Appendix 节在 PDF 的位置。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
out = []
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    for kw in ['Appendix', 'A.1 Defense', 'A.2 Victim', 'A.1', 'A.2']:
        idx = t.find(kw)
        if idx >= 0:
            ctx = t[max(0, idx - 40):idx + 70].replace('\n', ' ')
            out.append(f'页{i+1} [{kw}]: ...{ctx}')

open('app_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written app_check.txt')
