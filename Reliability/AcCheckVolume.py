import random
import time

import sys
from serial import SerialException

from utils.common import send_email
from utils.keycontrol import ac_off, ac_on
from utils.kkserial import KKSerialFactory
from utils.shellcmd import close_kk_serial, send_cmd_get_result, send_cmd
from utils.tv_utlils import check_tv_com


def test(com, count=1000, wait=90):
    res, mes = check_tv_com(com)
    send_cmd(com, 'file="/data/misc/konka/audio_log.txt";if [ ! -f "$file" ];then touch "$file"; fi')
    send_cmd(com, 'chmod 777 /data/misc/konka/audio_log.txt')
    if not res:
        print(mes)
    # 设置音量
    i = 0
    while i < count:
        volume = str(random.randrange(101))
        send_cmd(com, '\rsu\r')
        print('第{}次测试,开始设置音量为{}'.format(i, volume))
        if 'set volume to index='+volume not in send_cmd_get_result(com, 'media volume --stream 3 --set ' + volume):
            print('设置音量失败，请联系对应管理人员')
            send_email(['tengyuchen@konka.com', 'zhangqiao@konka.com'], 'AC断电音量检测脚本执行提示邮件', '设置音量失败，请检查权限')
            break
        if 'volume is '+volume in send_cmd_get_result(com, 'media volume --stream 3 --get'):
            print('音量设置成功，开始AC断电')
        send_cmd(com, 'echo "第{}次测试,开始设置音量为{}" >> /data/misc/konka/audio_log.txt'.format(i, volume))
        time.sleep(0.5)
        send_cmd(com, 'echo "重启前的audio_stream 日志:" >> /data/misc/konka/audio_log.txt')
        print('audio 信息是:')
        print(send_cmd_get_result(com, 'dumpsys audio | grep stream'))
        time.sleep(0.5)
        send_cmd(com, 'dumpsys audio | grep stream >> /data/misc/konka/audio_log.txt')
        time.sleep(1)
        ac_off()
        time.sleep(2)
        ac_on()
        time.sleep(wait)
        res, mes = check_tv_com(com)
        if not res:
            print(mes)
            print('异常处理中，断电重启')
            ac_on()
            time.sleep(wait)
            res, mes = check_tv_com(com)
            if not res:
                print(mes)
                print('连续2次串口不可以用，脚本中断')
                send_email(['tengyuchen@konka.com', 'zhangqiao@konka.com'], 'AC断电音量检测脚本执行提示邮件', 'AC断电后串口不可用，连续2次，请检查')
                break
        send_cmd(com, 'echo "重启后的audio_stream 日志:" >> /data/misc/konka/audio_log.txt')
        send_cmd(com, 'dumpsys audio | grep stream >> /data/misc/konka/audio_log.txt')
        send_cmd(com, 'echo "  " >> /data/misc/konka/audio_log.txt')
        if 'volume is '+volume in send_cmd_get_result(com, 'media volume --stream 3 --get '):
            print('音量检查成功')
            print('audio 信息是:')
            time.sleep(0.5)
            print(send_cmd_get_result(com, 'dumpsys audio | grep stream'))
        else:
            print('音量检查失败')
            print('audio 信息是:')
            time.sleep(0.5)
            print(send_cmd(com, 'dumpsys audio | grep stream'))
            time.sleep(0.5)
            send_email(['tengyuchen@konka.com', 'zhangqiao@konka.com'], 'AC断电音量检测脚本执行提示邮件', 'AC断电后音量检查失败，请现场确认')
            break
        i += 1
    if i == count:
        print('执行完成！！！')
        return True
    else:
        print('执行异常！！！')
        return False


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
                print('串口被占用，请先排查坏境后，重新输入')
                continue
        out_duration_count = input('请输入执行的次数：')
        if out_duration_count:
            try:
                out_duration_count = int(out_duration_count)
            except Exception as e:
                print('Exception: ' + str(e))
                print('请输入合法的数值，请勿在输入次数时输入非数字的按键')
                continue
        wait_time = input('请输入上电后的等待时长：')
        if wait_time:
            try:
                wait_time = int(wait_time)
            except Exception as e:
                print('Exception: ' + str(e))
                print('请输入合法的数值，请勿在输入次数时输入非数字的按键')
                continue
        test(tv_com, count=out_duration_count, wait=wait_time)
        close_kk_serial(tv_com)
        import msvcrt
        print('按任意键退出...')
        msvcrt.getch()
        sys.exit()
