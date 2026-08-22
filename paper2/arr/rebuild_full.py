"""用当前 paper_arr.md 完整重建：map citations -> pandoc -> build -> fix -> xelatex。"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

# 1. map citations
NUM2KEY = {1: 'yin2026grading', 2: 'xu2026memory', 3: 'han2025verifiagent',
           4: 'debenedetti2024agentdojo', 5: 'injection2026dissociation',
           6: 'slr2026source', 7: 'lu2025when', 8: 'zhou2023ralm',
           9: 'inan2023llamaguard', 10: 'chen2023codet', 11: 'shi2025progent',
           12: 'costa2025ifc', 13: 'zhang2026litmus', 14: 'amemguard2025', 15: 'camel2025'}
src = open('paper_arr.md', encoding='utf-8').read()
def repl(m):
    nums = [int(x.strip()) for x in m.group(1).split(',')]
    keys = [NUM2KEY[n] for n in nums if n in NUM2KEY]
    return '[' + ';'.join('@' + k for k in keys) + ']' if keys else m.group(0)
s2 = re.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]', repl, src)
open('paper_arr_cite.md', 'w', encoding='utf-8').write(s2)
print('1. map citations done, Appendix in cite:', s2.count('## Appendix'))

# 2. pandoc
import pypandoc
out = pypandoc.convert_file('paper_arr_cite.md', 'latex', format='markdown',
                            extra_args=['--citeproc', '--bibliography=refs.bib',
                                        '--csl=chicago-author-date.csl', '--standalone', '--wrap=none'])
open('paper_arr.tex', 'w', encoding='utf-8').write(out)
print('2. pandoc done, A.1 in tex:', out.count('A.1'))

# 3-5. build/fix/xelatex（重定向输出）
for script in ['build_arr.py', 'fix_latex.py']:
    r = subprocess.run([sys.executable, script], capture_output=True, encoding='utf-8', errors='replace')
    print(f'3. {script}: {"ok" if r.returncode == 0 else "FAIL"}')
env = dict(os.environ)
env['TEXMFCNF'] = r'C:\TinyTeX\texmf-dist\web2c'
for f in ['acl_submit.aux', 'acl_submit.log', 'acl_submit.out']:
    if os.path.exists(f):
        os.remove(f)
r = subprocess.run([r'C:\TinyTeX\bin\windows\xelatex.exe', '-interaction=nonstopmode', 'acl_submit.tex'],
                   capture_output=True, encoding='utf-8', errors='replace', env=env)
ok = 'Output written' in r.stdout
print(f'4. xelatex: {"ok" if ok else "FAIL"}')
if ok:
    from pypdf import PdfReader
    pdf = PdfReader('acl_submit.pdf')
    print('PDF 页数:', len(pdf.pages))
    # Appendix 检查
    for i, p in enumerate(pdf.pages):
        t = p.extract_text() or ''
        if 'A.1' in t or 'A.2' in t:
            print(f'  附录表在页 {i+1}')
