from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class IngredientAlias(Base):
    __tablename__ = "ingredient_aliases"
    __table_args__ = (
        Index("ix_ingredient_aliases_ingredient_id", "ingredient_id"),
        PrimaryKeyConstraint("id", name="pk_ingredient_aliases"),
        UniqueConstraint(
            "normalized_alias",
            name="uq_ingredient_aliases_normalized_alias",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    ingredient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "ingredients.id",
            name="fk_ingredient_aliases_ingredient_id_ingredients",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    alias: Mapped[str] = mapped_column(String(160), nullable=False)

    normalized_alias: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    ingredient: Mapped["Ingredient"] = relationship(back_populates="aliases")
