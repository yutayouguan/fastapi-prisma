"""
Author: 王猛
Date: 2024-12-24 22:01:33
LastEditors: 王猛
LastEditTime: 2024-12-24 23:31:51
FilePath: /fastapi-prisma/app/main.py
Description:

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager
from prisma import Prisma

prisma = Prisma()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    yield
    await prisma.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app


app: FastAPI = create_app()
