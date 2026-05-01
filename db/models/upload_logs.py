from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from .base import Base


class UploadLog(Base):
    __tablename__ = "upload_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    snapshot_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("portfolio_snapshots.id"),
        nullable=True,
    )
    filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    upload_status: Mapped[str | None] = mapped_column(String(20), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    processing_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "upload_status IN ('SUCCESS', 'FAILED', 'PARSING', 'CONFIRMED')",
            name="ck_upload_logs_upload_status",
        ),
    )

    user = relationship("User", back_populates="upload_logs")
    snapshot = relationship("PortfolioSnapshot", back_populates="upload_logs")
