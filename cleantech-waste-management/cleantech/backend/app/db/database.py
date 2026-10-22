import datetime
from sqlalchemy import create_engine, String, Float, JSON, DateTime, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from app.core import config

engine = create_engine(config.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): pass

def _now(): return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

class Record(Base):
    __tablename__ = "classifications"
    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    alternatives: Mapped[list] = mapped_column(JSON, default=list)
    low_confidence: Mapped[bool] = mapped_column(Boolean, default=False)
    filename: Mapped[str] = mapped_column(String(120))  # display name only; images are NOT stored
    model_version: Mapped[str] = mapped_column(String(64), default="unknown")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=_now)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
