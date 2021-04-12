import base64
import re
import socket
import logging

import time

from utils import shellcmd, kkserial

# channels
from utils.shellcmd import timeout_recovery

DTMB = 'DTMB'
ATV = 'ATV'
AV = 'AV'
HDMI1 = 'HDMI1'
HDMI2 = 'HDMI2'
HDMI3 = 'HDMI3'


def _send_cmd(com, cmd, timeout=60):
    if isinstance(com, str):
        res = shellcmd.send_cmd(com, cmd, timeout=timeout)
    else:
        res = com.tv.send_cmd(cmd, timeout=timeout)
    return res


def _send_cmd_get_result(com, cmd, timeout=60) -> str:
    if isinstance(com, str):
        res = shellcmd.send_cmd_get_result(com, cmd, timeout=timeout)
    else:
        res = com.tv.send_cmd_get_result(cmd, timeout=timeout)
    return res


def _timeout_recovery(com):
    logging.debug(f'timeout_recovery:{com},because of invalid instruction')
    if isinstance(com, str):
        res = shellcmd.timeout_recovery(com, root=False)
    else:
        res = com.tv.send_cmd('\r' + chr(3) + '\r', timeout=2)
    return res


def check_serial(func):
    def wrapper(*args, **kwargs):
        logging.debug('Some exceptions may occur in this instruction, try to recovery!')
        timeout_recovery(args[0])
        return func(*args, **kwargs)
    return wrapper()


device_send = _send_cmd
device_send_r = _send_cmd_get_result


def go_to_tv(com):
    _send_cmd(com, 'am broadcast -a com.konka.GO_TO_TV')


def mkdir(com, dir_path):
    _send_cmd(com, 'mkdir -p ' + dir_path + ' 2>/dev/null')


def rm(com, file, is_file=True):
    if is_file:
        _send_cmd(com, 'rm -f ' + file + ' 2>/dev/null')
    else:
        _send_cmd(com, 'rm -rf ' + file + ' 2>/dev/null')


def get_eth0_ip(com) -> str:
    cmd = 'busybox ifconfig eth0 |grep "inet addr:" |busybox awk \'{split($2,s,":");print s[2]}\''
    return _send_cmd_get_result(com, cmd)


def get_wlan0_ip(com) -> str:
    cmd = 'busybox ifconfig wlan0 |grep "inet addr:" |busybox awk \'{split($2,s,":");print s[2]}\''
    return _send_cmd_get_result(com, cmd)


def get_tv_ip(com) -> str:
    eth0_ip = get_eth0_ip(com)
    wlan0_ip = get_wlan0_ip(com)
    if eth0_ip:
        return eth0_ip
    elif wlan0_ip:
        return wlan0_ip
    return ''


def get_wifi_driver_state(com) -> bool:
    _send_cmd(com, 'svc wifi disable')
    time.sleep(2)
    _send_cmd(com, 'svc wifi enable')
    i = 0
    while i < 12:
        time.sleep(10)
        lines = _send_cmd_get_result(com, 'dumpsys wifiscanner').split('\r\n')
        start = False
        for line in lines:
            if 'Latest scan results:' in line:
                start = True
                continue
            if start:
                return line.strip() != ''
        i += 1
    return False


