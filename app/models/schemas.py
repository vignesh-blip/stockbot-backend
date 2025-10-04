from pydantic import BaseModel

class WatchlistCreate(BaseModel):
    user_id: int
    symbol: str
