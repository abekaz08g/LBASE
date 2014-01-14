#-*-coding:utf-8-*-
from pymongo import Connection
import re

"""
教科書データベース，目次モジュール
"""


def startUpDB():
    """
    データベースの起動
    """
    con = Connection('localhost', 27017)
    db = con[u'LBS']
    col = db[u'mokuji']
    return col


def getPageNumbers(pageRange):
    """
    目次ファイルから項目ごとにページ番号を抽出。簡単なパターン判断のロジックも含む。
    """
    st_end = pageRange.split(u'-')
    if len(st_end) == 2:
        pageNumbers = [i for i in range(int(st_end[0]), int(st_end[1]) + 1)]
    else:
        pageNumbers = [int(st_end[0])]
    return pageNumbers


def run(fin, lbid, cat=None):
    """
    実行メソッド
    """
    col = startUpDB()
    f = open(fin)
    for line in f:
        uline = line.decode('utf-8')[:-1]
        rec = uline.split('\t')
        if len(rec) == 2:
            pnums = getPageNumbers(rec[1])
            params = {}
            params[u'cat'] = cat
            params[u'title'] = rec[0]
            params[u'pageNumbers'] = pnums
            params[u'lbid'] = lbid
            col.insert(params)


def findWord(w, fopath):
    """
    単語wによる検索結果をfopathに書き出し。ファイル入出力用。
    """
    col = startUpDB()
    pat = re.compile(w)
    res = col.find({u'title': pat})
    items = []
    for item in res:
        strPnum = u', '.join([str(i) for i in item[u'pageNumbers']])
        items.append((item[u'title'], item[u'lbid'], strPnum))
    items.sort()
    fout = open(fopath, 'w')
    fout.write(w.encode('UTF-8') + '\n=====\n')
    for item in items:
        uline = '%s %s  %s\n' % (tuple(item))
        fout.write(uline.encode('UTF-8'))
findWord(u'格', 'kasus.txt')
