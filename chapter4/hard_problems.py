"""P3 实验补充：6 道手写难题（非经典、带陷阱），先审计测试再用。

每题的 test 用 canonical 解法先自验（audit-first 纪律），
再在 deepseek-chat 上跑 A(裸)/B(带类型)/C(类型检查反馈) 三条件。
"""

PROBLEMS = [
    {
        "id": "hard/0",
        "prompt": (
            "def kth_custom_number(n: int) -> int:\n"
            "    \"\"\"返回第 n 个（从 1 开始）同时满足以下条件的正整数：\n"
            "    ① 数字中包含 7；② 不是素数；③ 十进制各位数字之和是偶数。\n"
            "    >>> kth_custom_number(1)\n    57\n"
            "    \"\"\"\n"
        ),
        "test": (
            "def check(candidate):\n"
            "    assert candidate(1) == 57\n"
            "    assert candidate(2) == 75\n"
            "    assert candidate(3) == 77\n"
            "    assert candidate(4) == 147\n"
            "    assert candidate(10) == 187\n"
            "check(kth_custom_number)\n"
        ),
        "canonical": (
            "def kth_custom_number(n: int) -> int:\n"
            "    def ok(x):\n"
            "        if '7' not in str(x): return False\n"
            "        if x < 2: return False\n"
            "        for d in range(2, int(x**0.5)+1):\n"
            "            if x % d == 0: break\n"
            "        else:\n"
            "            return False  # 素数不满足\n"
            "        return sum(int(c) for c in str(x)) % 2 == 0\n"
            "    cnt, x = 0, 1\n"
            "    while True:\n"
            "        if ok(x):\n"
            "            cnt += 1\n"
            "            if cnt == n: return x\n"
            "        x += 1\n"
        ),
    },
    {
        "id": "hard/1",
        "prompt": (
            "def decode_escaped(s: str) -> str:\n"
            "    \"\"\"解码带转义的压缩串。规则：数字 k 后跟 [..] 表示重复 k 次；\n"
            "    反斜杠 \\ 转义下一个字符（\\[ 是字面左括号，\\\\ 是字面反斜杠）；\n"
            "    未匹配的右括号 ] 按字面输出。\n"
            "    >>> decode_escaped('2[a]')\n"
            "    'aa'\n"
            "    >>> decode_escaped(r'2[a\\[b]')\n"
            "    'a[ba[b'  # 转义的 [ 是字面字符，作为内容参与重复\n"
            "    \"\"\"\n"
        ),
        "test": (
            "def check(candidate):\n"
            "    assert candidate('2[a]') == 'aa'\n"
            "    assert candidate('3[b2[c]]') == 'bccbccbcc'\n"
            "    assert candidate(r'2[a\\[b]') == 'a[ba[b'\n"
            "    assert candidate(']a]') == ']a]'\n"
            "    assert candidate(r'a\\\\b') == 'a\\\\b'\n"
            "    assert candidate('10[a]') == 'a'*10\n"
            "check(decode_escaped)\n"
        ),
        "canonical": (
            "def decode_escaped(s: str) -> str:\n"
            "    stack, cur, num = [], '', 0\n"
            "    i = 0\n"
            "    while i < len(s):\n"
            "        ch = s[i]\n"
            "        if ch == '\\\\' and i+1 < len(s):\n"
            "            cur += s[i+1]; i += 2; continue\n"
            "        if ch.isdigit():\n"
            "            num = num*10 + int(ch); i += 1; continue\n"
            "        if ch == '[':\n"
            "            stack.append((cur, num)); cur, num = '', 0; i += 1; continue\n"
            "        if ch == ']' and stack:\n"
            "            prev, k = stack.pop(); cur = prev + cur*k; i += 1; continue\n"
            "        cur += ch; i += 1\n"
            "    return cur\n"
        ),
    },
    {
        "id": "hard/2",
        "prompt": (
            "def earliest_meeting(busy: list[tuple[int, int]], duration: int) -> int:\n"
            "    \"\"\"给定忙碌区间列表（闭区间 [start, end]，端点均被占用）和会议时长，\n"
            "    返回从时刻 0 开始能安排的最早会议开始时刻。忙碌区间已按 start 升序。\n"
            "    >>> earliest_meeting([(10, 12), (15, 18)], 2)\n"
            "    0\n"
            "    >>> earliest_meeting([(0, 5), (5, 8)], 3)\n"
            "    8\n"
            "    \"\"\"\n"
        ),
        "test": (
            "def check(candidate):\n"
            "    assert candidate([(10, 12), (15, 18)], 2) == 0\n"
            "    assert candidate([(0, 5), (5, 8)], 3) == 8\n"
            "    assert candidate([(0, 3), (3, 6), (6, 9)], 3) == 9\n"
            "    assert candidate([(0, 1), (2, 3)], 2) == 3\n"
            "    assert candidate([], 5) == 0\n"
            "check(earliest_meeting)\n"
        ),
        "canonical": (
            "def earliest_meeting(busy: list[tuple[int, int]], duration: int) -> int:\n"
            "    t = 0\n"
            "    for s, e in busy:\n"
            "        if t + duration <= s:\n"
            "            return t\n"
            "        t = max(t, e)\n"
            "    return t\n"
        ),
    },
    {
        "id": "hard/3",
        "prompt": (
            "def nibble_swap(x: int) -> int:\n"
            "    \"\"\"对 32 位无符号整数 x，每 4 位一组，交换组内高两位与低两位，\n"
            "    其余位不变。\n"
            "    >>> nibble_swap(0b0001)  # 0001 → 0100\n"
            "    4\n"
            "    >>> nibble_swap(0b0010)  # 0010 → 1000\n"
            "    8\n"
            "    \"\"\"\n"
        ),
        "test": (
            "def check(candidate):\n"
            "    assert candidate(0) == 0\n"
            "    assert candidate(1) == 4\n"
            "    assert candidate(2) == 8\n"
            "    assert candidate(0xF) == 0xF\n"
            "    assert candidate(0x1A) == 0x4A\n"
            "    assert candidate(0x12345678) == 0x48C159D2\n"
            "check(nibble_swap)\n"
        ),
        "canonical": (
            "def nibble_swap(x: int) -> int:\n"
            "    z = 0\n"
            "    for g in range(8):\n"
            "        nib = (x >> (g*4)) & 0xF\n"
            "        hi = (nib >> 2) & 0x3\n"
            "        lo = nib & 0x3\n"
            "        z |= ((lo << 2) | hi) << (g*4)\n"
            "    return z\n"
        ),
    },
    {
        "id": "hard/4",
        "prompt": (
            "def same_parity_pair(nums: list[int], target: int) -> tuple[int, int] | None:\n"
            "    \"\"\"在 nums 中找到两个不同下标的数，二者之和等于 target，\n"
            "    且两个数的奇偶性相同（同为奇数或同为偶数）。\n"
            "    返回 (小下标, 大下标)；不存在返回 None。\n"
            "    >>> same_parity_pair([1, 3, 2, 4], 6)\n"
            "    (2, 3)  # 2+4=6，同为偶数\n"
            "    \"\"\"\n"
        ),
        "test": (
            "def check(candidate):\n"
            "    assert candidate([1, 3, 2, 4], 6) == (2, 3)   # 2+4，同为偶\n"
            "    assert candidate([1, 3, 5], 4) == (0, 1)      # 1+3，同为奇\n"
            "    assert candidate([1, 2, 3], 4) == (0, 2)      # 1+3=4，同为奇\n"
            "    assert candidate([2, 4, 6], 10) == (1, 2)\n"
            "    assert candidate([1, 2], 3) is None           # 1 奇 2 偶，异偶\n"
            "    assert candidate([], 0) is None\n"
            "check(same_parity_pair)\n"
        ),
        "canonical": (
            "def same_parity_pair(nums: list[int], target: int) -> tuple[int, int] | None:\n"
            "    seen_even, seen_odd = {}, {}\n"
            "    for i, v in enumerate(nums):\n"
            "        need = target - v\n"
            "        pool = seen_even if v % 2 == 0 else seen_odd\n"
            "        if need in pool:\n"
            "            j = pool[need]\n"
            "            return (min(j, i), max(j, i))\n"
            "        pool[v] = i\n"
            "    return None\n"
        ),
    },
    {
        "id": "hard/5",
        "prompt": (
            "def flatten_skip(data: list) -> list:\n"
            "    \"\"\"展平嵌套列表：数字/字符串保留；None 跳过；字典值原样保留（不递归）；\n"
            "    元组视为列表递归展平。\n"
            "    >>> flatten_skip([1, [2, None, [3]], {'a': [4]}], )\n"
            "    [1, 2, 3, {'a': [4]}]\n"
            "    \"\"\"\n"
        ),
        "test": (
            "def check(candidate):\n"
            "    assert candidate([1, [2, None, [3]], {'a': [4]}]) == [1, 2, 3, {'a': [4]}]\n"
            "    assert candidate([None, None]) == []\n"
            "    assert candidate([(1, 2), [3]]) == [1, 2, 3]\n"
            "    assert candidate([]) == []\n"
            "    assert candidate([0, False, '', 'x']) == [0, False, '', 'x']\n"
            "check(flatten_skip)\n"
        ),
        "canonical": (
            "def flatten_skip(data: list) -> list:\n"
            "    out = []\n"
            "    for x in data:\n"
            "        if x is None:\n"
            "            continue\n"
            "        if isinstance(x, (list, tuple)):\n"
            "            out.extend(flatten_skip(x))\n"
            "        else:\n"
            "            out.append(x)\n"
            "    return out\n"
        ),
    },
]


def audit():
    """用 canonical 解法自验所有测试（audit-first）。"""
    import subprocess, sys
    ok = True
    for p in PROBLEMS:
        full = p["canonical"] + "\n\n" + p["test"]
        r = subprocess.run([sys.executable, "-c", full], capture_output=True, text=True, timeout=20)
        good = r.returncode == 0
        ok &= good
        print(f"{p['id']}: canonical {'PASS' if good else 'FAIL ' + (r.stderr[:200] or '')}")
    print("审计:", "全部通过" if ok else "有失败（测试或 canonical 有误，禁止用于实验）")
    return ok


if __name__ == "__main__":
    import sys
    sys.exit(0 if audit() else 1)
