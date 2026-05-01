from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    snapshot_id: Mapped[int | None] = mapped_column(ForeignKey("portfolio_snapshots.id"))
    entry_date: Mapped[str] = mapped_column(Date, nullable=False)
    raw_input: Mapped[str | None] = mapped_column(Text)
    ai_summary: Mapped[str | None] = mapped_column(Text)
    emotion_tag: Mapped[str | None] = mapped_column(String(20))
    created_at = mapped_column(Text, server_default=text("NOW()"))

    __table_args__ = (
        CheckConstraint(
            "emotion_tag IN ('confident','anxious','regret','neutral','greedy','fearful')",
            name="ck_journal_entries_emotion_tag",
        ),
    )

    user = relationship("User", back_populates="journal_entries")
    snapshot = relationship("PortfolioSnapshot", back_populates="journal_entries")
