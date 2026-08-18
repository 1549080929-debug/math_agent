"""全局配置：API 密钥、模型、流程控制参数"""

import json
import os


def _load_api_key():
    """密钥读取优先级：环境变量 DEEPSEEK_API_KEY → local_config.json（不入 git）。"""
    key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if key:
        return key
    try:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_config.json")
        with open(path, encoding="utf-8") as f:
            return json.load(f).get("DEEPSEEK_API_KEY", "").strip()
    except Exception:
        return ""


# ---- DeepSeek API 配置 ----
# 方式1：设置环境变量 DEEPSEEK_API_KEY
# 方式2：在 local_config.json 里写 {"DEEPSEEK_API_KEY": "sk-..."}（已被 .gitignore 排除）
DEEPSEEK_API_KEY = _load_api_key()

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# ---- 流程控制参数 ----
MAX_VERIFY_RETRIES = 3   # 单个子任务验证失败后的反馈纠错次数（补丁 P2）
MAX_REDECOMPOSE = 2      # 重试耗尽后，回溯重新拆解的轮数（补丁 P4）

TEMPERATURE_PLAN = 0.3   # 拆解/规划时的温度
TEMPERATURE_SOLVE = 0.2  # 求解时的温度（低一点，减少随机性）

NUMERIC_TOL = 1e-6       # 数值验证的误差容忍度
