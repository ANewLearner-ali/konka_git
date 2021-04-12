import enum
import time
import traceback
import pythoncom
import logging
from win32com.client import Dispatch
from utils import keycontrol


class PlayMode(enum.Enum):
    def __init__(self, code: int, cn_name: str):
        self._code = code
        self._cn_name = cn_name

    @property
    def code(self):
        return self._code

    @property
    def cn_name(self):
        return self._cn_name

    NEAR = 0, '近场播放'
    FAR = 1, '远场播放'
    NORMAL = 2, '直接播放'


def get_play_mode_by_code(code: int) -> PlayMode:
    for key, value in PlayMode.__members__.items():
        print(key, value)
        if value.code == code:
            return value


def play(file: str, mode: PlayMode, com=None):
    if mode == PlayMode.NEAR:
        _kk_play_voice(file=file, com=com, is_near=True)
    elif mode == PlayMode.FAR:
        _kk_play_voice(file=file, com=com, is_near=False)
    elif mode == PlayMode.NORMAL:
        play_normal(file)


def play_normal(file: str) -> bool:
    try:
        logging.debug('play voice : {}'.format(file))
        pythoncom.CoInitialize()
        wmp = Dispatch('WMPlayer.OCX')
        wmp.settings.autoStart = True
        wmp.settings.volume = 65
        wmp.URL = file  # auto-start
        while wmp.PlayState != 1:  # wait until stopped
            pythoncom.PumpWaitingMessages()
            time.sleep(0.1)
        wmp.URL = ""
        pythoncom.CoUninitialize()
        return True
    except Exception as e:
        logging.debug('play voice fail !!!')
        logging.debug(e)
        logging.warning(traceback.format_exc())
        return False


def _kk_play_voice(file, com=None, is_near=True, wait=1) -> bool:
    if is_near:
        if isinstance(com, str):
            keycontrol.press_blue(keycontrol.Key.BLUE_VOICE, com=com, mode=keycontrol.MODE_KEEP)
        elif isinstance(com, list) and com:
            for c in com:
                keycontrol.press_blue(keycontrol.Key.BLUE_VOICE, com=c, mode=keycontrol.MODE_KEEP)
        else:
            return False
        time.sleep(wait)
    logging.debug('play music : ' + file)
    play_result = True
    if play_normal(file) is False:
        logging.debug('file : ', file, '  play fail !!!')
        play_result = False
    if is_near:
        if isinstance(com, str):
            keycontrol.release_blue(com=com)
        elif isinstance(com, list):
            for c in com:
                keycontrol.release_blue(com=c)
        else:
            return False
    return play_result


if __name__ == '__main__':
    a = get_play_mode_by_code(1)
    print(a, type(a))