def push_file_by_base64(com: str, pc_file: str, tv_file: str):
    """
    example:
    push_file_by_base64(com='com28',
                        pc_file=r'F:\WORK_FILE\eclipse_work\kktestsocket\bin\kktestsocket.jar',
                        tv_file=r'/data/local/tmp/kktestsocket.jar')
    """
    with open(pc_file, 'rb') as f:
        b = f.read()
    base_string = base64.b64encode(b).decode()
    base_tv_file = tv_file + '.base'
    now = 0
    step = 2000
    write_label = '>'
    for i in range(len(base_string) // step):
        shellcmd.send_cmd(com, 'echo "' + base_string[now:now + step] + '" ' + write_label + ' ' + base_tv_file)
        now = now + step
        write_label = '>>'
    shellcmd.send_cmd(com, 'echo "' + base_string[now:now + step] + '" ' + write_label + ' ' + base_tv_file)
    shellcmd.send_cmd(com, 'cat ' + base_tv_file + ' | busybox base64 -d > ' + tv_file)


def get_cmd_pid(com, cmd):
    cmd = cmd + '\echo "my_pid"":$!"'
    result = _send_cmd_get_result(com, cmd)
    ret = ''
    for line in result.split('\r\n'):
        line = line.strip()
        if line and 'my_pid:' in line:
            ret = line.split('my_pid:', 1)[-1]
            break
    logging.debug('get_cmd_pid :' + cmd.replace('\r', '\\r') + ' , is ' + ret)
    return ret


def start_logcat(com, file) -> str:
    return get_cmd_pid(com, 'logcat -v time > ' + file + ' &')


def stop_logcat(com):
    _send_cmd(com, 'busybox killall logcat', timeout=2)


def start_kmsg(com, file) -> str:
    return get_cmd_pid(com, 'cat /proc/kmsg  > ' + file + ' &')


def stop_kmsg(com):
    _send_cmd(com, 'busybox killall cat', timeout=2)


def clear_traces(com):
    _send_cmd(com, 'rm /data/anr/* 1>/dev/null 2>&1')


def mv_log(com, ori_file, des_file):
    _send_cmd(com, 'mv ' + ori_file + ' ' + des_file + ' 1>/dev/null 2>&1')


def copy_traces(com, file_dir, is_rm=True):
    _send_cmd(com, 'anr_num=`ls /data/anr|wc -l 2>/dev/null`;if [ $anr_num -ge 1  ];then cp -r /data/anr ' + file_dir + ' 1>/dev/null 2>&1; fi')
    if is_rm:
        _send_cmd(com, 'rm /data/anr/* 1>/dev/null 2>&1')


def copy_tombstones(com, file_dir, is_rm=True):
    _send_cmd(com, 'tombstones_num=`ls /data/tombstones|wc -l 2>/dev/null`;if [ $tombstones_num -ge 1  ];then cp -r /data/tombstones ' + file_dir + ' 1>/dev/null 2>&1; fi')
    if is_rm:
        _send_cmd(com, 'rm /data/tombstones/* 1>/dev/null 2>&1')


def copy_bluedroid(com, file_dir, is_rm=True):
    _send_cmd(com, 'cp -r /data/misc/bluedroid ' + file_dir + ' 1>/dev/null 2>&1')
    # 不能删除该文件夹下文件
    # if is_rm:
    #     _send_cmd(com, 'rm /data/misc/bluedroid/* 1>/dev/null 2>&1 ')


def copy_bluetooth(com, file_dir, is_rm=True):
    _send_cmd(com, 'cp -r /data/misc/bluetooth ' + file_dir + ' 1>/dev/null 2>&1')
    # 不能删除该文件夹下文件
    # if is_rm:
    #     _send_cmd(com, 'rm /data/misc/bluetooth/* 1>/dev/null 2>&1 ')


def get_platform(com):
    return _send_cmd_get_result(com, 'getprop ro.product.model')


def send_voice_cmd(com, cmd, voice_package: str = 'com.konka.SmartControl'):
    if voice_package == 'com.konka.SmartControl':
        prev = 'am startservice -a konka.intent.action.speech.TEXT_TO_NLP --es konka.speech.intent.extra.WORD '
        _send_cmd(com, prev + cmd)


def current_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()


def close_kernel_print(com, timeout=2):
    _send_cmd(com, 'echo 0 > /proc/sys/kernel/printk', timeout=timeout)


def check_tv_com(com) -> tuple:
    try:
        # 新增修改，兼容视频煲机避免无限su
        if _send_cmd(com, '\r' + chr(3) + '\r ', timeout=3):
            if _check_su(com):
                _send_cmd(com, '\rsu\r')
                close_kernel_print(com)
            return True, 'pass'
        return False, '电视串口{!r}连接超时:'.format(com)
    except Exception as e:
        logging.exception(e)
        return False, '串口{!r}被占用'.format(com)


def check_mcu_com(com) -> tuple:
    if kkserial.KKSerialFactory.is_ch340_com_exist(com):
        return True, 'pass'
    return False, '找不到单片机端口{!r}'.format(com)


def _check_net():
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


def check_net(com) -> tuple:
    pc_ip = current_ip()
    tv_ip = get_tv_ip(com)
    if not _check_net():
        return False, '电脑网络不可以用{!r}'.format(pc_ip)
    if pc_ip.count('.') != 3:
        return False, '获取电脑IP异常:{!r}'.format(pc_ip)
    if tv_ip.count('.') != 3:
        return False, '获取电视IP异常:{!r}'.format(tv_ip)
    if pc_ip.rsplit('.', 1)[0] != tv_ip.rsplit('.', 1)[0]:
        return False, '电脑({!r})和电视({!r})不在同一网段'.format(pc_ip, tv_ip)
    return True, 'pass'


def check_monkey_tools(com):
    if 'com.konka.monkey' in _send_cmd_get_result(com, 'pm list packages'):
        if _send_cmd_get_result(com, 'ls /data/misc/konka |grep "^monkey.jar$"'):
            return True, 'pass'
        return False, '/data/misc/konka/monkey.jar 不存在，请自行执行一次MonkeyTool'
    return False, f'{com} 未安装MonkeyTools'


def _check_su(com):
    cur_sh_count = _send_cmd_get_result(com, "ps -p $$|busybox awk -F\" \" 'NR==2{print $3}' 2>/dev/null")
    logging.debug('_check_su: cur_shell start by pid:{}.'.format(cur_sh_count))
    if parse_str2int(cur_sh_count) == 1:
        return True
    return False


def _check_logd(com):
    pid_msg = _send_cmd_get_result(com, "ps -A|grep logd")
    logging.debug('_check_logd: pid_msg is {}.'.format(pid_msg))
    if pid_msg:
        return True
    return False


def init_tv_env(com, wifi: bool = False):
    _send_cmd(com, '\r' + chr(3) + '\r', timeout=10)
    if _check_su(com):
        _send_cmd(com, '\rsu\r')
    # if not _check_logd(com):
    _send_cmd(com, 'start logd\rlogcat -G 6M\r')
    if wifi:
        _send_cmd(com, 'a="";while [ "$a" != "OK" ] ; do sleep 0.5;a=`wpa_cli -iwlan0 log_level debug`;'
                       ' done;echo "wifi_cli debug start done" > /dev/console')


def check_env(tv_com, mcu_com='', monkey_tools=False) -> tuple:
    tv_com = tv_com.strip()
    mcu_com = mcu_com.strip()
    if tv_com:
        ret, info = check_tv_com(tv_com)
        if not ret:
            return False, info
    if monkey_tools:
        ret, info = check_monkey_tools(tv_com)
        if not ret:
            shellcmd.close_kk_serial(tv_com)
            return False, info
    if mcu_com:
        ret, info = check_mcu_com(mcu_com)
        if not ret:
            shellcmd.close_kk_serial(tv_com)
            return False, info
    ret, info = check_net(tv_com)
    if not ret:
        shellcmd.close_kk_serial(tv_com)
        return False, info
    return True, 'pass'


def _get_window_package(window: str):
    return window.split('/', 1)[0]


def is_window_shown(com: str, window: str) -> bool:
    logging.debug(f'is_window shown ? {window}')
    windows_str = _send_cmd_get_result(com, 'dumpsys window |grep -A 9 "Window #.*}:"')
    for line in windows_str.split('Window #'):
        logging.debug(f'Window info : \n{line}')
        if _get_window_package(window) in line:
            if 'shown=true' in line:
                logging.debug('window is shown')
                return True
    return False


def replace_ad(com, ad_root, index):
    cmd = 'du -a ' + ad_root + ' 2>/dev/null | grep "\.ts$" | busybox wc -l 2>/dev/null'
    count = _send_cmd_get_result(com, cmd)
    count = int(count)
    logging.debug(f'ad count:\n{count}')
    if count <= 0:
        logging.warning('not found ad source')
        return
    index = index % count
    cmd = 'du -a ' + ad_root + ' 2>/dev/null | grep "\.ts$" | busybox awk \'NR==' + str(index) + '{print $2}\''
    ad_file = _send_cmd_get_result(com, cmd)
    logging.warning(f'selected ad : {ad_file}')
    cmd = 'cp ' + ad_file + ' /data/misc/konka/AdBoot/AdBootMedia/bootvideo.mp4'
    _send_cmd(com, cmd)
    cmd = 'chmod 777 /data/misc/konka/AdBoot/AdBootMedia/bootvideo.mp4'
    _send_cmd(com, cmd)


def parse_str2int(string):
    try:
        return int(string)
    except:
        logging.warning(f'parse_str2int , string : {string}')
        return 0


def is_any_usb_mounted(com, return_device: bool=False):
    device = None
    second_ds = _send_cmd_get_result(com, 'ls /mnt |grep "^sd.[0-9]$"  2>/dev/null').split('\r\n')[0].strip()
    third_ds = _send_cmd_get_result(com, 'ls /mnt/usb |grep "^sd.[0-9]$"  2>/dev/null').split('\r\n')[0].strip()
    model = _send_cmd_get_result(com, 'getprop ro.product.model')
    if model == 'Konka Android TV 838':
        disk = _send_cmd_get_result(com, 'ls /mnt/usb | busybox awk \'NR==1{print $0}\' 2>$null')
        if disk:
            device = '/mnt/usb/' + disk
    elif second_ds and _send_cmd_get_result(com, 'ls /mnt/' + second_ds + ' 2>/dev/null'):
        device = '/mnt/' + second_ds
    elif third_ds and _send_cmd_get_result(com, 'ls /mnt/usb/' + third_ds + ' 2>/dev/null'):
        device = '/mnt/usb/' + third_ds
    elif _send_cmd_get_result(com, 'getprop|grep "mstar"'):
        if _send_cmd_get_result(com, 'ls /mnt/sdcard'):
            device = '/mnt/sdcard'
    if device is None:
        logging.debug(f'not found usb device')
    else:
        logging.debug(f'found usb device : {device}')
    if return_device:
        return device
    return device is not None


def is_usb_mounted(com, usb_count=1):
    count = 0
    model = _send_cmd_get_result(com, 'getprop ro.product.model')
    if model == 'Konka Android TV 838':
        count = parse_str2int(_send_cmd_get_result(com, 'ls /mnt/usb | busybox wc -l 2>$null'))
    elif _send_cmd_get_result(com,  'getprop|grep "mstar"'):
        count = count + 1 if _send_cmd_get_result(com,  'ls /mnt/sdcard') else count
        count += parse_str2int(_send_cmd_get_result(com, 'ls /mnt/usb/ |grep "^sd.1$" | busybox wc -l  2>/dev/null'))
    else:
        count += parse_str2int(_send_cmd_get_result(com, 'ls /mnt/usb/ |grep "^sd.[0-9]$" | busybox wc -l  2>/dev/null'))
        count += parse_str2int(_send_cmd_get_result(com, 'ls /mnt/ |grep "^sd.[0-9]$" | busybox wc -l  2>/dev/null'))
    logging.debug(f'found usb device count : {count}, expect : {usb_count}')
    return count >= usb_count


def check_usb(com) -> tuple:
    if is_any_usb_mounted(com):
        return True, 'pass'
    return False, '未发现任何U盘设备'


def check_bt_ct(com) -> tuple:
    if bt_ct_state(com):
        return True, 'pass'
    return False, '未发现已连接的蓝牙遥控器'


def check_bt_a2dp(com) -> tuple:
    if bt_a2dp_state(com):
        return True, 'pass'
    return False, '未发现已连接的蓝牙音箱'


def _send_keyevent_chain(com, chain, wait=0):
    for i in chain:
        _send_cmd(com, 'input keyevent ' + str(i))
        time.sleep(wait)


def _set_channel(com, channel: str):
    # prev = [21, 21, 21, 21, 21]
    prev = ['21 21 21 21 21 21']
    key_set = {
        DTMB: [[19, 21, 21], prev],
        ATV: [[19, 21, 21, 22], prev + [22] * 1],
        AV: [[19, 22, 22], prev + [22] * 2],
        HDMI1: [[20, 21, 21], prev + [22] * 3],
        HDMI2: [[20, 21, 21, 22], prev + [22] * 4],
        HDMI3: [[20, 22, 22], prev + [22] * 5],
    }
    if channel not in key_set.keys():
        raise ValueError(f'illegal channel : {channel}')
    if 'versionName=2.' in _send_cmd_get_result(
            com, 'dumpsys package com.konka.tvsettings|grep versionName|busybox awk \'NR==1{print $0}\''):
        _send_keyevent_chain(com, key_set[channel][1])
    else:
        _send_keyevent_chain(com, key_set[channel][0])


def set_channel(com, channel: str):
    logging.debug('set channel : {}'.format(channel))
    _send_cmd(com, 'am broadcast -a com.konka.GO_TO_TV')
    time.sleep(3)
    _send_cmd(com, 'am broadcast -a com.konka.tvsettings.action.GO_TO_SOURCEPAGE')
    _set_channel(com, channel)
    _send_keyevent_chain(com, [66])


def shot(com, save_path: str, is_tv_source=False):
    if not save_path.startswith('/'):
        raise ValueError('save_path is not a relative path')
    if is_tv_source:
        _send_cmd(com, 'am broadcast -a com.konka.GO_TO_TV')
        time.sleep(2)
    _send_cmd(com, 'screencap -p ' + save_path)


def close_voice_window(com, package='com.konka.SmartControl'):
    logging.debug('ensure close athena window')
    cmd = 'while true;do is_show=`dumpsys window |grep -A9 "Window #.*' + package + '}:" |grep "shown=true"`;if [ "$is_show" ];' \
          'then echo "athena showed";sendevent /dev/input/event0 1 158 1;sendevent /dev/input/event0 0 0 0;' \
          'sendevent /dev/input/event0 1 158 0;sendevent /dev/input/event0 0 0 0; else break;fi;sleep 0.5;done'
    _send_cmd(com, cmd)


def is_voice_window_show(com, timeout=3, need_close=True, package='com.konka.SmartControl'):
    if need_close:
        cmd = 'start_t=`busybox awk \'{print $1}\' /proc/uptime`;flag=1;while ((flag));do is_show=`dumpsys window |' \
              'grep -A9 "Window #.*' + package + '}:" |grep "shown=true"`;if [ "$is_show" ];then echo "athena showed";' \
              'sendevent /dev/input/event0 1 158 1;sendevent /dev/input/event0 0 0 0;' \
              'sendevent /dev/input/event0 1 158 0;sendevent /dev/input/event0 0 0 0;break; ' \
              'else let i++;fi;end_t=`busybox awk \'{print $1}\' /proc/uptime`;flag=`busybox awk \'' \
              'BEGIN{if(\'$end_t\'-\'$start_t\'>=' + str(timeout) + '){print 0}else{print 1}}\'`;sleep 0.1;done'
    else:
        cmd = 'start_t=`busybox awk \'{print $1}\' /proc/uptime`;flag=1;while ((flag));do is_show=`dumpsys window |' \
              'grep -A9 "Window #.*' + package + '}:" |grep "shown=true"`;if [ "$is_show" ];then echo "athena showed";break; ' \
              'else let i++;fi;end_t=`busybox awk \'{print $1}\' /proc/uptime`;flag=`busybox awk \'' \
              'BEGIN{if(\'$end_t\'-\'$start_t\'>=' + str(timeout) + '){print 0}else{print 1}}\'`;sleep 0.1;done'
    if _send_cmd_get_result(com, cmd) == 'athena showed':
        logging.debug('athena window shown')
        return True
    else:
        logging.debug('athena window not shown')
        # some exceptions may occur in this instruction
        _timeout_recovery(com)
        return False


def load_media_dir(com, root):
    cmd = 'am start -n com.konka.multimedia/com.konka.multimedia.view.fileexplorer.BrowseActivity ' \
          '-e DISK_PATH "' + root + '"'
    _send_cmd(com, cmd)


def play_video(com, root, index, wait=0):
    cmd = 'am start -n com.konka.multimedia/com.konka.multimedia.view.movie.VideoPlayerActivity ' \
          '-a com.konka.multimedia.action.PLAY_MOVIE -e browse_directory_path "' + root + '" --ei index ' + str(index)
    _send_cmd(com, cmd)
    time.sleep(wait)


def play_music(com, root, index, wait=0):
    cmd = 'am start -n com.konka.multimedia/com.konka.multimedia.view.music.MusicActivity ' \
          '-a com.konka.multimedia.action.PLAY_MUSIC -e browse_directory_path "' + root + '" --ei index ' + str(index)
    _send_cmd(com, cmd)
    time.sleep(wait)


def play_image(com, root, index, wait=0):
    cmd = 'am start -n com.konka.multimedia/com.konka.multimedia.view.photo.PhotoPlayerActivity ' \
          '-a com.konka.multimedia.action.PLAY_IMAGE -e browse_directory_path "' + root + '" --ei index ' + str(index)
    _send_cmd(com, cmd)
    time.sleep(wait)


def file_count(com, root: str) -> str:
    return _send_cmd_get_result(com, 'ls ' + root + ' 2>/dev/null | busybox wc -l  2>/dev/null')


def play_all(com, root, wait=30):
    n = parse_str2int(file_count(com, root))
    for i in range(n):
        cmd = 'ls ' + root + ' | busybox awk \'NR==' + str(i + 1) + '{print $0}\''
        video_name = _send_cmd_get_result(com, cmd)
        logging.debug(f'play video : {video_name}')
        play_video(com, root, i, wait)


def set_eth(com, state: bool):
    _send_cmd(com, 'busybox ifconfig eth0 ' + 'up' if state else 'down')


def set_wlan(com, state: bool):
    _send_cmd(com, 'busybox ifconfig wlan0 ' + 'up' if state else 'down')


def set_wifi(com, state: bool):
    _send_cmd(com, 'svc wifi ' + 'enable' if state else 'disable')


def am_start(com, cmp: str) -> bool:
    return _send_cmd(com, 'am start -n ' + cmp, timeout=5)


def input_android_key(com, key_code: int) -> bool:
    return _send_cmd(com, 'input keyevent ' + str(key_code), timeout=5)


def get_wm_size(com) -> tuple:
    result = _send_cmd_get_result(com, 'wm size |busybox awk \'{print $3}\'')
    result = result.split('x', 1)
    return result[0], result[-1]


def close_multi_media_dialog(com):
    cmd = 'dumpsys window |grep -A 9 "Window #.*PopupWindow.*}:"'
    result = _send_cmd_get_result(com, cmd)
    if result:
        for line in result.split('\r\n'):
            if 'shown=true' in line and str(get_wm_size(com)[0]) + '.0' in line:
                input_android_key(com, 66)


def tv_datetime(com) -> str:
    return _send_cmd_get_result(com, 'date +"%Y-%m-%d %H:%M:%S"')


def dump_mem_info(com):
    info = _send_cmd_get_result(com, 'dumpsys -t 40 meminfo')
    info = info.lower()
    default_val = '-1'
    mem = {
        'total ram'.lower(): default_val,
        'free ram'.lower(): default_val,
        'used ram'.lower(): default_val,
    }
    for line in info.split('\r\n'):
        line = line.strip()
        logging.warning(f'line : {line}')
        for key in mem.keys():
            if line.startswith(key):
                logging.warning(f'found : {key}')
                line = line.replace(',', '').replace('k', '').replace('K', '').replace('B', '')
                try:
                    mem[key] = re.split(r'\s+', line)[2]
                except:
                    logging.warning(f'mem key : {key}, get line {line} fail')
    logging.warning(f'mem {mem}')
    return mem


def bt_ct_state_old(com, mac):
    lines = _send_cmd_get_result(com, 'dumpsys bluetooth_manager')
    return mac + ' : 2' in lines


def bt_ct_state(com):
    lines = _send_cmd_get_result(com, 'dumpsys bluetooth_manager').replace('\r', '')
    if re.search("(\w{2}:){5}\w{2} : 2", lines):
        return True
    else:
        return False


def bt_a2dp_state(com):
    lines = _send_cmd_get_result(com, 'dumpsys bluetooth_manager')
    lines = lines.split('\r\n')
    start, is_this_a2dp = False, False
    for line in lines:
        if 'Profile: A2dpService' in line:
            start = True
        if not is_this_a2dp and re.search("mCurrentDevice: (\w{2}:){5}\w{2}", line): #810 android 8
            is_this_a2dp = True
        if not is_this_a2dp and re.search("mActiveDevice: (\w{2}:){5}\w{2}", line): #560 android 9
            is_this_a2dp = True
        if start and is_this_a2dp and 'curState=' in line:
            return 'curState=Connected' in line
    return False


def bt_a2dp_state_old(com, mac):
    lines = _send_cmd_get_result(com, 'dumpsys bluetooth_manager')
    lines = lines.split('\r\n')
    start, is_this_a2dp = False, False
    for line in lines:
        if 'Profile: A2dpService' in line:
            start = True
        if not is_this_a2dp and 'mCurrentDevice: ' + mac: #810 android 8
            is_this_a2dp = True
        if not is_this_a2dp and 'mActiveDevice: ' + mac: #560 android 9
            is_this_a2dp = True
        if start and is_this_a2dp and 'curState=' in line:
            return 'curState=Connected' in line
    return False


def get_bt_ct_mac(com):
    lines = _send_cmd_get_result(com, 'dumpsys bluetooth_manager')
    lines = lines.split('\r\n')
    start = False
    for line in lines:
        if 'mInputDevices:' in line:
            start = True
            continue
        if start:
            return line.strip().rsplit(':', 1)[0].strip()
    return ''


def get_a2dp_mac(com):
    lines = _send_cmd_get_result(com, 'dumpsys bluetooth_manager')
    lines = lines.split('\r\n')
    for line in lines:
        if 'mCurrentDevice: ' or 'mActiveDevice: ' in line:
            ret = line.strip().split(':', 1)[-1].strip()
            return '' if ret == 'null' else ret
    return ''


def install_apks(com, apk_dir):
    cmd = 'du -a ' + apk_dir + ' 2>/dev/null | grep ".*apk$" |busybox awk \'{print $NF}\''
    files = _send_cmd_get_result(com, cmd).split('\r\n')
    for file in files:
        _send_cmd(com, 'pm install -r ' + file)


def third_apks(com) -> list:
    return _send_cmd_get_result(com, 'pm list packages -3 |busybox awk -F ":" \'{print $2}\'').split('\r\n')


def go_home(com):
    for _ in range(3):
        _send_cmd(com, 'input keyevent 4')
        time.sleep(0.5)
        if 'com.konka.livelauncher' in _send_cmd_get_result(com, 'dumpsys window|grep mFocusedWindow'):
            return
    _send_cmd(com, 'input keyevent 3')
    time.sleep(3)


# 通过uiautomator1.0的方式去检测是否已打开ai识别开关，没有的话就先打开，然后进入人脸识别界面
# uiautomator1.0可能会不稳定或者平台不支持，如需更稳定的方式可以用uiautomator2.0去检测
def start_ai(com, wait=25, key_wait=3):
    ui_xml = '/data/local/tmp/ai.xml'
    am_start(com, 'com.konka.aiserver/com.konka.view.AiSetActivity')
    time.sleep(5)
    _send_cmd(com, 'uiautomator dump ' + ui_xml)
    cmd = 'busybox sed \'s/<node/\\n/g\' ' + ui_xml + ' 2>/dev/null | ' \
          'grep "resource-id=\\"com.konka.aiserver:id/ai_set_register\\"" |grep "focusable=\\"true\\""'
    if not _send_cmd_get_result(com, cmd):
        input_android_key(com, 66)
        time.sleep(wait)
    #循环三次 检测摄像头人脸识别是否已经打开
    for i in range(3):
        _send_cmd(com, 'uiautomator dump ' + ui_xml)
        time.sleep(1)
        cmd = 'busybox sed \'s/<node/\\n/g\' ' + ui_xml + ' 2>/dev/null | ' \
            'grep "resource-id=\\"com.konka.aiserver:id/ai_set_register\\"" |grep "focusable=\\"true\\""'
        if not _send_cmd_get_result(com, cmd):
            input_android_key(com, 66)
            time.sleep(3)
        else:
            break
    _send_keyevent_chain(com, [20, 66, 66], key_wait)


