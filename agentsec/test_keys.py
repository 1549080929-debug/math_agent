"""钥匙自检：验证受害者（DeepSeek 系）与异族攻击者端点是否可用。

用法：python agentsec/test_keys.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def probe(base_url, key, model, label):
    import urllib.request
    body = json.dumps({"model": model,
                       "messages": [{"role": "user", "content": "回复两个字：正常"}],
                       "max_tokens": 20}).encode("utf-8")
    req = urllib.request.Request(base_url.rstrip("/") + "/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read().decode("utf-8"))
            print(f"  [OK]   {label}: {d['choices'][0]['message']['content'][:20]}")
            return True
    except Exception as e:
        print(f"  [FAIL] {label} ({model}): {str(e)[:120]}")
        return False


def main():
    with io.open(os.path.join(ROOT, "local_config.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    from config import (ATTACKER_API_KEY, ATTACKER_BASE_URL, ATTACKER_MODEL,
                        DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL)
    print("== 端点自检 ==")
    print(f"  受害者: {DEEPSEEK_BASE_URL} / {DEEPSEEK_MODEL}")
    print(f"  攻击者: {ATTACKER_BASE_URL} / {ATTACKER_MODEL}")
    ok1 = probe(DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL, "受害者(DeepSeek 系)")
    ok2 = probe(ATTACKER_BASE_URL, ATTACKER_API_KEY, ATTACKER_MODEL, "异族攻击者")
    print("\n结论:", "全部可用，可以开跑" if (ok1 and ok2) else "有端点不可用——检查 local_config.json 的 key")


if __name__ == "__main__":
    main()
