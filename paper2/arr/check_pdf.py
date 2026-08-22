"""检查 acl_submit.pdf：节分布 + PDF 文本完整性。"""
import re
import os

BS = chr(92)

# 1. 每节字数（.tex）
s = open('acl_submit.tex', encoding='utf-8').read()
print('=== 各 section 字数 ===')
pos = [(m.start(), m.group(1)) for m in re.finditer(BS + r'section\{([^}]*)\}', s)]
for idx, (start, name) in enumerate(pos):
    end = pos[idx + 1][0] if idx + 1 < len(pos) else len(s)
    body = s[start:end]
    words = len(re.sub(r'[{}\\]', ' ', body).split())
    print(f'  {name[:50]}: ~{words} words')

# 2. PDF 页数与文本（pdftotext 或 PyPDF2）
print()
print('=== PDF 检查 ===')
print('PDF 大小:', os.path.getsize('acl_submit.pdf') // 1024, 'KB')
# 尝试 pdftotext（TinyTeX 可能带）
import shutil
pdftotext = shutil.which('pdftotext') or r'C:\TinyTeX\bin\windows\pdftotext.exe'
if os.path.exists(pdftotext):
    import subprocess
    r = subprocess.run([pdftotext, 'acl_submit.pdf', '-'], capture_output=True, text=True, encoding='utf-8')
    text = r.stdout
    print('PDF 文本长度:', len(text))
    print('页数(分页符):', text.count(chr(12)))
    # 检查关键内容是否在
    for kw in ['The Same Zero', 'Abstract', 'Introduction', 'Zero stability', 'Execution funnel', 'LITMUS', 'References']:
        print(f'  含 "{kw}":', kw in text)
else:
    print('pdftotext 不可用，跳过文本检查')
