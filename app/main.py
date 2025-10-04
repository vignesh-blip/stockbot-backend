from fastapi import FastAPI
from app.api import auth, watchlist
from app.db import Base, engine
from app.db import Base, engine
from app.models import user_model, watchlist_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="StockBot Backend", version="1.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(watchlist.router)

@app.get("/")
def root():
    return {"message": "✅ StockBot backend is running properly!"}
