from .social_presets import SOCIAL_PRESETS, get_preset_by_name
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class VideoClip:
    path: str
    label: str
    trim_start: float = 0.0
    trim_end: float = 0.0
    volume: float = 1.0
    speed: float = 1.0

    @property
    def duration(self) -> float:
        return max(0.0, self.trim_end - self.trim_start) if self.trim_end > self.trim_start else 0.0


@dataclass
class ProjectState:
    name: str = "Untitled Project"
    clips: List[VideoClip] = field(default_factory=list)
    preset_name: str = "Instagram_Reels_9_16"
    output_dir: str = "./exports"

    def selected_preset(self):
        return get_preset_by_name(self.preset_name) or SOCIAL_PRESETS[0]


__all__ = ["VideoClip", "ProjectState", "SOCIAL_PRESETS"]
