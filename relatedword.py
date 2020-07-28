#!/usr/local/bin/python3.6
# -*- coding:utf-8 -*-
# NAVER 연관 검색어
import sys
from datetime import datetime, timedelta
import MySQLdb
import requests
import codecs
import json
from lxml import html as lh

import dbconf
import naver_query as dbquery


# database connection
def get_db():
   try:
      db=MySQLdb.connect(host=mydb['HOST'],user=mydb['USER'],passwd=mydb['PASSWD'],db=mydb['DB'],charset=mydb['CHARSET'])
      cur=db.cursor()
      db.autocommit(True)
   except:
      (db,cur) = get_db()
   return db,cur

def get_data_all(c):
    query = dbquery.rkeywords
    response = ()
    try:
       c.execute( query )
       response = c.fetchall()
    except:
       print("EXCEPTION : %s" % query)
       file.write("-- EXCEPTION : %s" % query)
       #tb.LOGGER.debug("Unexpected error:[replaceIntoCountry]: %s" % sys.exc_info()[0])
       print("Unexpected error:[get_all_data]: %s" % sys.exc_info()[0])
       file.write("-- Unexpected error:[get_all_data]: %s" % sys.exc_info()[0])
    #end try
    return response[0]

def set_data( c, rword, data):
    query = dbquery.insrkeywords
    try:
       jdata = json.dumps(data,ensure_ascii=False)
       run_query = query % ('naver',current_day,rword,data.get(1,''),data.get(2,''),data.get(3,''),data.get(4,''),data.get(5,''),data.get(6,''),data.get(7,''),data.get(8,''),data.get(9,''),data.get(10,''),jdata)
       c.execute( run_query )
       file.write("%s ;\n" % run_query)
    except:
       print("EXCEPTION : %s" % run_query)
       file.write("-- EXCEPTION : %s" % run_query)
       #tb.LOGGER.debug("Unexpected error:[replaceIntoCountry]: %s" % sys.exc_info()[0])
       print("Unexpected error:[set_data]: %s" % sys.exc_info()[0])
       file.write("-- Unexpected error:[set_data]: %s" % sys.exc_info()[0])

if __name__ == "__main__":

   now = datetime.now()
   to_day = now.strftime("%Y-%m-%d")
   current_day = now.strftime("%Y-%m-%d %H:%M:%S")
   curr_hour = now.strftime("%H")
   curr_min = now.strftime("%M")

   #mydb = dbconf.TESTDB
   mydb = dbconf.PUBLICDB
   (db, cur) = get_db()

   file = codecs.open("/home/tokiman/naver/naverRelated.log", "a", "utf-8")
   file.write("-- >> %s %s:%s\n" % (to_day, curr_hour, curr_min))
   all_data={}

   url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%s"
   try: 
      kall=get_data_all(cur)
      for k in kall[3:13]:
         aurl = url % k
         #print aurl
         file.write("-- %s\n"% aurl)
         html = requests.get(aurl, headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/531.21.10'}, timeout=30)
         toxml = lh.fromstring(html.text)
         rt_rank = toxml.xpath('//div[@id="nx_related_keywords"]/dl/dd/ul/li/a/text()')
         rt_search = enumerate(rt_rank, 1)  
         for a in rt_search:
            print("%s %s" % (a[0],a[1]))
            all_data[a[0]] = a[1]
         set_data(cur,k,all_data)
         all_data={}
         #end for
      #end for 
   except:
      print("Unexpected error:[main]", sys.exc_info()[0])
      file.write( "-- Unexpected error:[main] %s" % sys.exc_info()[0] )
   finally:
      cur.close()
      db.close()  
      file.close()
