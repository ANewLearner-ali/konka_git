from time import sleep

from serial import SerialException

from utils.kkserial import KKSerialFactory
from utils.shellcmd import send_cmd_get_result, send_cmd

if __name__ == '__main__':
    while True:
        com = input('请输入电视串口：')
        if com:
            if com.upper() not in KKSerialFactory.get_all_serial():
                print('请输入正确的串口!!!')
                continue
            try:
                send_cmd(com, '')
            except SerialException as e:
                print('串口串口被占用，请先排查坏境后，重新输入')
                continue
        out_duration_count = input('请输入重启的次数：')
        if out_duration_count:
            try:
                out_duration_count = int(out_duration_count)
            except Exception as e:
                print('Exception: ' + str(e))
                print('请输入合法的数值，请勿在输入次数时输入非数字的按键')
                continue
        in_duration_count = input('请输入单次开机脚本的执行次数：')
        if in_duration_count:
            try:
                in_duration_count = int(in_duration_count)
            except Exception as e:
                print('Exception: ' + str(e))
                print('请输入合法的数值，请勿在输入次数时输入非数字的按键')
                continue
        break
    count = 0
    while count < out_duration_count:
        try:
            print('第' + str(count) + '次开始执行')
            send_cmd(com, '\rsu\r')
            send_cmd(com, 'sh /data/test-相机录制视频.sh ' + str(in_duration_count) + ' &')
            sleep(45)
            while True:
                # 持续检查是否执行完成
                result = send_cmd_get_result(com, 'cat /data/testDir/state_file.txt')
                if result and result == '1':
                    break
                sleep(3)
            count += 1
            send_cmd(com, 'reboot')
            sleep(90)
            print('第' + str(count-1) + '次执行完成，准备下一次执行')
        except SerialException:
            print('串口异常，请重新执行')
            break

