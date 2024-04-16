from fastapi import FastAPI
from app.config import settings
from app.database.db import initialize_db, engine
from app.routes.routes import user_router
from app.routes.admin_routes import admin_router
from app.routes.corporation_routes import corporation_router
from app.routes.market_routes import market_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME,
                  version=settings.VERSION
            )

    @app.on_event("startup")
    async def startup_event():
        initialize_db()

    app.include_router(user_router)
    app.include_router(corporation_router)
    app.include_router(market_router)
    app.include_router(admin_router)
    return app


app = create_app()


r"""
from sqlmodel import Session, select
from app.models.models import User
with Session(engine) as session:


    # Fetch the user somehow, e.g., by ID
    user_id = 1  # Example user ID
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if user:
        user.is_admin = True
        session.commit()  # This should commit the change
        session.refresh(user)
    else:
        print("User not found.")
"""

