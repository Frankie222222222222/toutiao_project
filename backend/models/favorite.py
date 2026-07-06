from datetime import datetime
from sqlalchemy import (
    UniqueConstraint,
    Index,
    Integer,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.news import News
from models.userlogin import User


class Base(DeclarativeBase):
    pass


class Favorite(Base):
    """
    收藏表 ORM 模型
    """
    __tablename__ = "favorite"

    __table_args__ = (
        #当前新闻只能收藏一次
        UniqueConstraint("user_id", "news_id", name="user_news_unique"),
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_news_idx", "news_id"),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="收藏ID"
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(User.id),
        nullable=False,
        comment="用户ID"
    )

    news_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(News.id),
        nullable=False,
        comment="新闻ID"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="收藏时间"
    )

    def __repr__(self):
        return (
            f"<Favorite("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"news_id={self.news_id}, "
            f"created_at={self.created_at}"
            f")>"
        )