from utils import log
from model.main_test_1 import Entrance_View
import sys
from PyQt5 import QtWidgets
from utils.config_utils import read_config
import constant

if __name__ == '__main__':
    log_dir = read_config(constant.CONFIG_FILE)['tool_config']['log_dir']
    output = True if read_config(constant.CONFIG_FILE)['tool_config']['output'] == 'True' else False
    log.init_logging_dir(log_dir, output=output)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = Entrance_View()
    ui.show()
    sys.exit(app.exec_())
