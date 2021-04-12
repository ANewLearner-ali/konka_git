import enum
import logging
import time
import threading
from utils.kkserial import KKSerialFactory
from utils import shellcmd

# 模式
MODE_ONCE = 0
MODE_LONG_PRESS = 1
MODE_KEEP = 2

# 释放按键键值
RELEASE_IR = 0X5F
RELEASE_KEY = 0XFF

# AC操作
# C AC_ON 发送的是1 高电平 继电器是连接 COM - NC 两个线的（常态就是常连的），帽连接低，表示低电平有效
# C AC_OFF 发送的是0 低电平 继电器进入工作状态，将电源断路

AC_ON = 16
AC_OFF = 17 # C 发送的是 0 低电平


class Key(enum.Enum):
    def __init__(self, code: int, cn_name: str):
        self._code = code
        self._cn_name = cn_name

    @property
    def code(self):
        return self._code

    @property
    def cn_name(self):
        return self._cn_name

    # 第一排继电器按键对应
    BLUE_POWER = 0, '蓝牙电源键'
    BLUE_UP = 1, '蓝牙上键'
    BLUE_DOWN = 2, '蓝牙下键'
    BLUE_LEFT = 3, '蓝牙左键'
    BLUE_RIGHT = 4, '蓝牙右键'
    BLUE_ENTER = 5, '蓝牙确认键'
    BLUE_HOME = 6, '蓝牙主页键'
    BLUE_VOICE = 7, '蓝牙语音键'

    # 第二排继电器
    BLUE_BACK = 8, '蓝牙返回键'
    BLUE_VOLUME_UP = 9, '蓝牙音量加键'
    BLUE_VOLUME_DOWN = 10, '蓝牙音量减键'
    BLUE_SOURCE = 11, '蓝牙信源键'
    BLUE_MENU = 12, '蓝牙菜单键'
    BLUE_CHANNEL_UP = 13, '蓝牙频道加键'
    BLUE_CHANNEL_DOWN = 14, '蓝牙频道减键'
    BLUE_MORE = 15, '蓝牙更多键'

    # AC
    KEY_AC_ON = AC_ON, 'AC_ON'
    KEY_AC_OFF = AC_OFF, 'AC_OFF'

    # 红外键值
    # 数字键
    IR_NUMBER_0 = 0X00, '红外数字0键'
    IR_NUMBER_1 = 0X01, '红外数字1键'
    IR_NUMBER_2 = 0X02, '红外数字2键'
    IR_NUMBER_3 = 0X03, '红外数字3键'
    IR_NUMBER_4 = 0X04, '红外数字4键'
    IR_NUMBER_5 = 0X05, '红外数字5键'
    IR_NUMBER_6 = 0X06, '红外数字6键'
    IR_NUMBER_7 = 0X07, '红外数字7键'
    IR_NUMBER_8 = 0X08, '红外数字8键'
    IR_NUMBER_9 = 0X09, '红外数字9键'

    IR_INPUT_METHOD = 0X0A, '红外输入法键'
    IR_POWER = 0X0B, '红外电源键'

    IR_CHANNEL_DOWN = 0X10, '红外频道减键'
    IR_CHANNEL_UP = 0X11, '红外频道加键'
    IR_VOLUME_DOWN = 0X12, '红外音量减键'
    IR_VOLUME_UP = 0X13, '红外音量加键'
    IR_MUTE = 0X14, '红外静音键'
    IR_MENU = 0X15, '红外菜单键'
    IR_SOURCE = 0X1C, '红外信源键'

    # 五维键
    IR_UP = 0X2B, '红外上键'
    IR_DOWN = 0X2C, '红外下键'
    IR_LEFT = 0X2D, '红外左键'
    IR_RIGHT = 0X2E, '红外右键'
    IR_ENTER = 0X2F, '红外确认键'

    IR_BACK = 0X30, '红外返回键'
    IR_HOME = 0X38, '红外主页键'
    IR_DELETE = 0X3A, '红外删除键'
    IR_MORE = 0X62, '红外更多键'
    IR_ONLINE = 0X0F, '红外直播键'
    IR_MOVIE = 0X1B, '红外电影键'
    IR_FAVORITE = 0X20, '红外喜爱键'

    # Android键值
    ANDROID_NUMBER_0 = 7, '安卓数字0键'
    ANDROID_NUMBER_1 = 8, '安卓数字1键'
    ANDROID_NUMBER_2 = 9, '安卓数字2键'
    ANDROID_NUMBER_3 = 10, '安卓数字3键'
    ANDROID_NUMBER_4 = 11, '安卓数字4键'
    ANDROID_NUMBER_5 = 12, '安卓数字5键'
    ANDROID_NUMBER_6 = 13, '安卓数字6键'
    ANDROID_NUMBER_7 = 14, '安卓数字7键'
    ANDROID_NUMBER_8 = 15, '安卓数字8键'
    ANDROID_NUMBER_9 = 16, '安卓数字9键'

    SERIAL_INPUT_METHOD = 165, '安卓输入法键'
    ANDROID_POWER = 26, '安卓电源键'

    ANDROID_CHANNEL_DOWN = 167, '安卓频道减键'
    ANDROID_CHANNEL_UP = 166, '安卓频道加键'
    ANDROID_VOLUME_DOWN = 25, '安卓音量减键'
    ANDROID_VOLUME_UP = 24, '安卓音量加键'
    ANDROID_MUTE = 164, '安卓静音键'
    ANDROID_MENU = 82, '安卓菜单键'
    ANDROID_SOURCE = 178, '安卓信源键'

    # 五维键
    ANDROID_UP = 19, '安卓上键'
    ANDROID_DOWN = 20, '安卓下键'
    ANDROID_LEFT = 21, '安卓左键'
    ANDROID_RIGHT = 22, '安卓右键'
    ANDROID_ENTER = 66, '安卓确认键'

    ANDROID_BACK = 4, '安卓返回键'
    ANDROID_HOME = 3, '安卓主页键'
    ANDROID_DELETE = 67, '安卓删除键'
    ANDROID_MORE = 1045, '安卓更多键'
    ANDROID_ONLINE = 1100, '安卓直播键'
    ANDROID_MOVIE = 1101, '安卓影视键'
    ANDROID_FAVORITE = 1102, '安卓喜爱键'


