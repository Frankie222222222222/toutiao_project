from typing import Any
import os
import  redis.asyncio as redis,json
from dotenv import load_dotenv


load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB ")
#创建redis的连接对象
redis_client = redis.Redis(host=REDIS_HOST, # redis服务地址
                           port= int(REDIS_PORT), # redis端口号
                           db=REDIS_DB, # redis数据库编号
                           decode_responses= True # 是否将字节数据解码为字符串
 )

#设置和读取（字符串，列表和字典）
#读取：字符串
async def get_cache(key :str):
    try:
        return redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败{e}")
        return None

#读取：列表和字典
async def get_cache_json(key :str):
    try:
         data = await redis_client.get(key)
         if data:
             return json.loads(data)
         return None
    except Exception as e:
        print(f"获取JSON缓存失败{e}")
        return None

#设置缓存
async def set_cache(key : str,value : Any ,expire : int = 3600):
    try:
        if isinstance(value,dict) or isinstance(value,list):
            # 将字典或者列表转换成JSON字符串
            value = json.dumps(value,ensure_ascii=False) #中文正常保存
        await redis_client.set(key,value,expire)
        return True
    except Exception as e:
        print(f"设置缓存失败{e}")
        return False

