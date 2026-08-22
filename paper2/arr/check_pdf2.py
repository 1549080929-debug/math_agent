"""用 pypdf 检查 acl_submit.pdf 文本完整性。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
print('PDF 页数:', len(r.pages))
full = ''
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    full += t
    print(f'  页{i+1}: {len(t)} 字符')

print()
for kw in ['The Same Zero', 'Abstract', 'Introduction', 'Zero stability', 'funnel',
           'LITMUS', 'References', 'A-MemGuard', 'CaMeL', 'Z(α)', 'Z(']:
    print(f'  含 "{kw}":', kw in full)
