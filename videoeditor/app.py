import os
from typing import List

from moviepy.editor import VideoFileClip, concatenate_videoclips

from .models import ProjectState, VideoClip
from .social_presets import SocialPreset


def _fit_to_preset(clip, preset: SocialPreset):
    """Center-crops and resizes video to the target aspect ratio."""
    target_aspect = preset.width / preset.height
    source_aspect = clip.w / clip.h

    if source_aspect > target_aspect:
        crop_width = clip.h * target_aspect
        x1 = (clip.w - crop_width) / 2
        clip = clip.crop(x1=x1, y1=0, x2=x1 + crop_width, y2=clip.h)
    else:
        crop_height = clip.w / target_aspect
        y1 = (clip.h - crop_height) / 2
        clip = clip.crop(x1=0, y1=y1, x2=clip.w, y2=y1 + crop_height)

    clip = clip.resize((preset.width, preset.height))
    return clip


def _process_clip(item: VideoClip, preset: SocialPreset):
    source = VideoFileClip(item.path)

    if item.trim_start > 0 or (item.trim_end > 0 and item.trim_end < source.duration):
        start = max(0.0, item.trim_start)
        end = item.trim_end if item.trim_end > 0 and item.trim_end < source.duration else source.duration
        source = source.subclip(start, end)

    source = _fit_to_preset(source, preset)
    source = source.fx(lambda c: c, 0)
    return source


def export_project(project: ProjectState, output_path: str, preset: SocialPreset | None = None):
    preset = preset or project.selected_preset()
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    if not project.clips:
        raise ValueError("Project has no clips to export.")

    processed_clips = []
    for clip in project.clips:
        movie_clip = _process_clip(clip, preset)
        processed_clips.append(movie_clip)

    final = concatenate_videoclips(processed_clips, method="compose")
    final.write_videofile(
        output_path,
        fps=preset.fps,
        codec=preset.codec,
        audio_codec=preset.audio_codec,
        preset="medium",
        ffmpeg_params=["-pix_fmt", "yuv420p"],
    )

    for clip in processed_clips:
        clip.close()

    return output_path


def export_batch(project: ProjectState, output_dir: str, presets: List[SocialPreset]):
    os.makedirs(output_dir, exist_ok=True)
    outputs = []

    for preset in presets:
        out = os.path.join(output_dir, f"{project.name}_{preset.name}.{preset.container}")
        export_project(project, out, preset)
        outputs.append(out)

    return outputs


__all__ = ["export_project", "export_batch"]
