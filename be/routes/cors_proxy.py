import hashlib

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pathlib import Path

cors_proxy_router = APIRouter(tags=["cors-proxy"], prefix="/cors-proxy")


@cors_proxy_router.api_route("/png/{arbitrary_path:path}")
async def proxy_png(arbitrary_path: str):
    if "../" in arbitrary_path:
        raise HTTPException(status_code=500, detail="No")

    arbitrary_file = Path(f"{Path(__file__).resolve().parent.parent}/static/img/{int(hashlib.sha1(arbitrary_path.encode('utf-8')).hexdigest(), 16)}.png")

    if arbitrary_file.is_file():
        return Response(arbitrary_file.read_bytes(), media_type="image/png")

    async with httpx.AsyncClient() as client:
        response = await client.get(url=arbitrary_path)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to proxy download of png")

        arbitrary_file.parent.mkdir(parents=True, exist_ok=True)
        with arbitrary_file.open("wb") as f:
            f.write(response.content)
        return Response(content=response.content,  media_type="image/png")
