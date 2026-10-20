# 文思 Agent —— 专精中文写作的 AI 助手（纯 Python）

一个命令行 AI Agent，三种专精模式：**小说家 / 文案师 / 文书官**。
核心机制：ReAct 循环（LLM 决策 → 调用工具 → 观察结果 → 继续），设定记忆持久化，成品自动落盘。

## 快速开始

### 一键启动（Windows，推荐）

双击根目录的 **`启动.bat`** 即可：自动检查 Python、自动装依赖、校验 LLM 配置，
然后启动网页版并自动打开浏览器。想用终端版就双击 `启动-终端版.bat`。
首次使用若提示未配置 LLM，会弹开 `config.py`，填好保存后重新双击即可。

### 手动启动

1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```
2. 配置 LLM（二选一）
   - 编辑 `config.py` 填入 `API_KEY` 与 `MODEL`
   - 或设置环境变量：`LLM_API_KEY`、`LLM_MODEL`、`LLM_API_BASE`
   - 默认 `API_BASE` 为豆包（火山方舟），换 OpenAI 改 `https://api.openai.com/v1` 即可
3. 启动（两种方式任选）
   ```bash
   python main.py        # 终端版
   python web.py         # Web 版，浏览器打开 http://127.0.0.1:8000
   python web.py --open  # Web 版，启动后自动打开浏览器
   ```

## 使用示例

```
选择写作模式：novel

你 > 写一个校园悬疑小说，主角是转学生，20章
文思 > （Agent 依次调用 plan_novel → 产出大纲 → save_draft 保存）
```

常用指令：`/mode novel|copy|doc` 切换模式、`/set 主角=林晚，26岁` 记录设定、
`/notes` 查看设定、`/new` 清空对话、`/exit` 退出。

## 目录结构

```
wenxue_agent/
├── main.py            CLI 入口（模式选择、对话循环、指令解析）
├── web.py             Web 版入口（Flask，复用同一引擎）
├── config.py          LLM 配置与环境变量
├── agent/
│   ├── llm.py         OpenAI 兼容 LLM 客户端 + 动作解析
│   ├── core.py        Agent 引擎：工具装配 + ReAct 循环（run 供 CLI，chat 供 Web）
│   └── memory.py      设定记忆（JSON 持久化）
├── domain/
│   └── profiles.py    三种专精角色的系统提示词
├── tools/
│   ├── registry.py    工具注册表
│   ├── base_tools.py  通用工具（保存/读取/设定管理）
│   ├── novel_tools.py 小说：策划/续章/润色/人设/起名
│   ├── copy_tools.py  文案：策划/标题/改写（5 平台调性）
│   └── doc_tools.py   文档：报告/总结/纪要/方案/学术
├── templates/
│   └── index.html     Web 版前端（聊天界面 + 设定管理）
├── storage/           成品落盘目录（自动创建）
└── memory/            设定文件目录（自动创建）
```

## 扩展新功能

新增一个写作能力只需两步：
1. 在对应 `tools/*_tools.py` 写一个返回"专家指令"的函数（专业方法内嵌其中）
2. 在 `agent/core.py` 的 `build_registry` 对应分支注册一行

Agent 循环自动获得该工具。新增写作模式则仿照 `domain/profiles.py` 加一条提示词即可。