# 继电器按键文本
BLUE_KEY_TEXTS = ['电源', '上', '下', '左', '右', '确认', '主页', '语音',
                  '返回', '音量加', '音量减', '信源', '菜单', '频道加', '频道减', '更多']
BLUE_KEY_OBJ = [
    Key.BLUE_POWER,
    Key.BLUE_UP,
    Key.BLUE_DOWN,
    Key.BLUE_LEFT,
    Key.BLUE_RIGHT,
    Key.BLUE_ENTER,
    Key.BLUE_HOME,
    Key.BLUE_VOICE,
    Key.BLUE_BACK,
    Key.BLUE_VOLUME_UP,
    Key.BLUE_VOLUME_DOWN,
    Key.BLUE_SOURCE,
    Key.BLUE_MENU,
    Key.BLUE_CHANNEL_UP,
    Key.BLUE_CHANNEL_DOWN,
    Key.BLUE_MORE,
]

IR_KEY_TEXTS = ['up', 'down', 'left', 'right', 'ok', 'volume_up', 'volume_down', 'channel_up',
                'channel_down', 'back', 'home', 'more', 'source', 'power', 'menu']
IR_KEY_OBJ = [
    Key.IR_UP,
    Key.IR_DOWN,
    Key.IR_LEFT,
    Key.IR_RIGHT,
    Key.IR_ENTER,
    Key.IR_VOLUME_UP,
    Key.IR_VOLUME_DOWN,
    Key.IR_CHANNEL_UP,
    Key.IR_CHANNEL_DOWN,
    Key.IR_BACK,
    Key.IR_HOME,
    Key.IR_MORE,
    Key.IR_SOURCE,
    Key.IR_POWER,
    Key.IR_MENU
]


def find_key_by_text(text) -> Key:
    if text in BLUE_KEY_TEXTS:
        return BLUE_KEY_OBJ[BLUE_KEY_TEXTS.index(text)]


def find_blue_key_by_index(index) -> Key:
    if 0 <= index < 16:
        return BLUE_KEY_OBJ[index]


def find_ir_key_by_text(text) -> Key:
    if text in IR_KEY_TEXTS:
        return IR_KEY_OBJ[IR_KEY_TEXTS.index(text)]


def press_blue(key: Key, com=None, mode=MODE_ONCE) -> bool:
    logging.debug('mcu {} send blue key: {}'.format(com, key.cn_name))
    if com is None:
        com = KKSerialFactory.get_ch340_com()
    if com:
        code = key.code
        if key.code < 0 or key.code > 17:
            code = -1
        muc = KKSerialFactory.get_kk_serial(com, baudrate=9600)
        muc.write(chr(ord('d') + code))
        if mode == MODE_ONCE:
            muc.write(chr(RELEASE_KEY))
        elif mode == MODE_LONG_PRESS:
            time.sleep(0.5)
            muc.write(chr(RELEASE_KEY))
        KKSerialFactory.close_kk_serial(com)
        return True
    return False


def press_blue_long(key: Key, com=None, wait=0.5, mode=MODE_ONCE) -> bool:
    logging.debug('mcu {} send blue key: {}'.format(com, key.cn_name))
    if com is None:
        com = KKSerialFactory.get_ch340_com()
    if com:
        code = key.code
        if key.code < 0 or key.code > 17:
            code = -1
        muc = KKSerialFactory.get_kk_serial(com, baudrate=9600)
        muc.write(chr(ord('d') + code))
        if mode == MODE_ONCE:
            muc.write(chr(RELEASE_KEY))
        elif mode == MODE_LONG_PRESS:
            time.sleep(wait)
            muc.write(chr(RELEASE_KEY))
        KKSerialFactory.close_kk_serial(com)
        return True
    return False

