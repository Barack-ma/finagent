from fastapi import FastAPI

from app.api.customers import router as customers_router


app = FastAPI(
    title="FinAgent API",
    description="AI-powered lending operations agent",
    version="0.1.0",
)


app.include_router(customers_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

"""
Create app
    ↓
attach routers
    ↓
define basic infrastructure endpoints
"""