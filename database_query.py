#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 2017年3月24日
@author: BG243022
'''
import MySQLdb

dbhost = "hx-mysql-p1.800best.com"
dbuser = "usr_djautotest"
dbpassword = "usr_djautotest123"
dbport = "djdb_autotest"

dbsaleuser = "usr_dianjiaauto_test"
dbsalsepassword = "usr_dianjiaauto_test"
dbsaleport = "dianjiaauto_test"

def db_query(name, condition, label='*'):
    '''数据库查询基本方法
    '''
    db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpassword, db=dbport, charset='utf8')
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    # 默认返回全部字段， 若给出相应字段则只返回相应字段
    temp = ','.join(label)
    sql = 'select {0} from {1} where '.format(temp, name)
    #拼接一个或多个查询条件
    length = len(condition)
    for key in condition:
        sql += '{0}="{1}"'.format(key, condition[key])
        length -= 1
        if length > 0:
            sql += ' and '
    #print sql
    cur.execute(sql)
    db.commit()
    data = cur.fetchall()
    return data
def db_sale_query(name, condition, label='*'):
    '''数据库查询基本方法
    '''
    db = MySQLdb.connect(host=dbhost, user=dbsaleuser, passwd=dbsalsepassword, db=dbsaleport, charset='utf8')
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    # 默认返回全部字段， 若给出相应字段则只返回相应字段
    temp = ','.join(label)
    sql = 'select {0} from {1} where '.format(temp, name)
    #拼接一个或多个查询条件
    length = len(condition)
    for key in condition:
        sql += '{0}="{1}"'.format(key, condition[key])
        length -= 1
        if length > 0:
            sql += ' and '
    #print sql
    cur.execute(sql)
    db.commit()
    data = cur.fetchall()
    return data
def db_time_query(name, condition,time, label='*'):
    '''数据库查询基本方法
    '''
    db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpassword, db=dbport, charset='utf8')
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    # 默认返回全部字段， 若给出相应字段则只返回相应字段
    temp = ','.join(label)
    sql = 'select {0} from {1} where '.format(temp, name)
    #拼接一个或多个查询条件
    length = len(condition)
    for key in condition:
        sql += '{0}="{1}"'.format(key, condition[key])
        length -= 1
        if length > 0:
            sql += ' and '
    if time:
        sql+=' and '+time
    print sql
    cur.execute(sql)
    db.commit()
    data = cur.fetchall()
    return data

def db_tables_query(name1, name2, key1, key2, condition1, condition2, label='*', joins='left'):
    '''多表联合查询基本方法
        Arguments:
            name(str):表一和表二名字
            key(str):二表关联外键
            condition(dict):查询条件
            label(str/dict):返回字段，默认返回全部，非默认包含返回字段所属表名及字段，ex:
                {'name':'table','info':['status','id']}
            joins(str):连接类型，默认左连接，可选择'right'/'inner'
    '''
    db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpassword, db=dbport, charset='utf8')
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    #拼接返回字段
    if label is not '*':
        temp = ''
        for i in xrange(len(label['info'])):
            temp += '{0}.{1},'.format(label['name'], label['info'][i])
        temp = temp[:-1]
    else:
        temp = '*'
    sql = 'select {0} from {1} {2} join {3} on {1}.{4}={3}.{5} where '.format(temp, name1, joins, name2, key1, key2)
    #拼接一个或多个查询条件
    sql += _add(name1, condition1) + ' and ' + _add(name2, condition2)
    print sql
    cur.execute(sql)
    db.commit()
    data = cur.fetchall()
    return data

def _add(name, condition):
    '''多表查询条件拼接
    '''
    length = len(condition)
    temp = ''
    for key in condition:
        temp += '{0}.{1}="{2}"'.format(name, key, condition[key])
        length -= 1
        if length > 0:
            temp += ' and '
    return temp
def db_sql_query(sql):
    db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpassword, db=dbport, charset='utf8')
    cur = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    db.commit()
    data = cur.fetchall()
    return data