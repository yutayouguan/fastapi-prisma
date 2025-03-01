"""
Author: 王猛
Date: 2025-02-28 20:33:33
LastEditors: 王猛
LastEditTime: 2025-02-28 22:29:30
FilePath: /fastapi-prisma/app/models/user.py
Description:

Copyright (c) 2025 by 王猛 wmdyx@outlook.com, All Rights Reserved.
"""

from databases import db
from prisma.models import User


async def get_user_by_id(user_id: int) -> User | None:
    return await db.user.find_first(
        where={"id": user_id}, include={"dept": False, "posts": False, "roles": False}
    )


async def create_user(name: str, email: str) -> User:
    user = await db.user.create(data={"username": name, "email": email})
    return user


async def get_users(skip: int = 0, limit: int = 10) -> list[User]:
    return await db.user.find_many(skip=skip, take=limit)


async def delete_user(user_id: int) -> User | None:
    return await db.user.delete(where={"id": user_id})


async def update_user(user_id: int, name: str, email: str) -> User | None:
    return await db.user.update(
        where={"id": user_id}, data={"username": name, "email": email}
    )
