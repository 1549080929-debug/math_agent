"""归档脚本：把历史/中间/一次性产物移入 archive/（git mv 保留历史，未跟踪文件用 os.rename）"""
import os, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

def git_mv(src, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    if not os.path.exists(src):
        print(f'  [skip] {src} 不存在')
        return
    r = subprocess.run(['git', 'mv', src, dst_dir], capture_output=True, text=True)
    if r.returncode != 0:
        # 未跟踪文件：普通移动
        shutil.move(src, os.path.join(dst_dir, os.path.basename(src)))
        print(f'  [mv ] {src} -> {dst_dir}')
    else:
        print(f'  [git] {src} -> {dst_dir}')

PLAN = [
    # (源, 目标目录, 文件列表)
    ('paper2/arr', 'archive/arr_intermediates', [
        'paper_arr.tex', 'paper_arr_cite.md', 'acl_submit.tex', 'acl_submit.log',
        'acl_submit.aux', 'final_pages.txt', 'pages2.txt', 'pages3.txt',
        'p89.txt', 'p89b.txt', 'integrity.txt', 'minitest.out',
        'compress_8p.py', 'compress_sec8b.py', 'compress_concl2.py', 'move_62_table.py',
    ]),
    ('paper2/arr', 'archive/arr_versions', ['versions']),
    ('paper2', 'archive/paper2_patches', [
        'patch_boundary.py', 'patch_funnel.py', 'patch_funnel2.py', 'patch_promote.py',
        'patch_sec62b.py', 'patch_z7.py', 'patch_zclaim.py', 'patch_zcurve.py',
        'assess_paper.py',
    ]),
    ('agentsec', 'archive/agentsec_results', ['results']),
    ('agentsec/jade', 'archive/agentsec_jade_assets', [
        'zcurve7_v3.png', 'funnel_v3.png', 'breakpoint_v3.png', 'zcurve_v3.png',
    ]),
    ('book', 'archive/book_builds', ['book.pdf', 'book.html']),
    ('logs', 'archive/logs', None),  # 整目录
]

for src_dir, dst, names in PLAN:
    print(f'--- {src_dir} -> {dst} ---')
    if names is None:
        git_mv(src_dir, dst)
        continue
    for n in names:
        git_mv(os.path.join(src_dir, n), dst)

# 删缓存
import glob
for pat in ['__pycache__', '.mypy_cache']:
    for p in glob.glob(f'**/{pat}', recursive=True):
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
            print(f'[del] {p}')
print('DONE')
