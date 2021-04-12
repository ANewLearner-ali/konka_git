import logging
import threading
import time

from utils.kkserial import KKSerialFactory


def send_cmd(com, cmd, wait=0, is_clear_cache=True, timeout=None):
    """
    输入串口命令并等待串口名字执行完成
    """
    logging.debug(com + ' send_cmd :' + cmd.replace('\r', '\\r'))
    kk_serial = KKSerialFactory.get_kk_serial(com)
    if is_clear_cache:
        kk_serial.clear_cache()
    kk_serial.write(cmd + '\r')
    time.sleep(wait)
    kk_serial.write('cat lalalalala\r')
    ret = kk_serial.wait_for_string('No such file or directory', timeout=timeout)
    return ret


def timeout_recovery(com, root=True):
    logging.debug(f'timeout_recovery:{com},because of valid')
    kk_serial = KKSerialFactory.get_kk_serial(com)
    if root:
        kk_serial.write('\r' + chr(3) + '\rsu\r')
    else:
        kk_serial.write('\r' + chr(3) + '\r')


def send_cmd_get_result(com, cmd, wait=0, is_clear_cache=True, timeout=None, is_strip=True):
    """
    输入串口命令并等待串口名字执行完成，并获取返回结果
    """
    logging.debug(com + ' send_cmd :' + cmd.replace('\r', '\\r'))
    if cmd.strip().endswith('&'):
        cmd = 'cat ssttaarrtt;' + cmd + '\echo "";cat eenndd'
    else:
        cmd = 'cat ssttaarrtt;' + cmd + ';echo "";cat eenndd'
    kk_serial = KKSerialFactory.get_kk_serial(com)
    if is_clear_cache:
        kk_serial.clear_cache()
    kk_serial.write(cmd + '\r')
    time.sleep(wait)
    kk_serial.wait_for_string('cat: eenndd: No such file or directory', timeout=timeout)
    result = kk_serial.read_all_quick()
    ret = result.split('cat: ssttaarrtt: No such file or directory', 1)[-1].rsplit('cat: eenndd: No such file or directory', 1)[0]
    ret = ret.rsplit('\r\n', 1)[0]
    if is_strip:
        return ret.strip()
    return ret


def close_kk_serial(com):
    return KKSerialFactory.close_kk_serial(com)



