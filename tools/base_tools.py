import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


def _stamp():
    return time.strftime("%Y%m%d_%H%M%S")


def save_draft(title, content, ext="md"):
    """把内容保存到 storage 目录，返回文件路径。"""
    os.makedirs(config.STORAGE_DIR, exist_ok=True)
    safe = "".join(c for c in title if c not in '\\/:*?"<>|') or "draft"
    path = os.path.join(config.STORAGE_DIR, f"{safe}_{_stamp()}.{ext}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"已保存至 {path}（{len(content)} 字）"


def read_draft(filename):
    """读取 storage 中已保存的文稿。"""
    path = os.path.join(config.STORAGE_DIR, filename)
    if not os.path.exists(path):
        return f"未找到 {filename}。可用文件名：" + "、".join(os.listdir(config.STORAGE_DIR))
    with open(path, encoding="utf-8") as f:
        return f.read()


def set_setting(key, value):
    """写入一条设定记忆（由 core 注入已实例化的 Memory）。"""
    return f"设定「{key}」已记录"


def list_settings(memory):
    notes = memory.list_notes()
    if not notes:
        return "暂无设定记录"
    return "\n".join(f"- {k}: {v}" for k, v in notes.items())
