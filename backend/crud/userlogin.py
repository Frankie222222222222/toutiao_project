import uuid
from datetime import datetime,timedelta

from fastapi import HTTPException

from config.set import AsyncSession
from sqlalchemy.sql import select,update
from models.userlogin import User,UserToken
from schemas.user import UserLogin,UpdateUserInfo
from utils.security import get_hash_password,verify_password

#查询用户
async  def get_user_info(username: str,db: AsyncSession):
    result = await db.execute(select(User).where(User.username == username))
    user_info = result.scalar_one_or_none()
    return user_info

#创建用户
async def create_user(db: AsyncSession,user_data:UserLogin):
    #先密码加密处理->然后数据库新增
    hashed_password =get_hash_password(user_data.password)
    user = User(username=user_data.username,password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user) #从数据库都会最新的user
    return user


#生产token
async def create_token(db: AsyncSession,user_id : int):
    # 生成token+设置过期时间->查询当前数据库用户是否有token->没有则创建|否则更新
    token = str(uuid.uuid4())
    expire_at = datetime.now() + timedelta(days=7)
    result = await db.execute(select(UserToken).where(UserToken.user_id == user_id))
    user_token = result.scalar_one_or_none()
    if user_token:
        user_token.token = token
        user_token.expires_at = expire_at
    else:
        user_token = UserToken(user_id=user_id,token=token,expires_at=expire_at)
        db.add(user_token)
        await db.commit()
    return token


async def authenticate_user(db: AsyncSession,username: str,password :str):
    user = await get_user_info(username,db)
    if not user:
        return None
    if not verify_password(password,user.password):
        return None
    return user


#根据token查询用户
async def get_user_by_token(db: AsyncSession,token : str):
    result = await db.execute(select(UserToken).where(UserToken.token == token))
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None
    query = select(User).where(User.id == db_token.user_id)
    user = await db.execute(query)
    return user.scalar_one_or_none()



#更新用户信息
async def update_user_info(db: AsyncSession,
                           user_name : str,
                           user_data: UpdateUserInfo):
    #update(User).where(User.username == user_name).values(字段=值，字段=值))
    #user_data 是一个pydantic类型，得到字典，**解包
    #没有设置值的不更新
    query = update(User).where(User.username == user_name).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none= True
    ))
    result = await db.execute(query)
    await db.commit()

    #检查更新
    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="用户不存在")

    #获取更新后的信息
    updated_user = await  get_user_info(user_name,db)
    return updated_user

#修改密码： 验证旧密码->更新新密码
async def update_password(db: AsyncSession,
                          user:User,
                          old_password: str,
                          new_password: str):
    if not verify_password(old_password,user.password):
        return False
    hashed_user_password = get_hash_password(new_password)
    user.password = hashed_user_password
    #更新由sqlalchemy真正接管这个User对象，确保可以提交，规避session过期或者关闭导致不能提交的问题
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True