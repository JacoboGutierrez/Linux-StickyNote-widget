#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import uuid
from pathlib import Path
from typing import Any

from PySide6.QtCore import (
    QEvent,
    QIODevice,
    QPoint,
    QSaveFile,
    QSettings,
    QStandardPaths,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QColor,
    QCloseEvent,
    QIcon,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QColorDialog,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QSizeGrip,
    QSystemTrayIcon,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)

APP_NAME = "Notas Adhesivas"
APP_ID = "virtual-sticky-notes"

CURRENT_LANGUAGE = "en"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "window_title": "Sticky Notes",
        "app_title": "Sticky Notes",
        "subtitle": "Choose which notes stay visible on the desktop.",
        "new": "+ New",
        "new_tooltip": "Create a new note",
        "show_all": "Show all",
        "hide_all": "Hide all",
        "your_notes": "Your notes",
        "hint": "Check to show · double-click to open · drag to reorder",
        "open": "Open",
        "duplicate": "Duplicate",
        "delete": "Delete",
        "language": "Language",
        "drag_note": "Drag note",
        "title_placeholder": "Title",
        "change_color": "Change color",
        "note_options": "Note theme and behavior",
        "hide_note": "Hide from desktop",
        "content_placeholder": "Write your note…",
        "custom_color": "Custom…",
        "choose_color": "Choose color",
        "theme": "Theme",
        "default_theme": "Default",
        "behavior": "Behavior",
        "desktop_only": "Desktop only",
        "always_on_top": "Always on top",
        "untitled": "Untitled",
        "new_note_title": "Note {n}",
        "copy_suffix": "copy",
        "delete_note_title": "Delete note",
        "delete_note_prompt": "Delete “{title}”?",
        "save_error": "Save error",
        "save_open_path": "Could not save {path}",
        "save_commit_path": "Could not finish saving {path}",
        "tray_open": "Open panel",
        "tray_new": "New note",
        "tray_quit": "Quit",
        "tray_running": "The application is still running in the notification area.",
        "color_yellow": "Yellow",
        "color_pink": "Pink",
        "color_blue": "Light blue",
        "color_green": "Green",
        "color_lavender": "Lavender",
        "color_peach": "Peach",
        "color_mint": "Mint",
        "color_warm_gray": "Warm gray",
    },
    "es": {
        "window_title": "Notas Adhesivas",
        "app_title": "Notas adhesivas",
        "subtitle": "Elige cuáles quedan visibles en el escritorio.",
        "new": "+ Nueva",
        "new_tooltip": "Crear una nueva nota",
        "show_all": "Mostrar todas",
        "hide_all": "Ocultar todas",
        "your_notes": "Tus notas",
        "hint": "Marca para mostrar · doble clic para abrir · arrastra para ordenar",
        "open": "Abrir",
        "duplicate": "Duplicar",
        "delete": "Eliminar",
        "language": "Idioma",
        "drag_note": "Arrastrar nota",
        "title_placeholder": "Título",
        "change_color": "Cambiar color",
        "note_options": "Tema y comportamiento de la nota",
        "hide_note": "Ocultar del escritorio",
        "content_placeholder": "Escribe tu nota…",
        "custom_color": "Personalizado…",
        "choose_color": "Elegir color",
        "theme": "Tema",
        "default_theme": "Por defecto",
        "behavior": "Comportamiento",
        "desktop_only": "Solo en el escritorio",
        "always_on_top": "Superponer a todas las ventanas",
        "untitled": "Sin título",
        "new_note_title": "Nota {n}",
        "copy_suffix": "copia",
        "delete_note_title": "Eliminar nota",
        "delete_note_prompt": "¿Eliminar “{title}”?",
        "save_error": "Error al guardar",
        "save_open_path": "No se pudo guardar {path}",
        "save_commit_path": "No se pudo confirmar el guardado de {path}",
        "tray_open": "Abrir panel",
        "tray_new": "Nueva nota",
        "tray_quit": "Salir",
        "tray_running": "La aplicación sigue activa en el área de notificación.",
        "color_yellow": "Amarillo",
        "color_pink": "Rosa",
        "color_blue": "Celeste",
        "color_green": "Verde",
        "color_lavender": "Lavanda",
        "color_peach": "Durazno",
        "color_mint": "Menta",
        "color_warm_gray": "Gris cálido",
    },
}

PASTEL_COLORS: dict[str, str] = {
    "yellow": "#FFF2A8",
    "pink": "#FFD4E5",
    "blue": "#CFE8FF",
    "green": "#D7F5D0",
    "lavender": "#E4D7FF",
    "peach": "#FFD9B8",
    "mint": "#CFF5E7",
    "warm_gray": "#ECE7DF",
}


def tr(key: str, **values: Any) -> str:
    text = TRANSLATIONS.get(CURRENT_LANGUAGE, TRANSLATIONS["en"]).get(key, key)
    return text.format(**values) if values else text


def set_current_language(language: str) -> None:
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = "es" if language == "es" else "en"


