"""确认页 8 正文结束、页 9 是 References。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
t8 = r.pages[7].extract_text() or ''
t9 = r.pages[8].extract_text() or ''
out = []
out.append('页8 末尾 200 字符:')
out.append(t8[-200:].replace('\n', ' '))
out.append('')
out.append('页9 开头 200 字符:')
out.append(t9[:200].replace('\n', ' '))
open('p8_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done')
