from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, ForeignKey, Table, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id:Mapped[str] = mapped_column(primary_key=True)
    name:Mapped[str]
    pictureUrl:Mapped[str] = mapped_column(nullable=True)
    email:Mapped[str] = mapped_column(nullable=True)
    password:Mapped[str] = mapped_column(nullable=True)

class Rss(Base):
    __tablename__ = "rss"

    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    source:Mapped[str]
    url:Mapped[str]
    fetched_at:Mapped[datetime] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<Rss(id={self.id}, source={self.source}, url={self.url})>"
class Article(Base):
    __tablename__ = "articles"

    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title:Mapped[str]
    engagement:Mapped[str] = mapped_column(nullable=True)
    public:Mapped[str] = mapped_column(nullable=True)
    regulation:Mapped[str] = mapped_column(nullable=True)
    innovation:Mapped[str] = mapped_column(nullable=True)
    deals:Mapped[str] = mapped_column(nullable=True)
    created_at:Mapped[datetime]

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title={self.title}, created_at={self.created_at})>"

class Link(Base):
    __tablename__ = "links"

    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    source:Mapped[str]
    title:Mapped[str]
    link:Mapped[str] = mapped_column(index=True)
    published_at:Mapped[datetime] = mapped_column(DateTime(timezone=True))
    text:Mapped[str] = mapped_column(default="")
    created_at:Mapped[datetime]

    def __repr__(self) -> str:
        return f"<Link(title={self.title}, link={self.link}), published_at={self.published_at}, created_at={self.created_at}>"
    
class FilteredLink(Base):
    __tablename__ = "filtered_links"

    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    source:Mapped[str]
    title:Mapped[str]
    link:Mapped[str]
    text:Mapped[str]
    category:Mapped[str] = mapped_column(default="")
    created_at:Mapped[datetime]

    def __repr__(self) -> str:
        return f"<FilteredLink(title={self.title}, link={self.link}), created_at={self.created_at}>"

class Collection(Base):
    __tablename__ = "collections"

    id:Mapped[uuid.UUID] = mapped_column(primary_key=True)
    user_id:Mapped[str] = mapped_column(index=True)
    article_id:Mapped[uuid.UUID] = mapped_column(index=True)                                