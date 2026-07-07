
from models.userlogin import User
from utils.response import success_response
from utils.auth import get_current_user
from  fastapi import APIRouter,Depends,Query,HTTPException
from config.set import get_db,AsyncSession
from crud.userlogin import  get_user_by_username,create_user,create_token,authenticate_user,update_user_info,update_password
from schemas.user import UserLogin, UpdateUserInfo,UserChangePassword
from starlette import status
from schemas.user import UserInfoResponse,UserAuthResponse

router = APIRouter(prefix="/api/user",tags=["user"])




@router.post("/register")
async def register(user_data : UserLogin,db:AsyncSession = Depends(get_db)):

    user = await  get_user_by_username(db,user_data.username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    user = await create_user(db,user_data)
    token = await create_token(db,user.id)


    response_data = UserAuthResponse(token=token,user_info = UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)


    # return {"code": 200,
    #         "message": "用户已存在",
    #         "data": {
    #             "token": token,
    #             "username": user_info.username,
    #             "nickname": user_info.nickname,
    #             "bio": user_info.bio,
    #             "avatar": user_info.avatar,
    #             "phone": user_info.phone,
    #             "gender": user_info.gender
    #          }
    #         }

@router.post("/login")
async def login(user_data : UserLogin,db:AsyncSession = Depends(get_db)):
    #登录逻辑：验证用户是否存在->验证密码->生成token->返回token和用户信息
    user = await authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户不存在")
    token = await create_token(db,user.id)
    user_info = UserInfoResponse.model_validate(user)
    return success_response(message="登录成功",data=UserAuthResponse(token=token,user_info=user_info))


#查Token->封装crud->功能整合成一个工具函数->路由导入使用
@router.get("/info")
async def get_current_user_info(user:User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

#修改用户信息：验证token，更新（用户输入数据put提交），请求体参数，模型类验证
@router.put("/update")
async def update_user(user_data:UpdateUserInfo,
                           user:User = Depends(get_current_user),
                           db:AsyncSession = Depends(get_db)):
    updated_user = await update_user_info(db,user.username,user_data)
    updated_user = UserInfoResponse.model_validate(updated_user)
    return success_response(message="修改用户信息成功",data=updated_user)

@router.put("/password")
async def update_password(user_data: UserChangePassword,
                           user:User = Depends(get_current_user),
                           db:AsyncSession = Depends(get_db)):
    res_change_pwd = await update_password(db,user,user_data.old_password,user_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="修改密码失败")
    return success_response(message="修改密码成功")