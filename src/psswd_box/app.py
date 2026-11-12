import sys

from PySide6.QtCore import QSettings, Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from .components.about_dialog import AboutDialog
from .components.character_options import CharacterOptions
from .components.generation_settings import GenerationSettings
from .components.output_section import OutputSection
from .components.password_generator import PasswordGenerator
from .components.preferences_dialog import PreferencesDialog
from .components.qss_file_handler import QssFileHandler
from .components.theme_manager import ThemeManager
from .components.yaml_file_handler import YamlFileHandler


class PsswdBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generator = PasswordGenerator()
        self._password_is_visible = False

        self.themes = YamlFileHandler(
            "../resources/styles/themes.yaml"
        ).load_yaml_file()
        qss = QssFileHandler("../resources/styles/styles.qss").load_qss_file()
        self.theme_manager = ThemeManager(self.themes, qss)

        self.settings = QSettings("psswd_box", "settings")
        self.theme_name = self.settings.value("theme", ThemeManager.DEFAULT_THEME)

        self._status_timer = QTimer(self)
        self._status_timer.setSingleShot(True)
        self._status_timer.timeout.connect(self.clear_status)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Psswd Box")
        self.setObjectName("MainWindow")

        # --- CUSTOM MENU BAR ---
        top_bar_container = QWidget()
        top_bar_container.setObjectName("TopBarContainer")
        top_bar_layout = QHBoxLayout(top_bar_container)
        top_bar_layout.setContentsMargins(4, 4, 4, 4)
        top_bar_layout.setSpacing(0)

        self.menu_bar = QMenuBar()
        self.menu_bar.setObjectName("MenuBar")
        self.menu_bar.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )

        file_menu = self.menu_bar.addMenu("File")
        file_menu.addAction("Exit", self.close)

        edit_menu = self.menu_bar.addMenu("Edit")
        edit_menu.addAction("Copy Password", self.copy_password)

        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction("About", self.open_about)

        self.prefs_btn = QPushButton("Preferences")
        self.prefs_btn.setObjectName("MenuButton")
        self.prefs_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.prefs_btn.clicked.connect(self.open_preferences)

        top_bar_layout.addWidget(self.menu_bar)
        top_bar_layout.addWidget(self.prefs_btn)
        top_bar_layout.addStretch()

        # --- MAIN LAYOUT ---
        central = QWidget()
        central.setObjectName("CentralWidget")
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(top_bar_container)

        content_widget = QWidget()
        content_widget.setObjectName("CentralWidget")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 16, 24, 24)
        content_layout.setSpacing(16)

        self.char_options = CharacterOptions(self.settings)
        self.gen_settings = GenerationSettings(self.settings)
        self.output_section = OutputSection()

        self.output_section.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )

        content_layout.addWidget(self.char_options)
        content_layout.addWidget(self.gen_settings)
        content_layout.addWidget(self.output_section)

        self.generate_button = QPushButton("Generate password")
        self.generate_button.setObjectName("PrimaryButton")
        self.generate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_button.setMinimumHeight(46)
        content_layout.addWidget(self.generate_button)

        root_layout.addWidget(content_widget)

        # --- SIGNALS ---
        self.char_options.changed.connect(self.update_strength)
        self.gen_settings.changed.connect(self.update_strength)
        self.output_section.visibility_btn.clicked.connect(
            self.toggle_password_visibility
        )
        self.output_section.copy_btn.clicked.connect(self.copy_password)
        self.generate_button.clicked.connect(self.generate_password)

        self.theme_manager.register(self.output_section.status_label)
        self.theme_manager.register(self.menu_bar)

        self.apply_theme(self.theme_name)

        muted_color = self.themes[self.theme_name]["muted-color"]
        self.output_section.toggle_visibility(False, muted_color)

        self.setMinimumWidth(600)
        self.adjustSize()

        if self.height() < 720:
            self.resize(self.width(), 720)

    # --- ACTIONS ---
    def open_preferences(self):
        dialog = PreferencesDialog(self.settings, self.theme_manager, self)
        dialog.settings_changed.connect(self.sync_live_settings)
        dialog.exec()

    def open_about(self):
        accent_color = self.themes[self.theme_name]["accent-color"]
        self.about_dialog = AboutDialog(accent_color, self)
        self.about_dialog.exec()

    def sync_live_settings(self):
        new_theme = self.settings.value("theme", ThemeManager.DEFAULT_THEME)
        if new_theme != self.theme_name:
            self.apply_theme(new_theme)

    def apply_theme(self, theme_name):
        self.theme_name = self.theme_manager.apply(self, theme_name)
        muted_color = self.themes[self.theme_name]["muted-color"]
        self.output_section.update_theme_icons(muted_color)
        if self._password_is_visible:
            self.output_section.toggle_visibility(True, muted_color)
        self.update_strength()

    def update_strength(self):
        character_types = self.char_options.get_types()
        pool_size = self.generator.pool_size(character_types)
        length = self.gen_settings.get_length()
        self.output_section.update_strength(pool_size, length)

    def generate_password(self):
        character_types = self.char_options.get_types()

        if not any(character_types):
            self.output_section.password_edit.clear()
            self.set_status("Choose at least one character type.", "danger")
            self.update_strength()
            return

        password = self.generator.generate_password(
            character_types, self.gen_settings.get_length()
        )

        if not password:
            self.set_status("Password generation failed.", "danger")
            return

        self.output_section.password_edit.setText(password)
        self.update_strength()

        if self.gen_settings.is_auto_copy_enabled():
            self.copy_to_clipboard()
            self.set_status("Password generated and copied.", "success")
        else:
            self.set_status("Password generated.", "success")

    def copy_password(self):
        if not self.output_section.password_edit.text():
            self.set_status("Nothing to copy yet.", "warning")
            return
        self.copy_to_clipboard()
        self.set_status("Copied to clipboard.", "success")

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.output_section.password_edit.text())

    def toggle_password_visibility(self):
        self._password_is_visible = not self._password_is_visible
        muted_color = self.themes[self.theme_name]["muted-color"]
        self.output_section.toggle_visibility(self._password_is_visible, muted_color)

    def set_status(self, message, kind="info"):
        self.output_section.status_label.setText(message)
        if self.output_section.status_label.property("kind") != kind:
            self.output_section.status_label.setProperty("kind", kind)
            self.theme_manager._repolish(self.output_section.status_label)
        self._status_timer.start(2500)

    def clear_status(self):
        self.output_section.status_label.setText("")
        self.output_section.status_label.setProperty("kind", "info")
        self.theme_manager._repolish(self.output_section.status_label)


def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("psswd_box")
    app.setApplicationName("psswd_box")
    window = PsswdBox()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
