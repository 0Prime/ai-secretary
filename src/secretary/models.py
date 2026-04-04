from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class VideoChapter(BaseModel):
    time: int
    title: str


class SecretaryMetadata(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    added_at: datetime = Field(default_factory=datetime.utcnow)
    novelty_score: float | None = None
    tags: list[str] = Field(default_factory=list)
    summary: str | None = None
    learned_at: datetime | None = None
    analyzed_at: datetime | None = None


class VideoMetadata(BaseModel):
    channel: str | None = None
    views: int | None = None
    likes: int | None = None
    transcript: str | None = None
    chapters: list[VideoChapter] = Field(default_factory=list)
    duration: int | None = None


class Material(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    obsidian_path: str | None = None
    type: str
    source_url: str | None = None
    title: str
    status: str = "pending"
    novelty_score: float | None = None
    tags: list[str] = Field(default_factory=list)
    summary: str | None = None
    added_at: datetime = Field(default_factory=datetime.utcnow)
    analyzed_at: datetime | None = None
    learned_at: datetime | None = None
    video_metadata: VideoMetadata | None = None
    related_materials: list[str] = Field(default_factory=list)

    def to_frontmatter(self) -> str:
        lines = [
            "---",
            f"created: {self.added_at.strftime('%Y-%m-%d')}",
            f"type: {self.type}",
            f"status: {self.status}",
        ]
        if self.source_url:
            lines.append(f"source_url: {self.source_url}")
        if self.tags:
            lines.append(f"tags: [{', '.join(self.tags)}]")
        if self.summary:
            lines.append(f"summary: \"{self.summary}\"")
        if self.video_metadata:
            if self.video_metadata.duration:
                lines.append(f"duration: {self.video_metadata.duration}")
            if self.video_metadata.chapters:
                lines.append("chapters:")
                for ch in self.video_metadata.chapters:
                    lines.append(f"  - {{time: {ch.time}, title: \"{ch.title}\"}}")
        if self.novelty_score is not None:
            lines.append(f"novelty_score: {self.novelty_score:.2f}")
        if self.learned_at:
            lines.append(f"learned_at: {self.learned_at.strftime('%Y-%m-%d')}")
        lines.append("---")
        return "\n".join(lines)


class LearningRecord(BaseModel):
    material_id: str
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    notes: str | None = None
