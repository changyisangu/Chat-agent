import time
import logging
from typing import Optional, Dict, Any, List
from openai import OpenAI, RateLimitError, APIError, APITimeoutError, APIConnectionError
from openai.types.chat import ChatCompletionMessageParam

from history import ChatHistory

logger: logging.Logger = logging.getLogger("chat_agent")


class ChatAgent:
    """聊天 Agent：封装 LLM API 调用、多轮对话、异常处理"""

    def __init__(self, config: Dict[str, Any]) -> None:
        self.client: OpenAI = OpenAI(
            api_key=config["api_key"],
            base_url=config.get("base_url"),
        )
        self.model: str = config["model"]
        self.temperature: float = config.get("temperature", 0.7)
        self.max_tokens: int = config.get("max_tokens", 2048)
        self.max_retries: int = config.get("max_retries", 3)
        self.retry_base_delay: float = config.get("retry_base_delay", 1.0)
        self.system_prompt: str = config.get("system_prompt", "你是一个有帮助的助手。")

        self.history: ChatHistory = ChatHistory(config.get("history_path", "history.json"))
        logger.info(f"ChatAgent 初始化完成 | model={self.model}")

    def chat(self, user_input: str) -> str:
        """处理用户输入，返回助手回复"""
        # 构建消息列表
        messages: List[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt}
        ]
        messages.extend(self.history.get_messages())
        messages.append({"role": "user", "content": user_input})

        # 调用 API（含重试）
        reply: Optional[str] = self._call_api_with_retry(messages)
        if reply is None:
            return "[错误] 多次重试失败，请检查网络或 API 配置。"

        # 保存历史
        self.history.add("user", user_input)
        self.history.add("assistant", reply)
        self.history.save()

        # 日志
        logger.info(f"User: {user_input}")
        logger.info(f"Assistant: {reply}")

        return reply

    def _call_api_with_retry(self, messages: List[ChatCompletionMessageParam]) -> Optional[str]:
        """带指数退避的 API 调用"""
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                return response.choices[0].message.content

            except RateLimitError:
                delay: float = self.retry_base_delay * (2 ** (attempt - 1))
                logger.warning(f"频率限制，{delay}s 后重试 ({attempt}/{self.max_retries})")
                time.sleep(delay)

            except APITimeoutError:
                delay = self.retry_base_delay * (2 ** (attempt - 1))
                logger.warning(f"请求超时，{delay}s 后重试 ({attempt}/{self.max_retries})")
                time.sleep(delay)

            except APIConnectionError:
                delay = self.retry_base_delay * (2 ** (attempt - 1))
                logger.warning(f"连接失败，{delay}s 后重试 ({attempt}/{self.max_retries})")
                time.sleep(delay)

            except APIError as e:
                logger.error(f"API 错误: {e}")
                return None

            except Exception as e:
                logger.error(f"未知错误: {e}")
                return None

        logger.error(f"重试 {self.max_retries} 次后仍然失败")
        return None

    def clear_history(self) -> None:
        """清空对话历史"""
        self.history.clear()
        logger.info("对话历史已清空")
