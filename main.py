import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from agent.core import Agent
from agent.llm import LLMError
from domain.profiles import MODE_NAMES

HELP = """可用指令：
  /mode novel|copy|doc   切换模式（小说家/文案师/文书官）
  /notes                 查看当前设定
  /set 键=值             记录一条设定，如 /set 主角=林晚，26岁，考古研究生
  /new                   清空本轮对话
  /help                  显示本帮助
  /exit                  退出"""


def pick_mode():
    print("文思 Agent —— 专精中文写作的 AI 助手")
    print("选择写作模式：")
    for key, name in MODE_NAMES.items():
        print(f"  {key}  {name}")
    while True:
        choice = input("> ").strip().lower()
        if choice in MODE_NAMES:
            return choice
        print("请输入 novel / copy / doc 之一：")


def main():
    mode = pick_mode()
    agent = Agent(mode)
    print(f"\n已进入「{MODE_NAMES[mode]}」模式。直接输入你的创作需求，例如：")
    print("  「写一个校园悬疑小说，20章，带系统提示」")
    print("输入 /help 查看指令，/exit 退出。\n")

    while True:
        try:
            user_input = input("你 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input in ("/exit", "退出", "q"):
            print("再见！")
            break
        if user_input == "/help":
            print(HELP)
            continue
        if user_input == "/new":
            agent.reset()
            print("已清空本轮对话。")
            continue
        if user_input == "/notes":
            print(agent.memory.dump() or "（暂无设定）")
            continue
        if user_input.startswith("/set "):
            body = user_input[5:].strip()
            if "=" in body:
                key, value = body.split("=", 1)
                agent.memory.set_note(key.strip(), value.strip())
                print(f"已记录设定：{key.strip()}")
            else:
                print("格式：/set 键=值")
            continue
        if user_input.startswith("/mode "):
            new_mode = user_input[6:].strip()
            if new_mode in MODE_NAMES:
                agent = Agent(new_mode)
                print(f"已切换至「{MODE_NAMES[new_mode]}」模式。")
            else:
                print("可用模式：novel / copy / doc")
            continue

        try:
            print("\n文思 > ", end="", flush=True)
            result = agent.run(user_input)
            print(result)
        except LLMError as e:
            print(f"\n[配置错误] {e}")
        except Exception as e:
            print(f"\n[执行出错] {e}")


if __name__ == "__main__":
    main()
