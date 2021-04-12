import re
import subprocess
import logging
import os
from time import sleep
import _io
from subprocess import TimeoutExpired
import smtplib
from email.mime.text import MIMEText
from email.header import Header


def shell_stdout(cmd, ip):
    ip = ip if ip.endswith(':5555') else ip + ':5555'
    return run_command_stdout('adb -s ' + ip + ' shell "' + cmd + '"')


def adb_pull(ip, tv, pc):
    ip = ip if ip.endswith(':5555') else ip + ':5555'
    cmd = 'adb -s ' + ip + ' pull "' + tv + '" "' + pc + '"'
    run_command(cmd)


def shell(cmd, ip: str, get_return_value=True, wait=True):
    ip = ip if ip.endswith(':5555') else ip + ':5555'
    return run_command('adb -s ' + ip + ' shell "' + cmd + '"', get_return_value=get_return_value, wait=wait)


def run_command_stdout(cmd, charset='utf-8'):
    return run_command(cmd)[0].decode(charset).strip()


def run_command(
        cmd,
        shell=True,
        get_return_value=True,
        wait=True,
        interval=0,
        redirection=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE):
    """
    执行cmd命令
    :param cmd: 命令字符串
    :param shell:是否执行完后退出
    :param get_return_value:是否获取返回值，默认获取
    :param wait:是否等待程序执行完成
    :param interval:执行命令后，等待时长，默认0s
    :param redirection:输出重定向
    :param stdout: 标准输出，默认为管道
    :param stderr: 标准输出，默认为管道
    :return:元组（标准输入，标准输出）
    """
    if not isinstance(shell, bool):
        raise AssertionError('invalid argument shell:' + str(shell))
    if not isinstance(get_return_value, bool):
        raise AssertionError(
            'invalid argument get_return_value:' +
            str(get_return_value))
    if not isinstance(wait, bool):
        raise AssertionError('invalid argument wait:' + str(wait))
    if not isinstance(interval, float) and not isinstance(interval, int):
        raise AssertionError('invalid argument interval:' + str(interval))
    if stdout != subprocess.PIPE and not isinstance(stdout, _io.TextIOWrapper):
        raise AssertionError('invalid argument stdout:' + str(stdout))
    if stderr != subprocess.PIPE and not isinstance(stderr, _io.TextIOWrapper):
        raise AssertionError('invalid argument stderr:' + str(stderr))

    args = str({'cmd': cmd,
                'shell': shell,
                'get_return_value': get_return_value,
                'wait': wait,
                'interval': interval,
                'redirection': redirection,
                'stdout': stdout,
                'stderr': stderr})
    logging.debug(args)
    return __execute_command(
        cmd,
        shell=shell,
        get_return_value=get_return_value,
        wait=wait,
        interval=interval,
        redirection=redirection,
        stdout=stdout,
        stderr=stderr)


def __execute_command(
        cmd,
        shell=True,
        get_return_value=True,
        wait=True,
        interval=0,
        redirection=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE):
    if shell is True and redirection is not None:
        slash = redirection.rfind('/')
        rslash = redirection.rfind('\\')
        if slash == -1 and rslash == -1:
            raise AssertionError('invalid rediretion path')
        parent_rpath = redirection[:slash if slash > rslash else rslash]
        if os.path.isdir(parent_rpath) is False:
            os.makedirs(parent_rpath)
        cmd += ' > ' + redirection
    elif shell is False:
        get_return_value = False
    ret = subprocess.Popen(cmd, shell=shell, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr)
    sleep(interval)
    if get_return_value is True:
        try:
            return ret.communicate(timeout=120)
        except TimeoutExpired:
            return (b'', b'')
    else:
        if wait is True:
            ret.wait()
        else:
            sleep(interval)
        return ret


def is_int(var, start_value=None, end_value=None):
    if var.isdigit() is False:
        return False
    try:
        var = int(var)
    except BaseException:
        return False
    if start_value is not None:
        if var < start_value:
            return False
    if end_value is not None:
        if var > end_value:
            return False
    return True


def send_email(msg_to, title, content, try_times=3):
    # 小号
    # user = '3152847590'
    # msg_from = "3152847590@qq.com"
    # EMAIL_HOST_PASSWORD = 'ocdfnwynnotodgjj'

    # # 娜姐
    msg_from = "562409811@qq.com"
    EMAIL_HOST_PASSWORD = 'esxmhferhdhfbejc'

    # MIMEText构建对象 参数分别是:邮件正文、MIMEsubtype中'plain'表示纯文本、utf-8编码
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = title
    msg['From'] = msg_from
    msg['To'] = msg_to

    try:
        s = smtplib.SMTP_SSL('smtp.qq.com', 465)
        s.login(msg_from, EMAIL_HOST_PASSWORD)
        s.sendmail(msg_from, msg_to, msg.as_string())
        logging.debug("email 发送成功")
    # except s.SMTPException.e:
    except:
        logging.debug("email 发送失败")
        try_times = try_times - 1
        if try_times >= 0:
            send_email(msg_to, title, content, try_times=try_times)
    finally:
        print('发送 失败')
        s.quit()


def email_check(email):
    # ^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$
    if re.match(
        r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$',
            email):
        return True
    return False


def check_ip(ip) -> bool:
    """
    检测ip的连接，root权限
    :param ip: 电视ip地址
    :return: ip是否有效
    """
    if re.match(
        r'^([0-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-4][0-9]'
        r'|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{1,2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{1,2}'
        r'|2[0-4][0-9]|25[0-5])$',
            ip):
        return True
    return False


def check_net_old():
    """
    通过ping 百度 检测网络是否正常
    :return: 是否网络异常
    """
    if b'TTL=' in run_command('ping www.baidu.com')[0]:
        return True
    return False


def check_net():
    """
    请求百度，检测网络是否正常
    :return: 是否网络异常
    """
    import requests
    try:
        requests.get('https://www.baidu.com/', timeout=3)
    except:
        return False
    return True


def clear_dir(dir_name, del_top_dir=True):
    dir_name = os.path.abspath(dir_name)
    print('dir_name :', dir_name)
    files = os.listdir(dir_name)
    for file in files:
        file = os.path.join(dir_name, file)
        print('file :', file)
        if os.path.isfile(file):
            print('remove file')
            os.remove(file)
        else:
            print('remove dir')
            clear_dir(file)
    if del_top_dir:
        os.removedirs(dir_name)
