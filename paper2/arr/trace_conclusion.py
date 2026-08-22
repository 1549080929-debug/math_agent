"""追踪 Conclusion/Appendix 在管线各文件的形态。"""
BS = chr(92)
for f in ['paper_arr.md', 'paper_arr_cite.md', 'paper_arr.tex', 'acl_submit.tex']:
    s = open(f, encoding='utf-8').read()
    concl = (s.count('\n## 9. Conclusion') or s.count('section{9. Conclusion')
             or s.count('section{Conclusion}') or s.count('section*{Conclusion}'))
    app = (s.count('## Appendix') or s.count('section{Appendix}')
           or s.count('section*{Appendix}'))
    print(f"{f}: Conclusion节={concl} Appendix节={app}")
    # 找 Conclusion 内容是否在
    if 'falsifiable framework' in s:
        i = s.find('falsifiable framework')
        print(f"  Conclusion内容@: {i}")
