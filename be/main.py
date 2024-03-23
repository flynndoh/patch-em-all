from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_db_and_tables
from routes.api_v1_router import api_v1_router

app = FastAPI()
app.include_router(api_v1_router)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    engine = await create_db_and_tables()
    yield
    await engine.dispose()


# Define your API routes here

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
