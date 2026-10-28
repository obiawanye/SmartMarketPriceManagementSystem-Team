from sqlalchemy import Boolean, ForeignKey, Index, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MarketCoverage(Base):
    __tablename__ = "market_coverage"
    __table_args__ = (
        Index("ix_market_coverage_zone_id", "zone_id"),
        PrimaryKeyConstraint(
            "market_id",
            "zone_id",
            name="pk_market_coverage",
        ),
    )

    market_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "markets.id",
            name="fk_market_coverage_market_id_markets",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    zone_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "delivery_zones.id",
            name="fk_market_coverage_zone_id_delivery_zones",
            ondelete="RESTRICT",
        ),
        primary_key=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
    )

    market: Mapped["Market"] = relationship(back_populates="market_coverages")
    delivery_zone: Mapped["DeliveryZone"] = relationship(
        back_populates="market_coverages",
    )
