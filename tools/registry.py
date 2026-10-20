class ToolRegistry:
    """工具注册表：统一登记、描述与调用，Agent 通过它执行工具。"""

    def __init__(self):
        self._tools = {}

    def register(self, name, description, func, params=""):
        self._tools[name] = {
            "name": name,
            "params": params,
            "description": description,
            "func": func,
        }

    def describe_all(self):
        lines = [f'- {t["name"]}({t["params"]}): {t["description"]}' for t in self._tools.values()]
        return "\n".join(lines)

    def names(self):
        return list(self._tools)

    def call(self, name, args):
        tool = self._tools.get(name)
        if not tool:
            return f"未知工具：{name}"
        try:
            return str(tool["func"](**args))
        except TypeError as e:
            return f"工具 {name} 参数错误：{e}"
        except Exception as e:
            return f"工具 {name} 执行失败：{e}"
