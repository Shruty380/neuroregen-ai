from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import diseases

# Create the FastAPI app
app = FastAPI(
    title="NeuroRegen AI API",
    description="Bioinformatics API for neurodegenerative disease research",
    version="1.0.0"
)

# Allow your Next.js frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

# Register our disease routes
app.include_router(diseases.router)

@app.get("/")
def root():
    return {
        "platform": "NeuroRegen AI",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}