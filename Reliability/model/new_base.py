from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QHBoxLayout, QVBoxLayout

button_style_2 = """
background: #FFFFFF;
font-family: "微软雅黑";
font-size: 16px;
color: #565E6C;
border: 0px;
"""

button_style_3 = """
background: #FFFFFF;
font-family: "微软雅黑";
font-size: 16px;
color: #2276FF;
border: 0px;
"""

button_style_map = {
    2: button_style_2,
    3: button_style_3,
}


class RUNQPushButton(QPushButton):
    def __init__(self, *args, object_name=None, min_size: tuple = None, max_size: tuple = None,
                 style=0, shadow=None, image_url=None, my_policy=None):
        super(RUNQPushButton, self).__init__(*args)
        if style:
            self.style = style
            self.setStyleSheet(button_style_map[style])
        if shadow:
            self.setGraphicsEffect(self._get_shadow(shadow))
        if min_size:
            self.setMinimumSize(QSize(*min_size))
        if max_size:
            self.setMaximumSize(QSize(*max_size))
        if image_url:
            pass
        if object_name:
            self.setObjectName(object_name)
        if my_policy:
            button_policy = self.sizePolicy()
            button_policy.setVerticalPolicy(my_policy)
            button_policy.setHorizontalPolicy(my_policy)
            self.setSizePolicy(button_policy)


    def _get_shadow(self, shadow):
        if shadow == 1:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setOffset(1, 1)  # 偏移
            shadow.setBlurRadius(10)  # 阴影半径
            shadow.setColor(QColor(86, 94, 108, 0.20*255))  # 阴影颜色
        elif shadow == 2:
            shadow = QGraphicsDropShadowEffect(self)
            shadow.setOffset(1, 1)  # 偏移
            shadow.setBlurRadius(10)  # 阴影半径
            shadow.setColor(QColor(24, 75, 159, 0.52*255))  # 阴影颜色
        return shadow

    def enterEvent(self, *args, **kwargs):
        self.setGraphicsEffect(self._get_shadow(2))
        self.setStyleSheet(button_style_map[3])

    def leaveEvent(self, *args, **kwargs):
        self.setGraphicsEffect(self._get_shadow(1))
        self.setStyleSheet(button_style_map[self.style])


class SpecificQHLayout(QHBoxLayout):

    def __init__(self):
        super(SpecificQHLayout, self).__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)


class SpecificQVLayout(QVBoxLayout):

    def __init__(self):
        super(SpecificQVLayout, self).__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

