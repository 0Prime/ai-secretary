from datetime import datetime
from typing import Optional
import urllib.parse

from secretary.models import Material, VideoMetadata
from secretary.enums import MaterialType, MaterialStatus
from secretary.database import db
from secretary.ai_router import ai_router


class URLNormalizer:
    @staticmethod
    def normalize(url: str) -> str:
        parsed = urllib.parse.urlparse(url)
        
        if "youtube.com" in parsed.netloc:
            video_id = urllib.parse.parse_qs(parsed.query).get("v", [None])[0]
            if video_id:
                return f"https://youtube.com/watch?v={video_id}"
        
        if "youtu.be" in parsed.netloc:
            return f"https://youtube.com/watch?v={parsed.path.lstrip('/')}"
        
        return url

    @staticmethod
    def is_youtube(url: str) -> bool:
        return "youtube.com" in url or "youtu.be" in url

    @staticmethod
    def extract_video_id(url: str) -> Optional[str]:
        normalized = URLNormalizer.normalize(url)
        parsed = urllib.parse.urlparse(normalized)
        query = urllib.parse.parse_qs(parsed.query)
        return query.get("v", [None])[0]


class MaterialManager:
    def __init__(self):
        self.db = db
        self.ai = ai_router

    def add_material(
        self,
        source: str,
        material_type: MaterialType,
        title: Optional[str] = None
    ) -> Material:
        normalized_url = URLNormalizer.normalize(source) if source.startswith("http") else None
        
        existing = None
        if normalized_url:
            existing = self.db.find_by_url(normalized_url)
        if existing:
            raise ValueError(f"Material already exists: {existing.id}")

        if title is None:
            title = normalized_url or source
        
        material = Material(
            type=material_type.value,
            source_url=normalized_url,
            title=title,
            status=MaterialStatus.PENDING.value,
        )
        
        return self.db.add_material(material)

    def get_material(self, material_id: str) -> Optional[Material]:
        return self.db.get_material(material_id)

    def list_materials(
        self,
        status: Optional[str] = None,
        limit: int = 100
    ) -> list[Material]:
        return self.db.get_materials(status=status, limit=limit)

    def analyze_material(self, material_id: str) -> Material:
        material = self.db.get_material(material_id)
        if not material:
            raise ValueError(f"Material not found: {material_id}")
        
        material.status = MaterialStatus.ANALYZING.value
        self.db.update_material(material)
        
        learned_summaries = self.db.get_learned_summaries()
        
        content_for_analysis = f"{material.title}"
        if material.summary:
            content_for_analysis += f"\n{material.summary}"
        
        material.novelty_score = self.ai.compute_novelty(
            content_for_analysis,
            learned_summaries
        )
        
        material.tags = self.ai.extract_tags(content_for_analysis)
        
        material.analyzed_at = datetime.utcnow()
        
        if material.novelty_score < 0.4:
            material.status = MaterialStatus.SKIPPED.value
        else:
            material.status = MaterialStatus.PENDING.value
        
        self.db.update_material(material)
        
        self.db.add_learning_record(
            type("LearningRecord", (), {
                "material_id": material_id,
                "action": "analyzed",
                "timestamp": datetime.utcnow(),
                "notes": None
            })()
        )
        
        return material

    def mark_as_learned(self, material_id: str) -> Material:
        material = self.db.get_material(material_id)
        if not material:
            raise ValueError(f"Material not found: {material_id}")
        
        material.status = MaterialStatus.LEARNED.value
        material.learned_at = datetime.utcnow()
        
        return self.db.update_material(material)

    def get_novelty_recommendation(self, material_id: str) -> str:
        material = self.db.get_material(material_id)
        if not material:
            raise ValueError(f"Material not found: {material_id}")
        
        if material.novelty_score is None:
            return "Analyze material first"
        
        if material.novelty_score > 0.7:
            return f"FULL (novelty: {material.novelty_score:.2f})"
        elif material.novelty_score > 0.4:
            return f"CHAPTERS (novelty: {material.novelty_score:.2f})"
        else:
            return f"SKIP (novelty: {material.novelty_score:.2f})"


manager = MaterialManager()
