import os
import sys
import yaml
import logging
from typing import Dict, Any

from logger import setup_logger
from agent import ChatAgent


def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """加载配置文件"""
    if not os.path.exists(path):
        print(f"错误: 找不到配置文件 {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    # 加载配置
    config: Dict[str, Any] = load_config()

    # 初始化日志
    logger: logging.Logger = setup_logger(
        log_path=config.get("log_path", "logs/chat.log"),
        log_level=config.get("log_level", "INFO"),
    )
    logger.info("===== 聊天 Agent 启动 =====")

    # 初始化 Agent
    agent: ChatAgent = ChatAgent(config)

    print(f"模型: {config['model']}")
    print(f"历史消息: {len(agent.history)} 条")
    print("输入 'quit' 或 'exit' 退出，输入 'clear' 清空历史")
    print("-" * 40)

    while True:
        # 交互式文本一定要多用try...except
        try:
            # .strip()：把输入内容前后的空格和换行符删掉。防止按了个空格，程序误以为说了话。
            user_input: str = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"): # .lower()表示输入内容转成小写
            print("用户退出对话！")
            break
        if user_input.lower() == "clear":
            agent.clear_history()
            print("历史已清空。")
            continue

        reply: str = agent.chat(user_input)
        print(f"\nAgent: {reply}")

    logger.info("===== 聊天 Agent 退出 =====")


if __name__ == "__main__":
    
    main()
