"""
测试设备模块，包含了电视设备和单片机设备
"""

from utils import keycontrol


class Device:
    def __init__(self, tv_com: str, mcu_com: str = ''):
        self.tv_com = tv_com
        self.tv = keycontrol.TVSerial(tv_com)
        self.mcu_com = mcu_com if mcu_com.strip() else None
        self.mcu = keycontrol.MicroControllerUnit(mcu_com) if self.mcu_com else None

    def __str__(self):
        return f'[Device {self.tv_com} {self.mcu_com}]'

    def __repr__(self):
        return self.__str__()
