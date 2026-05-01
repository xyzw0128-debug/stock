from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class OCRUnmatched(Base):
    __tablename__ = "ocr_unmatched"
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'resolved', 'ignored')", name="chk_ocr_unmatched_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("portfolio_snapshots.id", ondelete="CASCADE"), nullable=False
    )
    raw_name: Mapped[str | None] = mapped_column(String(100))
    quantity: Mapped[int | None] = mapped_column(Integer)
    avg_price: Mapped[float | None] = mapped_column(Numeric(12, 2))
    resolved_ticker: Mapped[str | None] = mapped_column(ForeignKey("stocks_master.ticker"), String(10))
    status: Mapped[str] = mapped_column(String(20), server_default="pending", default="pending")
    resolved_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    snapshot = relationship("PortfolioSnapshot", back_populates="ocr_unmatched_items")
    stock = relationship("StockMaster")

    def __repr__(self) -> str:
        return (
            f"OCRUnmatched(id={self.id}, snapshot_id={self.snapshot_id}, raw_name={self.raw_name!r}, "
            f"status={self.status!r})"
        )
