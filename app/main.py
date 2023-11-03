from fastapi import FastAPI
from .routers import search, eco_scoring, test
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定
origins = ["http://localhost:3000", "https://www.yobiwave.com"]  # アクセスを許可するオリジンを指定

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(search.router)
app.include_router(eco_scoring.router)
app.include_router(test.router)