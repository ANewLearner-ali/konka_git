"""
环境依赖模块
"""

from utils import tv_utlils
from task import device as dv, i_serializable as i_s


class Dependent(i_s.ISerializable):
    def __init__(self,
                 tv: bool = True,
                 muc: bool = False,
                 monkey_tool: bool = False,
                 bt_ct: bool = False,
                 bt_a2dp: bool = False,
                 usb: bool = False):
        self.tv = tv
        self.muc = muc
        self.monkey_tool = monkey_tool
        self.bt_ct = bt_ct
        self.bt_a2dp = bt_a2dp
        self.usb = usb
        self.device = None

    def serialize(self):
        return {'tv': self.tv,
                'muc': self.muc,
                'monkey_tool': self.monkey_tool,
                'usb': self.usb,
                'bt_ct': self.bt_ct,
                'bt_a2dp': self.bt_a2dp
                }

    def init(self, **kwargs):
        """
        额外初始化检测项
        :param kwargs:
        :return:
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and value is True:
                setattr(self, key, True)

    def setup(self, device: dv.Device):
        self.device = device

    def get_detail(self) -> list:
        """
        获取环境依赖文本描述
        :return:
        """
        return get_detail(self)

    def check(self):
        """
        检查环境并返回结果
        :return:
        """
        if self.device is None:
            raise PermissionError('device is not Initialized')
        if self.tv:
            ret, msg = tv_utlils.check_tv_com(self.device.tv_com)
            if not ret:
                return ret, msg
        if self.muc:
            ret, msg = tv_utlils.check_mcu_com(self.device.mcu_com)
            if not ret:
                return ret, msg
        if self.monkey_tool:
            ret, msg = tv_utlils.check_monkey_tools(self.device.tv_com)
            if not ret:
                return ret, msg
        if self.usb:
            ret, msg = tv_utlils.check_usb(self.device)
            if not ret:
                return ret, msg
        if self.bt_ct:
            ret, msg = tv_utlils.check_bt_ct(self.device)
            if not ret:
                return ret, msg
        if self.bt_a2dp:
            ret, msg = tv_utlils.check_bt_a2dp(self.device)
            if not ret:
                return ret, msg
        return True, 'PASS'

    def get_dependent_info(self):
        return ','.join([
            '单片机' if self.muc else '',
            'monkey_tool' if self.monkey_tool else ''
        ])

    @staticmethod
    def deserialize(d: dict)-> 'Dependent':
        return Dependent(**d)


def get_detail(d) -> list:
    entries = {
        'tv': '电视',
        'muc': '单片机',
        'monkey_tool': 'monkey_tool',
        'usb': 'U盘',
        'bt_ct': '蓝牙遥控器',
        'bt_a2dp': '蓝牙音箱'
    }
    ret = list()
    for key in entries.keys():
        if isinstance(d, Dependent):
            if getattr(d, key, False):
                ret.append(entries[key])
        else:
            if d.get(key, False):
                ret.append(entries[key])
    return ['环境依赖:' + '、'.join(ret)]
