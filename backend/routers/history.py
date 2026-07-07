
from fastapi import  APIRouter,Depends,Query,Path,HTTPException
from schemas.history import HistoryNewId
from models.userlogin import User
from utils.auth import get_current_user
from config.set import get_db
from sqlalchemy.ext.asyncio import  AsyncSession
from crud.history import  add_history,get_history_list,delete_history,delete_all_history
from schemas.history import HistoryResponse,HistoryRequestResponse,HistoryListFinalResponse
from utils.response import success_response
from starlette import  status


router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_histories(history: HistoryNewId,
                      user: User = Depends(get_current_user) ,
                      db : AsyncSession = Depends(get_db)
                      ):
    added_history = await add_history(history.id, user, db)
    data = HistoryResponse.model_validate(added_history).model_dump(by_alias=True)
    success_response(message="添加历史记录成功", data=data)


@router.get("/list")
async def get_history_lists_api(user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db),
                           page: int = Query(1, description="页码", alias="page"),
                           page_size: int =Query(10,le=100,ge=1, description="每页数量", alias="pageSize"),
                           ):
    history_list, total = await get_history_list(page, page_size, user, db)
    is_more = True if total > page_size * page else False
    history_lists =[HistoryRequestResponse.model_validate(item).model_dump(by_alias=True) for item in history_list]
    data = HistoryListFinalResponse(list=history_lists, total=total, hasMore=is_more)
    return success_response(message="获取历史记录成功", data=data.model_dump(by_alias=True))


@router.delete("/delete/{history_id}")
async def delete_history_api(history_id: int = Path(..., description="历史ID", alias="history_id") ,
                         user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)
                         ):
   is_delete = await delete_history(history_id =history_id, user= user, db=db)
   if is_delete:
       raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除失败")
   return success_response(message="删除成功")


@router.delete("/clear")
async def clear_favorite_list(user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
        is_delete_all =await delete_all_history(db=db,user=user)
        
        return success_response(message="清空历史记录成功")


