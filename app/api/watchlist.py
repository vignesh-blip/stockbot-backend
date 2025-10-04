from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.watchlist_model import Watchlist
from app.models.schemas import WatchlistCreate

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])


# ➕ Add a stock symbol to a user's watchlist
@router.post("/add")
def add_to_watchlist(data: WatchlistCreate, db: Session = Depends(get_db)):
    # Check if symbol already exists for this user
    existing = db.query(Watchlist).filter_by(user_id=data.user_id, symbol=data.symbol).first()
    if existing:
        return {"message": f"{data.symbol} already in watchlist."}

    # Add new watchlist entry
    new_item = Watchlist(user_id=data.user_id, symbol=data.symbol)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "message": f"{data.symbol} added successfully.",
        "entry": {"id": new_item.id, "symbol": new_item.symbol},
    }


# 📋 Get all symbols for a user's watchlist
@router.get("/")
def get_watchlist(user_id: int, db: Session = Depends(get_db)):
    items = db.query(Watchlist).filter(Watchlist.user_id == user_id).all()
    return {
        "user_id": user_id,
        "watchlist": [{"id": i.id, "symbol": i.symbol} for i in items],
    }


# ❌ Remove a symbol from a user's watchlist
@router.delete("/remove")
def remove_from_watchlist(user_id: int, symbol: str, db: Session = Depends(get_db)):
    item = db.query(Watchlist).filter_by(user_id=user_id, symbol=symbol).first()

    if not item:
        return {"error": f"{symbol} not found in watchlist."}

    db.delete(item)
    db.commit()
    return {"message": f"{symbol} removed successfully."}
