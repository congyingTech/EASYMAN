# coding=utf-8
"""
@author: congying
@email: wangcongyinga@gmail.com 
"""
from logging.handlers import RotatingFileHandler
import logging
import imp


class ConfLoader(object):
    def __init__(self, conf_name, project_path):
        self.conf_name = conf_name
        self.project_path = project_path

    def set_logger(self, settings):

        log_format = '%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(threadName)s - %(thread)d - %(message)s'
        log_level = settings['LOG_LEVEL']
        log_file = settings['LOG_FILE']

        rotating_file_log = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
        rotating_file_log.setFormatter(logging.Formatter(log_format))
        rotating_file_log.setLevel(log_level)

        logging.root.setLevel(log_level)
        logging.root.addHandler(rotating_file_log)

    def load_conf(self):
        """
        加载conf文件夹下的setting文件
        :return: dict格式的setting
        """
        conf_path = 'conf/settings_{}.py'.format(self.conf_name)
        print conf_path
        module = imp.load_source(conf_path, self.project_path+'EASYMAN/EASYBLOG/'+conf_path)
        print module
        settings = dict()
        for key in dir(module):
            if key.isupper():
                settings[key] = getattr(module, key)
                print key, getattr(module, key)
        self.set_logger(settings)
        print settings
        return settings


if __name__ == "__main__":
    conf = ConfLoader('default', '/Users/wangcongying/PycharmProjects/')
    conf.load_conf()
