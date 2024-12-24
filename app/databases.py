"""
Author: 王猛
Date: 2024-12-24 23:19:29
LastEditors: 王猛
LastEditTime: 2024-12-24 23:21:16
FilePath: /fastapi-prisma/app/databases.py
Description:

Copyright (c) 2024 by 王猛 wmdyx@outlook.com, All Rights Reserved.
"""

from prisma import Prisma

prisma = Prisma()


async def get_db():
    await prisma.connect()
    yield prisma
    await prisma.disconnect()
