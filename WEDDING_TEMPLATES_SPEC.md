# VideoEditor-Pro with Wedding & Event Templates

Professional desktop video editing application with animated titles, templates, and background/music customization for Uzbek weddings and events.

## Feature Requirements

### 1. Animated Titles & Overlays (20+ Templates)
- **Uzbek Wedding Titles:**
  - "Nikoh to'yi" (Wedding ceremony)
  - "To'y boshi" (Wedding start)
  - "Atollar" (Bride's family)
  - "Atirgullar" (Rose/flower animations)
  - "Uzuk olib chiqish" (Ring ceremony)
  - "Qiz/O'g'il nomi" (Bride/Groom names)
  - "Sana va vaqt" (Date and time)
  - "Rahmat" (Thank you)
  - "Dualylar" (Blessings)
  - "Xotira" (Memory/Flashback)
  - "Yangi hayot" (New life)
  - "Sevgi" (Love)

- **Event-Specific Titles:**
  - Birthday animations
  - Anniversary titles
  - Graduation text
  - Corporate event headers
  - Festival titles

### 2. Title Animation Types
- Fade in/out with duration control
- Slide from left/right/top/bottom
- Zoom in/out effect
- Rotate animation
- Blur and focus effect
- Color gradient animation
- Text shadow and glow effects
- 3D text rotation (optional)
- Typewriter effect (letter by letter)
- Bounce and elastic animations

### 3. Background Customization
- Upload custom background image
- Select background video
- Color background (solid color or gradient)
- Blur/opacity controls
- Background position and scale
- Animated background option

### 4. Music/Audio Management
- Replace background music
- Audio volume slider
- Fade in/fade out audio
- Audio preview
- Multiple audio track support
- Audio sync with video timeline
- Mute option for specific clips

### 5. Title Template Editor
- Drag-and-drop text placement
- Font selection (Arial, Times, custom fonts)
- Text size, color, style (bold, italic)
- Text position: top, center, bottom, custom
- Text animation speed control
- Batch apply title to multiple clips
- Save custom title templates
- Preset template library (20+ built-in)

### 6. Preview & Export
- Real-time preview of title + background + music
- Export final video in social media formats
- Support Instagram Reels, Facebook, YouTube
- Resolution options: 720p, 1080p, 4K
- Video codec: H.264/H.265
- Audio codec: AAC
- Bitrate adjustment

## Technical Implementation

### Architecture
- PySide6 GUI
- FFmpeg for rendering
- OpenCV for image/video processing
- PyQt for animations
- Pillow for image manipulation

### Modules
- ui/title_editor.py - Title template editor
- ui/background_panel.py - Background selector
- ui/audio_panel.py - Audio mixer
- core/title_templates.py - 20+ title presets
- core/animation_engine.py - Animation system
- services/title_renderer.py - Render titles with effects
- services/video_composer.py - Combine video + titles + music
- models/title.py - Title data model
- models/template.py - Template model
- render/ffmpeg_engine.py - FFmpeg export

### Data Models
```python
@dataclass
class Title:
    text: str
    font: str
    size: int
    color: tuple
    position: tuple
    animation_type: str
    animation_duration: float
    start_time: float
    end_time: float
    opacity: float
    blur: bool
    shadow: bool
    glow: bool

@dataclass
class TitleTemplate:
    name: str
    description: str
    titles: List[Title]
    background_type: str  # image, video, color
    background_path: str
    music_path: str
    default_duration: float
```

### UI Components
1. **Title Template Selector** - Browse 20+ templates
2. **Text Editor** - Edit title text and properties
3. **Animation Panel** - Choose animation type and speed
4. **Background Panel** - Upload/select background
5. **Audio Mixer** - Upload/adjust background music
6. **Preview Window** - Real-time preview
7. **Timeline** - Adjust timing for each title
8. **Export Dialog** - Choose format and quality

### Pre-built Templates (20+)
1. Nikoh to'yi (fade + slide)
2. To'y boshi (zoom + glow)
3. Atollar (flower animation)
4. Atirgullar (rose/flower effect)
5. Uzuk olib chiqish (ring animation)
6. Qiz nomi (elegant scroll)
7. O'g'il nomi (bold bounce)
8. Sana (typewriter effect)
9. Vaqt (digital clock style)
10. Rahmat (thank you fade)
11. Dualylar (blessing text)
12. Xotira (memory flashback)
13. Yangi hayot (new life glow)
14. Sevgi (love heart animation)
15. Tug'ilgan kun (birthday balloons)
16. Yildonama (anniversary sparkle)
17. Bitiruvchi (graduation scroll)
18. Korporativ (professional title)
19. Bayram (festival colorful)
20. Sahifa (chapter/scene transition)

### Export Presets
- Instagram Reels 9:16 1080x1920
- Facebook Story 9:16 1080x1920
- YouTube 16:9 1920x1080
- TikTok 9:16 1080x1920
- Telegram 16:9 1920x1080

## User Workflow
1. Open VideoEditor-Pro
2. Select title template from 20+ presets
3. Edit title text and properties
4. Upload background image/video (or use default)
5. Upload background music (or use default)
6. Preview result in real-time
7. Adjust timing, animations, colors
8. Export to desired social media format

## Installation & Run
```bash
pip install -r requirements.txt
python main.py
```

## Dependencies
- PySide6>=6.7.0
- FFmpeg
- OpenCV
- moviepy
- Pillow
- NumPy
