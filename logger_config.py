import logging
import os
from datetime import datetime

if not os.path.exists('logs'):
    os.makedirs('logs')

def get_logger(model_name):
    #创建记录器
    logger = logging.getLogger(model_name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        logger.handlers.clear()

    log_format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    #date_format = '%Y-%m-%d %H:%M:%S'
    # 创建文件处理器
    today = datetime.now().strftime('%Y-%m-%d')
    file_handler = logging.FileHandler(f'logs/log_{today}.txt', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    #格式化器
    file_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setFormatter(logging.Formatter(log_format))

    #添加处理器到日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger