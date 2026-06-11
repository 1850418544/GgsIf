"""
日志模块
使用loguru库实现日志记录功能，支持控制台输出和文件输出
自动按日期分割日志文件，保留30天历史日志
"""
from loguru import logger
import sys
from pathlib import Path
from config.config import Config

def setup_logger():
    """初始化日志配置
    
    配置说明：
    - 控制台输出：只显示INFO级别及以上，带颜色，UTF-8编码
    - 文件输出：DEBUG级别及以上，按日期分割，保留30天，UTF-8编码
    
    返回：
        logger对象，可直接用于记录日志
    
    使用示例：
        from utils.logger import logger
        
        logger.debug("调试信息，详细的执行过程")
        logger.info("一般信息，正常的操作记录")
        logger.warning("警告信息，需要关注的情况")
        logger.error("错误信息，操作失败")
        logger.critical("严重错误，系统可能无法运行")
    """
    # 设置Windows终端编码为UTF-8(通过环境变量)
    import os
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # 设置Windows命令行代码页为UTF-8
    if os.name == 'nt':
        try:
            os.system('chcp 65001 > nul')
        except:
            pass
    
    # 确保日志目录存在
    Config.ensure_dirs()
    
    # 移除默认的日志处理器(避免重复输出)
    logger.remove()
    
    # 添加控制台输出处理器
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"  # 控制台只显示INFO及以上级别
    )
    
    # 添加文件输出处理器(使用open函数确保UTF-8编码)
    def log_file_sink(message):
        with open(str(Config.LOG_DIR / f"test_{message.record['time'].strftime('%Y-%m-%d')}.log"), 'a', encoding='utf-8') as f:
            f.write(message.record['message'] + '\n')
    
    # 使用loguru的add方法添加文件处理器
    log_file = Config.LOG_DIR / "test_{time:YYYY-MM-DD}.log"
    logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",  # 文件记录DEBUG及以上级别
        rotation="00:00",  # 每天0点自动分割
        retention="30 days",  # 保留30天
        compression="zip"  # 压缩历史日志
    )
    
    return logger

# 创建全局logger实例，其他模块直接导入使用
logger = setup_logger()