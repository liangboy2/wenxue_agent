import os

# LLM 配置：兼容 OpenAI 格式的接口均可使用
# 默认指向豆包（火山方舟）API；换 OpenAI 则改为 https://api.openai.com/v1
API_BASE = os.environ.get("LLM_API_BASE", "https://ark.cn-beijing.volces.com/api/v3")
API_KEY = os.environ.get("LLM_API_KEY", "")  # 优先读环境变量，也可直接在此填入
MODEL = os.environ.get("LLM_MODEL", "")      # 豆包模型 ID 或 OpenAI 模型名，如 gpt-4o-mini

TEMPERATURE = 0.8      # 创作类任务偏高的温度，增加多样性
MAX_ROUNDS = 12        # 单次任务的 ReAct 最大循环轮数
HISTORY_LIMIT = 20     # 对话上下文保留的最大消息条数

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")   # 生成内容落盘目录
MEMORY_DIR = os.path.join(BASE_DIR, "memory")     # 设定记忆文件目录
