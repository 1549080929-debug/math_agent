"""全局配置：API 密钥、模型、流程控制参数"""

import json
import os


def _load_cfg(key_name, default=""):
    """配置读取优先级：环境变量 → local_config.json（不入 git）。"""
    val = os.environ.get(key_name, "").strip()
    if val:
        return val
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_config.json")
        with open(path, encoding="utf-8") as f:
            return json.load(f).get(key_name, default)
    except Exception:
        return default


# ---- LLM API 配置（默认 DeepSeek 直连；可在 local_config.json 覆盖网关，如切到 OpenRouter）----
# local_config.json 示例：
#   {"DEEPSEEK_API_KEY": "sk-or-v1-...",
#    "DEEPSEEK_BASE_URL": "https://openrouter.ai/api/v1",
#    "DEEPSEEK_MODEL": "deepseek/deepseek-chat"}
DEEPSEEK_API_KEY = _load_cfg("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = _load_cfg("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = _load_cfg("DEEPSEEK_MODEL", "deepseek-chat")

# ---- 异族攻击者配置（方向 3：跨家族攻击实验）----
# 攻击者默认与受害者同网关，但模型换家族：
#   "ATTACKER_MODEL": "meta-llama/llama-3.3-70b-instruct"  (Groq 可免费；OpenRouter 按量)
#   "ATTACKER_BASE_URL"/"ATTACKER_API_KEY" 可独立指定（如 Groq 免费档）
ATTACKER_API_KEY = _load_cfg("ATTACKER_API_KEY", DEEPSEEK_API_KEY)
ATTACKER_BASE_URL = _load_cfg("ATTACKER_BASE_URL", DEEPSEEK_BASE_URL)
ATTACKER_MODEL = _load_cfg("ATTACKER_MODEL", "meta-llama/llama-3.3-70b-instruct")

# ---- 流程控制参数 ----
MAX_VERIFY_RETRIES = 3   # 单个子任务验证失败后的反馈纠错次数（补丁 P2）
MAX_REDECOMPOSE = 2      # 重试耗尽后，回溯重新拆解的轮数（补丁 P4）

TEMPERATURE_PLAN = 0.3   # 拆解/规划时的温度
TEMPERATURE_SOLVE = 0.2  # 求解时的温度（低一点，减少随机性）

NUMERIC_TOL = 1e-6       # 数值验证的误差容忍度
