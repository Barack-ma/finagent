from fastapi import FastAPI

app = FastAPI(
    title="FinAgent API",
    description="AI-powered lending operations agent",
    version="0.1.0",
)

@app.get("/health")
def health_check():
    return {"status": "ok"}