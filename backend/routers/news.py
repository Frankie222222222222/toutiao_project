from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.news import get_categories,get_news_list,get_news_count,get_news_detail,increase_news_views,get_news_related
from config.set import get_db
from crud.news_cache import get_cache_categories, get_caches_news_list

#创建APIRouter实例
router = APIRouter(prefix="/api/news",tags=["news"])




@router.get("/categories")
async def ger_categories(skip : int = 0, limit : int = 10,db : AsyncSession = Depends(get_db)):
    categories = await get_cache_categories(db,skip=skip,limit=limit)
    return {"code": 200,
            "message" :"获取新闻分类成功",
            "data": categories
            }

@router.get("/list")
async def ger_news_list(category_id : int = Query(...,alias="categoryId"),
                        page : int = 1,
                        page_size : int = Query(10,alias="pageSize",le=100),
                        db : AsyncSession = Depends(get_db)):
    offset = (page-1)*page_size
    news_list = await get_caches_news_list( db=db,
    category_id=category_id,
    skip=(page - 1) * page_size,
    limit=page_size)
    total = await get_news_count(category_id = category_id,db=db)
    has_more = True if total > offset + page_size else False


    return {"code": 200,
            "message" :"获取新闻列表成功",
            "data": {
                "list" : news_list,
                "total" : total ,
                "hasMore":has_more

             }
            }

@router.get("/detail")
async def ger_news_detail(news_id : int = Query(...,alias="id"),db : AsyncSession = Depends(get_db)):
    news_detail = await get_news_detail(news_id,db)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")

    views_res = await increase_news_views(news_id,db)
    if not views_res:
        raise HTTPException(status_code=500,detail="更新新闻浏览量失败")
    related_news = await get_news_related(news_id,db,news_detail.category_id)
    return {"code": 200,
            "message" :"获取新闻详情成功",
            "data": {
                "id" : news_detail.id,
                "title" : news_detail.title,
                "content" : news_detail.content,
                "image" : news_detail.image,
                "author" : news_detail.author,
                "categoryId" : news_detail.category_id,
                "views" : news_detail.views,
                "publish_time" : news_detail.publish_time,
                "relatedNews" : related_news
             }
    }

