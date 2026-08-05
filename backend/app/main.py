from fastapi import FastAPI

app = FastAPI(
    title="SmartRetail API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "SmartRetail API is running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }