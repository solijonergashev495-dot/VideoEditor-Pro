import os
from pathlib import Path
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QGroupBox,
    QTextEdit,
)

from .models import ProjectState, VideoClip
from .social_presets import SOCIAL_PRESETS, get_preset_by_name
from .exporter import export_project, export_batch


class VideoEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project = ProjectState(name="New Project")
        self.library_paths: List[str] = []
        self.current_file = ""
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("VideoEditor-Pro")
        self.resize(1300, 820)

        central = QWidget()
        root = QHBoxLayout(central)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        add_media_btn = QPushButton("Add media")
        add_media_btn.clicked.connect(self._add_media)
        left_layout.addWidget(add_media_btn)

        self.library_list = QListWidget()
        left_layout.addWidget(self.library_list)

        add_timeline_btn = QPushButton("Add to timeline")
        add_timeline_btn.clicked.connect(self._add_selected_to_timeline)
        left_layout.addWidget(add_timeline_btn)

        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)

        title = QLabel("Timeline")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        center_layout.addWidget(title)

        self.timeline_list = QListWidget()
        center_layout.addWidget(self.timeline_list)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        info_group = QGroupBox("Project")
        info_layout = QFormLayout(info_group)
        self.project_name = QLabel("New Project")
        self.project_info = QTextEdit()
        self.project_info.setReadOnly(True)
        self.project_info.setPlainText("No video selected.")
        info_layout.addRow("Name:", self.project_name)
        info_layout.addRow("Info:", self.project_info)
        right_layout.addWidget(info_group)

        export_group = QGroupBox("Export")
        export_layout = QFormLayout(export_group)
        self.preset_combo = QComboBox()
        for preset in SOCIAL_PRESETS:
            self.preset_combo.addItem(f"{preset.platform} - {preset.label}", preset.name)
        export_layout.addRow("Preset:", self.preset_combo)

        self.export_btn = QPushButton("Export")
        self.export_btn.clicked.connect(self._export_current)
        export_layout.addRow(self.export_btn)

        self.batch_export_btn = QPushButton("Export all social formats")
        self.batch_export_btn.clicked.connect(self._export_batch)
        export_layout.addRow(self.batch_export_btn)
        right_layout.addWidget(export_group)

        self.timeline_list.currentItemChanged.connect(self._show_selected_clip_info)

        left_panel.setMinimumWidth(260)
        center_panel.setMinimumWidth(460)
        right_panel.setMinimumWidth(300)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(center_panel)
        splitter.addWidget(right_panel)
        root.addWidget(splitter)

        self.setCentralWidget(central)

    def _add_media(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select video files",
            os.path.expanduser("~"),
            "Video files (*.mp4 *.mov *.mkv *.avi *.m4v *.wmv *.webm)",
        )
        if not paths:
            return

        for path in paths:
            if path not in self.library_paths:
                self.library_paths.append(path)
                item = QListWidgetItem(os.path.basename(path))
                item.setData(Qt.UserRole, path)
                self.library_list.addItem(item)

        if self.library_paths:
            self.current_file = self.library_paths[0]

    def _add_selected_to_timeline(self):
        selected = self.library_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No media selected", "Select one or more video files from the media library.")
            return

        for item in selected:
            path = item.data(Qt.UserRole)
            clip = VideoClip(path=path, label=os.path.basename(path), trim_start=0.0, trim_end=0.0)
            self.project.clips.append(clip)
            timeline_item = QListWidgetItem(f"{clip.label}")
            timeline_item.setData(Qt.UserRole, len(self.project.clips) - 1)
            self.timeline_list.addItem(timeline_item)

        self.project_info.setPlainText(
            f"{len(self.project.clips)} clips in timeline\n"
            f"Project ready for export."
        )

    def _show_selected_clip_info(self):
        item = self.timeline_list.currentItem()
        if not item:
            return
        index = item.data(Qt.UserRole)
        clip = self.project.clips[index]
        info = (
            f"File: {clip.label}\n"
            f"Trim start: {clip.trim_start:.2f}s\n"
            f"Trim end: {clip.trim_end:.2f}s\n"
            f"Volume: {clip.volume}\n"
            f"Speed: {clip.speed}x"
        )
        self.project_info.setPlainText(info)

    def _export_current(self):
        if not self.project.clips:
            QMessageBox.warning(self, "No timeline clips", "Add at least one video to the timeline before exporting.")
            return

        preset_name = self.preset_combo.currentData()
        preset = get_preset_by_name(preset_name)
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save exported video",
            os.path.join(os.path.expanduser("~"), "Desktop", f"{preset.name}.{preset.container}"),
            "MP4 video (*.mp4)",
        )
        if not output_path:
            return

        try:
            export_project(self.project, output_path, preset)
            QMessageBox.information(self, "Export complete", f"Video saved:\n{output_path}")
        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, "Export failed", str(exc))

    def _export_batch(self):
        if not self.project.clips:
            QMessageBox.warning(self, "No timeline clips", "Add at least one video to the timeline before exporting.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Choose export folder", os.path.expanduser("~"))
        if not output_dir:
            return

        try:
            outputs = export_batch(self.project, output_dir, SOCIAL_PRESETS[:5])
            QMessageBox.information(self, "Batch export complete", "\n".join(outputs))
        except Exception as exc:  # pragma: no cover
            QMessageBox.critical(self, "Batch export failed", str(exc))


def main():
    app = QApplication([])
    w = VideoEditorWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
