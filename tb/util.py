# -*- coding:utf-8 -*-

import sys, os, re, glob, datetime, time, simplejson as json, traceback, math, locale, pytz, hashlib, random
import socket, urlparse, httplib, urllib, urllib2
import htmlentitydefs, HTMLParser
import logging, logging.handlers
import commands
import requests
from requests_oauthlib import OAuth1
from pprint import *
from dateutil.parser import parse as dateparse
import config
import lxml.html

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
SILENT = CRITICAL + 1

level_names = {
	logging.DEBUG: "DEBUG",
	logging.INFO: "INFO",
	logging.WARNING: "WARNING",
	logging.ERROR: "ERROR",
	logging.CRITICAL: "CRITICAL",
	SILENT: "SILENT",
}


LOGGER = logging.getLogger(__name__)

def stripslashes(s):
	r = re.sub(r"\\(n|r)", "\n", s)
	r = re.sub(r"\\", "", r)
	return r

class DateEncoder(json.JSONEncoder):
  def default(self, obj):
	if hasattr(obj, 'isoformat'):
	  return obj.isoformat()
	else:
	  return str(obj)
	return json.JSONEncoder.default(self, obj)

# user error
class user_error(Exception):
  def __init__(self, value):
	self.value = value
  def __str__(self):
	return repr(self.value)

def get_domain(url):
	domain = urlparse.urlparse(url).hostname.replace('www.', '')
	return domain

def get_domain_path(url):
	domain_path = re.sub('\/([^\/]+)?$', '', urlparse.urlparse(url).path)
	return domain_path

blank_pt = re.compile('\s{2,}')
def blank_change(str, change_str='\n'):
	return blank_pt.sub(change_str, str)


def regdate_change(str):
	return str.replace('/','-').replace('.','-')


def requests_connec(url, **kwargs):
	r = None

	try:
		if not kwargs.get('timeout'):
			kwargs['timeout'] = 3

		r = requests.get(url, **kwargs)

	except requests.exceptions.Timeout:
		# Maybe set up for a retry, or continue in a retry loop
		LOGGER.error("Timeout, url: %s", url)

	except requests.exceptions.TooManyRedirects:
		# Tell the user their URL was bad and try a different one
		LOGGER.error("TooManyRedirects, url: %s", url)

	except requests.exceptions.RequestException as e:
		# catastrophic error. bail.
		LOGGER.error("RequestException, url: %s err:%s", url, e)

	except Exception, err:
		LOGGER.error("requests Exception, url: %s, err: %s", url, err)
		LOGGER.error("requests Exception, url: %s, traceback: %s", url, traceback.format_exc())

	return r

# httplib 접속
def http_connec(url, **options):
	res = None
	conn = None

	try:
		parsed = urlparse.urlparse(url)

		header = options.get("header", {})
		params = urllib.urlencode(options.get("params", {}))
		timeout = options.get("timeout", 3)
		method = options.get("method", 'POST')

		if 'http' == parsed.scheme:
			conn = httplib.HTTPConnection(parsed.netloc)
		else:
			conn = httplib.HTTPSConnection(parsed.netloc)

		conn.connect()
		conn.sock.settimeout(timeout)
		conn.request(method, parsed.path, params, headers=header)
		resp = conn.getresponse()

		body = ''
		CHUNK = 16 * 1024
		while True:
			chunk = resp.read(CHUNK)
			if not chunk: break
			body+=chunk

		# resp.status, resp.reason, resp.version, resp.msg, resp.getheaders()
		if options.get('get_header') == True:
			res = {
				'header': {},
				'body': body
			}
			for hr in resp.getheaders():
				res['header'][hr[0].upper()] = hr[1]
		else:
			res = body
			#print res

		#print resp.status, resp.reason, resp.version, resp.msg, resp.getheaders()

	except socket.timeout:
		LOGGER.error('http connec time out: %s', socket.timeout)
	except Exception, exception:
		LOGGER.error('http connec %s', exception)

	if conn:
		conn.close()

	return res