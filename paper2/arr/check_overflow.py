"""检查页 8 末尾/页 9 开头（溢出量）。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
t8 = r.pages[7].extract_text() or ''
t9 = r.pages[8].extract_text() or ''
out = []
out.append('=== 页8 末尾 300 ===')
out.append(t8[-300:].replace('\n', ' '))
out.append('')
out.append('=== 页9 开头 300 ===')
out.append(t9[:300].replace('\n', ' '))
open('overflow_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
