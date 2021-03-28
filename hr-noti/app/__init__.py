# -*- coding: utf-8 -*-
import imp

# The priority of available config-file declarations:
# 1. Commandline Argumnet (customized - good for local dev, test, flexible deployment)
# 2. DEFAULT_GLOBAL_CONFIG_FILE (hard-coded - recommended for deployment)
# 3. DEFAULT_APPLICATION_CONFIG_FILE (hard-coded - recommended for development, svn-committed content)
DEFAULT_GLOBAL_CONFIG_FILE = '/home/sf/soc/conf/sirc.py'
DEFAULT_APPLICATION_CONFIG_FILE = 'app/config.py'
DEFAULT_CONFIG_CLASS = 'ApiAppConfig'
DEFAULT_TEST_CLASS = 'TestingConfig'


def load_module(filename):
    """
    Load module from a python file
    :param filename:
    :return:
    """
    mod = imp.new_module('config')
    mod.__file__ = filename
    try:
        with open(filename) as config_file:
            exec (compile(config_file.read(), filename, 'exec'), mod.__dict__)
    except Exception as e:
        raise e
    return mod