DEFAULT_NOTE = {
    "title": "",
    "content": "",
    "color": PASTEL_COLORS["yellow"],
    "theme": "default",
    "always_on_top": True,
    "visible": True,
    "x": 120,
    "y": 120,
    "width": 300,
    "height": 250,
}


class NotesStore:
    def __init__(self) -> None:
        base = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        if not base:
            base = str(Path.home() / ".local" / "share" / APP_ID)
        self.directory = Path(base)
        self.path = self.directory / "notes.json"
        self.directory.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            backup = self.path.with_suffix(".broken.json")
            try:
                self.path.replace(backup)
            except OSError:
                pass
            return []

        if not isinstance(data, dict) or not isinstance(data.get("notes"), list):
            return []

        notes: list[dict[str, Any]] = []
        for raw in data["notes"]:
            if not isinstance(raw, dict):
                continue
            note = dict(DEFAULT_NOTE)
            note.update(raw)
            note["id"] = str(raw.get("id") or uuid.uuid4())
            note["visible"] = bool(note.get("visible", False))
            note["theme"] = "crs" if str(note.get("theme", "default")).lower() == "crs" else "default"
            note["always_on_top"] = bool(note.get("always_on_top", True))
            for key in ("x", "y", "width", "height"):
                try:
                    note[key] = int(note[key])
                except (TypeError, ValueError):
                    note[key] = DEFAULT_NOTE[key]
            note["width"] = max(220, note["width"])
            note["height"] = max(170, note["height"])
            notes.append(note)
        return notes

    def save(self, notes: list[dict[str, Any]]) -> None:
        payload = json.dumps({"version": 2, "notes": notes}, ensure_ascii=False, indent=2)
        save_file = QSaveFile(str(self.path))
        if not save_file.open(QIODevice.OpenModeFlag.WriteOnly):
            raise OSError(tr("save_open_path", path=self.path))
        save_file.write(payload.encode("utf-8"))
        if not save_file.commit():
            raise OSError(tr("save_commit_path", path=self.path))


