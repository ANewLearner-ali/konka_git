import time


TYPE1 = "%Y%m%d%H%M%S"
TYPE2 = "%Y-%m-%d %H:%M:%S"
TYPE3 = "%Y_%m_%d_%H_%M_%S"


def datetime_string(format_type: str=TYPE1, p_tuple: tuple=None):
    if p_tuple:
        return time.strftime(format_type, p_tuple)
    return time.strftime(format_type, time.localtime())


def datetime_string_set(format_type: list = None, p_tuple: tuple=None) -> list:
    format_type = [TYPE1] if format_type is None else format_type
    ret = []
    p_tuple = time.localtime() if p_tuple is None else p_tuple
    for ft in format_type:
        ret.append(time.strftime(ft, p_tuple))
    return ret


def datetime_stamp(format_type, string):
    return int(time.mktime(time.strptime(string, format_type)))


def second_to_datetime(second):
    day, second = divmod(second, 86400)
    hour, second = divmod(second, 3600)
    minute, second = divmod(second, 60)
    if day:
        return str(int(day)) + '天' + str(int(hour)) + '时' + str(int(minute)) + '分' + str(int(second)) + '秒'
    return str(int(hour)) + '时' + str(int(minute)) + '分' + str(int(second)) + '秒'

