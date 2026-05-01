from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Holding(Base):
    __tablename__ = "holdings"
    __table_args__ = (
        UniqueConstraint("snapshot_id", "ticker", name="uq_holdings_snapshot_ticker"),
        CheckConstraint("quantity >= 0", name="chk_holdings_quantity_non_negative"),
        CheckConstraint("avg_price >= 0", name="chk_holdings_avg_price_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("portfolio_snapshots.id", ondelete="CASCADE"), nullable=False
    )
    ticker: Mapped[str | None] = mapped_column(ForeignKey("stocks_master.ticker"), String(10))
    stock_name: Mapped[str] = mapped_column(String(100), nullable=False)
    normalized_name: Mapped[str | None] = mapped_column(String(100))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    current_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    market_value: Mapped[float | None] = mapped_column(Numeric(18, 2))
    pnl: Mapped[float | None] = mapped_column(Numeric(18, 2))
    pnl_pct: Mapped[float | None] = mapped_column(Numeric(8, 4))
    weight_pct: Mapped[float | None] = mapped_column(Numeric(8, 4))
    is_matched: Mapped[bool] = mapped_column(Boolean, server_default="false", default=False)
    match_score: Mapped[int | None] = mapped_column(Integer)

    snapshot = relationship("PortfolioSnapshot", back_populates="holdings")
    stock = relationship("StockMaster", back_populates="holdings")

    def __repr__(self) -> str:
        return (
            f"Holding(id={self.id}, snapshot_id={self.snapshot_id}, ticker={self.ticker!r}, "
            f"stock_name={self.stock_name!r}, quantity={self.quantity})"
        )
