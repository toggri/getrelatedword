# -*- coding:utf-8 -*-

from tb.util import *
import inspect

LOGGER = None

def setLogger(logname=None,
		logfile=None,
		loglevel=None,
		logprint=True,
		logsize=100,
		logbackupcount=3):

	global LOGGER

	maxsize = 1024*1024*logsize

	if not logname:
		frm = inspect.stack()[1]
		mod = inspect.getmodule(frm[0])
		logname = re.findall('.+\/(.+).py$', sys.argv[0])[0]

	loglevel = loglevel or config.LOG_LEVEL

	LOGGER = logging.getLogger(config.LOG_HEAD)
	LOGGER.setLevel(loglevel)

	logfile = logfile or "%s/%s.log" % (config.LOG_HOME, logname)
	formatstr = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
	formatter = logging.Formatter(formatstr)

	if logprint is True:
		handler = logging.StreamHandler()
		handler.setFormatter(formatter)
		LOGGER.addHandler(handler)

	''' size 
	handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=maxsize, backupCount=logbackupcount)
	handler.setFormatter(formatter)
	LOGGER.addHandler(handler)
	# '''
	
	#''' time rotating
	handler = logging.handlers.TimedRotatingFileHandler(logfile, when='D')
	#handler.suffix = "%Y%m%d%H%M"
	handler.setFormatter(formatter)
	LOGGER.addHandler(handler)
	# '''

	LOGGER.debug("LOGGING SET Level:%s filename:%s", level_names[loglevel], logfile)
	LOGGER = logging.getLogger('%s.%s' % (config.LOG_HEAD, logname))

def getLogger(logname, loglevel=None):
	logger = logging.getLogger('%s.%s' % (config.LOG_HEAD, logname))
	if loglevel:
		logger.setLevel(loglevel)

	return logger

def msg(msgstr, _level=INFO):
	'''
	frm = inspect.stack()[1]
	mod = inspect.getmodule(frm[0])
	logger = logging.getLogger(mod.__name__)
	#'''
	LOGGER.log(_level, msgstr)
