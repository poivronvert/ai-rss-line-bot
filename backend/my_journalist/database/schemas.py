from typing import Optional
from pydantic import BaseModel

class ArticleResponse(BaseModel):
    id: str

class ArticleDetails(BaseModel):
    title: str
    engagement: str
    public: str
    regulation: str
    innovation: str
    deals: str
    links: dict
    in_collection: bool

class BroadcastPayload(BaseModel):
    token: str

class PostPayload(BaseModel):
    token: str

class PaginationResponse(BaseModel):
    totalPages: int
    pageWindowSize: int

class Post(BaseModel):
    id:str
    imageUrl:Optional[str] = "/assets/robot.jpeg"
    name:str
    in_collection:bool
    collection_count:int

class PostDetail(BaseModel):
    posts: list[Post]

class TotalPages(BaseModel):
    totalPages: int

class Token(BaseModel):
    token: str
    token_type: str

class UserInput(BaseModel):
    name: str
    email: str
    password: str

class UserSignin(BaseModel):
    email: str
    password: str

class LineUser(BaseModel):
    id: str
    name: str
    pictureUrl: str