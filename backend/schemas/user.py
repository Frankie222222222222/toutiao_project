from pydantic import  BaseModel,Field, ConfigDict
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str



class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

class UserInfoResponse(UserInfoBase):
    """
    用户信息响应模型
    """
    id: int
    username: str
    phone: Optional[ str] = Field(None,alias="手机号",max_length=20)

    model_config = ConfigDict(
        from_attributes=True,  # 允许从orm对象取值
    )

class UserAuthResponse(BaseModel):
    """
    用户登录响应模型
    """
    token: str
    user_info: UserInfoResponse
    #模型类配置
    model_config = ConfigDict(
        from_attributes=True, #允许从orm对象取值
        populate_by_name=True #alias /字段名兼容
    )

#更新用户信息的模型类
class UpdateUserInfo(BaseModel):
    nickname: str = None
    avatar: str = None
    gender: str = None
    bio: str = None
    phone: str = None

class UserChangePassword(BaseModel):
    old_password: str = Field(...,alias="旧密码",description="旧密码")
    new_password: str = Field(...,min_length=6,alias="新密码",description="新密码")

