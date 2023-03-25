from fastapi import FastAPI
import uvicorn
from router import user_router

app = FastAPI()

app.include_router(user_router.router)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")
