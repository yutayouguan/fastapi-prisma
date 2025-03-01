"""
Author: 王猛
Date: 2024-12-24 22:01:33
LastEditors: 王猛
LastEditTime: 2025-03-01 19:52:43
FilePath: /fastapi-prisma/app/main.py
Description:

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from databases import db
from base.router import router as base_router
from posts.router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app


app: FastAPI = create_app()

app.include_router(base_router, tags=["用户"])
app.include_router(posts_router, tags=["文章"])