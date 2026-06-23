这里是自主学习ai agent的教学文档
项目结构如下

```text
chat_agent/
├── config.yaml          # 配置文件
├── main.py              # 入口
├── agent.py             # 核心逻辑（LLM 调用）
├── history.py           # 聊天历史管理
├── logger.py            # 日志模块
├── requirements.txt     # 依赖声明
└── logs/                # 日志输出目录
```
运行代码步骤：
1. 下载所需依赖：
```bash
cd 目标文件夹
pip install -r requirements.txt
```
2. 在config.yaml中配置 DeepSeek 的 API
3. 在终端中 python main.py

