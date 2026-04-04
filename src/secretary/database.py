import json
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, String, DateTime, Float, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.dialects.sqlite import insert

from secretary.config import settings
from secretary.models import Material, LearningRecord


class Base(DeclarativeBase):
    pass


class MaterialDB(Base):
    __tablename__ = "materials"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    obsidian_path: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String)
    source_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="pending")
    novelty_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    tags_json: Mapped[str] = mapped_column(JSON, default=list)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    analyzed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    learned_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    video_metadata_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    related_materials_json: Mapped[str] = mapped_column(JSON, default=list)

    def to_model(self) -> Material:
        from secretary.models import VideoMetadata, VideoChapter
        import json
        
        video_metadata = None
        if self.video_metadata_json:
            vm_dict = json.loads(self.video_metadata_json)
            chapters = [
                VideoChapter(time=ch["time"], title=ch["title"])
                for ch in vm_dict.get("chapters", [])
            ]
            video_metadata = VideoMetadata(
                channel=vm_dict.get("channel"),
                views=vm_dict.get("views"),
                likes=vm_dict.get("likes"),
                transcript=vm_dict.get("transcript"),
                chapters=chapters,
                duration=vm_dict.get("duration"),
            )
        
        return Material(
            id=self.id,
            obsidian_path=self.obsidian_path,
            type=self.type,
            source_url=self.source_url,
            title=self.title,
            status=self.status,
            novelty_score=self.novelty_score,
            tags=self.tags_json if isinstance(self.tags_json, list) else json.loads(self.tags_json) if self.tags_json else [],
            summary=self.summary,
            added_at=self.added_at,
            analyzed_at=self.analyzed_at,
            learned_at=self.learned_at,
            video_metadata=video_metadata,
            related_materials=self.related_materials_json if isinstance(self.related_materials_json, list) else json.loads(self.related_materials_json) if self.related_materials_json else [],
        )


class LearningHistoryDB(Base):
    __tablename__ = "learning_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    material_id: Mapped[str] = mapped_column(String)
    action: Mapped[str] = mapped_column(String)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class Database:
    def __init__(self, db_path: str | None = None):
        if db_path is None:
            db_path = str(settings.secretary_db_path)
        
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)

    def add_material(self, material: Material) -> Material:
        with Session(self.engine) as session:
            db_material = MaterialDB(
                id=material.id,
                obsidian_path=material.obsidian_path,
                type=material.type,
                source_url=material.source_url,
                title=material.title,
                status=material.status,
                novelty_score=material.novelty_score,
                tags_json=json.dumps(material.tags),
                summary=material.summary,
                added_at=material.added_at,
                analyzed_at=material.analyzed_at,
                learned_at=material.learned_at,
                video_metadata_json=(
                    material.video_metadata.model_dump_json()
                    if material.video_metadata else None
                ),
                related_materials_json=json.dumps(material.related_materials),
            )
            session.add(db_material)
            session.commit()
        return material

    def get_material(self, material_id: str) -> Material | None:
        with Session(self.engine) as session:
            db_material = session.get(MaterialDB, material_id)
            if db_material:
                return db_material.to_model()
        return None

    def get_materials(
        self,
        status: str | None = None,
        limit: int = 100
    ) -> list[Material]:
        with Session(self.engine) as session:
            query = session.query(MaterialDB)
            if status:
                query = query.filter(MaterialDB.status == status)
            query = query.order_by(MaterialDB.added_at.desc()).limit(limit)
            return [m.to_model() for m in query.all()]

    def update_material(self, material: Material) -> Material:
        with Session(self.engine) as session:
            db_material = session.get(MaterialDB, material.id)
            if db_material:
                db_material.status = material.status
                db_material.novelty_score = material.novelty_score
                db_material.tags_json = material.tags
                db_material.summary = material.summary
                db_material.analyzed_at = material.analyzed_at
                db_material.learned_at = material.learned_at
                if material.video_metadata:
                    db_material.video_metadata_json = material.video_metadata.model_dump_json()
                db_material.related_materials_json = material.related_materials
                session.commit()
        return material

    def delete_material(self, material_id: str) -> bool:
        with Session(self.engine) as session:
            db_material = session.get(MaterialDB, material_id)
            if db_material:
                session.delete(db_material)
                session.commit()
                return True
        return False

    def find_by_url(self, url: str) -> Material | None:
        with Session(self.engine) as session:
            db_material = session.query(MaterialDB).filter(
                MaterialDB.source_url == url
            ).first()
            if db_material:
                return db_material.to_model()
        return None

    def add_learning_record(self, record: LearningRecord) -> None:
        with Session(self.engine) as session:
            db_record = LearningHistoryDB(
                material_id=record.material_id,
                action=record.action,
                timestamp=record.timestamp,
                notes=record.notes,
            )
            session.add(db_record)
            session.commit()

    def get_learned_summaries(self) -> list[str]:
        with Session(self.engine) as session:
            learned = session.query(MaterialDB).filter(
                MaterialDB.status == "learned"
            ).all()
            summaries = []
            for m in learned:
                text_parts = [m.title]
                if m.summary:
                    text_parts.append(m.summary)
                tags = json.loads(m.tags_json) if m.tags_json else []
                text_parts.extend(tags)
                summaries.append(" ".join(text_parts))
            return summaries


db = Database()
