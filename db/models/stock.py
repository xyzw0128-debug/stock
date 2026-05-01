from typing import List

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class StockMaster(Base):
    __tablename__ = "stocks_master"
    __table_args__ = (
        CheckConstraint("market IN ('KOSPI', 'KOSDAQ', 'KONEX')", name="ck_stocks_master_market"),
    )

    ticker: Mapped[str] = mapped_column(String(10), primary_key=True)
    stock_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    short_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    market: Mapped[str] = mapped_column(String(10), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )

    aliases: Mapped[List["StockAlias"]] = relationship(
        "StockAlias", back_populates="stock", cascade="all, delete-orphan"
    )


class StockAlias(Base):
    __tablename__ = "stock_aliases"
    __table_args__ = (UniqueConstraint("alias", "source", name="uq_stock_aliases_alias_source"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(
        String(10), ForeignKey("stocks_master.ticker", ondelete="CASCADE"), nullable=False, index=True
    )
    alias: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    confidence_score: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("100"))

    stock: Mapped[StockMaster] = relationship("StockMaster", back_populates="aliases")
