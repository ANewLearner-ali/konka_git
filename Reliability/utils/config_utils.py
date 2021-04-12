import json
import logging


def read_config(file: str):
    with open(file, 'r', encoding='utf-8') as f:
        config_string = f.read()
    config = json.loads(config_string)
    # logging.debug('read config, file : ' + file + ' config : ' + config_string)
    return config


def write_config(file: str, config):
    config_string = json.dumps(config)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(config_string)
    # logging.debug('write config, file : ' + file + ' config : ' + config_string)


def update_config(file, key, value):
    settings = read_config(file)
    settings.update({key: value})
    write_config(file, settings)
    # logging.debug('update config, file:' + file + ' key:' + str(key) + ' value:' + str(value))


def append_config(file, item):
    settings = read_config(file)
    settings.append(item)
    write_config(file, settings)
    # logging.debug('append config list, file:' + file + ' append:' + str(item))


def config_check(file) -> bool:
    try:
        read_config(file)
    except BaseException as e:
        logging.warning('config_check fail : {} , error msg : {}', file, e)
        return False
    return True


def qss_read(file):
    with open(file, 'r', encoding='utf-8') as f:
        config_string = f.read()
    return config_string
