from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Integer, String, Float, DateTime, Text, BigInteger, Boolean, func
)
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class UTR(Base):
    """
    Single source of truth for every UTR. Primary key is UTR itself —
    one row per UTR ever, no duplication across tables.
    """
    __tablename__ = 'utrs'

    utr:          Mapped[str]                = mapped_column(String(50), primary_key=True)

    # SMS side — filled when bank SMS arrives (or admin /addpayment)
    amount:       Mapped[Optional[float]]    = mapped_column(Float, nullable=True)
    sender:       Mapped[Optional[str]]      = mapped_column(String(200), nullable=True)
    sms_date:     Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    raw_sms:      Mapped[Optional[str]]      = mapped_column(Text, nullable=True)
    sms_at:       Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # User side — filled when user submits UTR via bot
    user_id:         Mapped[Optional[int]]      = mapped_column(BigInteger, nullable=True, index=True)
    username:        Mapped[Optional[str]]      = mapped_column(String(100), nullable=True)
    bot_name:        Mapped[Optional[str]]      = mapped_column(String(100), nullable=True, index=True)
    days:            Mapped[Optional[int]]      = mapped_column(Integer, nullable=True)
    expected_amount: Mapped[Optional[float]]    = mapped_column(Float, nullable=True)
    submitted_at:    Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Final state
    redeemed:     Mapped[bool]               = mapped_column(Boolean, default=False, nullable=False, index=True)
    redeemed_at:  Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_at:   Mapped[datetime]           = mapped_column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<UTR(utr='{self.utr}', user_id={self.user_id}, amount={self.amount}, redeemed={self.redeemed})>"
