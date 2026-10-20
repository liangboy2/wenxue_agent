# 小说专精工具：每个工具返回一段"专家写作指令"，
# 由 Agent 在下一轮依据指令产出正文，保证方法与模型解耦。

PLAN_PROMPT = """你是一位资深小说策划编辑。请基于用户需求产出一份完整创作方案，必须包含：
1. 【题材定位】类型、目标读者、核心卖点（一句话钩子）
2. 【世界观】时代背景、核心规则、冲突根源（不超过150字）
3. 【人物卡】主角与2-3个关键配角：姓名、年龄、身份、性格标签、欲望、缺陷
4. 【分章大纲】按用户要求章数逐章列出：每章标题、本章事件、章末钩子
5. 【风格基调】叙事视角、节奏、语言风格示例

方案用 Markdown 输出。"""

WRITE_CHAPTER_PROMPT = """你是一位擅长网文与出版文学的小说作者。请续写/创作本章内容，要求：
1. 承接已有情节与人物设定，不偏离
2. 开篇3行内设置钩子，保持章节节奏（起承转合）
3. 对话符合人物性格，动作细节具体，避免大段平铺叙述
4. 章末留下悬念或情绪落点
5. 中文原创，目标字数约 {wordcount} 字

直接输出正文，不要输出标题以外的解释。"""

POLISH_PROMPT = """你是一位文字功底深厚的编辑。请对原文进行润色提升，要求：
1. 保留原意与情节，不增删关键信息
2. 优化用词（更精准、更具画面感）、句式节奏、对话质感
3. 去除重复、啰嗦、说教式表达
4. 输出润色后的全文，并在末尾附【改动说明】列出主要修改点"""

CHARACTER_PROMPT = """你是一位人设策划师。请为用户创建人物设定卡，格式：
- 姓名 / 年龄 / 身份 / 外貌特征 / 性格（含矛盾点）/ 欲望 / 缺陷 / 背景故事（100字内）/ 口头禅与标志动作
要求人物有内在冲突与成长弧线。"""

NAME_PROMPT = """你是一位起名专家。请为角色/书名提供{count}组候选名，每组含：
- 名字、寓意解析（结合题材与人物气质）、适用性别/身份
要求风格贴合题材，避免玛丽苏与生僻字堆砌。"""


def plan_novel(topic, chapters="20", style=""):
    req = f"用户需求：题材/故事核 {topic}；预计 {chapters} 章；风格偏好 {style or '未指定'}"
    return PLAN_PROMPT + "\n\n" + req


def write_chapter(plot_hint, wordcount="2000"):
    return WRITE_CHAPTER_PROMPT.format(wordcount=wordcount) + f"\n\n本章线索/要求：{plot_hint}"


def polish_text(text):
    return POLISH_PROMPT + "\n\n原文：\n" + text


def create_character_sheet(role_brief):
    return CHARACTER_PROMPT + f"\n\n人物需求：{role_brief}"


def name_character(brief, count="6"):
    return NAME_PROMPT.format(count=count) + f"\n\n命名需求：{brief}"
