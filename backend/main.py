from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import diseases, bio_tools, ai_models, exports

# Create the FastAPI app
app = FastAPI(
    title="NeuroRegen AI API",
    description="Bioinformatics API for neurodegenerative disease research",
    version="1.0.0"
)

# Allow your Next.js frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables automatically on startup
Base.metadata.create_all(bind=engine)

# Auto-seed database if empty
from app.database import SessionLocal
from app import models as _models
def auto_seed():
    db = SessionLocal()
    if db.query(_models.Disease).count() == 0:
        db.close()
        try:
            import sys
            import os
            sys.path.insert(0, os.path.dirname(__file__))
            import seed_data
            seed_data.seed()
        except Exception as e:
            print(f"Seeding failed: {e}")
    else:
        db.close()

auto_seed()

# Register our disease routes
app.include_router(diseases.router)
app.include_router(bio_tools.router)
app.include_router(ai_models.router)
app.include_router(exports.router)
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

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)