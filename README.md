# Chat Agent

这是一个用于自主学习 AI Agent 工程基础的聊天 Agent 项目。

项目功能：

- 调用 DeepSeek / OpenAI 兼容接口完成对话
- 支持多轮聊天历史
- 支持配置文件
- 支持日志记录
- 支持 API 异常处理和重试

## 项目结构

```text
chat_agent/
├── main.py              # 入口
├── agent.py             # 核心逻辑（LLM 调用）
├── history.py           # 聊天历史管理
├── logger.py            # 日志模块
├── requirements.txt     # 依赖声明
├── config.example.yaml  # 配置文件示例
└── .gitignore           # Git 忽略规则
```

运行时本地会生成：

```text
config.yaml
history.json
logs/
```

这些文件不会提交到 GitHub。

## 运行代码

1. 下载所需依赖：

```bash
cd chat_agent
pip install -r requirements.txt
```

2. 复制配置文件示例：

```bash
copy config.example.yaml config.yaml
```

3. 在 `config.yaml` 中配置自己的 DeepSeek API Key。

4. 启动聊天 Agent：

```bash
python main.py
```

## 退出和清空历史

- 输入 `quit` 或 `exit` 退出程序。
- 输入 `clear` 清空本地聊天历史。

