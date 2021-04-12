import json
import logging
import os


VERSION = 'V1.1.06-2021-3-3'


def make_dir(dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)


DEFAULT_CMP = '文件管理', 'com.konka.multimedia/com.konka.multimedia.view.MainActivity'


REPORTS_ROOT_TV_DIR_NAME = 'reliability'
REPORTS_ROOT_TV = '/data/misc/konka/reliability'
BASE_ROOT = os.path.dirname(__file__)
REPORTS_ROOT = os.path.join(BASE_ROOT, 'reports')
TEMPLATE_ROOT = os.path.join(BASE_ROOT, 'html')
SRC_ROOT = os.path.join(BASE_ROOT, 'src')
TMP_ROOT = os.path.join(BASE_ROOT, 'tmp')
WAKE_UP_MP3 = os.path.join(SRC_ROOT, 'wakeup.mp3')
SOCKET_JAR_PC = os.path.join(SRC_ROOT, 'kktestsocket.jar')
PIC_UTILS_JAR_PC = os.path.join(SRC_ROOT, 'picutils.jar')
VOICE_TMP_MP3 = os.path.join(SRC_ROOT, 'voice_tmp.mp3')
TURN_ON = os.path.join(SRC_ROOT, 'turn_on.mp3')
REPORT_RECORD_FILE = os.path.join(SRC_ROOT, 'report_record')
APPS_INFO = os.path.join(SRC_ROOT, 'apps')
MONKEY_DEFAULT = os.path.join(SRC_ROOT, 'monkey_default.json')
SCENE_FILE = os.path.join(SRC_ROOT, 'scene.json')
CONFIG_FILE = os.path.join(SRC_ROOT, 'config.json')
VIDEO_BRAND = os.path.join(SRC_ROOT, 'video_brand.json')
RECOVERY_SCRIPT = os.path.join(SRC_ROOT, 'open_serial.txt')
RESET_SCRIPT = os.path.join(SRC_ROOT, 'reset.txt')
RECORD_PATH = os.path.join(SRC_ROOT, 'kkrecord_path')
all_icon = os.path.join(SRC_ROOT, 'icon', 'app.ico')
QSS_DIR = os.path.join(SRC_ROOT, 'qss')
QSS_FILE = os.path.join(QSS_DIR, 'UI_Qss.qss')

make_dir(REPORTS_ROOT)
make_dir(SRC_ROOT)
make_dir(TMP_ROOT)
if not os.path.isfile(REPORT_RECORD_FILE):
    with open(REPORT_RECORD_FILE, 'w', encoding='utf-8') as f:
        f.write('[]')
if not os.path.isfile(SCENE_FILE):
    with open(SCENE_FILE, 'w', encoding='utf-8') as f:
        f.write('[]')
if not os.path.isfile(RECORD_PATH):
    open(RECORD_PATH, 'w', encoding='utf-8').close()


SECOND = 'second'
MINUTE = 'minute'
HOUR = 'hour'
UNIT = {
    HOUR: 60 * 60,
    MINUTE: 60,
    SECOND: 1
}


def get_second(ori, domain: str = '', key: str = ''):
    logging.debug(f'get_second  val:{ori} domain:{domain} key:{key}')
    if ori is not None:
        return ori
    with open(CONFIG_FILE, 'r', encoding='utf-8') as ff:
        d = json.loads(ff.read())
    value = d[domain][key]
    unit = value.get('unit', None)
    val = value.get('val', None)
    if unit is None or val is None:
        raise KeyError('config error, not found key {!r} or {!r}'.format('unit', 'val'))
    unit = UNIT[unit.lower()]
    return unit * val


def second2other(second, other_unit, bit=2):
    unit = UNIT[other_unit]
    return round(second / unit, bit)
