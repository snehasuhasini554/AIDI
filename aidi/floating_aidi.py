import sys
import os
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QUrl
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMenu,
    QAction,
    QSystemTrayIcon,
    QFileDialog,
    QShortcut,
    QGraphicsDropShadowEffect
)
from PyQt5.QtMultimedia import QSoundEffect

DING_PATH = os.path.join(os.path.dirname(__file__), "assets", "ding.wav")
DEFAULT_SKIN = os.path.join(os.path.dirname(__file__), "assets", "koala.png")
SKINS_FOLDER = os.path.join(os.path.dirname(__file__), "skins")

# Helper to get skin images
def get_skin_images():
    skins = []
    try:
        for fname in os.listdir(SKINS_FOLDER):
            if fname.lower().endswith(('.png', '.gif', '.jpg', '.jpeg')):
                skins.append(os.path.join(SKINS_FOLDER, fname))
    except Exception:
        pass
    if os.path.exists(DEFAULT_SKIN):
        skins.insert(0, DEFAULT_SKIN)
    return skins

class FloatingAIDI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(260, 320)
        self.setStyleSheet("background:rgba(240,248,255,220); border-radius:18px;")

        # Koala image
        self.skin_images = get_skin_images()
        self.skin_index = 0
        self.koala_label = QLabel(self)
        self.koala_label.setPixmap(QPixmap(self.skin_images[self.skin_index]).scaled(190, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.koala_label.setGeometry(35, 24, 190, 190)

        # Pomodoro timer
        self.timer_label = QLabel("25:00", self)
        self.timer_label.setGeometry(62, 220, 136, 46)
        self.timer_label.setStyleSheet("""
            background: rgba(255,255,255,230);
            border-radius: 14px;
            color: #1a2042;
            font: bold 24px Arial;
            border: 2px solid #88B9DA;
        """
        )
        self.timer_label.setAlignment(Qt.AlignCenter)

        # Controls
        self.start_btn = QPushButton("▶", self)
        self.start_btn.setGeometry(65, 275, 44, 38)
        self.start_btn.setStyleSheet("background:#BFEAFF; font-size:22px; border-radius:12px;")
        self.pause_btn = QPushButton("⏸", self)
        self.pause_btn.setGeometry(111, 275, 44, 38)
        self.pause_btn.setStyleSheet("background:#EFD6FF; font-size:20px; border-radius:12px;")
        self.reset_btn = QPushButton("⟲", self)
        self.reset_btn.setGeometry(157, 275, 38, 38)
        self.reset_btn.setStyleSheet("background:#FFF1BF; font-size:18px; border-radius:12px;")

        # Status bubble (break/focus)
        self.show_status = QLabel(self)
        self.show_status.setGeometry(18, 14, 88, 28)
        self.show_status.setStyleSheet("""
            background: #ffffffDD;
            border-radius: 12px;
            color: #3B53A6;
            font-weight: bold;
            font-size: 15px;
            padding: 2px 6px;
        """
        )
        self.show_status.setAlignment(Qt.AlignCenter)
        self.show_status.hide()

        # Achievements/statistics placeholder
        self.achiev_label = QLabel("", self)
        self.achiev_label.setGeometry(12, 268, 48, 22)
        self.achiev_label.setStyleSheet("color: #FA8E00; font-size:14px;")
        self.achiev_label.hide()

        # Mood Booster (popup menu)
        self.mood_booster_links = [
            ("Affirmation", "You're crushing it 🚀"),
            ("Music", "https://lofi.cafe/"),
            ("Video", "https://www.youtube.com/watch?v=5qap5aO4i9A")
        ]

        # Timer logic
        self.pomodoro_duration = 25 * 60  # 25 min
        self.break_duration = 5 * 60  # 5 min
        self.remaining_seconds = self.pomodoro_duration
        self.is_running = False
        self.is_on_break = False
        self.completed_sessions = 0
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        # System tray
        self.tray = QSystemTrayIcon(self)
        tray_icon_path = self.skin_images[self.skin_index] if self.skin_images else DEFAULT_SKIN
        self.tray.setIcon(QIcon(tray_icon_path))
        self.tray.show()

        # Fade-in and shadow
        self.do_fade_in()
        self.init_shadow()

        # Keyboard shortcuts
        self.add_shortcuts()
        self.font_size = 24

        # Connect btns
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

        # Mouse drag for window movement
        self.old_pos = None

        # Context menu for features
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

        # Show stats/badges on timer completion
        self.session_badges = ("⭐","🔥","🎉","🏆","💙")
        self.achiev_label.setText("")

    def do_fade_in(self):
        self.setWindowOpacity(0.0)
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(700)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start(QPropertyAnimation.DeleteWhenStopped)
        self.anim = anim

    def init_shadow(self):
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(25)
        effect.setXOffset(0)
        effect.setYOffset(8)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)

    def add_shortcuts(self):
        self.shortcut_start = QShortcut(Qt.CTRL + Qt.Key_S, self)
        self.shortcut_start.activated.connect(self.start_timer)
        self.shortcut_pause = QShortcut(Qt.CTRL + Qt.Key_P, self)
        self.shortcut_pause.activated.connect(self.pause_timer)
        self.shortcut_reset = QShortcut(Qt.CTRL + Qt.Key_R, self)
        self.shortcut_reset.activated.connect(self.reset_timer)
        self.shortcut_skins = QShortcut(Qt.CTRL + Qt.Key_G, self)
        self.shortcut_skins.activated.connect(self.open_skins_dialog)
        self.shortcut_booster = QShortcut(Qt.CTRL + Qt.Key_B, self)
        self.shortcut_booster.activated.connect(self.show_mood_booster)

    def polished_notify(self, text, icon=None):
        # Show in system tray, play sound
        icon_path = icon or self.skin_images[self.skin_index]
        self.tray.setIcon(QIcon(icon_path))
        self.tray.showMessage("AIDI", text, QIcon(icon_path), 2500)
        self.play_ding()

    def play_ding(self):
        if os.path.exists(DING_PATH):
            ding = QSoundEffect(self)
            ding.setSource(QUrl.fromLocalFile(DING_PATH))
            ding.setVolume(0.6)
            ding.play()

    def show_mode_status(self, status):
        self.show_status.setText(status)
        self.show_status.show()
        QTimer.singleShot(2000, self.show_status.hide)

    def apply_font_size(self, size):
        self.font_size = size
        self.timer_label.setStyleSheet(f"""
            background: rgba(255,255,255,230);
            border-radius: 14px;
            color: #1a2042;
            font: bold {size}px Arial;
            border: 2px solid #88B9DA;
        """
        )

    def apply_high_contrast(self, enable):
        if enable:
            self.setStyleSheet("background:#1a1a1a; border-radius:18px;")
            self.timer_label.setStyleSheet(f"""
                background: #fff;
                color: #000;
                border-radius: 14px;
                font: bold {self.font_size}px Arial;
                border: 3px solid #222;
            """
            )
        else:
            self.setStyleSheet("background:rgba(240,248,255,220); border-radius:18px;")
            self.apply_font_size(self.font_size)

    # Pomodoro logic
    def start_timer(self):
        if not self.is_running:
            self.timer.start()
            self.is_running = True
            self.show_mode_status("Focus Mode")
            self.polished_notify("Started a Pomodoro session! 🚀")

    def pause_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            self.show_mode_status("Paused")
            self.polished_notify("Paused ⏸")

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.remaining_seconds = self.pomodoro_duration if not self.is_on_break else self.break_duration
        self.update_timer_label()
        self.show_mode_status("Reset!")
        self.polished_notify("Timer reset 🔄")

    def update_timer(self):
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_timer_label()
        else:
            self.timer.stop()
            self.is_running = False
            self.play_ding()
            self.completed_sessions += 1 if not self.is_on_break else 0
            if not self.is_on_break:
                self.achiev_label.setText(self.session_badges[self.completed_sessions % len(self.session_badges)])
                self.achiev_label.show()
                self.is_on_break = True
                self.remaining_seconds = self.break_duration
                self.polished_notify("Break time! 🌴")
                self.show_mode_status("Break!")
                QTimer.singleShot(2500, self.show_mood_booster)
            else:
                self.achiev_label.hide()
                self.is_on_break = False
                self.remaining_seconds = self.pomodoro_duration
                self.polished_notify("Back to focus! 💙")
                self.show_mode_status("Focus!")
            self.timer.start()
            self.is_running = True

    def update_timer_label(self):
        m, s = divmod(self.remaining_seconds, 60)
        self.timer_label.setText(f"{m:02}:{s:02}")

    # Mouse drag events
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # Context menu (skins/mood booster/settings)
    def open_context_menu(self, position):
        menu = QMenu()
        skin_action = QAction("Koala Skins", self)
        skin_action.triggered.connect(self.open_skins_dialog)
        booster_action = QAction("Mood Boosters", self)
        booster_action.triggered.connect(self.show_mood_booster)
        font_action = QAction("Font Size +", self)
        font_action.triggered.connect(lambda: self.apply_font_size(self.font_size + 2))
        contrast_action = QAction("High Contrast Toggle", self)
        contrast_action.triggered.connect(lambda: self.apply_high_contrast(self.styleSheet() != "background:#1a1a1a; border-radius:18px;"))
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(skin_action)
        menu.addAction(booster_action)
        menu.addAction(font_action)
        menu.addAction(contrast_action)
        menu.addSeparator()
        menu.addAction(exit_action)
        menu.exec_(self.mapToGlobal(position))

    # Skins selector dialog
    def open_skins_dialog(self):
        skins = get_skin_images()
        menu = QMenu()
        for idx, skin_path in enumerate(skins):
            act = QAction(os.path.basename(skin_path), self)
            def make_apply_skin(i):
                return lambda: self.apply_skin(i)
            act.triggered.connect(make_apply_skin(idx))
            menu.addAction(act)
        menu.exec_(self.mapToGlobal(self.koala_label.pos() + self.koala_label.rect().bottomLeft()))

    def apply_skin(self, idx):
        self.skin_index = idx
        self.koala_label.setPixmap(QPixmap(self.skin_images[self.skin_index]).scaled(190, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.tray.setIcon(QIcon(self.skin_images[self.skin_index]))
        self.polished_notify(f"Koala skin changed!", self.skin_images[self.skin_index])

    # Mood Booster popup
    def show_mood_booster(self):
        menu = QMenu()
        for text, link in self.mood_booster_links:
            act = QAction(f"{text}: {link}", self)
            if link.startswith("http"):
                act.triggered.connect(lambda l=link: os.startfile(l) if sys.platform == "win32" else os.system(f"xdg-open '{l}'"))
            else:
                act.triggered.connect(lambda l=link: self.polished_notify(l))
            menu.addAction(act)
        menu.addSeparator()
        add_act = QAction("Add Booster...", self)
        add_act.triggered.connect(self.add_mood_booster)
        menu.addAction(add_act)
        menu.exec_(self.mapToGlobal(self.timer_label.pos() + self.timer_label.rect().bottomRight()))

    def add_mood_booster(self):
        # Quick file dialog add for demo.
        fname, _ = QFileDialog.getOpenFileName(self, "Add Music/Video/Link Booster", "", "All Files (*)")
        if fname:
            self.mood_booster_links.append(("Added", fname))
            self.polished_notify(f"Added booster: {fname}")

    # Window close
    def closeEvent(self, event):
        self.tray.hide()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    window = FloatingAIDI()
    window.show()
    sys.exit(app.exec_())