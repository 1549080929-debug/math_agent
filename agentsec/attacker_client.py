"""异族攻击者客户端：OpenAI 兼容（OpenRouter/Groq/Gemini 均可）。

攻击者模型与受害者（DeepSeek）分属不同家族——P07 的核心启示：
同族验证增益趋零，异族才能测出防御的真实脆弱性。

配置（local_config.json，已 gitignore）：
  ATTACKER_API_KEY / ATTACKER_BASE_URL / ATTACKER_MODEL
  （默认与受害者同网关同 key，模型换家族）
"""
import json
import urllib.request

from config import ATTACKER_API_KEY, ATTACKER_BASE_URL, ATTACKER_MODEL


def attacker_chat(messages, temperature=0.8, max_tokens=600, attempts=8):
    """攻击者 LLM 调用（用于改写/生成攻击载荷）。429 限流退避重试（Kimi 组织级 3 RPM）。"""
    import time
    import urllib.error
    body = json.dumps({
        "model": ATTACKER_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode("utf-8")
    last_err = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(
                ATTACKER_BASE_URL.rstrip("/") + "/chat/completions",
                data=body,
                headers={"Authorization": f"Bearer {ATTACKER_API_KEY}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read().decode("utf-8"))
            return d["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429:
                retry = int(e.headers.get("Retry-After", "20") or 20)
                wait = max(retry + 2, 20)  # 3 RPM 下限：每次至少等 20s
                print(f"  [限流] 等待 {wait}s 后重试（{i + 1}/{attempts}）...", flush=True)
                time.sleep(wait)
                continue
            time.sleep(5)
        except Exception as e:
            last_err = e
            time.sleep(5)
    raise RuntimeError(f"攻击者 LLM 调用失败（{ATTACKER_MODEL}）：{last_err}")
