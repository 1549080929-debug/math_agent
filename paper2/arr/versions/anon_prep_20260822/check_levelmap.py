"""Locate Level map table and measure row geometry."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pymupdf

doc = pymupdf.open('paper2/arr/acl_submit.pdf')

def rules(page):
    ys = []
    for d in page.get_drawings():
        for it in d['items']:
            if it[0] == 'l':
                p1, p2 = it[1], it[2]
                if abs(p1.y - p2.y) < 0.5:
                    ys.append(round(p1.y, 1))
    return sorted(set(ys))

LABELS = {'L0', 'L1', 'L2', 'L3', 'L4', 'N/A'}
for i, page in enumerate(doc):
    rs = rules(page)
    if not rs:
        continue
    words = page.get_text('words')
    lev = sorted(set(round((w[1] + w[3]) / 2) for w in words if w[4] in LABELS and w[0] < 130))
    lvl_hdr = [round((w[1] + w[3]) / 2) for w in words if w[4] == 'Level' and w[0] < 130]
    if lev or lvl_hdr:
        print(f'page {i+1}: rules={rs}')
        print(f'  Level header y: {lvl_hdr}')
        print(f'  L0-L4/N-A row y-centers: {lev}')
        if lev:
            print(f'  row-to-row gaps: {[lev[j+1]-lev[j] for j in range(len(lev)-1)]}')
        # bottom-most text
        if words:
            print(f'  lowest text y: {round(max(w[3] for w in words),1)} (page h=841.9)')
