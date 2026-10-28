from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Unit(Base):
    __tablename__ = "units"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_units"),
        UniqueConstraint("code", name="uq_units_code"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    code: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(String(80), nullable=False)

    dimension: Mapped[str] = mapped_column(String(24), nullable=False)

    conversion_factor: Mapped[Decimal | None] = mapped_column(
        Numeric(18, 9),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
    )

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="unit",
    )
