from fastapi import FastAPI
from routers import waha_router

app = FastAPI(
    title="API",
    description="Webhook para whatsapp",
    version="0.1.0"
)

app.include_router(waha_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="0.0.0.0", port=8000)