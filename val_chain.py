"""val_chain.py：一条命令跑完整工具链（全部自测 + 演示走查）。

用法：
    python val_chain.py
"""
import subprocess
import sys

STEPS = [
    ("① 追问层自测（buzzword 不豁免）", ["val_interrogate.py", "--auto"]),
    ("② 判级器自测（你在哪一级）", ["val_standard.py"]),
    ("③ 抬级器自测（怎么上去/上不去为什么）", ["val_raise.py"]),
    ("④ 演示走查（判级→抬级→处方→体检）", ["val_demo.py"]),
]


def main():
    ok_all = True
    for name, args in STEPS:
        print(f"\n{'=' * 62}\n▶ {name}\n{'=' * 62}")
        r = subprocess.run([sys.executable] + args)
        ok_all = ok_all and (r.returncode == 0)
    print("\n" + "=" * 62)
    print("工具链全部自测:", "✅ 通过" if ok_all else "❌ 有失败")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