def release_blue(com=None) -> bool:
    logging.debug('mcu {} release blue')
    if com is None:
        com = KKSerialFactory.get_ch340_com()
    if com:
        muc = KKSerialFactory.get_kk_serial(com, baudrate=9600)
        muc.write(chr(RELEASE_KEY))
        KKSerialFactory.close_kk_serial(com)
        return True
    return False


def press_ir(key: Key, com=None, interval=0.3, mode=MODE_ONCE) -> bool:
    logging.debug('mcu {} send ir key: {}'.format(com, key.cn_name))
    if com is None:
        com = KKSerialFactory.get_ch340_com()
    if com:
        muc = KKSerialFactory.get_kk_serial(com, baudrate=9600)
        muc.write(chr(key.code))
        time.sleep(interval)
        if mode == MODE_ONCE:
            muc.write(chr(RELEASE_IR))
        elif mode == MODE_LONG_PRESS:
            time.sleep(1)
            muc.write(chr(RELEASE_IR))
        KKSerialFactory.close_kk_serial(com)
        return True
    return False


def release_ir(com=None) -> bool:
    logging.debug('mcu {} release ir')
    if com is None:
        com = KKSerialFactory.get_ch340_com()
    if com:
        muc = KKSerialFactory.get_kk_serial(com, baudrate=9600)
        muc.write(chr(RELEASE_IR))
        KKSerialFactory.close_kk_serial(com)
        return True
    return False


def press_android(key, com, long_press=MODE_ONCE) -> bool:
    logging.debug('tv serial {} send key: {}'.format(com, key.cn_name))
    if isinstance(key, Key):
        code = str(key.code)
    elif isinstance(key, str):
        code = key
    elif isinstance(key, int) and int(key) > 0:
        code = str(key)
    else:
        return False
    cmd = 'input keyevent --longpress ' + code if long_press else 'input keyevent ' + code
    shellcmd.send_cmd(com, cmd)
    return True


def ac_on(com=None) -> bool:
    logging.debug('mcu {} send ac_on'.format(com))
    return press_blue(Key.KEY_AC_ON, com, mode=MODE_KEEP)


def ac_off(com=None) -> bool:
    logging.debug('mcu {} send ac_off'.format(com))
    return press_blue(Key.KEY_AC_OFF, com, mode=MODE_KEEP)


def find_enum_by_tuple(t: tuple) -> Key:
    if len(t) == 2:
        for key, value in Key.__members__.items():
            if t == value.value:
                return value


class MicroControllerUnit:
    """
    for thread sync
    """
    def __init__(self, mcu_com: str):
        self.com = mcu_com
        self.lock = threading.RLock()

    def press_blue(self, key: Key, mode=MODE_ONCE) -> bool:
        self.lock.acquire()
        ret = press_blue(key=key, com=self.com, mode=mode)
        self.lock.release()
        return ret

    def release_blue(self) -> bool:
        self.lock.acquire()
        ret = release_blue(com=self.com)
        self.lock.release()
        return ret

    def press_ir(self, key: Key, interval=0.3, mode=MODE_ONCE) -> bool:
        self.lock.acquire()
        ret = press_ir(key=key, com=self.com, interval=interval, mode=mode)
        self.lock.release()
        return ret

    def release_ir(self) -> bool:
        self.lock.acquire()
        ret = release_ir(com=self.com)
        self.lock.release()
        return ret

    def ac_on(self) -> bool:
        self.lock.acquire()
        ret = ac_on(com=self.com)
        self.lock.release()
        return ret

    def ac_off(self) -> bool:
        self.lock.acquire()
        ret = ac_off(com=self.com)
        self.lock.release()
        return ret


class TVSerial:
    """
    for thread sync
    """
    def __init__(self, tv_com):
        self.com = tv_com
        self.lock = threading.RLock()

    def send_cmd(self, cmd, wait=0, is_clear_cache=True, timeout=None):
        self.lock.acquire()
        ret = shellcmd.send_cmd(com=self.com, cmd=cmd, wait=wait, is_clear_cache=is_clear_cache, timeout=timeout)
        self.lock.release()
        return ret

    def send_cmd_get_result(self, cmd, wait=0, is_clear_cache=True, timeout=None, is_strip=True):
        self.lock.acquire()
        ret = shellcmd.send_cmd_get_result(com=self.com, cmd=cmd, wait=wait, is_clear_cache=is_clear_cache,
                                           timeout=timeout, is_strip=is_strip)
        self.lock.release()
        return ret