class DragBar(QFrame):
    def __init__(self, window: "StickyNoteWindow") -> None:
        super().__init__(window)
        self.note_window = window
        self._drag_offset: QPoint | None = None
        self.setFixedHeight(34)
        self.setCursor(Qt.CursorShape.SizeAllCursor)

    def eventFilter(self, watched, event) -> bool:  # type: ignore[override]
        if event.type() == QEvent.Type.MouseButtonPress:
            self.mousePressEvent(event)
            return event.isAccepted()
        if event.type() == QEvent.Type.MouseMove:
            self.mouseMoveEvent(event)
            return event.isAccepted()
        if event.type() == QEvent.Type.MouseButtonRelease:
            self.mouseReleaseEvent(event)
            return event.isAccepted()
        return super().eventFilter(watched, event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_offset = event.globalPosition().toPoint() - self.note_window.frameGeometry().topLeft()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_offset is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.note_window.move(event.globalPosition().toPoint() - self._drag_offset)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_offset = None
        super().mouseReleaseEvent(event)


class NoteSheet(QFrame):
    """Superficie visual de una nota, con forma pastel o CRS."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.theme_name = "default"
        self.note_color = QColor(DEFAULT_NOTE["color"])
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

    def set_appearance(self, theme_name: str, color: str) -> None:
        self.theme_name = "crs" if theme_name == "crs" else "default"
        parsed = QColor(color)
        self.note_color = parsed if parsed.isValid() else QColor(DEFAULT_NOTE["color"])
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(3, 3, -3, -3)
        path = QPainterPath()

        if self.theme_name == "crs":
            cut = max(24.0, min(42.0, min(rect.width(), rect.height()) * 0.14))
            path.moveTo(rect.left() + cut, rect.top())
            path.lineTo(rect.right(), rect.top())
            path.lineTo(rect.right(), rect.bottom() - cut)
            path.lineTo(rect.right() - cut, rect.bottom())
            path.lineTo(rect.left(), rect.bottom())
            path.lineTo(rect.left(), rect.top() + cut)
            path.closeSubpath()
            painter.fillPath(path, QColor("#000000"))
            pen = QPen(QColor("#001dff"), 5)
            pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
            painter.setPen(pen)
            painter.drawPath(path)
        else:
            path.addRoundedRect(rect, 12, 12)
            painter.fillPath(path, self.note_color)
            painter.setPen(QPen(self.note_color.darker(122), 1))
            painter.drawPath(path)

        painter.end()


class StickyNoteWindow(QWidget):
    changed = Signal(str, dict)
    visibility_requested = Signal(str, bool)

    def __init__(self, note: dict[str, Any]) -> None:
        super().__init__()
        self.note_id = note["id"]
        self.current_color = str(note.get("color", DEFAULT_NOTE["color"]))
        self.current_theme = "crs" if note.get("theme") == "crs" else "default"
        self.always_on_top = bool(note.get("always_on_top", True))
        self._loading = True
        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(300)
        self._save_timer.timeout.connect(self._emit_text_changes)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setMinimumSize(220, 170)
        self._apply_window_flags(self.always_on_top, restore_visibility=False)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(0)

        self.sheet = NoteSheet()
        self.sheet.setObjectName("sheet")
        self.sheet_layout = QVBoxLayout(self.sheet)
        self.sheet_layout.setContentsMargins(10, 6, 8, 8)
        self.sheet_layout.setSpacing(4)

        self.drag_bar = DragBar(self)
        bar_layout = QHBoxLayout(self.drag_bar)
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setSpacing(4)

        self.drag_handle = QLabel("⠿")
        self.drag_handle.setToolTip(tr("drag_note"))
        self.drag_handle.setCursor(Qt.CursorShape.SizeAllCursor)
        self.drag_handle.installEventFilter(self.drag_bar)

        self.title_edit = QLineEdit()
        self.title_edit.setObjectName("desktopTitle")
        self.title_edit.setPlaceholderText(tr("title_placeholder"))
        self.title_edit.textChanged.connect(self._schedule_text_save)

        self.color_button = QToolButton()
        self.color_button.setText("●")
        self.color_button.setToolTip(tr("change_color"))
        self.color_button.clicked.connect(self._show_color_menu)

        self.options_button = QToolButton()
        self.options_button.setText("⋮")
        self.options_button.setToolTip(tr("note_options"))
        self.options_button.clicked.connect(self._show_options_menu)

        self.hide_button = QToolButton()
        self.hide_button.setText("×")
        self.hide_button.setToolTip(tr("hide_note"))
        self.hide_button.clicked.connect(lambda: self.visibility_requested.emit(self.note_id, False))

        bar_layout.addWidget(self.drag_handle)
        bar_layout.addWidget(self.title_edit, 1)
        bar_layout.addWidget(self.color_button)
        bar_layout.addWidget(self.options_button)
        bar_layout.addWidget(self.hide_button)

        self.content_edit = QTextEdit()
        self.content_edit.setObjectName("desktopContent")
        self.content_edit.setAcceptRichText(False)
        self.content_edit.setPlaceholderText(tr("content_placeholder"))
        self.content_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_edit.textChanged.connect(self._schedule_text_save)

        grip_row = QHBoxLayout()
        grip_row.setContentsMargins(0, 0, 0, 0)
        grip_row.addStretch(1)
        self.grip = QSizeGrip(self.sheet)
        grip_row.addWidget(self.grip)

        self.sheet_layout.addWidget(self.drag_bar)
        self.sheet_layout.addWidget(self.content_edit, 1)
        self.sheet_layout.addLayout(grip_row)
        outer.addWidget(self.sheet)

        self.apply_note(note)
        self.apply_language()
        self._loading = False

    def apply_note(self, note: dict[str, Any]) -> None:
        self._loading = True
        self.title_edit.setText(note.get("title", ""))
        self.content_edit.setPlainText(note.get("content", ""))
        self.current_theme = "crs" if note.get("theme") == "crs" else "default"
        self.set_note_color(note.get("color", DEFAULT_NOTE["color"]), emit_change=False)
        self.set_theme(self.current_theme, emit_change=False)
        self.set_always_on_top(bool(note.get("always_on_top", True)), emit_change=False)
        self.setGeometry(
            int(note.get("x", 120)),
            int(note.get("y", 120)),
            int(note.get("width", 300)),
            int(note.get("height", 250)),
        )
        self._loading = False

    def apply_language(self) -> None:
        self.drag_handle.setToolTip(tr("drag_note"))
        self.title_edit.setPlaceholderText(tr("title_placeholder"))
        self.color_button.setToolTip(tr("change_color"))
        self.options_button.setToolTip(tr("note_options"))
        self.hide_button.setToolTip(tr("hide_note"))
        self.content_edit.setPlaceholderText(tr("content_placeholder"))

    def _show_color_menu(self) -> None:
        if self.current_theme == "crs":
            return
        menu = QMenu(self)
        for color_key, color in PASTEL_COLORS.items():
            action = QAction(tr(f"color_{color_key}"), self)
            action.setCheckable(True)
            action.setChecked(QColor(color).name() == QColor(self.current_color).name())
            action.triggered.connect(lambda checked=False, c=color: self._set_color_from_picker(c))
            menu.addAction(action)
        menu.addSeparator()
        custom_action = QAction(tr("custom_color"), self)
        custom_action.triggered.connect(self._choose_custom_color)
        menu.addAction(custom_action)
        menu.exec(self.color_button.mapToGlobal(self.color_button.rect().bottomLeft()))

    def _show_options_menu(self) -> None:
        menu = QMenu(self)

        theme_menu = menu.addMenu(tr("theme"))
        theme_group = QActionGroup(theme_menu)
        theme_group.setExclusive(True)
        for label, value in ((tr("default_theme"), "default"), ("CRS", "crs")):
            action = QAction(label, theme_menu)
            action.setCheckable(True)
            action.setChecked(self.current_theme == value)
            action.triggered.connect(lambda checked=False, v=value: self.set_theme(v))
            theme_group.addAction(action)
            theme_menu.addAction(action)

        position_menu = menu.addMenu(tr("behavior"))
        position_group = QActionGroup(position_menu)
        position_group.setExclusive(True)

        desktop_action = QAction(tr("desktop_only"), position_menu)
        desktop_action.setCheckable(True)
        desktop_action.setChecked(not self.always_on_top)
        desktop_action.triggered.connect(lambda checked=False: self.set_always_on_top(False))
        position_group.addAction(desktop_action)
        position_menu.addAction(desktop_action)

        top_action = QAction(tr("always_on_top"), position_menu)
        top_action.setCheckable(True)
        top_action.setChecked(self.always_on_top)
        top_action.triggered.connect(lambda checked=False: self.set_always_on_top(True))
        position_group.addAction(top_action)
        position_menu.addAction(top_action)

        menu.exec(self.options_button.mapToGlobal(self.options_button.rect().bottomLeft()))

    def _choose_custom_color(self) -> None:
        current = QColor(self.current_color)
        chosen = QColorDialog.getColor(current, self, tr("choose_color"))
        if chosen.isValid():
            self._set_color_from_picker(chosen.name())

    def _set_color_from_picker(self, color: str) -> None:
        self.set_note_color(color)

    def set_note_color(self, color: str, emit_change: bool = True) -> None:
        safe = QColor(color)
        if not safe.isValid():
            safe = QColor(DEFAULT_NOTE["color"])
        self.current_color = safe.name()
        self._apply_note_style()
        if emit_change:
            self.changed.emit(self.note_id, {"color": self.current_color})

    def set_theme(self, theme_name: str, emit_change: bool = True) -> None:
        self.current_theme = "crs" if theme_name == "crs" else "default"
        self._apply_note_style()
        if emit_change:
            self.changed.emit(self.note_id, {"theme": self.current_theme})

    def set_always_on_top(self, enabled: bool, emit_change: bool = True) -> None:
        enabled = bool(enabled)
        if self.always_on_top != enabled or not self.windowFlags():
            self.always_on_top = enabled
            self._apply_window_flags(enabled)
        else:
            self.always_on_top = enabled
        if emit_change:
            self.changed.emit(self.note_id, {"always_on_top": enabled})

    def _apply_window_flags(self, always_on_top: bool, restore_visibility: bool = True) -> None:
        """Aplica el nivel de apilado únicamente a esta nota.

        Qt.Tool puede hacer que algunos gestores de ventanas de Linux agrupen todas
        las notas de la aplicación como ventanas auxiliares y las mantengan encima
        en conjunto. Usar Qt.Window conserva cada nota como una ventana superior
        independiente, de modo que WindowStaysOnTopHint solo afecta a la nota que
        tiene activada esa opción.
        """
        was_visible = self.isVisible() if restore_visibility else False
        geometry = self.geometry()

        flags = Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint
        if always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint

        self.setWindowFlags(flags)
        if geometry.isValid():
            self.setGeometry(geometry)

        if was_visible:
            self.show()
            if always_on_top:
                self.raise_()

    def _apply_note_style(self) -> None:
        safe = QColor(self.current_color)
        if not safe.isValid():
            safe = QColor(DEFAULT_NOTE["color"])
        hover = safe.darker(108).name()
        border = safe.darker(122).name()

        self.sheet.set_appearance(self.current_theme, safe.name())
        if self.current_theme == "crs":
            self.sheet_layout.setContentsMargins(18, 12, 18, 18)
            self.color_button.hide()
            self.drag_handle.setStyleSheet(
                'color: #ffffff; font-family: "Consolas", "Courier New", monospace; '
                'font-size: 18px; padding: 0 2px;'
            )
            self.sheet.setStyleSheet(
                """
                QLineEdit#desktopTitle {
                    background: transparent;
                    border: none;
                    color: #ffffff;
                    font-family: "Consolas", "Courier New", monospace;
                    font-size: 16px;
                    font-weight: 700;
                    padding: 2px 4px;
                }
                QTextEdit#desktopContent {
                    background: transparent;
                    border: none;
                    color: #ffffff;
                    font-family: "Consolas", "Courier New", monospace;
                    font-size: 14px;
                    padding: 2px;
                    selection-background-color: #001dff;
                    selection-color: #ffffff;
                }
                QTextEdit#desktopContent QScrollBar {
                    width: 0px;
                    height: 0px;
                    background: transparent;
                }
                QToolButton {
                    background: transparent;
                    border: none;
                    border-radius: 12px;
                    color: #ffffff;
                    font-family: "Consolas", "Courier New", monospace;
                    font-size: 18px;
                    min-width: 26px;
                    min-height: 26px;
                }
                QToolButton:hover { background: #00115f; color: #ffffff; }
                QSizeGrip { background: transparent; }
                """
            )
        else:
            self.sheet_layout.setContentsMargins(10, 6, 8, 8)
            self.color_button.show()
            self.drag_handle.setStyleSheet("color: #666; font-size: 18px; padding: 0 2px;")
            self.sheet.setStyleSheet(
                f"""
                QLineEdit#desktopTitle {{
                    background: transparent;
                    border: none;
                    color: #2f2f2f;
                    font-size: 16px;
                    font-weight: 700;
                    padding: 2px 4px;
                }}
                QTextEdit#desktopContent {{
                    background: transparent;
                    border: none;
                    color: #303030;
                    font-size: 14px;
                    padding: 2px;
                    selection-background-color: {hover};
                }}
                QTextEdit#desktopContent QScrollBar {{
                    width: 0px;
                    height: 0px;
                    background: transparent;
                }}
                QToolButton {{
                    background: transparent;
                    border: none;
                    border-radius: 12px;
                    color: #555;
                    font-size: 18px;
                    min-width: 26px;
                    min-height: 26px;
                }}
                QToolButton:hover {{ background: {hover}; color: #111; }}
                QSizeGrip {{ background: transparent; }}
                """
            )
            self.color_button.setStyleSheet(
                f"background: transparent; border: none; color: {border}; "
                "font-size: 18px; min-width: 26px; min-height: 26px;"
            )

    def _schedule_text_save(self) -> None:
        if not self._loading:
            self._save_timer.start()

    def _emit_text_changes(self) -> None:
        self.changed.emit(
            self.note_id,
            {"title": self.title_edit.text(), "content": self.content_edit.toPlainText()},
        )

    def moveEvent(self, event) -> None:  # type: ignore[override]
        super().moveEvent(event)
        self._schedule_geometry_save()

    def resizeEvent(self, event) -> None:  # type: ignore[override]
        super().resizeEvent(event)
        self._schedule_geometry_save()

    def _schedule_geometry_save(self) -> None:
        if self._loading:
            return
        self.changed.emit(
            self.note_id,
            {
                "x": self.x(),
                "y": self.y(),
                "width": self.width(),
                "height": self.height(),
            },
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        event.ignore()
        self.visibility_requested.emit(self.note_id, False)


class MainWindow(QMainWindow):
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app
        self.settings = QSettings("SantiApps", APP_ID)
        saved_language = str(self.settings.value("language", "en"))
        set_current_language(saved_language if saved_language in {"en", "es"} else "en")

        self.store = NotesStore()
        self.notes = self.store.load()
        self.note_windows: dict[str, StickyNoteWindow] = {}
        self._loading_ui = False
        self._quitting = False
        self._tray_notice_shown = False

        self.setWindowTitle(tr("window_title"))
        self.resize(423, 623)
        self.setMinimumSize(423, 623)
        self.setWindowIcon(make_icon())

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(250)
        self._save_timer.timeout.connect(self._save_now)

        self._build_ui()
        self._build_tray()
        self._populate_list()

        if not self.notes:
            self.create_note()
        else:
            self.note_list.setCurrentRow(0)

        QTimer.singleShot(0, self._restore_visible_notes)

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(15, 14, 15, 14)
        root.setSpacing(9)

        header = QHBoxLayout()
        header.setSpacing(9)

        self.app_title_label = QLabel()
        self.app_title_label.setObjectName("appTitle")
        self.new_button = QPushButton()
        self.new_button.setObjectName("primary")
        self.new_button.clicked.connect(self.create_note)

        header.addWidget(self.app_title_label, 1)
        header.addWidget(self.new_button)
        root.addLayout(header)

        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("subtitle")
        self.subtitle_label.setWordWrap(True)
        root.addWidget(self.subtitle_label)

        language_row = QHBoxLayout()
        language_row.setSpacing(8)
        language_row.addStretch(1)
        self.language_label = QLabel()
        self.language_label.setObjectName("languageLabel")
        self.language_combo = QComboBox()
        self.language_combo.setObjectName("languageCombo")
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Español", "es")
        selected_index = self.language_combo.findData(CURRENT_LANGUAGE)
        self.language_combo.setCurrentIndex(max(0, selected_index))
        self.language_combo.currentIndexChanged.connect(self._on_language_changed)
        language_row.addWidget(self.language_label)
        language_row.addWidget(self.language_combo)
        root.addLayout(language_row)

        visibility_actions = QHBoxLayout()
        visibility_actions.setSpacing(8)
        self.show_all_button = QPushButton()
        self.show_all_button.clicked.connect(lambda: self.set_all_visibility(True))
        self.hide_all_button = QPushButton()
        self.hide_all_button.clicked.connect(lambda: self.set_all_visibility(False))
        visibility_actions.addWidget(self.show_all_button)
        visibility_actions.addWidget(self.hide_all_button)
        root.addLayout(visibility_actions)

        panel = QFrame()
        panel.setObjectName("panel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(10, 10, 10, 10)
        panel_layout.setSpacing(8)

        self.panel_title_label = QLabel()
        self.panel_title_label.setObjectName("panelTitle")
        panel_layout.addWidget(self.panel_title_label)

        self.note_list = QListWidget()
        self.note_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.note_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.note_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.note_list.itemChanged.connect(self._on_item_changed)
        self.note_list.currentItemChanged.connect(self._on_selection_changed)
        self.note_list.itemDoubleClicked.connect(lambda _item: self._focus_current_note())
        self.note_list.model().rowsMoved.connect(self._on_rows_moved)
        panel_layout.addWidget(self.note_list, 1)

        self.hint_label = QLabel()
        self.hint_label.setObjectName("hint")
        self.hint_label.setWordWrap(True)
        panel_layout.addWidget(self.hint_label)
        root.addWidget(panel, 1)

        bottom_actions = QHBoxLayout()
        bottom_actions.setSpacing(8)
        self.focus_button = QPushButton()
        self.focus_button.clicked.connect(self._focus_current_note)
        self.duplicate_button = QPushButton()
        self.duplicate_button.clicked.connect(self._duplicate_current_note)
        self.delete_button = QPushButton()
        self.delete_button.setObjectName("danger")
        self.delete_button.clicked.connect(self._delete_current_note)
        bottom_actions.addWidget(self.focus_button)
        bottom_actions.addWidget(self.duplicate_button)
        bottom_actions.addWidget(self.delete_button)
        root.addLayout(bottom_actions)

        self.setStyleSheet(
            """
            QMainWindow, QWidget {
                background: #e8e7e4;
                color: #121212;
                font-size: 13px;
            }
            QLabel#appTitle {
                font-size: 24px;
                font-weight: 700;
            }
            QLabel#subtitle, QLabel#hint, QLabel#languageLabel {
                color: #716d65;
            }
            QLabel#hint {
                font-size: 12px;
                background: #e8e7e4;
                padding: 2px 0;
            }
            QLabel#panelTitle {
                background: #e7e6e2;
                color: #111111;
                font-size: 14px;
                font-weight: 700;
                padding: 1px 2px;
            }
            QFrame#panel {
                background: #dfddd7;
                border: 1px solid #c4c0b6;
                border-radius: 12px;
            }
            QListWidget {
                background: #e7e6e2;
                color: #111111;
                border: 1px solid #c4c0b6;
                border-radius: 9px;
                padding: 5px;
                outline: none;
            }
            QListWidget::item {
                min-height: 36px;
                border-radius: 7px;
                padding: 5px 7px;
            }
            QListWidget::item:selected {
                background: #c4c0b6;
                color: #111111;
            }
            QPushButton, QComboBox {
                background: #cfccc4;
                color: #111111;
                border: 1px solid #bbb7ac;
                border-radius: 9px;
                padding: 8px 10px;
            }
            QPushButton:hover, QComboBox:hover {
                background: #d7d4cd;
            }
            QPushButton:pressed {
                background: #c1bdb4;
            }
            QPushButton:disabled {
                color: #8c877f;
                background: #dfddd7;
                border-color: #c9c5bc;
            }
            QPushButton#primary {
                background: #101d5e;
                color: #ffffff;
                border-color: #101d5e;
                font-weight: 700;
            }
            QPushButton#primary:hover {
                background: #192a78;
            }
            QPushButton#danger {
                background: #b2d6d1;
                color: #111111;
                border-color: #94c7c0;
            }
            QPushButton#danger:hover {
                background: #c3e4e0;
            }
            QComboBox {
                min-width: 105px;
                padding-right: 24px;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox QAbstractItemView {
                background: #e7e6e2;
                color: #111111;
                border: 1px solid #bbb7ac;
                selection-background-color: #c4c0b6;
                selection-color: #111111;
                outline: none;
            }
            """
        )

        self._apply_language()

    def _apply_language(self) -> None:
        self.setWindowTitle(tr("window_title"))
        self.app.setApplicationDisplayName(tr("window_title"))

        if hasattr(self, "app_title_label"):
            self.app_title_label.setText(tr("app_title"))
            self.subtitle_label.setText(tr("subtitle"))
            self.language_label.setText(tr("language"))
            self.new_button.setText(tr("new"))
            self.new_button.setToolTip(tr("new_tooltip"))
            self.show_all_button.setText(tr("show_all"))
            self.hide_all_button.setText(tr("hide_all"))
            self.panel_title_label.setText(tr("your_notes"))
            self.hint_label.setText(tr("hint"))
            self.focus_button.setText(tr("open"))
            self.duplicate_button.setText(tr("duplicate"))
            self.delete_button.setText(tr("delete"))

        if hasattr(self, "tray"):
            self.tray.setToolTip(tr("window_title"))
            self.tray_open_action.setText(tr("tray_open"))
            self.tray_new_action.setText(tr("tray_new"))
            self.tray_show_all_action.setText(tr("show_all"))
            self.tray_hide_all_action.setText(tr("hide_all"))
            self.tray_quit_action.setText(tr("tray_quit"))

    def _on_language_changed(self, _index: int) -> None:
        language = str(self.language_combo.currentData() or "en")
        language = "es" if language == "es" else "en"
        if language == CURRENT_LANGUAGE:
            return

        selected_id = self.current_note_id()
        set_current_language(language)
        self.settings.setValue("language", language)
        self.settings.sync()
        self._apply_language()

        for window in self.note_windows.values():
            window.apply_language()

        self._populate_list(preferred_id=selected_id)

    def _build_tray(self) -> None:
        self.tray = QSystemTrayIcon(make_icon(), self)
        menu = QMenu()
        self.tray_open_action = QAction(self)
        self.tray_open_action.triggered.connect(self.show_manager)
        self.tray_new_action = QAction(self)
        self.tray_new_action.triggered.connect(self.create_note)
        self.tray_show_all_action = QAction(self)
        self.tray_show_all_action.triggered.connect(lambda: self.set_all_visibility(True))
        self.tray_hide_all_action = QAction(self)
        self.tray_hide_all_action.triggered.connect(lambda: self.set_all_visibility(False))
        self.tray_quit_action = QAction(self)
        self.tray_quit_action.triggered.connect(self.quit_application)
        menu.addAction(self.tray_open_action)
        menu.addAction(self.tray_new_action)
        menu.addSeparator()
        menu.addAction(self.tray_show_all_action)
        menu.addAction(self.tray_hide_all_action)
        menu.addSeparator()
        menu.addAction(self.tray_quit_action)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._tray_activated)
        self._apply_language()
        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray.show()

    def _tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.show_manager()

    def show_manager(self) -> None:
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _populate_list(self, preferred_id: str | None = None) -> None:
        self._loading_ui = True
        current_id = preferred_id or self.current_note_id()
        self.note_list.clear()
        selected_row = 0
        for row, note in enumerate(self.notes):
            item = QListWidgetItem(note.get("title") or tr("untitled"))
            item.setData(Qt.ItemDataRole.UserRole, note["id"])
            item.setFlags(
                item.flags()
                | Qt.ItemFlag.ItemIsUserCheckable
                | Qt.ItemFlag.ItemIsDragEnabled
                | Qt.ItemFlag.ItemIsDropEnabled
            )
            item.setCheckState(Qt.CheckState.Checked if note.get("visible") else Qt.CheckState.Unchecked)
            tooltip_title = note.get("title") or tr("untitled")
            tooltip_content = note.get("content") or ""
            item.setToolTip(f"{tooltip_title}\n\n{tooltip_content[:300]}")
            color = QColor(note.get("color", DEFAULT_NOTE["color"]))
            color.setAlpha(55)
            item.setBackground(color)
            self.note_list.addItem(item)
            if note["id"] == current_id:
                selected_row = row
        if self.note_list.count():
            self.note_list.setCurrentRow(selected_row)
        self._loading_ui = False
        self._update_action_states()

    def _restore_visible_notes(self) -> None:
        for note in self.notes:
            if note.get("visible"):
                self._show_note_window(note["id"])

    def current_note_id(self) -> str | None:
        item = self.note_list.currentItem()
        if item is None:
            return None
        return str(item.data(Qt.ItemDataRole.UserRole))

    def get_note(self, note_id: str | None) -> dict[str, Any] | None:
        if note_id is None:
            return None
        return next((note for note in self.notes if note["id"] == note_id), None)

    def create_note(self) -> None:
        cascade = len(self.notes) % 8
        note = dict(DEFAULT_NOTE)
        note.update(
            {
                "id": str(uuid.uuid4()),
                "title": tr("new_note_title", n=len(self.notes) + 1),
                "content": "",
                "x": 120 + cascade * 28,
                "y": 120 + cascade * 28,
            }
        )
        self.notes.append(note)
        self._populate_list(preferred_id=note["id"])
        self._show_note_window(note["id"])
        self._schedule_save()

    def _duplicate_current_note(self) -> None:
        source = self.get_note(self.current_note_id())
        if source is None:
            return
        note = dict(source)
        note["id"] = str(uuid.uuid4())
        note["title"] = f"{source.get('title') or tr('untitled')} ({tr('copy_suffix')})"
        note["x"] = int(source.get("x", 120)) + 30
        note["y"] = int(source.get("y", 120)) + 30
        note["visible"] = True
        self.notes.append(note)
        self._populate_list(preferred_id=note["id"])
        self._show_note_window(note["id"])
        self._schedule_save()

    def _delete_current_note(self) -> None:
        note = self.get_note(self.current_note_id())
        if note is None:
            return
        answer = QMessageBox.question(
            self,
            tr("delete_note_title"),
            tr("delete_note_prompt", title=note.get("title") or tr("untitled")),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        window = self.note_windows.pop(note["id"], None)
        if window is not None:
            window.setParent(None)
            window.deleteLater()
        self.notes = [item for item in self.notes if item["id"] != note["id"]]
        self._populate_list()
        self._schedule_save()

    def _on_selection_changed(self, _current: QListWidgetItem | None, _previous: QListWidgetItem | None) -> None:
        self._update_action_states()

    def _update_action_states(self) -> None:
        enabled = self.current_note_id() is not None
        for widget in (self.focus_button, self.duplicate_button, self.delete_button):
            widget.setEnabled(enabled)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        if self._loading_ui:
            return
        note_id = str(item.data(Qt.ItemDataRole.UserRole))
        self.set_note_visibility(note_id, item.checkState() == Qt.CheckState.Checked, update_item=False)

    def _on_rows_moved(self, *_args) -> None:
        if self._loading_ui:
            return
        order = [
            str(self.note_list.item(i).data(Qt.ItemDataRole.UserRole))
            for i in range(self.note_list.count())
        ]
        by_id = {note["id"]: note for note in self.notes}
        self.notes = [by_id[note_id] for note_id in order if note_id in by_id]
        self._schedule_save()

    def _on_editor_visibility_changed_from_window(self, note_id: str, visible: bool) -> None:
        self.set_note_visibility(note_id, visible)

    def _on_window_changed(self, note_id: str, changes: dict[str, Any]) -> None:
        note = self.get_note(note_id)
        if note is None:
            return

        # El tema se comporta como una selección de grupo para las notas que
        # están visibles en ese momento. Las notas ocultas conservan su tema
        # individual hasta que el usuario las muestre y vuelva a cambiarlo.
        if "theme" in changes:
            selected_theme = "crs" if changes.get("theme") == "crs" else "default"
            for visible_note in self.notes:
                if not visible_note.get("visible"):
                    continue
                visible_note["theme"] = selected_theme
                visible_window = self.note_windows.get(visible_note["id"])
                if visible_window is not None:
                    visible_window.set_theme(selected_theme, emit_change=False)
            changes = {key: value for key, value in changes.items() if key != "theme"}

        note.update(changes)
        item = self._find_list_item(note_id)
        if item is not None:
            self._loading_ui = True
            item.setText(note.get("title") or tr("untitled"))
            item.setToolTip(f"{note.get('title') or tr('untitled')}\n\n{(note.get('content') or '')[:300]}")
            background = QColor(note.get("color", DEFAULT_NOTE["color"]))
            background.setAlpha(55)
            item.setBackground(background)
            self._loading_ui = False
        self._schedule_save()

    def _show_note_window(self, note_id: str) -> None:
        note = self.get_note(note_id)
        if note is None:
            return
        window = self.note_windows.get(note_id)
        if window is None:
            window = StickyNoteWindow(note)
            window.changed.connect(self._on_window_changed)
            window.visibility_requested.connect(self._on_editor_visibility_changed_from_window)
            self.note_windows[note_id] = window
        else:
            window.apply_note(note)
        window.show()
        # No elevar automáticamente las notas normales: deben quedar por debajo
        # de otras aplicaciones. Solo las notas configuradas como "siempre encima"
        # reciben una elevación explícita.
        if window.always_on_top:
            window.raise_()

    def set_note_visibility(self, note_id: str, visible: bool, update_item: bool = True) -> None:
        note = self.get_note(note_id)
        if note is None:
            return
        note["visible"] = visible
        if visible:
            self._show_note_window(note_id)
        else:
            window = self.note_windows.get(note_id)
            if window is not None:
                window.hide()

        if update_item:
            item = self._find_list_item(note_id)
            if item is not None:
                self._loading_ui = True
                item.setCheckState(Qt.CheckState.Checked if visible else Qt.CheckState.Unchecked)
                self._loading_ui = False
        self._schedule_save()

    def set_all_visibility(self, visible: bool) -> None:
        for note in self.notes:
            self.set_note_visibility(note["id"], visible)
        self._populate_list(preferred_id=self.current_note_id())

    def _focus_current_note(self) -> None:
        note_id = self.current_note_id()
        if not note_id:
            return
        self.set_note_visibility(note_id, True)
        window = self.note_windows.get(note_id)
        if window is not None:
            window.showNormal()
            window.raise_()
            window.activateWindow()

    def _find_list_item(self, note_id: str) -> QListWidgetItem | None:
        for index in range(self.note_list.count()):
            item = self.note_list.item(index)
            if str(item.data(Qt.ItemDataRole.UserRole)) == note_id:
                return item
        return None

    def _schedule_save(self) -> None:
        self._save_timer.start()

    def _save_now(self) -> None:
        try:
            self.store.save(self.notes)
        except OSError as exc:
            QMessageBox.warning(self, tr("save_error"), str(exc))

    def quit_application(self) -> None:
        self._quitting = True
        self._save_now()
        for window in self.note_windows.values():
            window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            window.hide()
        self.tray.hide()
        self.app.quit()

    def closeEvent(self, event: QCloseEvent) -> None:
        if self._quitting:
            event.accept()
            return
        if QSystemTrayIcon.isSystemTrayAvailable():
            event.ignore()
            self.hide()
            if not self._tray_notice_shown:
                self.tray.showMessage(
                    tr("window_title"),
                    tr("tray_running"),
                    QSystemTrayIcon.MessageIcon.Information,
                    2500,
                )
                self._tray_notice_shown = True
        else:
            self.quit_application()
            event.accept()



def make_icon() -> QIcon:
    pixmap = QPixmap(128, 128)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#FFF2A8"))
    painter.setPen(QColor("#C6B45B"))
    painter.drawRoundedRect(12, 8, 104, 108, 18, 18)
    painter.setBrush(QColor("#E6D478"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawPolygon([QPoint(86, 116), QPoint(116, 86), QPoint(116, 116)])
    painter.setPen(QColor("#5C5530"))
    font = painter.font()
    font.setBold(True)
    font.setPointSize(44)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "N")
    painter.end()
    return QIcon(pixmap)



def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationDisplayName(APP_NAME)
    app.setOrganizationName("SantiApps")
    app.setDesktopFileName(APP_ID)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow(app)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
