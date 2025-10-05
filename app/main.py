from fastapi import FastAPI
from app.api import auth, watchlist
from app.db import Base, engine
from app.models import user_model, watchlist_model
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="StockBot Backend", version="1.0")

# ✅ Enable CORS for frontend communication
origins = [
    "*",  # Allow all origins for now (later replace with your Flask frontend URL)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(watchlist.router)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Root endpoint
@app.get("/")
def root():
    return {"message": "✅ StockBot backend is running properly!"}
