from enum import Enum


class MaterialType(str, Enum):
    VIDEO = "video"
    ARTICLE = "article"
    BOOK = "book"
    COURSE = "course"
    NOTE = "note"


class MaterialStatus(str, Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    LEARNED = "learned"
    SKIPPED = "skipped"
    DUPLICATE = "duplicate"


class WatchRecommendation(str, Enum):
    FULL = "full"
    CHAPTERS = "chapters"
    SKIP = "skip"
