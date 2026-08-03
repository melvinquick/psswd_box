import math
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .password_generator import PasswordGenerator
from .qss_file_handler import QssFileHandler
from .yaml_file_handler import YamlFileHandler

config_file = YamlFileHandler("resources/configs/config.yaml")
config = config_file.load_yaml_file()

themes_file = YamlFileHandler("resources/configs/themes.yaml")
themes = themes_file.load_yaml_file()

qss_file = QssFileHandler("resources/styles/nord.qss")
qss = qss_file.load_qss_file()


class PsswdBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.generator = PasswordGenerator()
        self.theme_name = "dark"
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(config["window_title"])
        self.setFixedSize(
            config["window_size"]["width"],
            config["window_size"]["height"],
        )
        self.setObjectName("MainWindow")

        central = QWidget()
        central.setObjectName("CentralWidget")
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        root_layout.addWidget(self.build_top_bar())
        root_layout.addWidget(self.build_character_options_section())
        root_layout.addWidget(self.build_generation_settings_section())
        root_layout.addWidget(self.build_output_section())

        self.generate_button = QPushButton("Generate password")
        self.generate_button.setObjectName("PrimaryButton")
        self.generate_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_button.setMinimumHeight(46)
        self.generate_button.clicked.connect(self.generate_password)
        root_layout.addWidget(self.generate_button)

        self.apply_theme(self.theme_name)
        self.update_strength()

    def build_top_bar(self):
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_bar.setFrameShape(QFrame.Shape.NoFrame)
        top_bar.setFixedHeight(48)

        layout = QHBoxLayout(top_bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        app_name = QLabel("Psswd Box")
        app_name.setObjectName("AppName")

        self.theme_toggle = QPushButton("Switch theme")
        self.theme_toggle.setObjectName("SecondaryButton")
        self.theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_toggle.clicked.connect(self.toggle_theme)

        layout.addWidget(app_name)
        layout.addStretch()
        layout.addWidget(self.theme_toggle)

        return top_bar

    def make_section(self, title):
        section = QFrame()
        section.setObjectName("Section")
        section.setFrameShape(QFrame.Shape.NoFrame)

        layout = QVBoxLayout(section)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        section_title = QLabel(title)
        section_title.setObjectName("SectionTitle")
        layout.addWidget(section_title)

        return section, layout

    def build_character_options_section(self):
        section, layout = self.make_section("Character options")

        self.lowercase_letters = self.make_checkbox("Lowercase letters", True)
        self.uppercase_letters = self.make_checkbox("Uppercase letters", True)
        self.numbers = self.make_checkbox("Numbers", True)
        self.symbols = self.make_checkbox("Symbols", True)

        option_grid = QGridLayout()
        option_grid.setSpacing(12)
        option_grid.setColumnStretch(0, 1)
        option_grid.setColumnStretch(1, 1)

        option_grid.addWidget(self.lowercase_letters, 0, 0)
        option_grid.addWidget(self.uppercase_letters, 0, 1)
        option_grid.addWidget(self.numbers, 1, 0)
        option_grid.addWidget(self.symbols, 1, 1)

        layout.addLayout(option_grid)

        return section

    def build_generation_settings_section(self):
        section, layout = self.make_section("Generation settings")

        min_len = int(config.get("num_characters", {}).get("min", 8))
        max_len = int(config.get("num_characters", {}).get("max", 128))
        default_len = int(config.get("num_characters", {}).get("default", 20))

        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(min_len, max_len)
        self.length_slider.setValue(default_len)
        self.length_slider.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.length_slider.valueChanged.connect(self.on_slider_changed)

        self.length_spin = QSpinBox()
        self.length_spin.setRange(min_len, max_len)
        self.length_spin.setValue(default_len)
        self.length_spin.setSuffix(" characters")
        self.length_spin.valueChanged.connect(self.on_spin_changed)

        length_row = QHBoxLayout()
        length_row.setSpacing(12)
        length_row.addWidget(self.length_slider, 1)
        length_row.addWidget(self.length_spin)
        layout.addLayout(length_row)

        self.auto_copy = self.make_checkbox("Copy automatically after generation", True)
        layout.addWidget(self.auto_copy)

        return section

    def build_output_section(self):
        section, layout = self.make_section("Generated password")

        self.password_edit = QLineEdit()
        self.password_edit.setObjectName("PasswordEdit")
        self.password_edit.setReadOnly(True)
        self.password_edit.setPlaceholderText("Generate a password to see it here.")
        self.password_edit.setMinimumHeight(58)

        password_font = QFont("Monospace", 16)
        password_font.setStyleHint(QFont.StyleHint.Monospace)
        self.password_edit.setFont(password_font)

        self.visibility_button = QPushButton("Hide")
        self.visibility_button.setObjectName("SecondaryButton")
        self.visibility_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.visibility_button.clicked.connect(self.toggle_password_visibility)

        self.copy_button = QPushButton("Copy")
        self.copy_button.setObjectName("SecondaryButton")
        self.copy_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_button.clicked.connect(self.copy_password)

        password_row = QHBoxLayout()
        password_row.setSpacing(10)
        password_row.addWidget(self.password_edit, 1)
        password_row.addWidget(self.visibility_button)
        password_row.addWidget(self.copy_button)
        layout.addLayout(password_row)

        strength_row = QHBoxLayout()
        strength_row.setSpacing(10)

        self.strength_label = QLabel("Strength: --")
        self.strength_label.setObjectName("MutedLabel")

        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setMinimumHeight(14)

        strength_row.addWidget(self.strength_label)
        strength_row.addWidget(self.strength_bar, 1)
        layout.addLayout(strength_row)

        self.status_label = QLabel("")
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        return section

    def make_checkbox(self, text, checked):
        checkbox = QCheckBox(text)
        checkbox.blockSignals(True)
        checkbox.setChecked(checked)
        checkbox.blockSignals(False)
        checkbox.stateChanged.connect(self.update_strength)
        return checkbox

    def toggle_theme(self):
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.apply_theme(self.theme_name)

    def apply_theme(self, theme_name):
        self.theme_name = theme_name if theme_name in themes else "dark"
        self.theme_toggle.setText(
            "Switch to light" if self.theme_name == "dark" else "Switch to dark"
        )

        tokens = {**themes[self.theme_name], **themes["general"]}
        stylesheet = qss
        for key, value in tokens.items():
            stylesheet = stylesheet.replace("{{" + key + "}}", str(value))

        self.setStyleSheet(stylesheet)
        self.update_strength()

    def on_slider_changed(self, value):
        if self.length_spin.value() != value:
            self.length_spin.setValue(value)
        self.update_strength()

    def on_spin_changed(self, value):
        if self.length_slider.value() != value:
            self.length_slider.setValue(value)
        self.update_strength()

    def get_character_types(self):
        return [
            "y" if self.lowercase_letters.isChecked() else "n",
            "y" if self.uppercase_letters.isChecked() else "n",
            "y" if self.numbers.isChecked() else "n",
            "y" if self.symbols.isChecked() else "n",
        ]

    def generate_password(self):
        character_types = self.get_character_types()

        if character_types == ["n", "n", "n", "n"]:
            self.password_edit.clear()
            self.set_status("Choose at least one character type.", "danger")
            self.update_strength()
            return

        password = self.generator.generate_password(
            character_types,
            self.length_spin.value(),
        )

        if not password:
            self.set_status("Password generation failed.", "danger")
            return

        self.password_edit.setText(password)
        self.update_strength()

        if self.auto_copy.isChecked():
            self.copy_to_clipboard()
            self.set_status("Password generated and copied.", "success")
            QTimer.singleShot(2500, self.clear_status)
        else:
            self.set_status("Password generated.", "success")
            QTimer.singleShot(2500, self.clear_status)

    def copy_password(self):
        if not self.password_edit.text():
            self.set_status("Nothing to copy yet.", "warning")
            return

        self.copy_to_clipboard()
        self.set_status("Copied to clipboard.", "success")
        QTimer.singleShot(2500, self.clear_status)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.password_edit.text())

    def toggle_password_visibility(self):
        if self.password_edit.echoMode() == QLineEdit.EchoMode.Normal:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.visibility_button.setText("Show")
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.visibility_button.setText("Hide")

    def selected_pool_size(self):
        pool_size = 0
        if self.lowercase_letters.isChecked():
            pool_size += 26
        if self.uppercase_letters.isChecked():
            pool_size += 26
        if self.numbers.isChecked():
            pool_size += 10
        if self.symbols.isChecked():
            pool_size += 14
        return pool_size

    def update_strength(self):
        pool_size = self.selected_pool_size()
        length = self.length_spin.value()

        if pool_size == 0:
            self.strength_label.setText("Strength: add at least one character type")
            self.strength_bar.setValue(0)
            self.strength_bar.setStyleSheet("")
            return

        entropy = length * math.log2(pool_size)
        percentage = min(100, int((entropy / 128) * 100))

        if entropy < 45:
            label = "Weak"
            color = themes[self.theme_name]["danger-color"]
        elif entropy < 80:
            label = "Fair"
            color = themes[self.theme_name]["warning-color"]
        else:
            label = "Strong"
            color = themes[self.theme_name]["success-color"]

        self.strength_label.setText(f"Strength: {label} ({entropy:.0f} bits)")
        self.strength_bar.setValue(percentage)
        self.strength_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {color}; border-radius: {themes['general']['border-radius']}; }}"
        )

    def set_status(self, message, kind="info"):
        colors = {
            "info": themes[self.theme_name]["color"],
            "success": themes[self.theme_name]["success-color"],
            "warning": themes[self.theme_name]["warning-color"],
            "danger": themes[self.theme_name]["danger-color"],
        }
        self.status_label.setStyleSheet(f"color: {colors[kind]};")
        self.status_label.setText(message)

    def clear_status(self):
        if self.status_label.text() in {
            "Password generated.",
            "Password generated and copied.",
            "Copied to clipboard.",
        }:
            self.status_label.setText("")
            self.status_label.setStyleSheet("")


def main():
    app = QApplication(sys.argv)
    window = PsswdBox()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
