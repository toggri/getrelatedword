# -*- coding:utf-8 -*-
import sys, logging
LOGGER = logging.getLogger(__name__)

# path
BIN_HOME = sys.path[0]
if BIN_HOME[-4:] == '/bin':
	PROGRAM_HOME = BIN_HOME.replace('/bin', '')
else:
	PROGRAM_HOME = BIN_HOME
LIB_HOME = PROGRAM_HOME + '/lib'
LOG_HOME = PROGRAM_HOME + '/log'
LOCK_DIR = PROGRAM_HOME + '/var'
CONF_DIR = PROGRAM_HOME + '/conf'
CONF_DB_DIR = CONF_DIR
CONF_DB_EXTENSION = '.db.conf.py'

sys.path.insert(1, LIB_HOME)

# conf file
DEFAULT_CONF_FILE = CONF_DIR + '/default.conf.py'

# log 
LOG_HEAD = 'tb'
LOG_LEVEL = logging.DEBUG # logging.DEBUG

try:
	fp = file(DEFAULT_CONF_FILE)
	inf = fp.read()
	fp.close()
except Exception, err:
	errmsg = 'default conf file not load'
	LOGGER.debug(errmsg)

try:
	exec(inf)
except Exception, err:
	errmsg = 'default conf not eval'
	LOGGER.debug(errmsg)