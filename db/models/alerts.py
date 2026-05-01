from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("portfolio_snapshots.id"))
    alert_type: Mapped[str | None] = mapped_column(String(30))
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, server_default=text("FALSE"))
    created_at = mapped_column(Text, server_default=text("NOW()"))

    __table_args__ = (
        CheckConstraint(
            "alert_type IN ('HIGH_CONCENTRATION','AVG_DOWN_REPEATED','CASH_LOW','LARGE_LOSS','RAPID_WEIGHT_CHANGE')",
            name="ck_alerts_alert_type",
        ),
    )

    user = relationship("User", back_populates="alerts")
    snapshot = relationship("PortfolioSnapshot", back_populates="alerts")
