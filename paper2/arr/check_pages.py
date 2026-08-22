"""找 References 起始页 + 每页字符数。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
ref_page = None
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    if 'References' in t and i > 3:
        ref_page = i + 1
        print(f'References 出现在页 {ref_page}')
        print('  该页开头:', t[:150].replace(chr(10), ' '))
        break
print()
for i, p in enumerate(r.pages):
    print(f'页{i+1}: {len(p.extract_text() or "")} 字符')
if ref_page:
    print(f'\n正文约 {ref_page-1} 页 + 参考文献')
