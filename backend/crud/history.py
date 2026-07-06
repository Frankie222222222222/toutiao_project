from models.history import History
from config.set import AsyncSession
from models.userlogin import User
from sqlalchemy.sql import  select,func,delete
from fastapi import  HTTPException
from starlette import  status
from datetime import  datetime
from models.news import News



async def add_history(news_id: int, user: User, db: AsyncSession):
    """
    添加历史记录
    :param news_id: 新闻ID
    :param user: 用户
    :param db: 数据库连接
    :return:
    """
    history = History(news_id=news_id, user_id=user.id)
    query = select(History).where(History.news_id == news_id, History.user_id == user.id)
    result = await db.execute(query)
    if result:
        history.view_time = datetime.now()
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def get_history_list(page: int, page_size: int, user: User, db: AsyncSession):
    """
    获取用户历史记录
    """
    offset = (page - 1) * page_size

    # 查询总数，不要加 offset 和 limit
    query1 = (
        select(func.count())
        .where(History.user_id == user.id)
    )

    result = await db.execute(query1)
    total = result.scalar()

    # 查询历史记录 + 新闻信息
    query2 = (
        select(
            News.id.label("id"),                      # 关键：补上 id
            History.id.label("history_id"),
            History.news_id.label("news_id"),
            History.view_time.label("history_view"),

            News.title.label("title"),
            News.description.label("description"),
            News.image.label("image"),
            News.author.label("author"),
            News.category_id.label("category_id"),
            News.views.label("views"),
            News.publish_time.label("publish_time"),
        )
        .join(News, History.news_id == News.id)
        .where(History.user_id == user.id)
        .order_by(History.view_time.desc())
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(query2)

    # 多字段查询必须用 mappings()
    history_list = result.mappings().all()

    return history_list, total


async def delete_history(user: User, db: AsyncSession,history_id : int):
    """
    删除用户所有历史记录
    """
    query = delete(History).where(History.news_id == history_id, History.user_id == user.id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0

async def delete_all_history(user: User, db: AsyncSession):
    """
    删除用户所有历史记录
    """
    query = delete(History).where(History.user_id == user.id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0


