from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Content:
    id: Optional[str] = None
    platform: str = None
    topic: str = None
    audience: str = None
    text: str = None
    generated_at: datetime = None
    language: str = "es"
    
    def __post_init__(self):
        if self.generated_at is None:
            self.generated_at = datetime.now()
    
    def preview(self, max_length: int = 100) -> str:
        return self.text[:max_length] + "..." if len(self.text) > max_length else self.text
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "platform": self.platform,
            "topic": self.topic,
            "audience": self.audience,
            "text": self.text,
            "generated_at": self.generated_at.isoformat(),
            "language": self.language
        }

class ContentManager:
    def __init__(self):
        self.contents = []
    
    def add_content(self, content: Content):
        self.contents.append(content)
    
    def get_contents_by_platform(self, platform: str) -> list:
        return [content for content in self.contents if content.platform == platform]