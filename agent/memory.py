import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config


class Memory:
    """基于 JSON 文件的设定记忆：按模式（novel/copy/doc）分组存储，
    用于保存世界观、人物卡、大纲、风格要求等长期信息。"""

    def __init__(self, mode):
        self.mode = mode
        os.makedirs(config.MEMORY_DIR, exist_ok=True)
        self.path = os.path.join(config.MEMORY_DIR, f"{mode}.json")
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        return {"notes": {}}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def set_note(self, key, value):
        """写入一条设定，如 ('主角', '林晚，26岁，考古系研究生')。"""
        self.data["notes"][key] = value
        self._save()

    def get_note(self, key):
        return self.data["notes"].get(key)

    def list_notes(self):
        return self.data["notes"]

    def delete_note(self, key):
        self.data["notes"].pop(key, None)
        self._save()

    def dump(self):
        """返回设定全文，注入到 system prompt 供 LLM 参考。"""
        if not self.data["notes"]:
            return ""
        lines = [f"- {k}: {v}" for k, v in self.data["notes"].items()]
        return "\n".join(lines)
