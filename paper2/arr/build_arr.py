"""组装 acl_submit.tex：ACL 模板 preamble + 论文正文。

修正：
1. 去掉 pandoc 的标题 section + 作者文本块
2. Abstract 包 abstract 环境
3. 层级提升：\subsection{数字.X} -> \section{数字.X}（markdown ## 是章节）；
   \subsubsection{X} -> \subsection{X}（markdown ### 是小节）
"""
import re

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[review]{acl}  % review=匿名投稿; final=署名版; preprint=带页码
\usepackage{times}
\usepackage{latexsym}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{microtype}
\usepackage{inconsolata}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{multirow}
% pandoc 正文需要的包
\usepackage{amsmath,amssymb}
\usepackage{longtable}
\usepackage{upquote}
\usepackage{xcolor}
\usepackage{array}
\usepackage{calc}
\usepackage{etoolbox}
\usepackage{parskip}
\usepackage{bookmark}
\IfFileExists{xurl.sty}{\usepackage{xurl}}{}
\urlstyle{same}
\hypersetup{hidelinks}

% [动态插入 citeproc/CSL 定义——见 build 时从 paper_arr.tex 提取]
__CSL_BLOCK__

\title{The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security}
\author{Yajie Yin \\
  Independent Researcher \\
  \texttt{1549080929@qq.com}}

\begin{document}
\maketitle
\nolinenumbers  % xelatex lineno bug, disable
"""

arr = open('paper_arr.tex', encoding='utf-8').read()

# 动态提取 citeproc/CSL 定义块（从 pandoc 输出原样取，保证括号正确）
csl_start = arr.find('% definitions for citeproc citations')
csl_end = arr.find('\\urlstyle{same}')
if csl_start >= 0 and csl_end >= 0:
    csl_block = arr[csl_start:csl_end + len('\\urlstyle{same}')]
    # 去掉其中的 \usepackage{calc} 等（PREAMBLE 已含）
    csl_block = csl_block.replace('\\usepackage{calc}\n', '')
    csl_block = csl_block.replace('\\usepackage{bookmark}\n', '')
    csl_block = csl_block.replace('\\IfFileExists{xurl.sty}{\\usepackage{xurl}}{}\n', '')
    # 去掉 CSLReferences 环境定义（使用处已转 thebibliography；定义本身触发括号错位）
    csl_start_env = csl_block.find('\\newenvironment{CSLReferences}')
    csl_end_env = csl_block.find('\\newcommand{\\CSLBlock')
    if csl_start_env >= 0 and csl_end_env >= 0:
        csl_block = csl_block[:csl_start_env] + csl_block[csl_end_env:]
        print('[ok] 移除 CSLReferences 环境定义')
    PREAMBLE = PREAMBLE.replace('__CSL_BLOCK__', csl_block)
else:
    print('[warn] 未提取到 citeproc 块')

i_doc = arr.find('\\begin{document}')
i_end = arr.find('\\end{document}')
body = arr[i_doc + len('\\begin{document}'):i_end]

# 去掉 pandoc 的标题 section
m = re.search(r'\\section\{The Same Zero.*?\}\\label\{.*?\}', body, re.S)
if m:
    body = body[:m.start()] + body[m.end():]

# 去掉作者文本块
m = re.search(r'\\textbf\{Yajie Yin\}.*?(?=\\subsection\{Abstract\})', body, re.S)
if m:
    body = body[:m.start()] + body[m.end():]

# Abstract 包 abstract 环境（到下一个数字章节前）
m = re.search(r'\\subsection\{Abstract\}\s*\\label\{abstract\}(.*?)(?=\\subsection\{\d)', body, re.S)
if m:
    abstract_content = m.group(1)
    body = body[:m.start()] + '\\begin{abstract}\n' + abstract_content + '\\end{abstract}\n' + body[m.end():]
    print('[ok] Abstract 包 abstract 环境')
else:
    print('[warn] Abstract 环境未包（检查格式）')

# 层级提升：数字章节 \subsection{1. X} -> \section{1. X}
body = re.sub(r'\\subsection\{(\d\.)', r'\\section{\1', body)
# 小节提升：\subsubsection -> \subsection
body = body.replace('\\subsubsection{', '\\subsection{')

body = re.sub(r'\n{3,}', '\n\n', body)

out = PREAMBLE + body + '\n\\end{document}\n'
open('acl_submit.tex', 'w', encoding='utf-8').write(out)
# 验证
n_sec = len(re.findall(r'\\section\{', out))
n_sub = len(re.findall(r'\\subsection\{', out))
print(f'生成 acl_submit.tex | \\section={n_sec} \\subsection={n_sub} | 长度={len(out)}')
