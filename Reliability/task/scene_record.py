"""
录制脚本场景实现
"""
import logging
import os
import constant

from task import scene as sc, excel as ex, checker as ck
from utils import common, config_utils, shellcmd, file_utils


class SceneRecord(sc.Scene):
    """
    录制脚本场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 scripts: (list, str),
                 by: int = sc.BY_COUNT):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        if isinstance(scripts, list):
            self.scripts = scripts
        elif isinstance(scripts, str):
            if not os.path.isfile(scripts):
                raise AssertionError(f'illegal scripts : {scripts}')
            self.scripts = config_utils.read_config(scripts)
        else:
            raise AssertionError(f'illegal scripts : {scripts}')

    def serialize(self):
        ret = {
            'scripts': self.scripts,
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneRecord':
        return sc.Scene.base_deserialize(SceneRecord, d)

    def _get_config_detail(self):
        second = list()
        scripts = []
        for script in self.scripts:
            scripts.append(os.path.basename(script).rpartition('.')[0])
        second.append('脚本名称:' + '、'.join(scripts))
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def work(self):
        # 删除excel报告
        # file_utils.rm(self.fd.excel)
        # 获取串口号
        tv_com, mcu_com = self.device.tv_com, self.device.mcu_com
        dir_set_start = _get_kk_record_report_set()
        # 关闭电视串口
        shellcmd.close_kk_serial(tv_com)
        # 通过子进程拉起脚本录制工具执行场景
        exec_scene(tv_com, mcu_com, self.scripts)
        dir_set_complete = _get_kk_record_report_set()
        logging.warning(f'!!!!! should copy {dir_set_complete - dir_set_start} !!!!!')
        _copy_report(self.device.tv_com, dir_set_complete - dir_set_start, self.fd.root_pc)
        if not _parse_result(self.fd.root_pc):
            setattr(self, 'state', sc.STATE_FAIL)
            # raise AssertionError(f'{self.device.tv_com} 脚本录制场景失败')


def _init():
    """
    初始化，检测录制工具的路径和可执行文件是否有效
    :return:
    """
    with open(constant.RECORD_PATH, 'r', encoding='utf-8') as f:
        directory = f.read()
    if not directory or not os.path.isdir(directory):
        raise AssertionError(f'kkrecord path not found : {directory}')
    exe = os.path.join(directory, 'main.exe')
    if not os.path.isfile(exe):
        raise AssertionError(f'kkrecord exe not found')
    return directory, exe


def _run_cmd(cmd):
    logging.debug(f'start cmd : {cmd}')
    common.run_command(cmd)
    logging.debug(f'end cmd : {cmd}')


def set_kk_record_path(path):
    """
    设置脚本录制工具路径
    :param path:
    :return:
    """
    with open(constant.RECORD_PATH, 'w', encoding='utf-8') as f:
        f.write(path)


def create_kk_record_scene():
    """
    创建脚本录制场景
    :return:
    """
    try:
        directory, exe = _init()
    except BaseException as e:
        logging.exception(e)
        return False, str(e)
    scene_file = os.path.join(directory, 'src', 'scene')
    file_utils.rm(scene_file)
    cmd = exe + ' -c'
    _run_cmd(cmd)
    if not os.path.isfile(scene_file):
        return False, f'录制脚本场景创建失败， 未发现文件:{scene_file}'
    return True, config_utils.read_config(scene_file)


def exec_scene(tv_com, mcu_com, scripts: list):
    """
    执行脚本录制场景
    :param tv_com:
    :param mcu_com:
    :param scripts:
    :return:
    """
    directory, exe = _init()
    scripts = ' '.join(['"' + script + '"' for script in scripts])
    cmd = [exe, '-d', str(tv_com) + ',' + str(mcu_com), '-t', scripts]
    cmd = ' '.join(cmd)
    _run_cmd(cmd)


def _get_kk_record_report_set() -> set:
    directory, exe = _init()
    reports_root = os.path.join(directory, 'reports')
    if os.path.isdir(reports_root):
        return set([os.path.join(reports_root, root) for root in os.listdir(reports_root)])
    else:
        return set()


def _get_first_dir(root):
    logging.warning(f'_get_first_dir {root}')
    for file_name in os.listdir(root):
        if os.path.isdir(os.path.join(root, file_name)):
            return file_name
    return None


def _get_target_dir(com, roots):
    logging.warning(f'_get_target_dir {com} {roots}')
    for root in roots:
        if os.path.isdir(root):
            first_dir = _get_first_dir(root)
            logging.warning(f'find first_dir {first_dir}')
            if first_dir is not None and com + '_'in os.listdir(os.path.join(root, first_dir)):
                return root
    return None


def _copy_files(ori_root, des_root):
    logging.warning(f'_copy_files {ori_root} {des_root}')
    ori_len = len(ori_root)
    for dir_path, dir_names, file_names in os.walk(ori_root):
        des_dir_path = des_root + dir_path[ori_len:]
        file_utils.mkdir(des_dir_path)
        for file in file_names:
            if os.path.isfile(os.path.join(dir_path, file)):
                file_utils.cp(os.path.join(dir_path, file), os.path.join(des_dir_path, file), is_binary=True)


def _copy_report(com, roots, des_root):
    ori_root = _get_target_dir(com, roots)
    if ori_root is None:
        logging.warning(f'{com} target kk record root not found')
        return
    _copy_files(ori_root, des_root)


def _parse_result(report_root) -> bool:
    index_html = os.path.join(report_root, 'index.html')
    if not os.path.isfile(index_html):
        logging.warning(f'_parse_result not found {index_html}')
        return False
    try:
        with open(index_html, 'r', encoding='utf-8') as f:
            start = False
            results = []
            for line in f.readlines():
                if start:
                    results.append('<td class="pass">PASS</td>' in line)
                    start = False
                if '<td><a href="' in line:
                    start = True
            logging.warning(f'_parse_result index.html results {results}')
            return len(results) > 0 and all(results)
    except BaseException as e:
        logging.warning('_parse_result index.html fail')
        logging.exception(e)
        return False


if __name__ == '__main__':
    # set_kk_record_path(r"F:\LittleTools\KKRecord\dist\main")
    # # ret = create_kk_record_scene()
    # # print('ret', ret)
    # exec_scene(
    #     'com32',
    #     None,
    #     [
    #         r'F:\LittleTools\KKRecord\dist\main\scripts\2.json',
    #         r'F:\LittleTools\KKRecord\dist\main\scripts\2 - 副本.json'
    #     ]
    # )
    # _copy_report('com32', [r'F:\LittleTools\KKRecord\reports\20200331172855'], r'F:\PythonProjects\Reliability\reports\_20200415172703')
    ret = _parse_result(r'F:\PythonProjects\Reliability\reports\_20200415172703 - 副本')
    print('ret', ret)
