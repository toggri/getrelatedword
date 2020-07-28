#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

realtimekeyword="""
INSERT IGNORE INTO realkeywords (rday,rhour,rmin,rank,rword,site) VALUES ('%s','%s','%s',%s,'%s','%s')
"""
realtimenaver="""
INSERT IGNORE INTO realtime (site,created,query_0,query_1,query_2,query_3,query_4,query_5,query_6,query_7,query_8,query_9) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
"""
rkeywords="""SELECT * FROM realtime WHERE site='naver' ORDER BY id DESC LIMIT 1"""
insrkeywords="""INSERT IGNORE INTO relatedkeywords (site,created,rword,query_0,query_1,query_2,query_3,query_4,query_5,query_6,query_7,query_8,query_9,query_json) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
"""
