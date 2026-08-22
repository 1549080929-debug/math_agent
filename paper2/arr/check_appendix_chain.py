"""检查 Appendix 在管线各文件的状态。"""
for f in ['paper_arr.md', 'paper_arr_cite.md', 'paper_arr.tex', 'acl_submit.tex']:
    try:
        s = open(f, encoding='utf-8').read()
        appendix_hdr = s.count('\n## Appendix') + s.count('\r## Appendix')
        print(f"{f}: Appendix标题={appendix_hdr} A.1={s.count('A.1')} LevelMap表={'| Level | Defenses' in s}")
    except Exception as e:
        print(f"{f}: ERR {e}")
