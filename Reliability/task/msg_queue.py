"""
该工具用到的两个消息队列，主要是添加一些信息，然后ui层去拿到信息后做处理
"""
import queue


TAG_START = '开始调试'
TAG_END = '结束调试'
TAG_EXCEPTION = '调试异常'
TAG_MSG = '调试信息'

# 一键检测log的消息队列
# msg type : (TAG, MSG_STRING), example : (TAG_MSG, 'input android key - back')
ck_queue = queue.Queue()

# 场景测试异常的消息队列
# msg type : (COM, MSG_STRING), example : (com1, 'json parse failed')
error_queue = queue.Queue()

# 脚本检测log的消息队列
# msg type : (TAG, MSG_STRING), example : (TAG_MSG, 'input android key - back')
sk_queue = queue.Queue()