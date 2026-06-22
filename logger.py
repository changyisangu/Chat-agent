import logging
import os


def setup_logger(log_path: str = "logs/chat.log", log_level: str = "INFO") -> logging.Logger:
    """配置日志：同时输出到文件和终端"""
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger: logging.Logger = logging.getLogger("chat_agent")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if logger.handlers:
        return logger

    fmt: logging.Formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh: logging.FileHandler = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh: logging.StreamHandler = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger
