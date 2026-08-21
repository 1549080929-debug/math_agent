"""受害者 LLM 客户端：OpenAI 兼容，支持 DeepSeek API / 本地 Ollama 切换。

配置（local_config.json）：
  VICTIM_BASE_URL / VICTIM_API_KEY / VICTIM_MODEL
  （默认 = DeepSeek API：api.deepseek.com / deepseek-chat）
  切到本地：VICTIM_BASE_URL=http://localhost:11434/v1, VICTIM_API_KEY=ollama, VICTIM_MODEL=llama3.1:8b
"""
import json
import time
import urllib.error
import urllib.request

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL, _load_cfg

VICTIM_API_KEY = _load_cfg("VICTIM_API_KEY", DEEPSEEK_API_KEY)
VICTIM_BASE_URL = _load_cfg("VICTIM_BASE_URL", DEEPSEEK_BASE_URL)
VICTIM_MODEL = _load_cfg("VICTIM_MODEL", DEEPSEEK_MODEL)


def victim_chat(messages, temperature=0.2, max_tokens=400, attempts=3):
    """受害者 LLM 调用。429 退避重试。"""
    body = json.dumps({"model": VICTIM_MODEL,
                       "messages": messages,
                       "temperature": temperature,
                       "max_tokens": max_tokens}).encode("utf-8")
    last_err = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(
                VICTIM_BASE_URL.rstrip("/") + "/chat/completions", data=body,
                headers={"Authorization": f"Bearer {VICTIM_API_KEY}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read().decode("utf-8"))
            return d["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code == 429:
                retry = int(e.headers.get("Retry-After", "10") or 10)
                time.sleep(max(retry + 1, 10))
                continue
            time.sleep(3)
        except Exception as e:
            last_err = e
            time.sleep(3)
    raise RuntimeError(f"受害者 LLM 调用失败（{VICTIM_MODEL}）：{last_err}")
