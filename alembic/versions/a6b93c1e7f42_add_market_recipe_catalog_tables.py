"""Add market and recipe catalog tables.

Revision ID: a6b93c1e7f42
Revises: d4dbb44eb27c
Create Date: 2026-10-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a6b93c1e7f42"
down_revision: Union[str, Sequence[str], None] = "d4dbb44eb27c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "workers",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=24),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_workers_user_id_users",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("user_id", name="pk_workers"),
    )
    op.create_index("ix_workers_status", "workers", ["status"], unique=False)

    op.create_table(
        "delivery_zones",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_delivery_zones"),
        sa.UniqueConstraint("name", name="uq_delivery_zones_name"),
    )

    op.create_table(
        "markets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column("address_text", sa.String(length=500), nullable=True),
        sa.Column("locality", sa.String(length=120), nullable=True),
        sa.Column("state", sa.String(length=120), nullable=True),
        sa.Column("latitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column("longitude", sa.Numeric(precision=9, scale=6), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_markets"),
    )
    op.create_index("ix_markets_name", "markets", ["name"], unique=False)

    op.create_table(
        "market_coverage",
        sa.Column("market_id", sa.Integer(), nullable=False),
        sa.Column("zone_id", sa.Integer(), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["market_id"],
            ["markets.id"],
            name="fk_market_coverage_market_id_markets",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["zone_id"],
            ["delivery_zones.id"],
            name="fk_market_coverage_zone_id_delivery_zones",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "market_id",
            "zone_id",
            name="pk_market_coverage",
        ),
    )
    op.create_index(
        "ix_market_coverage_zone_id",
        "market_coverage",
        ["zone_id"],
        unique=False,
    )

    op.create_table(
        "ingredients",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("canonical_name", sa.String(length=160), nullable=False),
        sa.Column("normalized_name", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_ingredients"),
        sa.UniqueConstraint(
            "normalized_name",
            name="uq_ingredients_normalized_name",
        ),
    )

    op.create_table(
        "ingredient_aliases",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.Column("alias", sa.String(length=160), nullable=False),
        sa.Column("normalized_alias", sa.String(length=160), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredients.id"],
            name="fk_ingredient_aliases_ingredient_id_ingredients",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_ingredient_aliases"),
        sa.UniqueConstraint(
            "normalized_alias",
            name="uq_ingredient_aliases_normalized_alias",
        ),
    )
    op.create_index(
        "ix_ingredient_aliases_ingredient_id",
        "ingredient_aliases",
        ["ingredient_id"],
        unique=False,
    )

    op.create_table(
        "units",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("display_name", sa.String(length=80), nullable=False),
        sa.Column("dimension", sa.String(length=24), nullable=False),
        sa.Column(
            "conversion_factor",
            sa.Numeric(precision=18, scale=9),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="pk_units"),
        sa.UniqueConstraint("code", name="uq_units_code"),
    )

    op.create_table(
        "recipes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("base_servings", sa.Integer(), nullable=False),
        sa.Column(
            "version_no",
            sa.Integer(),
            server_default="1",
            nullable=False,
        ),
        sa.Column("source_type", sa.String(length=32), nullable=True),
        sa.Column("provider_name", sa.String(length=100), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("1"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "base_servings > 0",
            name="ck_recipes_base_servings",
        ),
        sa.CheckConstraint(
            "version_no > 0",
            name="ck_recipes_version_no",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_recipes"),
    )
    op.create_index(
        "ix_recipes_name_version",
        "recipes",
        ["name", "version_no"],
        unique=False,
    )

    op.create_table(
        "recipe_ingredients",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.Column("unit_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=12, scale=4), nullable=False),
        sa.Column("preparation_note", sa.String(length=500), nullable=True),
        sa.Column(
            "sort_order",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.CheckConstraint(
            "quantity > 0",
            name="ck_recipe_ingredients_quantity",
        ),
        sa.CheckConstraint(
            "sort_order >= 0",
            name="ck_recipe_ingredients_sort_order",
        ),
        sa.ForeignKeyConstraint(
            ["recipe_id"],
            ["recipes.id"],
            name="fk_recipe_ingredients_recipe_id_recipes",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredients.id"],
            name="fk_recipe_ingredients_ingredient_id_ingredients",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["unit_id"],
            ["units.id"],
            name="fk_recipe_ingredients_unit_id_units",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_recipe_ingredients"),
    )
    op.create_index(
        "ix_recipe_ingredients_recipe_sort",
        "recipe_ingredients",
        ["recipe_id", "sort_order"],
        unique=False,
    )
    op.create_index(
        "ix_recipe_ingredients_ingredient_id",
        "recipe_ingredients",
        ["ingredient_id"],
        unique=False,
    )
    op.create_index(
        "ix_recipe_ingredients_unit_id",
        "recipe_ingredients",
        ["unit_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_table("recipe_ingredients")
    op.drop_index("ix_recipes_name_version", table_name="recipes")
    op.drop_table("recipes")
    op.drop_table("units")
    op.drop_index(
        "ix_ingredient_aliases_ingredient_id",
        table_name="ingredient_aliases",
    )
    op.drop_table("ingredient_aliases")
    op.drop_table("ingredients")
    op.drop_index(
        "ix_market_coverage_zone_id",
        table_name="market_coverage",
    )
    op.drop_table("market_coverage")
    op.drop_index("ix_markets_name", table_name="markets")
    op.drop_table("markets")
    op.drop_table("delivery_zones")
    op.drop_index("ix_workers_status", table_name="workers")
    op.drop_table("workers")
