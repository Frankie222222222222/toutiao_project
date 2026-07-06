from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,update
from models.news import Categories,News
from config.set import get_db
from fastapi import Depends

async  def get_categories(db : AsyncSession,skip : int = 0, limit : int = 10):
    stmt = select(Categories).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all ()
    return categories

async def get_news_list(db : AsyncSession,category_id : int ,
                        skip : int = 0,
                        limit : int = 10
                        ):

    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


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
