# 重复易投屏打开应用，查看其腾讯私有协议是否初始化成功。
import time

import sys

from serial import SerialException

from utils.kkserial import KKSerialFactory
from utils.shellcmd import send_cmd, send_cmd_get_result, close_kk_serial


def init_env(com):
    if int(send_cmd_get_result(com, 'ps -A|grep "S sh"|wc -l')) < 3:
        send_cmd(com, '\rsu\r')
    send_cmd(com, 'echo 0 > /proc/sys/kernel/printk')
    send_cmd(com, 'start logd;logcat -G 2M')


def aria_test(com, count, wait_time, usb):
    i = 0
    usb_aria_root = usb + '/aria_log'
    send_cmd(com, 'if [ ! -d "' + usb_root + '" ];then mkdir /data/aria_log;fi')
    while i < count:
        print('当前执行次数为: {}'.format(i))
        cur_date_stamp = str(int(time.time()))
        log_file = usb_aria_root + '/第' + str(i) + '次_' + cur_date_stamp + '.log'
        send_cmd(com, 'am start com.konka.kkmultiscreen/com.konka.throwingscreen.WelcomeActivity')
        pid = send_cmd_get_result(com, 'logcat -v time |grep `ps -A|grep com.konka.kkmultis'
                                       'creen|busybox awk -F" " \'{print $2}\'` > ' + log_file +' &')
        time.sleep(wait_time)
        send_cmd(com, 'busybox killall logcat')
        error_1 = send_cmd_get_result(com, 'cat ' + log_file + '|grep "java.lang.ClassCastException: android.os.BinderProxy cannot be cast to com.konka.kkmultiscreen.DataService"')
        error_2 = send_cmd_get_result(com, 'cat ' + log_file + '|grep "java.lang.RuntimeException: Unable to start'
                                           ' service com.konka.kkmultiscreen.tecentscreen.TencentService"')
        if error_1 or error_2:
            print('error_1: ', error_1)
            print('error_2: ', error_2)
            print('第{}次启动过程发现指定异常'.format(i))
        # else:
        #     send_cmd(com, 'rm -rf ' + log_file)
        send_cmd(com, 'am force-stop com.konka.kkmultiscreen')
        # send_cmd(com, 'logcat -c')
        time.sleep(5)
        i += 1


if __name__ == '__main__':
    while True:
        tv_com = input('请输入电视串口：')
        if tv_com:
            if tv_com.upper() not in KKSerialFactory.get_all_serial():
                print('请输入正确的串口!!!')
                continue
            try:
                send_cmd(tv_com, '')
            except SerialException as e:
                print('串口被占用，请先排查坏境后，新重输入')
                continue
        out_duration_count = input('请输入启动易投屏的次数：')
        if out_duration_count:
            try:
                out_duration_count = int(out_duration_count)
            except Exception as e:
                print('Exception: ' + str(e))
                print('请输入合法的数值，请勿在输入次数时输入非数字的按键')
                continue
        wait_time = input('请输入启动应用后的等待时长：')
        if wait_time:
            try:
                wait_time = int(wait_time)
            except Exception as e:
                print('Exception: ' + str(e))
                print('请输入合法的数值，请勿在输入次数时输入非数字的按键')
                continue
        usb_root = input('请输入日志保存路径：')
        if usb_root:
            try:
                file_num = int(send_cmd_get_result(tv_com, 'ls -l '+usb_root+'|wc -l'))
                if file_num <= 1:
                    print('请输入正确U盘路径')
                    continue
            except Exception as e:
                print('Exception: ' + str(e))
                print('请输入合法的数值，请勿在输入次数时输入非数字的按键')
                continue
        init_env(tv_com)
        aria_test(tv_com, out_duration_count, wait_time, usb_root)
        close_kk_serial(tv_com)
        import msvcrt
        print('按任意键退出...')
        msvcrt.getch()
        sys.exit()
