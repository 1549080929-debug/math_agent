"""verify_checksum.py：下载文件校验（把 L2 锚落到实操——哈希与官方值比对）。

用法：
    python verify_checksum.py <文件路径> <期望 sha256>
    python verify_checksum.py --gen <文件路径>      # 生成文件自身的 sha256（备用）

原理（VAL 视角）：下载软件时，"这是官方安装包"是一个声称（L0）。
独立的锚 = 官方公布的 sha256 值（L2 客观真值）。哈希比对通过 = 该声称被独立锚支持。
比对不通过 = 声称无锚 → 不安装（这是工具会说的"不"）。
"""
import hashlib
import sys


def sha256_of(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            block = f.read(chunk)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    if args[0] == "--gen" and len(args) == 2:
        print(sha256_of(args[1]))
        return 0
    if len(args) != 2:
        print("用法: python verify_checksum.py <文件> <期望sha256>  或  --gen <文件>")
        return 1
    path, expected = args
    try:
        actual = sha256_of(path)
    except FileNotFoundError:
        print(f"文件不存在: {path}")
        return 1
    ok = actual.lower() == expected.lower().strip()
    print(f"文件    : {path}")
    print(f"实际    : {actual}")
    print(f"期望    : {expected.strip()}")
    print("判定    :", "✅ 匹配——独立锚支持该声称，可安装" if ok
          else "❌ 不匹配——声称无锚支持，不要安装")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
