"""文思 Agent Web 版：Flask 后端，复用 agent/core.py 的引擎，服务端无状态。

启动：python web.py  → 浏览器打开 http://127.0.0.1:8000
可选参数：
  --open     启动后自动打开浏览器
  --port N   自定义端口（默认 8000）
"""

import argparse
import os
import sys
import threading
import time
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify, render_template, request

from agent.core import Agent
from agent.llm import LLMError
from domain.profiles import MODE_NAMES

app = Flask(__name__)

VALID_MODES = {"novel", "copy", "doc"}


def _agent(mode):
    if mode not in VALID_MODES:
        raise ValueError("未知模式")
    return Agent(mode)


@app.get("/")
def index():
    return render_template("index.html", modes=MODE_NAMES)


@app.get("/api/modes")
def modes():
    return jsonify(MODE_NAMES)


@app.post("/api/chat")
def chat():
    data = request.get_json(force=True)
    mode = data.get("mode", "novel")
    history = data.get("messages", [])
    try:
        agent = _agent(mode)
        reply, messages = agent.chat(history)
        return jsonify({"reply": reply, "messages": messages})
    except LLMError as e:
        return jsonify({"error": str(e)}), 200
    except Exception as e:
        return jsonify({"error": f"执行出错：{e}"}), 500


@app.post("/api/set")
def set_note():
    data = request.get_json(force=True)
    try:
        agent = _agent(data.get("mode", "novel"))
        agent.memory.set_note(data["key"].strip(), data["value"].strip())
        return jsonify({"ok": True})
    except Exception as e:
        return jsonify({"error": f"写入失败：{e}"}), 400


@app.get("/api/notes")
def notes():
    try:
        agent = _agent(request.args.get("mode", "novel"))
        return jsonify(agent.memory.list_notes())
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文思 Agent Web 版")
    parser.add_argument("--open", action="store_true", help="启动后自动打开浏览器")
    parser.add_argument("--port", type=int, default=8000, help="端口，默认 8000")
    args = parser.parse_args()

    if args.open:
        def _open_browser():
            time.sleep(1.5)
            webbrowser.open(f"http://127.0.0.1:{args.port}")
        threading.Thread(target=_open_browser, daemon=True).start()

    app.run(host="127.0.0.1", port=args.port, debug=False)
