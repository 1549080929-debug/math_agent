"""检查 PDF 附录是否渲染（A.1/A.2 表）。"""
from pypdf import PdfReader

r = PdfReader('acl_submit.pdf')
out = []
for i, p in enumerate(r.pages):
    t = p.extract_text() or ''
    out.append(f'=== 页{i+1} ===')
    # 找表格特征或附录标记
    if 'A.1' in t or 'A.2' in t or 'Level map' in t or 'Appendix' in t:
        idx = max(t.find('A.1'), t.find('A.2'), t.find('Appendix'), t.find('Level map'))
        out.append('  含附录标记: ' + t[max(0, idx-30):idx+120].replace('\n', ' '))
    # 页 12 完整内容（附录可能在这）
    if i == len(r.pages) - 1:
        out.append('  最后一页开头: ' + t[:300].replace('\n', ' '))
        out.append('  最后一页结尾: ' + t[-300:].replace('\n', ' '))

open('appendix_pdf_check.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('written')
