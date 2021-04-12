import logging
import os
import sys
import time


def init_logging(dir_name="", output=True):
    if output and dir_name:
        kk_log = "D:\\kk_log"
        if os.path.isdir(kk_log) is False:
            os.mkdir(kk_log)
        logs_dir = os.path.join(kk_log, dir_name)
        if os.path.isdir(logs_dir) is False:
            os.mkdir(logs_dir)
        # 利用logging模块纪录全局的log，log文件名格式为log + 时间戳
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=os.path.join(logs_dir, 'log_' +
                                                  time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'),
                            filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='w')

    # 全局未捕获的异常输出日志，并退出程序
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        logging.error("exit process by method handle_exception() !!!")
        os._exit(100)

    sys.excepthook = handle_exception


def init_logging_dir(dir_name="", output=True):
    if output and dir_name:
        file_name = dir_name.replace('\\', '\\\\')
        dir_dict = {}
        _dir_path = file_name.split(r'\\')
        _dir_length = len(_dir_path)
        for i, name in enumerate(_dir_path):
            dir_dict[i] = name
        count = 0
        while True:
            if not os.path.isdir(file_name):
                file_name = os.path.dirname(file_name)
                count += 1
            else:
                break
        if count != 0:
            for i in range(count):
                file_name = os.path.join(file_name, dir_dict[_dir_length - (count - i)])
                os.mkdir(file_name)
        logs_dir = file_name
        # 利用logging模块纪录全局的log，log文件名格式为log + 时间戳
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=os.path.join(logs_dir, 'log_' +
                                                  time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'),
                            filemode='w')
    else:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filemode='w')

    # 全局未捕获的异常输出日志，并退出程序
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
        logging.error("exit process by method handle_exception() !!!")
        os._exit(100)

    sys.excepthook = handle_exception

