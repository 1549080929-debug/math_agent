"""精确定位各关键节在 PDF 的页。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
out = []
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    for kw in ['9. Conclusion', '8. Limitations', '7. Analysis', 'Appendix', 'A.1 Defense', 'A.2 Victim']:
        idx = t.find(kw)
        if idx >= 0:
            ctx = t[max(0, idx - 20):idx + 40].replace('\n', ' ')
            out.append(f'页{i+1} [{kw}]: ...{ctx}')
# References（thebibliography 的标题）
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    if t.strip().startswith('References') or '\nReferences\n' in t:
        out.append(f'页{i+1} [References 标题]: 该页开头 {t[:60].replace(chr(10), " ")}')
open('locate_all.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
