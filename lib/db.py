#!/usr/bin/env python
# coding=utf-8

"""数据库操作工具"""

import MySQLdb
import config

DBCONFIG = config.dbconfig

class Dbclass:
    def __init__(self,  source):
        self._conn = None
        self._cursor = None
        self._source = source
        
    def connect(self, charset='utf8', commit=True):

        self._charset = charset
        db_arg = self._source
        attempt = 0
        while True:
            try:
                if db_arg.has_key('sql_db'):
                    self._conn = MySQLdb.connect(host=db_arg['sql_host'], 
                        user=db_arg['sql_user'], passwd=db_arg['sql_pass'], \
                        db=db_arg['sql_db'], port=db_arg['sql_port'], \
                        charset=charset, use_unicode=False)
                else:
                    self._conn = MySQLdb.connect(host=db_arg['sql_host'], 
                        user=db_arg['sql_user'], passwd=db_arg['sql_pass'], \
                        port=db_arg['sql_port'], \
                        charset=charset, use_unicode=False)

                self._cursor = self._conn.cursor(MySQLdb.cursors.DictCursor)
                #self._cursor = self._conn.cursor(MySQLdb.cursors.Cursor)
                if commit:
                    self._cursor.execute("set autocommit=1;")
                break
            except MySQLdb.Error , e:
                attempt += 1
                if attempt >= 3:
                    return (-1, e)
        
        return (0, None)

    def escape_string(self, val):
        return MySQLdb.escape_string(val)

 
    def query(self, sql, param=None):
        ver = MySQLdb.version_info
        ver = ver[0] * 100 + ver[1] * 10 + ver[2]

        #版本1.2.1之后无须转换
        if ver <= 121:
            if not isinstance(sql, unicode):
                sql = sql.decode(self._charset, 'ignore')

        attempt = 0
        while True:
            try:
                if not param:
                    self._cursor.execute(sql)
                else:
                    self._cursor.execute(sql, param)
                
                break
                #infos = self._cursor.fetchall()
            except MySQLdb.Error , e:
                if e[0] in (2006, 2013):  
                    attempt += 1
                    if attempt >= 3:
                        return (-1, e)
                    self.connect()
                    continue
                return (-1, e)
            except UnicodeDecodeError, e:
                return (-1, e)
        
        infos = self._cursor.fetchall()

        return (0, infos)
                
           
    def commit(self):
        try:
            self._conn.commit()
        except Exception, e:
            return (e[0], e)

        return 0, None


    def rollback(self):
        try:
            self._conn.rollback()
        except Exception, e:
            return (e[0], e)

        return 0, None

    
    def close(self):
        try:
            if self._cursor:
                self._cursor.close()
                self._cursor = None
            if self._conn:
                self._conn.close()
                self._conn = None
        except:
            pass

    def __del__(self):

        self.close()

def get_row(sql):
    """
        获取一行数据
    """
    info = Dbclass(DBCONFIG)
    res, desc = info.connect()
    if res != 0:
        log("error [%d] %s " % (desc[0], desc[1]))
        exit(0)
        return (res, desc)    
    res, desc = info.query(sql)
    if res != 0:
        log("error [%d] %s " % (desc[0], desc[1]))
        exit(0)
        return (res, desc)
    info.close()
    return (res, desc[0])

def get_all(sql):
    """
        获取一行数据
    """
    info = Dbclass(DBCONFIG)
    res, desc = info.connect()
    if res != 0:
        log("error [%d] %s " % (desc[0], desc[1]))
        exit(0)
        return (res, desc)
    res, desc = info.query(sql)
    info.close()
    if res != 0:
        log("error [%d] %s " % (desc[0], desc[1]))
        exit(0)
    return (res, desc)

def execute(sql, get_lastid=False):
    info = Dbclass(DBCONFIG)
    res, desc = info.connect()
    if res != 0:
        log("error [%d] %s " % (desc[0], desc[1]))
        exit(0)
        return (res, desc)
    res, desc = info.query(sql)
    info.close()
    if res != 0:
        log("error [%d] %s " % (desc[0], desc[1]))
        exit(0)
    return (res, desc)

def log(strs):
    print strs

if __name__ == '__main__':

    sql = "select * from cjtools.successurls limit 10;"
    re, desc = get_row(sql)
    print re
    print desc

    sql = "select * from cjtools.successurls limit 10;"
    re, desc = get_all(sql)
    print re
    print desc






