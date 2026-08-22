"""ARR 完整管线（一条命令）：paper_arr.md -> acl_submit.pdf。

步骤：
1. map citations（[n] -> [@key]）
2. pandoc（citeproc + wrap=none）-> paper_arr.tex
3. build_arr.py（ACL 模板 + 动态 CSL + 正文）-> acl_submit.tex
4. fix_latex.py（Unicode 转义 + longtable -> table* 正确列数）
5. fix_format.py（章节编号去重 + Appendix section*）
6. fix_natbib3.py（参考文献 -> enumerate）
7. xelatex -> acl_submit.pdf

用法：python paper2/arr/rebuild_full.py
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

def run(script):
    r = subprocess.run([sys.executable, script], capture_output=True, encoding='utf-8', errors='replace')
    ok = 'ok' if r.returncode == 0 else 'FAIL'
    print(f'  {script}: {ok}')
    return r.returncode == 0

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
print('1. map citations done')

# 2. pandoc
import pypandoc
out = pypandoc.convert_file('paper_arr_cite.md', 'latex', format='markdown',
                            extra_args=['--citeproc', '--bibliography=refs.bib',
                                        '--csl=chicago-author-date.csl', '--standalone', '--wrap=none'])
open('paper_arr.tex', 'w', encoding='utf-8').write(out)
print('2. pandoc done')

# 3-6. 修复脚本
for script in ['build_arr.py', 'fix_latex.py', 'fix_format.py', 'fix_natbib3.py']:
    run(script)

# 7. xelatex
env = dict(os.environ)
env['TEXMFCNF'] = r'C:\TinyTeX\texmf-dist\web2c'
for f in ['acl_submit.aux', 'acl_submit.log', 'acl_submit.out']:
    if os.path.exists(f):
        os.remove(f)
r = subprocess.run([r'C:\TinyTeX\bin\windows\xelatex.exe', '-interaction=nonstopmode', 'acl_submit.tex'],
                   capture_output=True, encoding='utf-8', errors='replace', env=env)
ok = 'Output written' in r.stdout
print(f'7. xelatex: {"ok" if ok else "FAIL"}')
if ok:
    from pypdf import PdfReader
    pdf = PdfReader('acl_submit.pdf')
    print(f'   PDF {len(pdf.pages)} 页')

# 8. 清理中间产物到 archive/（主目录只留源 + PDF，token 友好）
import shutil
ARCHIVE = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'archive', 'arr_intermediates')
os.makedirs(ARCHIVE, exist_ok=True)
for f in ['paper_arr_cite.md', 'paper_arr.tex', 'acl_submit.tex', 'acl_submit.log', 'acl_submit.aux', 'acl_submit.out']:
    p = os.path.join(HERE, f)
    if os.path.exists(p):
        shutil.move(p, os.path.join(ARCHIVE, f))
print('8. intermediates archived')
