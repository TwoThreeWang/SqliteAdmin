#!/usr/bin/python
# coding: utf-8
# +-------------------------------------------------------------------
# | 宝塔Linux面板
# editor: WangTwoThree(https://www.wangtwothree.com)
#+--------------------------------------------------------------------
#|   宝塔第三方应用开发 sqliteadmin
#+--------------------------------------------------------------------
import sys,os,json,sqlite3,re
#设置运行目录
basedir = os.path.abspath(os.path.dirname(__file__))
plugin_path = "/www/server/panel/plugin/sqliteadmin/"
try:
    os.chdir("/www/server/panel")
except :
    print("FileNotFoundError") 
    os.chdir(os.path.join(basedir, '..', '..'))
    plugin_path = basedir.rstrip('/')+'/'

#添加包引用位置并引用公共包
sys.path.append("class/")
import public

__all__ = ["sqliteadmin_main"]

from BTPanel import app, cache,session
from flask import render_template, request,redirect, url_for

prefix="sqliteadmin"
   
def scan_sqlite(sPath, exts='*.*', callback=None):
    rs = []
    if isinstance(exts, str):
        _exts = exts.replace('.','[.]').replace('*','.*').replace(';','|').strip('|')
        _exts = '('+_exts+')'+'$'
           
    for root, dirs, files in os.walk(sPath, True, None, False):     
        for f in files:
            fpath = os.path.join(root,f)
            if not os.path.isfile(fpath):  continue
            if isinstance(exts, str):
                if '*.*' not in exts:
                    if not re.match(_exts, f, flags=re.I): continue #match
            else:
                ext = os.path.splitext(f)[1].lower() 
                if ext not in exts: continue
                
            fp=open(fpath, 'rb')
            words = fp.read(15)
            fp.close()
            if words!= b'SQLite format 3': continue
            rs.append(fpath)
            if callback: callback(fpath)
    return rs

class sqliteadmin_main:
    "sqlite3数据库web可视化操作"
    
    __plugin_path = plugin_path
    __config = None
    
    #构造方法
    def  __init__(self):
        pass
    
    def get_scan(self, args):
        if not ('folder' in args and args.folder): return {'error':'搜索目录不能为空'}
        if not os.path.isdir(args.folder): return {'error':'搜索目录不存在'}
        exts = args.exts if 'exts' in args else '*.db;*.sqlite;*sqlite3'
        rs = scan_sqlite(args.folder, exts=exts, callback=None)
        rs = [s.replace('\\','/') for s in rs]
        return {'result':rs}
    
    def add_dbs(self, args):
        with open(plugin_path+"/dbs.txt","a+") as fo:
            fo.write(f"{args.db_path}\n")
        return public.returnMsg(True, 'Success!')
        
    def del_dbs(self, args):
        output = []
        with open(plugin_path+"/dbs.txt","r") as fo:
            for line in fo.readlines():
                if args.db_path not in line:
                    output.append(line)
        with open(plugin_path+"/dbs.txt","w") as fo:
            fo.writelines(output)
        return public.returnMsg(True, 'Success!')
        
    def get_dbs(self, args):
        db_paths = []
        with open(plugin_path+"/dbs.txt","r") as fo:
            for line in fo.readlines():
                db_paths.append(line.strip())
        return {'result':db_paths}
    
    def get_tables(self,args):
        conn = sqlite3.connect(args.db_path)
        cursor = conn.cursor()
        rows = cursor.execute("select name from sqlite_master where type = 'table' order by name").fetchall()
        table_names = [row[0] for row in rows]
        return {'result':table_names}

    def get_col(self,cursor,table_name):
        col_names=[]
        cursor.execute('pragma table_info(`{}`)'.format(table_name))
        col_name=cursor.fetchall()
        col_name=[x[1] for x in col_name]
        col_names.append(col_name)
        return col_names
    
    def get_table_rows(self, args):
        conn = sqlite3.connect(args.db_path)
        cursor = conn.cursor()
        rows = cursor.execute(f"select * from `{args.table_name}`").fetchall()
        col_names = self.get_col(cursor,args.table_name)
        datas = [list(row) for row in rows]
        return {'table_name':args.table_name,'col_names':col_names,'datas':datas}
    
    def run_sql(self,args):
        conn = sqlite3.connect(args.db_path)
        cursor = conn.cursor()
        datas = []
        msg = 'Success'
        flag = 1
        try:
            cursor.execute(args.sql)
            conn.commit()
            if 'select' in args.sql:
                rows=cursor.fetchall()
                datas=[list(row) for row in rows]
        except Exception as e:
            msg = str(e)
            flag = 2
        return {'datas':datas,'msg':msg, 'flag':flag}
