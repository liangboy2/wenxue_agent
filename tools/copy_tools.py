# 文案专精工具

PLATFORM_RULES = {
    "小红书": "标题带情绪钩子，正文分段短、emoji克制、结尾带互动引导，口语化真诚",
    "公众号": "标题信息量足，正文结构完整（痛点-展开-案例-观点-行动号召），专业但有温度",
    "抖音": "前3秒抓注意力，口播句式短促，强节奏，结尾引导关注",
    "朋友圈": "短平快，一句话金句+轻互动",
    "电商详情": "卖点分点式，数据化、场景化，突出利益点与差异化",
}

COPY_PLAN_PROMPT = """你是一位资深广告文案策划。请产出文案策划方案：
1. 【核心卖点】从产品信息中提炼1-3个差异化卖点
2. 【目标人群】画像（年龄、场景、痛点、决策因素）
3. 【内容结构】按平台调性设计整体结构
4. 【风格基调】语气、用词、句式特征
5. 【标题候选】3个，标注各自策略（痛点/悬念/数字/对比）

平台调性参考：
{platform_rules}"""

REWRITE_PROMPT = """你是一位文案优化专家。请改写用户提供的文案：
1. 保持核心信息不变，输出更吸引人的版本
2. 针对目标平台调整语气与结构
3. 给出【改写思路】说明改动逻辑（不超过100字）"""

HEADLINE_PROMPT = """你是一位标题党专家（正向意义的）。请为给定内容产出{count}个标题：
- 每个标注策略类型（悬念/数字/痛点/对比/身份认同）
- 避免夸张失实与标题党红线（不虚构、不夸大效果）"""


def plan_copy(product, platform="小红书", audience=""):
    rules = PLATFORM_RULES.get(platform, "通用内容调性：清晰、有吸引力")
    req = f"产品/主题：{product}；目标平台：{platform}；目标人群：{audience or '未指定'}"
    return COPY_PLAN_PROMPT.format(platform_rules=rules) + "\n\n" + req


def write_headline(topic, count="5"):
    return HEADLINE_PROMPT.format(count=count) + f"\n\n内容主题：{topic}"


def rewrite_copy(text, platform="小红书"):
    rules = PLATFORM_RULES.get(platform, "通用调性")
    return REWRITE_PROMPT + f"\n\n目标平台：{platform}（调性：{rules}）\n原文案：\n{text}"
