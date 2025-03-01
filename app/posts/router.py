"""
Author: 王猛
Date: 2025-02-28 20:15:39
LastEditors: 王猛
LastEditTime: 2025-02-28 23:18:49
FilePath: /fastapi-prisma/app/posts/router.py
Description:

Copyright (c) 2025 by 王猛 wmdyx@outlook.com, All Rights Reserved.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status
import aiofiles
from pathlib import Path

from fastapi.responses import JSONResponse, StreamingResponse
import urllib.parse

router = APIRouter()

UPLOAD_DIR = "./uploads"
# 创建上传文件目录，如果不存在，则创建，存在则忽略
# parents=True表示创建多级目录，exist_ok=True表示如果目录已经存在，不会抛出异常
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)


@router.post("/upload/")
async def upload(file: UploadFile):
    """上传文件"""
    if file.filename:
        try:
            file_path = Path(UPLOAD_DIR) / file.filename
            async with aiofiles.open(file_path, "wb") as out_file:
                while content := await file.read(1024 * 1024):
                    await out_file.write(content)
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"msg": "上传成功", "file": file.filename},
            )
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="文件名为空"
        )


@router.post("/uploads/")
async def uploads(files: list[UploadFile]) -> JSONResponse:
    """
    ## 上传多个文件
    - `files`: list[UploadFile] - 文件列表 \n
    - `返回值`: JSONResponse - 返回上传成功的文件列表
    """
    for file in files:
        if file.filename:
            try:
                file_path = Path(UPLOAD_DIR) / file.filename
                async with aiofiles.open(file_path, "wb") as out_file:
                    while content := await file.read(1024 * 1024):
                        await out_file.write(content)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="文件名为空"
            )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"msg": "上传成功", "file": [file.filename for file in files]},
    )


@router.get("/download/{file_name}")
async def download(file_name: str) -> StreamingResponse:
    """下载文件"""
    file_path = Path(UPLOAD_DIR) / file_name
    if not file_path.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文件不存在")

    async def iterfile(file_path):
        async with aiofiles.open(file_path, mode="rb") as f:
            while chunk := await f.read(1024 * 1024):  # 1MB
                yield chunk

    return StreamingResponse(
        content=iterfile(file_path),
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{urllib.parse.quote(file_name)}"
        },
    )
    # 格式是filename*=charset''encoded-value，其中charset是字符集，encoded-value是编码后的文件名。UTF-8表示字符集是UTF-8，encoded-value是编码后的文件名。
    # Content - Disposition头用于描述如何处理响应的内容
