from fastapi import FastAPI
from app.api.v1 import endpoints
from fastapi.middleware.cors import CORSMiddleware
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("critical_tutor")

app = FastAPI(
    title="Critical Thinking Tutor",
    description="Backend API for a user-driven critical thinking and philosophical reasoning tutor.",
    version="0.1.0"
)

# CORS middleware (optional for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(endpoints.router, prefix="/api/v1")

# Health check endpoint
@app.get("/health", summary="Check API status")
def health_check():
    return {"status": "ok", "message": "Critical Thinking Tutor API is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)