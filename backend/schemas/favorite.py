from pydantic import  BaseModel,Field,ConfigDict
from datetime import  datetime
from utils.Base import NewsItemBase

class Base (BaseModel):
    pass

class NewsCollectionResponse(Base):
    isFavorite : bool= Field(...,description="是否收藏",alias="isFavorite")



class GetNewsId( Base):
    news_id: int = Field(...,description="新闻ID",alias="newsId")


class NewsCollectionRequest(Base):

    id : int = Field(...,description="收藏ID",alias="id")
    user_id: int = Field(..., description="用户ID", alias="userId")
    news_id: int = Field(...,description="新闻ID",alias="newsId")
    created_at: datetime = Field(...,description="收藏时间",alias="createTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # 允许从orm对象取值
    )

class NewsItems(NewsItemBase):

    id: int = Field(...,description="收藏ID",alias="id")
    user_id: int = Field(..., description="用户ID", alias="userId")
    news_id: int = Field(...,description="新闻ID",alias="newsId")
    created_at: datetime = Field(...,description="收藏时间",alias="createTime")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从orm对象取值
    )



class NewsCollectionListResponse(Base):

    news_list: list[NewsItems] = Field(..., description="新闻列表", alias="list")
    total: int = Field(...,description="总条数",alias="total")
    has_more: bool = Field(...,description="是否有更多",alias="hasMore")


