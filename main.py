from fastapi import FastAPI

from app.apis.generate_agenda import router as agenda_router
from app.apis.generate_summary import router as summary_router

app = FastAPI()

app.include_router(agenda_router)
app.include_router(summary_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
