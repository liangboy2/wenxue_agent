"""冒烟测试：用模拟 LLM 驱动真实 Agent 引擎，验证工具调用→观察→最终输出的完整循环。
运行：python3 tests/smoke_test.py"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core import Agent, build_registry
from agent.memory import Memory

# 模拟 LLM：第一轮返回工具调用，第二轮返回最终文本
SCRIPT = [
    {"action": "set_setting", "args": {"key": "主角", "value": "林晚，26岁，考古系研究生"}},
    {"action": "plan_novel", "args": {"topic": "盗墓题材", "chapters": "3"}},
    {"final": True, "text": "## 第一章 古井\n夜色里林晚推开锈蚀的铁门……"},
]


class FakeLLM:
    def __init__(self):
        self.i = 0

    def chat(self, messages, temperature=None):
        # 校验 system 提示中确实注入了工具与设定
        sys_prompt = messages[0]["content"]
        assert "plan_novel" in sys_prompt, "工具描述未注入 system prompt"
        act = SCRIPT[min(self.i, len(SCRIPT) - 1)]
        self.i += 1
        return json.dumps(act, ensure_ascii=False)


def test_registry():
    mem = Memory("novel")
    reg = build_registry("novel", mem)
    assert "save_draft" in reg.names() and "plan_novel" in reg.names()
    result = reg.call("name_character", {"brief": "悬疑小说男配"})
    assert "起名专家" in result, result
    print("[1] 工具注册与调用 OK")


def test_agent_loop():
    agent = Agent("novel")
    agent.llm = FakeLLM()
    out = agent.run("写一个盗墓小说")
    assert "第一章" in out, out
    assert agent.memory.get_note("主角") == "林晚，26岁，考古系研究生", "设定未写入记忆"
    # 对话历史应包含工具调用轨迹
    roles = [m["role"] for m in agent.messages]
    assert "tool" in roles, "工具结果未回填对话"
    print("[2] ReAct 循环（工具调用→观察→产出）OK")
    print("[3] 设定记忆持久化 OK")


if __name__ == "__main__":
    test_registry()
    test_agent_loop()
    print("\n全部通过 ✓")
