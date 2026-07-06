from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,update
from models.news import Categories,News
from cache.news_cache import get_cached_categories, set_cached_categories, get_cached_news_list, set_cached_news_list
from fastapi.encoders import jsonable_encoder
from utils.Base import NewsItemBase


#写入缓存
#返回数据
async  def get_cache_categories(db : AsyncSession,skip : int = 0, limit : int = 10):
    #先尝试从缓存中获取数据
    cached_categories = await get_cached_categories()
    if cached_categories:
        return cached_categories
    stmt = select(Categories).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all ()


#写入缓存
    if categories:
        categories = jsonable_encoder( categories)
        await set_cached_categories(categories)
#返回数据
    return  categories


async def get_caches_news_list(db : AsyncSession,category_id : int ,
                        skip : int = 0,
                        limit : int = 10
                        ):
    #先尝试从缓存获取数据
    news_cache_list = await get_cached_news_list(category_id,skip,limit)
    if news_cache_list:
        return  [News(**item) for item in news_cache_list]
    #查询的是指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    news_list =result.scalars().all()
    #写入缓存
    if news_list:
        #先把ORM转换成字典才能写入缓存
        #需要先转换成pydantic类型然后转换成字典
        news_list_prepared_caches = [NewsItemBase.model_validate( item ).model_dump(by_alias= False,mode="json") for item in news_list]
        await set_cached_news_list(category_id, skip, limit, news_list_prepared_caches)

        # news_list = jsonable_encoder(news_list)
        # caches_list = [News(**item) for item in news_list]
        # await set_cached_news_list(category_id, skip, limit, caches_list)
    #将数据添加写进缓存
    return news_list


async def get_news_count(category_id : int,db : AsyncSession):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_news_detail(news_id : int,db : AsyncSession):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def increase_news_views(news_id : int,db : AsyncSession):
    stmt = update(News).where(News.id == news_id).values(views = News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def get_news_related(news_id : int,db : AsyncSession,category_id : int,limit : int = 5):
    stmt = select(News).where(
        News.category_id == category_id,
        News.id != news_id
    ).order_by(
        News.views.desc()
    ).limit(limit)
    result = await db.execute(stmt)
    related_news = result.scalars().all()

    return [{ "id" : news_detail.id,
                "title" : news_detail.title,
                "content" : news_detail.content,
                "image" : news_detail.image,
                "author" : news_detail.author,
                "categoryId" : news_detail.category_id,
                "views" : news_detail.views,
                "publish_time" : news_detail.publish_time} for news_detail in related_news]
