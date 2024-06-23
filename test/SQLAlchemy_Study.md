# SQLAlchemy

引用文章: [https://www.cnblogs.com/aylin/p/5770888.html](https://www.cnblogs.com/aylin/p/5770888.html)

## 安装

```shell
# 安装
pip install SQLAlchemy

# 验证
python

>>> import sqlalchemy
>>> sqlalchemy.__version__
'1.4.39'
>>> 
```
## 数据库操作

### 连接数据库

在sqlalchemy中，session用于创建程序与数据库之间的会话。所有对象的载入和保存都需要通过session对象。

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 连接数据库采用pymysq模块做映射，后面参数是最大连接数5
host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'test'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8', max_overflow=5)
Session = sessionmaker(bind=engine)

session = Session()

```

### 创建映射

一个映射对应着一个Python类，用来表示一个表的结构。下面创建一个person表，包括id和name两个字段。也就是说创建表就是用python的的类来实现

```python
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import sessionmaker

host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'test'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8', max_overflow=5)

#生成一个SQL ORM基类，创建表必须继承他, 类似于pydantic的BaseModel
Base = declarative_base()

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

```

上面定义了一个User模型，对应的sql如下:

```sql
DROP DATABASE IF EXISTS test;

CREATE DATABASE test;

use test;

DROP TABLE IF EXISTS tb_user;
create table tb_user
(
    id          int auto_increment
        primary key,
    name        varchar(60)                        not null,
    sex         tinyint  default 0                 null comment '[0男 1女]',
    birthday    date     default '1970-01-01'      null,
    create_time datetime default CURRENT_TIMESTAMP null,
    update_time datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
) engine InnoDB default character set utf8mb4 COLLATE utf8mb4_0900_ai_ci;

```

### 添加数据

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import sessionmaker
import datetime

host = 'localhost'
port = 3306
user = 'root'
password = '123456'
database = 'test'
engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8', max_overflow=5)

#生成一个SQL ORM基类，创建表必须继承他, 类似于pydantic的BaseModel
Base = declarative_base()

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


if __name__ == '__main__':
    # 创建Session类型:
    Session = sessionmaker(bind=engine)
    # 创建session对象:
    session = Session()
    new_user = User(name='Bob', sex=0, birthday=datetime.date(2020, 1, 1))
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()

    new_user1 = User(name='Bob1', sex=0, birthday=datetime.date(2020, 1, 1))
    new_user2 = User(name='Bob2', sex=0, birthday=datetime.date(2020, 1, 1))
    # 插入多个
    session.add_all([new_user1, new_user2])
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

```

### 查找数据

```python
#获取所有数据
session.query(User).all()

#获取name=‘张岩林’的那行数据
session.query(User).filter(User.name=='张岩林').one()

#获取返回数据的第一行
session.query(User).first()

#查找id大于1的所有数据
session.query(User.name).filter(User.id>1).all()

#limit索引取出第一二行数据
session.query(User).all()[1:3]

#order by,按照id从大到小排列
session.query(User).ordre_by(User.id)

#equal/like/in
query = session.query(User)
query.filter(User.id==1).all()
query.filter(User.id!=1).all()
query.filter(User.name.like('%ay%')).all()
query.filter(User.id.in_([1,2,3])).all()
query.filter(~User.id.in_([1,2,3])).all()
query.filter(User.name==None).all()

#and or
from sqlalchemy import and_
from sqlalchemy import or_
query.filter(and_(User.id==1, User.name=='张岩林')).all()
query.filter(User.id==1, User.name=='张岩林').all()
query.filter(User.id==1).filter(User.name=='张岩林').all()
query.filter(or_(User.id==1, User.id==2)).all()

# count计算个数
session.query(User).count()

# 修改update
session.query(User).filter(User.id > 2).update({'name' : '张岩林'})

# 通配符
ret = session.query(User).filter(User.name.like('e%')).all()
ret = session.query(User).filter(~User.name.like('e%')).all()

# 限制
ret = session.query(User)[1:2]

# 排序
ret = session.query(User).order_by(User.name.desc()).all()
ret = session.query(User).order_by(User.name.desc(), User.id.asc()).all()

# 分组
from sqlalchemy.sql import func

ret = session.query(User).group_by(User.extra).all()
ret = session.query(
    func.max(User.id),
    func.sum(User.id),
    func.min(User.id)).group_by(User.name).all()

ret = session.query(
    func.max(User.id),
    func.sum(User.id),
    func.min(User.id)).group_by(User.name).having(func.min(User.id) >2).all()

# 连表

ret = session.query(User, Favor).filter(User.id == Favor.nid).all()

ret = session.query(User).join(Favor).all()

ret = session.query(User).join(Favor, isouter=True).all()


# 组合
q1 = session.query(User.name).filter(User.id > 2)
q2 = session.query(Favor.caption).filter(Favor.nid < 2)
ret = q1.union(q2).all()

q1 = session.query(User.name).filter(User.id > 2)
q2 = session.query(Favor.caption).filter(Favor.nid < 2)
ret = q1.union_all(q2).all()
```


### 一对多外键

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column,Integer,ForeignKey,UniqueConstraint,Index,String
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine


engine=create_engine('mysql+pymysql://root@127.0.0.1:3306/db1')

Base = declarative_base()

class Son(Base):
    __tablename__ = 'son'
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    age = Column(Integer())
    # 创建外键，对应父亲那张表的id项
    father_id = Column(Integer,ForeignKey('father.id'))

class Father(Base):
    __tablename__ = 'father'
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    age = Column(String(32))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

f1 = Father(name = 'zhangyanlin',age = '18')
session.add(f1)
session.commit()

w1 = Son(name = 'xiaozhang1', age = 3,father_id = 1)
w2 = Son(name = 'xiaozhang2', age = 3,father_id = 1)

session.add_all([w1,w2])
session.commit()
```

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column,Integer,ForeignKey,UniqueConstraint,Index,String
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine


engine = create_engine('mysql+pymysql://root@127.0.0.1:3306/db1')

Base = declarative_base()

class Son(Base):
    __tablename__ = 'son'
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    age = Column(Integer())

    father_id = Column(Integer,ForeignKey('father.id'))

class Father(Base):
    __tablename__ = 'father'
    id = Column(Integer,primary_key=True)
    name = Column(String(32))
    age = Column(String(32))
    son = relationship('Son')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

f1 = Father(name = 'zhangyanlin',age = '18')

w1 = Son(name = 'xiaozhang1',age = 3)
w2 = Son(name = 'xiaozhang2',age = 4)
# 重点是这里绑定关系
f1.son = [w1,w2]
# 只需要把父亲给传进去，儿子的自然就上传进去啦
session.add(f1)
session.commit()
```
