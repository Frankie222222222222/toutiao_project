from models.news import News
from sqlalchemy.ext.asyncio import  AsyncSession
from models.userlogin import User
from sqlalchemy import select,delete,func
from models.favorite import Favorite

"""
   检查新闻是否被收藏
   :param news_id:
   :return:
   """
async def check_favorite_collection(news_id: int,user:User,db: AsyncSession):
    query = select(Favorite).where(Favorite.news_id == news_id,Favorite.user_id == user.id)
    result = await db.execute(query)
    is_favorite = result.scalar_one_or_none()
    return is_favorite is not None

async def add_favorite_collections(news_id: int,user:User,db: AsyncSession):
    add_favorite_collection = Favorite(user_id=user.id,news_id=news_id)
    db.add(add_favorite_collection)
    await db.commit()
    await db.refresh(add_favorite_collection)
    return add_favorite_collection

async def remove_favorite_collection(news_id: int,user:User,db: AsyncSession):
    query = delete(Favorite).where(Favorite.news_id == news_id,Favorite.user_id == user.id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0



async def get_favorite_collections_lists(user:User,db: AsyncSession, page: int = 1, page_size: int = 10):
    count_query1 = select(func.count()).where(Favorite.user_id == user.id).offset((page - 1) * page_size).limit(page_size)
    count_result = await db.execute(count_query1)
    total = count_result.scalar_one()

    skip = (page - 1) * page_size

    query2 = (select(Favorite,Favorite.created_at.label("favorite_time"),Favorite.id.label("favorite_id"))
              .join(News.id ==Favorite.news_id)
              .where(Favorite.user_id == user.id).
              offset(skip).limit(page_size))

    result = await db.execute(query2)
    rows = result.all()
    return  rows,total


async def delete_list_collections(db: AsyncSession, user: User):
    query = delete(Favorite).where(Favorite.user_id == user.id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


