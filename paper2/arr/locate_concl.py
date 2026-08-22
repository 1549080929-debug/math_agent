"""定位 Conclusion 和 References 的页。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
out = []
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    for kw in ['9 Conclusion', '9. Conclusion', 'Conclusion', 'References']:
        idx = t.find(kw)
        if idx >= 0:
            ctx = t[max(0, idx - 15):idx + 40].replace('\n', ' ')
            out.append(f'页{i+1} [{kw}]: ...{ctx}')
open('concl_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
