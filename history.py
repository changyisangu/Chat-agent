import json
import os
import logging
from typing import List, Dict, Optional

logger: logging.Logger = logging.getLogger("chat_agent")

Message = Dict[str, str]  # {"role": "user"|"assistant"|"system", "content": "..."}


class ChatHistory:
    """聊天历史管理：加载/保存 JSON 格式的对话记录"""

    def __init__(self, path: str = "history.json") -> None:
        self.path: str = path
        self.messages: List[Message] = []
        self.load()

    def load(self) -> None:
        """从文件加载历史"""
        if not os.path.exists(self.path):
            self.messages = []
            logger.info(f"历史文件不存在，新建: {self.path}")
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.messages = json.load(f)
            logger.info(f"加载历史 {len(self.messages)} 条消息: {self.path}")
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"历史文件加载失败，重置: {e}")
            self.messages = []

    def save(self) -> None:
        """保存历史到文件"""
        try:
            os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
        except IOError as e:
            logger.error(f"历史文件保存失败: {e}")

    def add(self, role: str, content: str) -> None:
        """添加一条消息"""
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> List[Message]:
        """返回当前历史（不含 system prompt）"""
        return list(self.messages)

    def clear(self) -> None:
        """清空历史"""
        self.messages = []
        self.save()
        logger.info("历史已清空")

    def __len__(self) -> int:
        return len(self.messages)
