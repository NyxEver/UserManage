import logging
import os
from datetime import datetime

current_dir=os.path.dirname(os.path.abspath(__file__))
main_dir=os.path.dirname(current_dir)
logs_dir=os.path.join(main_dir,'logs')

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
#class Date_Check():
#    pass

date_check=None

def get_logger(model_name):
    global date_check
    #创建记录器
    logger = logging.getLogger(model_name)
    logger.setLevel(logging.DEBUG)

    today = datetime.now().strftime('%Y-%m-%d')

    if today!=date_check or logger.handlers:
        logger.handlers.clear()

        log_format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        #创建文件处理器
        file_handler = logging.FileHandler(f'{logs_dir}/log_{today}.txt', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        # 格式化器
        file_handler.setFormatter(logging.Formatter(log_format))
        console_handler.setFormatter(logging.Formatter(log_format))
        # 添加处理器到日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        #更新日期
        date_check= today
    return logger
