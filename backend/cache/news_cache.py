#新闻相关的缓存方法：新闻分类的读取和写入
from typing import Dict, Any, Optional
from config.cache import set_cache
from config.cache import get_cache_json

#key-value
CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list:"
#获取新闻分类缓存
async def get_cached_categories():
    return await get_cache_json(CATEGORIES_KEY)


#写入新闻分类缓存:缓存的数据，过期时间
#分类,配置 7200； 列表 ：6000； 详情：1800； 验证码：120 -- 数据越稳定，缓存越长久，缓存越短，越容易失效
async def set_cached_categories(data : list[Dict[str,Any]],expire : int = 3600):
    return await set_cache(CATEGORIES_KEY,data,expire)



#定义新闻列表
#写入缓存
async def set_cached_news_list(category_id:Optional[int],page:int,page_size:int,news_list:list[Dict[str,Any]],expire:int=1800):
    #调用前面封装的redis方法
    category_part = category_id if category_id is not  None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{page_size}"
    await set_cache(key,news_list,expire)


#读取缓存
async def get_cached_news_list(category_id:Optional[int],page:int,page_size:int):
    category_part = category_id if category_id is not  None else "all"
    key = f"{NEWS_LIST_PREFIX}{category_part}:{page}:{page_size}"
    return await get_cache_json( key)