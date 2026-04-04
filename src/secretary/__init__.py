from .ai_router import ai_router, AIRouter
from .database import db, Database
from .material_manager import manager, MaterialManager, URLNormalizer
from .video_analyzer import video_analyzer, VideoAnalyzer
from .obsidian import vault, ObsidianVault
from .models import Material, VideoMetadata, VideoChapter
from .enums import MaterialType, MaterialStatus
from .config import settings

__all__ = [
    "ai_router",
    "AIRouter",
    "db",
    "Database",
    "manager",
    "MaterialManager",
    "URLNormalizer",
    "video_analyzer",
    "VideoAnalyzer",
    "vault",
    "ObsidianVault",
    "Material",
    "MaterialType",
    "MaterialStatus",
    "VideoMetadata",
    "VideoChapter",
    "settings",
]
