#-*-coding:utf-8-*-
from pymongo import Connection
import re

def startUpDB():
  con = Connection('localhost', 27017)
  db = con[u'LBS']
  col = db[u'mokuji']
  return col
  
def getPageNumbers(pageRange):
  st_end = pageRange.split(u'-')
  if len(st_end) == 2:
    pageNumbers = [i for i in range(int(st_end[0]), int(st_end[1])+1)]
  else:
    pageNumbers = [int(st_end[0])]
  return pageNumbers

def run(fin, lbid, cat=None):
  col = startUpDB()
  f = open(fin)
  for line in f:
    uline = line.decode('utf-8')[:-1]
    rec = uline.split('\t')
    if len(rec) == 2:
      pnums = getPageNumbers(rec[1])
    col.insert({u'cat':cat, u'title':rec[0], u'pageNumbers':pnums, u'lbid':lbid})

def findWord(w, fopath):
  col = startUpDB()
  pat = re.compile(w)
  res = col.find({u'title':pat} )
  items = []
  for item in res:
    items.append((item[u'title'],item[u'lbid'], u', '.join([str(i) for i in item[u'pageNumbers']])))
  items.sort()
  fout = open(fopath, 'w')
  fout.write(w.encode('UTF-8')+'\n=====\n')
  for item in items:
    uline = '%s %s  %s\n'%(tuple(item))
    fout.write(uline.encode('UTF-8'))

findWord(u'格', 'kasus.txt')