from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class DeliveryZone(Base):
    __tablename__ = "delivery_zones"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_delivery_zones"),
        UniqueConstraint("name", name="uq_delivery_zones_name"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    market_coverages: Mapped[list["MarketCoverage"]] = relationship(
        back_populates="delivery_zone",
    )
