#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
from datetime import datetime, timedelta
import MySQLdb
import requests
import codecs
import dbconf
import naver_query as dbquery

from lxml import html as lh

# database connection
def get_db():
   try:
      db=MySQLdb.connect(host=mydb['HOST'],user=mydb['USER'],passwd=mydb['PASSWD'],db=mydb['DB'],charset=mydb['CHARSET'])
      cur=db.cursor()
      db.autocommit(True)
   except:
      (db,cur) = get_db()
   return db,cur

def set_data_all( c, data):
    query = dbquery.realtimenaver
    try:
       run_query = query % ("naver",current_day, data.get(1,''), data.get(2,''), data.get(3,''), data.get(4,''), data.get(5,''), data.get(6,''), data.get(7,''), data.get(8,''), data.get(9,''), data.get(10,''))
       #file.write(run_query)
       #print "%s" % run_query
       c.execute( run_query )
    except:
       print("EXCEPTION : %s" % run_query)
       file.write("EXCEPTION : %s" % run_query)
       #tb.LOGGER.debug("Unexpected error:[replaceIntoCountry]: %s" % sys.exc_info()[0])
       print("Unexpected error:[set_data]: %s" % sys.exc_info()[0])
       file.write("Unexpected error:[set_data]: %s" % sys.exc_info()[0])

def set_data( c, rank, data):
    query = dbquery.realtimekeyword
    try:
       run_query = query % (to_day,curr_hour,curr_min, rank, data,'naver')
       #file.write(run_query)
       c.execute( run_query )
    except:
       print("EXCEPTION : %s" % run_query)
       file.write("EXCEPTION : %s" % run_query)
       #tb.LOGGER.debug("Unexpected error:[replaceIntoCountry]: %s" % sys.exc_info()[0])
       print("Unexpected error:[set_data]: %s" % sys.exc_info()[0])
       file.write("Unexpected error:[set_data]: %s" % sys.exc_info()[0])

if __name__ == "__main__":
   now = datetime.now()
   to_day = now.strftime("%Y-%m-%d")
   current_day = now.strftime("%Y-%m-%d %H:%M:%S")
   curr_hour = now.strftime("%H")
   curr_min = now.strftime("%M")

   #mydb = dbconf.TESTDB
   mydb = dbconf.PUBLICDB
   (db, cur) = get_db()

   file = codecs.open("/home/tokiman/naver/naver.log", "a", "utf-8")
   file.write(">> %s %s:%s\n" % (to_day, curr_hour, curr_min))
   all_data={}
   try: 
      html = requests.get('http://www.naver.com', headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/531.21.10'}, timeout=30)
      toxml = lh.fromstring(html.text)
      rt_rank = toxml.xpath('//dl[@id="ranklist"]/dd/ol/li[not(@id="lastrank")]/a/@title')
      rt_search = enumerate(rt_rank, 1)  
      for a in rt_search:
         #print "%s %s"%(a[0],a[1])
         log="%s %s\n"%(a[0],a[1])
         file.write(log)
         set_data(cur,a[0],a[1])
         all_data[a[0]] = a[1]
      #
      set_data_all(cur,all_data)
      #db.commit()
   except:
      print "Unexpected error:[main]", sys.exc_info()[0]
      file.write( "Unexpected error:[main] %s" % sys.exc_info()[0] )
   finally:
      cur.close()
      db.close()  
   file.close()
