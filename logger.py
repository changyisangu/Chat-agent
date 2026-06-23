import logging
import os


def setup_logger(log_path: str = "logs/chat.log", log_level: str = "INFO") -> logging.Logger:
    """配置日志：同时输出到文件和终端"""
    # 如果文件夹不存在就创建
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    logger: logging.Logger = logging.getLogger("chat_agent")

    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # 如果这个 logger 已经挂载过输出管道了，就直接返回老的那个，绝不重复添加
    if logger.handlers:
        return logger

    # asctime:时间戳，占位符; levelname:左对齐，固定占 7 个字符宽度
    fmt: logging.Formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 文件输出
    fh: logging.FileHandler = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    
    # 终端输出
    sh: logging.StreamHandler = logging.StreamHandler()
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger
