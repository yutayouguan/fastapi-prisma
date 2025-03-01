"""
Author: 王猛
Date: 2025-02-28 21:19:10
LastEditors: 王猛
LastEditTime: 2025-02-28 21:58:29
FilePath: /fastapi-prisma/prisma/partial_types.py
Description:

Copyright (c) 2025 by 王猛 wmdyx@outlook.com, All Rights Reserved.
"""

from prisma.models import User

User.create_partial("UserWithOutRelations", exclude={"dept", "posts", "roles"})
User.create_partial("UserWithOutPassword", include={"username", "email"})
User.create_partial("UserCreate", include={"username", "email"})
User.create_partial("UserUpdate", include={"username", "email"})
