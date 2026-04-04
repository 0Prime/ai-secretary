from pathlib import Path
from typing import Optional
import re

from secretary.config import settings
from secretary.models import Material
from secretary.database import db


class ObsidianVault:
    def __init__(self, vault_path: Optional[Path] = None):
        self._vault_path = vault_path or settings.obsidian_vault_path
        self._exists = self._vault_path.exists()
    
    @property
    def vault_path(self) -> Path:
        if not self._exists:
            raise ValueError(f"Obsidian vault not found: {self._vault_path}")
        return self._vault_path

    def create_note_from_material(self, material: Material) -> Path:
        if not material.obsidian_path:
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', material.title)
            safe_title = safe_title[:100].strip()
            
            filename = f"{safe_title}.md"
            inbox_path = self.vault_path / "_INBOX"
            inbox_path.mkdir(parents=True, exist_ok=True)
            material.obsidian_path = str(inbox_path / filename)
        
        path = Path(material.obsidian_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        content = material.to_frontmatter()
        
        if material.summary:
            content += f"\n\n# {material.title}\n\n{material.summary}\n"
        elif material.video_metadata:
            if material.video_metadata.transcript:
                content += f"\n\n# {material.title}\n\n## Transcript\n\n{material.video_metadata.transcript[:2000]}...\n"
        
        path.write_text(content, encoding="utf-8")
        
        return path

    def sync_material(self, material_id: str) -> Optional[Path]:
        material = db.get_material(material_id)
        if not material:
            return None
        
        if not self._exists:
            return None
        
        return self.create_note_from_material(material)

    def get_existing_notes(self) -> list[Path]:
        if not self._exists:
            return []
        notes = list(self.vault_path.rglob("*.md"))
        return [n for n in notes if ".obsidian" not in str(n)]

    def parse_note_frontmatter(self, path: Path) -> Optional[dict]:
        content = path.read_text(encoding="utf-8")
        
        if not content.startswith("---"):
            return None
        
        parts = content.split("---", 2)
        if len(parts) < 3:
            return None
        
        frontmatter_text = parts[1]
        
        metadata = {}
        for line in frontmatter_text.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')
        
        return metadata

    def find_notes_without_tags(self) -> list[Path]:
        notes = self.get_existing_notes()
        untagged = []
        
        for note_path in notes:
            fm = self.parse_note_frontmatter(note_path)
            if not fm or not fm.get('tags'):
                untagged.append(note_path)
        
        return untagged


vault = ObsidianVault()
