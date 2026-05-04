from datetime import datetime
from typing import Optional
from sqlalchemy import select, desc, func, text

from .engine import engine, async_session
from .models import Base, UTR


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(
            "ALTER TABLE utrs ADD COLUMN IF NOT EXISTS expected_amount DOUBLE PRECISION"
        ))
        await conn.execute(text(
            "ALTER TABLE utrs ADD COLUMN IF NOT EXISTS username VARCHAR(100)"
        ))


async def record_sms(
    utr: str, amount: float, sender: str, sms_date: datetime,
    raw_sms: str, received_at: Optional[datetime] = None,
) -> tuple[str, UTR]:
    async with async_session() as session:
        async with session.begin():
            row = await session.scalar(select(UTR).where(UTR.utr == utr))
            if row:
                if row.amount is not None:
                    return "duplicate", row
                row.amount, row.sender, row.sms_date = amount, sender, sms_date
                row.raw_sms, row.sms_at = raw_sms, (received_at or datetime.now())
                if row.user_id:
                    if row.expected_amount and abs(amount - row.expected_amount) > 0.01:
                        return "amount_mismatch", row
                    return "auto_verified", row
                return "sms_only_updated", row
            session.add(UTR(
                utr=utr, amount=amount, sender=sender,
                sms_date=sms_date, raw_sms=raw_sms,
                sms_at=received_at or datetime.now(),
            ))
            return "new", None


async def get_utr(utr: str) -> Optional[UTR]:
    async with async_session() as session:
        return await session.scalar(select(UTR).where(UTR.utr == utr))


async def submit_utr(
    utr: str, user_id: int, bot_name: str = "unknown",
    days: int = 0, expected_amount: float = 0.0,
    username: Optional[str] = None,
) -> tuple[str, Optional[dict]]:
    async with async_session() as session:
        async with session.begin():
            row = await session.scalar(select(UTR).where(UTR.utr == utr))
            if row:
                if row.redeemed:
                    return "already_submitted", {
                        "user_id": row.user_id,
                        "username": row.username,
                        "bot_name": row.bot_name,
                        "redeemed_at": row.redeemed_at.isoformat() if row.redeemed_at else None,
                    }
                if row.user_id and row.user_id != user_id:
                    return "claimed_by_other", {
                        "user_id": row.user_id,
                        "username": row.username,
                        "bot_name": row.bot_name,
                        "submitted_at": row.submitted_at.isoformat() if row.submitted_at else None,
                    }
                if row.amount is not None:
                    if expected_amount > 0 and abs(row.amount - expected_amount) > 0.01:
                        row.user_id, row.bot_name, row.days, row.username = user_id, bot_name, days, username
                        row.expected_amount, row.submitted_at = expected_amount, datetime.now()
                        return "amount_mismatch", {
                            "utr": row.utr, "actual": row.amount, "expected": expected_amount,
                        }
                    row.user_id, row.bot_name, row.days, row.username = user_id, bot_name, days, username
                    row.expected_amount = expected_amount or row.expected_amount
                    row.submitted_at = datetime.now()
                    row.redeemed, row.redeemed_at = True, datetime.now()
                    return "ok", {"utr": row.utr, "amount": row.amount, "sender": row.sender}
                if row.user_id == user_id:
                    return "already_pending", None
                row.user_id, row.bot_name, row.days = user_id, bot_name, days
                row.expected_amount, row.username = expected_amount, username
                row.submitted_at = datetime.now()
                return "pending", None

            count = (
                await session.execute(
                    select(func.count()).select_from(UTR)
                    .where(UTR.user_id == user_id, UTR.redeemed == False)
                )
            ).scalar() or 0
            if count >= 3:
                return "too_many_pending", None
            session.add(UTR(
                utr=utr, user_id=user_id, bot_name=bot_name,
                days=days, expected_amount=expected_amount,
                username=username, submitted_at=datetime.now(),
            ))
            return "pending", None


async def mark_redeemed(utr: str) -> bool:
    async with async_session() as session:
        async with session.begin():
            row = await session.scalar(select(UTR).where(UTR.utr == utr))
            if not row or row.redeemed or row.amount is None or row.user_id is None:
                return False
            row.redeemed, row.redeemed_at = True, datetime.now()
            return True


async def get_recent_sms(limit: int = 50) -> list[UTR]:
    async with async_session() as session:
        return (await session.execute(
            select(UTR).where(UTR.amount.isnot(None))
            .order_by(desc(UTR.sms_at)).limit(limit)
        )).scalars().all()


async def get_recent_redeemed(limit: int = 50) -> list[UTR]:
    async with async_session() as session:
        return (await session.execute(
            select(UTR).where(UTR.redeemed == True)
            .order_by(desc(UTR.redeemed_at)).limit(limit)
        )).scalars().all()


async def get_recent_pending(limit: int = 50) -> list[UTR]:
    async with async_session() as session:
        return (await session.execute(
            select(UTR).where(UTR.user_id.isnot(None), UTR.redeemed == False)
            .order_by(desc(UTR.submitted_at)).limit(limit)
        )).scalars().all()


async def delete_utr(utr: str) -> bool:
    async with async_session() as session:
        async with session.begin():
            row = await session.scalar(select(UTR).where(UTR.utr == utr))
            if row:
                await session.delete(row)
                return True
            return False
