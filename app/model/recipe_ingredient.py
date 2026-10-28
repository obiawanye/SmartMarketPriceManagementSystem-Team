from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_recipe_ingredients_quantity"),
        CheckConstraint("sort_order >= 0", name="ck_recipe_ingredients_sort_order"),
        Index("ix_recipe_ingredients_recipe_sort", "recipe_id", "sort_order"),
        Index("ix_recipe_ingredients_ingredient_id", "ingredient_id"),
        Index("ix_recipe_ingredients_unit_id", "unit_id"),
        PrimaryKeyConstraint("id", name="pk_recipe_ingredients"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    recipe_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "recipes.id",
            name="fk_recipe_ingredients_recipe_id_recipes",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    ingredient_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "ingredients.id",
            name="fk_recipe_ingredients_ingredient_id_ingredients",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    unit_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "units.id",
            name="fk_recipe_ingredients_unit_id_units",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(12, 4),
        nullable=False,
    )

    preparation_note: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")
    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipe_ingredients",
    )
    unit: Mapped["Unit"] = relationship(back_populates="recipe_ingredients")
