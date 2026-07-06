from fastapi import APIRouter, Query, Depends,HTTPException
from utils.response import success_response
from utils.auth import get_current_user
from models.userlogin import User
from config.set import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.favorite import NewsCollectionResponse,GetNewsId,NewsCollectionRequest,NewsCollectionListResponse,NewsItems
from crud.favorite import check_favorite_collection,add_favorite_collections,remove_favorite_collection,get_favorite_collections_lists,delete_list_collections
from starlette import  status

router = APIRouter(prefix="/api/favorite", tags=["favorite"])



@router.get("/check")
async def check_favorite_collections(news_id: int = Query(..., description="新闻ID", alias="newsId"),
                                    user: User = Depends(get_current_user),
                                    db: AsyncSession = Depends(get_db)
                                    ):

    is_favorite =await  check_favorite_collection(news_id, user, db)
    is_favorites =NewsCollectionResponse(isFavorite=is_favorite)
    return success_response(message="检查新闻收藏成功", data= is_favorites)

@router.post("/add")
async def add_favorite_collection(news: GetNewsId,
                                  user: User = Depends(get_current_user),
                                  db: AsyncSession = Depends(get_db)
                                  ):

   added_favorite_collections = await add_favorite_collections(news.news_id, user, db)
   data = NewsCollectionRequest.model_validate(
       added_favorite_collections
   ).model_dump(by_alias=True)
   return success_response(message="收藏成功", data=data)

@router.delete("/remove")
async def remove_favorite_collections(news_id: int = Query(..., description="新闻ID", alias="newsId"),
                                     user: User = Depends(get_current_user),
                                     db: AsyncSession = Depends(get_db)
                                     ):
    is_delete = await remove_favorite_collection(news_id, user, db)
    if is_delete:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
    return success_response(message="删除成功")

@router.get("/list")
async def get_favorite_list(user: User = Depends(get_current_user),
                            db: AsyncSession = Depends(get_db),
                            page: int = Query(1, description="页码", alias="page"),
                            page_size: int = Query(10,le=100, description="每页数量", alias="pageSize")
                            ):
    rows,total = await get_favorite_collections_lists(user, db, page, page_size)
    has_more = True if total > page * page_size else False
    content = [NewsItems(**row.model_dump()) for row in rows]
    return success_response(message="获取收藏列表成功", data=NewsCollectionListResponse(list=content,total=total,hasMore=has_more))

@router.delete("/clear")
async def clear_favorite_list(user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
     is_delete =await delete_list_collections(db=db,user=user)
     if is_delete:
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
     return success_response(message="清空收藏列表成功")




