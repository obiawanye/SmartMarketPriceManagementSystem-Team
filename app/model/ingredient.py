from sqlalchemy import (
    Boolean,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Ingredient(Base):
    __tablename__ = "ingredients"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_ingredients"),
        UniqueConstraint(
            "normalized_name",
            name="uq_ingredients_normalized_name",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    canonical_name: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    normalized_name: Mapped[str] = mapped_column(
        String(160),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
    )

    aliases: Mapped[list["IngredientAlias"]] = relationship(
        back_populates="ingredient",
    )

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient",
    )
