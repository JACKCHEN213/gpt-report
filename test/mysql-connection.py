# -*- coding: utf-8 -*-
import datetime

import mysql.connector
import pymysql
from sqlalchemy import Column, String, create_engine, Integer, DateTime, Date, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'tb_user'

    # 表的结构:
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(20))
    sex = Column(Integer())
    birthday = Column(Date())
    create_time = Column(DateTime())
    update_time = Column(DateTime())


def test_mysql_connector():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        database="information_schema",
        auth_plugin='mysql_native_password',
    )

    my_cursor = mydb.cursor()
    my_cursor.execute("show  databases")
    print('mysql-connector: ', my_cursor.fetchall())


def test_pymysql():
    db = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="information_schema",
    )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute()  方法执行 SQL 查询
    sql = "SELECT VERSION()"
    cursor.execute(sql)
    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()
    print('pymysql: ', "Database version : %s " % data)
    # 关闭数据库连接
    db.close()


def test_sqlalchemy():
    # 初始化数据库连接:
    host = "localhost"
    user = "root"
    password = "123456"
    database = "test"
    engine = create_engine('mysql+pymysql://{}:{}@{}:3306/{}'.format(user, password, host, database))
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    # 添加一条记录
    # 创建session对象:
    session = DBSession()
    # 建库
    # session
    # 创建新User对象:
    new_user = User(name='Bob', sex=0, birthday=datetime.date(2020, 1, 1))
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()


def main():
    test_mysql_connector()
    test_pymysql()
    test_sqlalchemy()


if __name__ == '__main__':
    main()
