import asyncio,logging

import aiomysql

#创建连接池 每个HTTP请求都从连接池中直接获取数据库连接
@asyncio.coroutine
def create_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool=yield from aiomysql.create_pool(
    host=kw.get('host', 'localhost'),#返回键的值，若不存在返回默认值
    port=kw.get('port',3306),
    user=kw['user'],
    password=kw['password'],
    db=kw['db'],
    charset=kw.get('charset','utf8'),
    autocommit=kw.get(autocommit, True),
    maxsize=kw.get('maxsize',10),
    minsize=kw.get('minsize',1),
    loop=loop
)

@asyncio.coroutine
def select(sql,args,size=None):
    log(sql,args)
    global __pool
    with(yield from __pool)as conn:
        cur=yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs=yield from cur.fetchmany(size)
        else:
            rs=yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returnd:%s'%len(rs))
        return rs
        
