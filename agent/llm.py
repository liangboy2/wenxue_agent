import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class LLMError(Exception):
    pass


class LLMClient:
    """OpenAI 兼容格式的 LLM 客户端，基于 requests 实现，无框架依赖。"""

    def __init__(self):
        if not config.API_KEY or not config.MODEL:
            raise LLMError(
                "未配置 API_KEY / MODEL。请编辑 config.py 或设置环境变量 "
                "LLM_API_KEY、LLM_MODEL 后重试。"
            )

    def chat(self, messages, temperature=None):
        try:
            import requests
        except ImportError:
            raise LLMError("缺少依赖 requests，请先执行 pip install requests")

        payload = {
            "model": config.MODEL,
            "messages": messages,
            "temperature": config.TEMPERATURE if temperature is None else temperature,
        }
        try:
            resp = requests.post(
                config.API_BASE.rstrip("/") + "/chat/completions",
                headers={"Authorization": f"Bearer {config.API_KEY}"},
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.HTTPError as e:
            raise LLMError(f"HTTP {resp.status_code}: {resp.text[:300]}")
        except Exception as e:
            raise LLMError(f"请求失败: {e}")

        content = data["choices"][0]["message"]["content"]
        return content.strip()


def parse_action(text):
    """解析 LLM 输出的动作指令。优先取 ```json 代码块，否则尝试整段解析。"""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json", 1)[1].split("```", 1)[0].strip()
    elif text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        # 没有结构化动作时，视为直接输出文本
        return {"type": "text", "text": text}
    if isinstance(obj, dict) and ("action" in obj or "final" in obj):
        return obj
    return {"type": "text", "text": text}
