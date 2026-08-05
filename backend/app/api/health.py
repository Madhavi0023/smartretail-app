from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
def root():
    return {
        "message": "SmartRetail API is running"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.get("/health/live")
def liveness():
    return {
        "status": "alive"
    }


@router.get("/health/ready")
def readiness():
    return {
        "status": "ready"
    }