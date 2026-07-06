from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import  select
from config.set import get_db
from utils.security import get_hash_password,verify_password
from crud.userlogin import get_user_by_token
from starlette import  status


#整合根据token查询用户
async def get_current_user(authorization: str = Header(...,alias="Authorization"),
                           db: AsyncSession = Depends(get_db)
                           ):
    token = authorization.replace("Bearer ", "")
    user = await get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户不存在")
    return user