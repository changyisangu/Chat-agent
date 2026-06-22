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
        try:
            user_input: str = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("再见！")
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
