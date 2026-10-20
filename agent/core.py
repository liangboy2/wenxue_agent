import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from agent.llm import LLMClient, LLMError, parse_action
from agent.memory import Memory
from domain.profiles import PROFILES
from tools.registry import ToolRegistry
import tools.base_tools as base
import tools.novel_tools as novel
import tools.copy_tools as copy
import tools.doc_tools as doc


def build_registry(mode, memory):
    """按写作模式装配工具集：通用工具 + 专精工具。"""
    reg = ToolRegistry()
    reg.register("save_draft", "把最终成品保存到本地，返回路径。写完整篇作品前必须调用", base.save_draft, "title, content, ext='md'")
    reg.register("read_draft", "读取 storage 中已保存的文稿", base.read_draft, "filename")
    reg.register("set_setting", "记录一条设定（人物/世界观/风格等），之后所有创作都须遵守",
                 lambda key, value: (memory.set_note(key, value) or base.set_setting(key, value)), "key, value")
    reg.register("list_settings", "查看当前已记录的设定", lambda: base.list_settings(memory))

    if mode == "novel":
        reg.register("plan_novel", "获取小说创作方案（题材定位/世界观/人物卡/分章大纲/风格基调）", novel.plan_novel, "topic, chapters='20', style=''")
        reg.register("write_chapter", "获取续写章节的写作指令（含节奏与钩子要求）", novel.write_chapter, "plot_hint, wordcount='2000'")
        reg.register("polish_text", "获取润色指令，用于提升文字质感", novel.polish_text, "text")
        reg.register("create_character_sheet", "获取人物设定卡创建指令", novel.create_character_sheet, "role_brief")
        reg.register("name_character", "获取角色/书名起名指令", novel.name_character, "brief, count='6'")
    elif mode == "copy":
        reg.register("plan_copy", "获取文案策划方案（卖点/人群/结构/标题）", copy.plan_copy, "product, platform='小红书', audience=''")
        reg.register("write_headline", "获取标题创作指令", copy.write_headline, "topic, count='5'")
        reg.register("rewrite_copy", "获取文案改写指令", copy.rewrite_copy, "text, platform='小红书'")
    elif mode == "doc":
        reg.register("plan_doc", "获取文档大纲（工作报告/总结/纪要/方案/学术）", doc.plan_doc, "doc_type, topic, extra=''")
        reg.register("polish_doc", "获取文档润色指令", doc.polish_doc, "text")
        reg.register("summarize_material", "获取资料整理为结构化摘要的指令", doc.summarize_material, "material")
    return reg


class Agent:
    """ReAct 循环：LLM 决策 → 执行工具 → 观察结果 → 继续，直到输出最终文本。"""

    def __init__(self, mode):
        self.mode = mode
        self.memory = Memory(mode)
        self.tools = build_registry(mode, self.memory)
        self.messages = []
        self.llm = None

    def _system_prompt(self):
        mem = self.memory.dump() or "（暂无设定）"
        return PROFILES[self.mode].format(memory=mem, tools=self.tools.describe_all())

    def _execute(self):
        """执行一轮 ReAct 循环（LLM 决策 → 工具 → 观察），返回最终文本。"""
        for _ in range(config.MAX_ROUNDS):
            msgs = [{"role": "system", "content": self._system_prompt()}] + self.messages[-config.HISTORY_LIMIT:]
            reply = self.llm.chat(msgs)
            action = parse_action(reply)

            if action.get("final") or action.get("type") == "text":
                text = action.get("text", reply)
                self.messages.append({"role": "assistant", "content": text})
                return text

            tool_name = action.get("action", "")
            args = action.get("args", {}) or {}
            result = self.tools.call(tool_name, args)
            self.messages.append({"role": "assistant", "content": json.dumps(action, ensure_ascii=False)})
            self.messages.append({"role": "tool", "content": result})

        return "已达最大轮数，任务未完成，请分步执行或检查配置。"

    def run(self, user_input):
        if self.llm is None:
            self.llm = LLMClient()
        self.messages.append({"role": "user", "content": user_input})
        return self._execute()

    def chat(self, history):
        """Web 版接口：接收完整消息历史（不含 system），执行一轮，
        返回 (回复文本, 更新后的消息历史)。历史由前端持久化，服务端无状态。"""
        if self.llm is None:
            self.llm = LLMClient()
        self.messages = [dict(m) for m in history]
        text = self._execute()
        return text, self.messages

    def reset(self):
        self.messages = []
