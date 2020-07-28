#!/usr/local/bin/python
# -*- coding:utf-8 -*-
import requests
from lxml import html as lh

html = requests.get('http://www.naver.com', headers={'User-Agent': 'Mozilla/5.0 AppleWebKit/531.21.10'}, timeout=30)
toxml = lh.fromstring(html.text)
#rt_rank = toxml.xpath('//dl[@id="ranklist"]/dd/ol/li[not(@id="lastrank")]/a/text()')
rt_rank = toxml.xpath('//dl[@id="ranklist"]/dd/ol/li[not(@id="lastrank")]/a/@title')
rt_search = enumerate(rt_rank, 1)  
for a in rt_search:
   print "%s %s"%(a[0],a[1])
