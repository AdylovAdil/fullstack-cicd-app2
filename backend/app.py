import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


def normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg2://", 1)
    if url.startswith("postgresql://") and "+psycopg2" not in url:
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


def build_engine(database_url: str):
    database_url = normalize_database_url(database_url)

    if database_url.startswith("sqlite"):
        return create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool if ":memory:" in database_url else None,
        )

    return create_engine(database_url, pool_pre_ping=True)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    database_url = os.getenv("DATABASE_URL", "sqlite:///local.db")
    if test_config and test_config.get("DATABASE_URL"):
        database_url = test_config["DATABASE_URL"]

    engine = build_engine(database_url)
    SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))

    Base.metadata.create_all(bind=engine)

    if test_config:
        app.config.update(test_config)

    CORS(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        SessionLocal.remove()

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/api/data")
    def get_data():
        db = SessionLocal()
        try:
            items = db.query(Item).order_by(Item.id.desc()).all()
            return jsonify([item.to_dict() for item in items]), 200
        finally:
            db.close()

    @app.post("/api/data")
    def add_data():
        payload = request.get_json(silent=True) or {}
        title = (payload.get("title") or payload.get("name") or "").strip()

        if not title:
            return jsonify({"error": "Поле title обязательно"}), 400

        db = SessionLocal()
        try:
            item = Item(title=title)
            db.add(item)
            db.commit()
            db.refresh(item)
            return jsonify(item.to_dict()), 201
        except SQLAlchemyError as exc:
            db.rollback()
            return jsonify({"error": "Ошибка при сохранении данных", "details": str(exc)}), 500
        finally:
            db.close()

    @app.delete("/api/data/<int:item_id>")
    def delete_data(item_id):
        db = SessionLocal()
        try:
            item = db.get(Item, item_id)
            if not item:
                return jsonify({"error": "Запись не найдена"}), 404

            db.delete(item)
            db.commit()
            return jsonify({"message": "Запись удалена"}), 200
        except SQLAlchemyError as exc:
            db.rollback()
            return jsonify({"error": "Ошибка при удалении данных", "details": str(exc)}), 500
        finally:
            db.close()

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
