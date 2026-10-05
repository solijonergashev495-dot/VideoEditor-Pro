from dataclasses import dataclass


@dataclass(frozen=True)
class SocialPreset:
    name: str
    platform: str
    label: str
    width: int
    height: int
    fps: int = 30
    codec: str = "libx264"
    audio_codec: str = "aac"
    container: str = "mp4"

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    @property
    def filename(self) -> str:
        safe = self.name.replace(" ", "_")
        return f"{safe}.{self.container}"


SOCIAL_PRESETS = [
    SocialPreset("Instagram_Reels_9_16", "Instagram", "Reels (9:16)", 1080, 1920),
    SocialPreset("Instagram_Story_9_16", "Instagram", "Story (9:16)", 1080, 1920),
    SocialPreset("Instagram_Feed_1_1", "Instagram", "Feed Square (1:1)", 1080, 1080),
    SocialPreset("Instagram_Feed_4_5", "Instagram", "Feed Portrait (4:5)", 1080, 1350),
    SocialPreset("Instagram_Feed_16_9", "Instagram", "Feed Landscape (16:9)", 1920, 1080),
    SocialPreset("Facebook_Story_9_16", "Facebook", "Story (9:16)", 1080, 1920),
    SocialPreset("Facebook_Feed_1_1", "Facebook", "Feed Square (1:1)", 1080, 1080),
    SocialPreset("Facebook_Feed_16_9", "Facebook", "Feed Landscape (16:9)", 1920, 1080),
    SocialPreset("Facebook_Ads_4_5", "Facebook", "Ads Portrait (4:5)", 1080, 1350),
    SocialPreset("Facebook_Ads_9_16", "Facebook", "Ads Vertical (9:16)", 1080, 1920),
]


def get_preset_by_name(name: str) -> SocialPreset | None:
    for preset in SOCIAL_PRESETS:
        if preset.name == name:
            return preset
    return None


def get_presets_by_platform(platform: str):
    return [preset for preset in SOCIAL_PRESETS if preset.platform.lower() == platform.lower()]


__all__ = ["SocialPreset", "SOCIAL_PRESETS", "get_preset_by_name", "get_presets_by_platform"]
