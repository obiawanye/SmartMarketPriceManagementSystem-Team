
import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine, SessionLocal
from app.model import User, Role


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_migrations() -> None:
    """Apply existing Alembic migrations before serving requests."""
    alembic_ini = PROJECT_ROOT / "alembic.ini"

    if not alembic_ini.exists():
        raise FileNotFoundError(
            f"Alembic configuration not found: {alembic_ini}"
        )

    config = Config(str(alembic_ini))
    config.set_main_option(
        "script_location",
        str(PROJECT_ROOT / "alembic"),
    )

    command.upgrade(config, "head")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run database migrations when the application starts."""
    await asyncio.to_thread(run_migrations)

    try:
        yield
    finally:
        engine.dispose()


app = FastAPI(
    title="Smart Price Management System",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Smart Price Management System API is running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/seed-data")
def seed_data():
    """Create initial roles and test users with role assignments."""
    with SessionLocal() as db:
        # Create roles if they do not exist.
        role_names = ["admin", "customer"]
        roles = {}

        for role_name in role_names:
            role = db.scalar(
                select(Role).where(Role.name == role_name)
            )

            if role is None:
                role = Role(name=role_name)
                db.add(role)
                db.flush()

            roles[role_name] = role

        # Create test users if they do not exist.
        test_users = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "role": "admin",
            },
            {
                "username": "testcustomer",
                "email": "customer@example.com",
                "role": "customer",
            },
        ]

        for user_data in test_users:
            user = db.scalar(
                select(User).where(
                    User.username == user_data["username"]
                )
            )

            if user is None:
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    # Replace with a securely generated password hash.
                    password="REPLACE_WITH_A_REAL_PASSWORD_HASH",
                )
                db.add(user)
                db.flush()

            # Assign the appropriate role if not already assigned.
            role = roles[user_data["role"]]

            if role not in user.roles:
                user.roles.append(role)

        db.commit()

        return {
            "message": "Seed data created successfully",
            "roles": role_names,
            "users": ["admin", "testcustomer"],
        }
