"""ARR 完整管线：paper_arr.md -> LaTeX -> PDF。

步骤：map citations -> pandoc -> build_arr -> fix_latex -> xelatex
"""
import os
import subprocess
import sys

BS = chr(92)

HERE = os.path.dirname(os.path.abspath(__file__))

# 1. map citations（读 paper_arr.md）
import importlib.util
spec = importlib.util.spec_from_file_location('map_citations', os.path.join(HERE, 'map_citations.py'))
# map_citations 读死 paper.md——直接在这里做映射
import re
NUM2KEY = {
    1: 'yin2026grading', 2: 'xu2026memory', 3: 'han2025verifiagent',
    4: 'debenedetti2024agentdojo', 5: 'injection2026dissociation',
    6: 'slr2026source', 7: 'lu2025when', 8: 'zhou2023ralm',
    9: 'inan2023llamaguard', 10: 'chen2023codet', 11: 'shi2025progent',
    12: 'costa2025ifc', 13: 'zhang2026litmus', 14: 'amemguard2025', 15: 'camel2025',
}
src = open(os.path.join(HERE, 'paper_arr.md'), encoding='utf-8').read()

def repl(m):
    nums = [int(x.strip()) for x in m.group(1).split(',')]
    keys = [NUM2KEY[n] for n in nums if n in NUM2KEY]
    if not keys:
        return m.group(0)
    return '[' + ';'.join('@' + k for k in keys) + ']'

s2 = re.sub(r'\[(\d+(?:\s*,\s*\d+)*)\]', repl, src)
unmapped = re.findall(r'\[(\d+(?:\s*,\s*\d+)*)\]', s2)
if unmapped:
    print('警告：未映射引用:', unmapped[:5])
open(os.path.join(HERE, 'paper_arr_cite.md'), 'w', encoding='utf-8').write(s2)
print('1. 引用映射完成')

# 2. pandoc -> paper_arr.tex
import pypandoc
out = pypandoc.convert_file('paper_arr_cite.md', 'latex', format='markdown',
                            extra_args=['--citeproc', '--bibliography=refs.bib',
                                        '--csl=chicago-author-date.csl', '--standalone', '--wrap=none'])
open(os.path.join(HERE, 'paper_arr.tex'), 'w', encoding='utf-8').write(out)
print('2. pandoc 转换完成')

# 3. build_arr
r = subprocess.run([sys.executable, 'build_arr.py'], cwd=HERE, capture_output=True, text=True, encoding='utf-8')
print(r.stdout.strip())
if r.returncode != 0:
    print('build_arr 失败:', r.stderr[-500:])

# 4. fix_latex
r = subprocess.run([sys.executable, 'fix_latex.py'], cwd=HERE, capture_output=True, text=True, encoding='utf-8')
print(r.stdout.strip())

# 5. xelatex
env = dict(os.environ)
env['TEXMFCNF'] = r'C:\TinyTeX\texmf-dist\web2c'
for f in ['acl_submit.aux', 'acl_submit.log', 'acl_submit.out']:
    p = os.path.join(HERE, f)
    if os.path.exists(p):
        os.remove(p)
r = subprocess.run([r'C:\TinyTeX\bin\windows\xelatex.exe', '-interaction=nonstopmode', 'acl_submit.tex'],
                   cwd=HERE, env=env, capture_output=True, text=True, encoding='utf-8')
out_text = r.stdout
for line in out_text.split('\n'):
    if 'Error' in line or 'Output written' in line or 'Fatal' in line:
        print(line)
print('5. xelatex 完成')
