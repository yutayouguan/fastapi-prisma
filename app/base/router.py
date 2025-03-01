"""
Author: 王猛
Date: 2025-02-28 20:16:13
LastEditors: 王猛
LastEditTime: 2025-02-28 22:32:52
FilePath: /fastapi-prisma/app/base/router.py
Description:

Copyright (c) 2025 by 王猛 wmdyx@outlook.com, All Rights Reserved.
"""

from fastapi import APIRouter, Form, Query
from prisma.models import User
from models import user
from prisma.partials import UserWithOutPassword
from fastapi import HTTPException

router = APIRouter()


@router.get("/users/me")
async def read_users_me():
    return {"user_id": "the current user"}


@router.get("/users/{user_id}", response_model=UserWithOutPassword)
async def read_user(user_id: int) -> User | None:
    me: User | None = await user.get_user_by_id(user_id)
    if not me:
        raise HTTPException(status_code=404, detail="User not found")
    return me


@router.post("/users/", response_model=UserWithOutPassword)
async def add_user(
    name: str = Form(..., min_length=1, max_length=50),
    email: str = Form(..., min_length=1, max_length=50),
) -> User:
    try:
        result = await user.create_user(name, email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.get("/users/", response_model=list[UserWithOutPassword])
async def read_users(
    skip: int = Query(0, ge=0), limit: int = Query(10, ge=0)
) -> list[User]:
    return await user.get_users(skip=skip, limit=limit)


@router.patch("/users/{user_id}", response_model=UserWithOutPassword)
async def update_user(
    user_id: int,
    name: str = Form(..., min_length=1, max_length=50),
    email: str = Form(..., min_length=1, max_length=50),
) -> User | None:
    try:
        result = await user.update_user(user_id, name, email)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@router.delete("/users/{user_id}")
async def delete_user(user_id: int) -> User | None:
    res = await user.delete_user(user_id)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    return res
