from pydantic import BaseModel
from typing import Optional


class VerifyBody(BaseModel):
    user_id: int
    username: Optional[str] = None
    bot_name: str = "unknown"
    days: int = 0
    expected_amount: float = 0.0
