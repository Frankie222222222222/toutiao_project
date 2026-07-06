from pydantic import  BaseModel,Field,ConfigDict
from datetime import  datetime
from utils.Base import NewsItemBase

class Base (BaseModel):
    pass
class HistoryNewId(Base):
    id: int = Field(default=1,description="历史ID",alias="newsId")



class HistoryResponse(Base):
    id: int = Field(...,description="历史ID",alias="id")
    user_id: int = Field(..., description="用户ID", alias="userId")
    news_id: int = Field(...,description="新闻ID",alias="newsId")
    view_time: datetime = Field(...,description="浏览时间",alias="viewTime")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # 允许从orm对象取值
    )

class HistoryRequestResponse(NewsItemBase):
    history_view : datetime = Field(...,description="浏览时间",alias="viewTime")
    history_id: int = Field(alias="historyId")
    news_id: int = Field(alias="newsId")
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True  # 允许从orm对象取值
    )

class HistoryListFinalResponse(Base):
    history_list: list[HistoryRequestResponse] = Field(..., description="历史列表", alias="list")
    total: int = Field(...,description="总条数",alias="total")
    has_more: bool = Field(...,description="是否有更多",alias="hasMore")