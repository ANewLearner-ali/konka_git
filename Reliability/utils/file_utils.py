import logging
import os


def mkdir(root: str):
    if not os.path.isdir(root):
        os.mkdir(root)


def rm(file: str):
    if os.path.isfile(file):
        try:
            os.remove(file)
        except:
            ...
    return True


def cp(ori_file, des_file, is_binary=False) -> bool:
    logging.warning(f'cp {ori_file} , {des_file} , is_binary {is_binary}')
    if is_binary:
        read_mode, write_mode = 'rb', 'wb'
    else:
        read_mode, write_mode = 'r', 'w'
    if is_binary:
        with open(ori_file, read_mode) as fr:
            with open(des_file, write_mode) as fw:
                fw.write(fr.read())
    else:
        with open(ori_file, read_mode, encoding='utf-8') as fr:
            with open(des_file, write_mode, encoding='utf-8') as fw:
                fw.write(fr.read())
    return True
