"""LLM 客户端：封装 DeepSeek API 调用，支持 JSON 结构化输出

你的核心主张在这里的第一个落点：
LLM 只负责"翻译"——把题目翻译成结构化数据（拆解、答案）。
它输出的所有中间量，都必须能被符号引擎（verifier.py）验证。
"""

import json
import time

from openai import OpenAI

from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

_client = None


def get_client():
    global _client
    if _client is None:
        if not DEEPSEEK_API_KEY:
            raise RuntimeError("未设置 DeepSeek API Key！请在 config.py 中填写，或设置环境变量 DEEPSEEK_API_KEY")
        _client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
    return _client


def chat(messages, temperature=0.3, max_tokens=2000):
    """普通对话，返回文本。"""
    resp = get_client().chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def chat_json(messages, temperature=0.3, max_tokens=2500, attempts=3):
    """要求模型输出 JSON，返回解析后的 dict/list。

    模型经常在 JSON 外夹带废话，这里自动提取第一个 JSON 块；
    解析失败则重试，最多 attempts 次。
    """
    msgs = messages + [
        {"role": "system",
         "content": "你必须只输出合法的 JSON，不要输出任何解释文字、不要使用 Markdown 代码块标记。"}
    ]
    last_err = None
    for i in range(attempts):
        try:
            text = chat(msgs, temperature=temperature, max_tokens=max_tokens)
            return parse_json(text)
        except (json.JSONDecodeError, ValueError) as e:
            last_err = e
            time.sleep(1)
    raise ValueError(f"LLM JSON 输出解析失败（{attempts} 次）：{last_err}")


def parse_json(text):
    """从文本中提取 JSON（容忍 ```json 包裹或前后废话）。"""
    text = text.strip()
    # 去掉 Markdown 代码块标记
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    # 提取第一个 JSON 对象或数组
    for open_ch, close_ch in [("{", "}"), ("[", "]")]:
        start = text.find(open_ch)
        if start != -1:
            end = text.rfind(close_ch)
            if end > start:
                candidate = text[start:end + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    continue
    raise ValueError(f"无法从文本中提取 JSON：{text[:200]}")
