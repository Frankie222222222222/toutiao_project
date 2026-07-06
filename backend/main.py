from fastapi import APIRouter, FastAPI
from routers import news,userlogin,favorite,history
from config.set import  async_engine
from models.news import Base
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handles import register_exception_handles

app = FastAPI()
register_exception_handles(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #允许的源
    allow_credentials=True,#允许的cookie
    allow_methods=["*"],#允许的请求方法
    allow_headers=["*"],#允许的请求头
)

@app.get("/")
async def index():
    return {"message": "Hello FastAPI"}

@app.on_event("startup")
async def startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

#挂载路由
app.include_router(news.router)
app.include_router(userlogin.router)
app.include_router(favorite.router)
app.include_router(history.router)