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


def attacker_chat(messages, temperature=0.8, max_tokens=600, attempts=3):
    """攻击者 LLM 调用（用于改写/生成攻击载荷）。返回文本。"""
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
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read().decode("utf-8"))
            return d["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_err = e
    raise RuntimeError(f"攻击者 LLM 调用失败（{ATTACKER_MODEL}）：{last_err}")
