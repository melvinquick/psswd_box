"""
Password generator that never leaves your machine.
"""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QCheckBox,
    QLabel,
    QHBoxLayout,
    QSpinBox,
    QGridLayout,
)

from .password_generator import PasswordGenerator
from .yaml_file_handler import YamlFileHandler

config_file = YamlFileHandler("resources/configs/config.yaml")
config = config_file.load_yaml_file()

themes_file = YamlFileHandler("resources/configs/themes.yaml")
themes = themes_file.load_yaml_file()


class PsswdBox(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.show()

        # * Set window default settings
        self.setWindowTitle(config["window_title"])
        self.setFixedSize(
            config["window_size"]["width"], config["window_size"]["height"]
        )

        # * Create end user widgets and apply settings to them
        self.generate_password = QPushButton("Generate and Copy Password")

        self.password = QLabel(
            " ", alignment=Qt.AlignmentFlag.AlignCenter, wordWrap=False
        )
        self.password.setFixedWidth(540)

        self.lowercase_letters = QCheckBox("Lowercase")
        self.lowercase_letters.setCheckState(Qt.CheckState.Checked)

        self.uppercase_letters = QCheckBox("Uppercase")
        self.uppercase_letters.setCheckState(Qt.CheckState.Checked)

        self.numbers = QCheckBox("Numbers")
        self.numbers.setCheckState(Qt.CheckState.Checked)

        self.symbols = QCheckBox("Symbols")
        self.symbols.setCheckState(Qt.CheckState.Checked)

        self.num_characters = QSpinBox(prefix="Number of Characters: ")
        self.num_characters.setRange(
            config["num_characters"]["min"], config["num_characters"]["max"]
        )
        self.num_characters.setValue(config["num_characters"]["default"])

        self.theme_toggle = QPushButton("Dark")

        # * Define button connections and/or actions
        self.generate_password.pressed.connect(self.get_password)
        self.generate_password.pressed.connect(self.copy_text)
        self.theme_toggle.pressed.connect(self.toggle_theme)

        # * Create layouts
        page = QGridLayout()
        inputs = QGridLayout()
        outputs = QHBoxLayout()

        # * Add widgets to layouts
        inputs.addWidget(self.generate_password, 0, 0, 1, 2)
        inputs.addWidget(self.lowercase_letters, 1, 0)
        inputs.addWidget(self.uppercase_letters, 1, 1)
        inputs.addWidget(self.numbers, 2, 0)
        inputs.addWidget(self.symbols, 2, 1)
        inputs.addWidget(self.num_characters, 3, 0, 1, 2)
        inputs.addWidget(self.theme_toggle, 4, 0, 1, 2)

        outputs.addWidget(self.password)

        # * Setup overall page layout and set default window theme
        page.addLayout(inputs, 0, 0)
        page.addLayout(outputs, 0, 2)

        gui = QWidget()
        gui.setLayout(page)

        self.setCentralWidget(gui)

        self.apply_theme(self.theme_toggle.text().lower())
        self.set_font()

    def get_password(self):
        character_types = self.get_character_types()
        if character_types == ["n", "n", "n", "n"]:
            self.password.setText("You MUST select one of the character types below!")
        else:
            psswd = PasswordGenerator()
            self.password.setText(
                psswd.generate_password(character_types, self.num_characters.value())
            )
        self.set_font_password()

    def get_character_types(self):
        lowercase_letters_value = "y" if self.lowercase_letters.isChecked() else "n"
        uppercase_letters_value = "y" if self.uppercase_letters.isChecked() else "n"
        numbers_value = "y" if self.numbers.isChecked() else "n"
        symbols_value = "y" if self.symbols.isChecked() else "n"
        character_types = [
            lowercase_letters_value,
            uppercase_letters_value,
            numbers_value,
            symbols_value,
        ]

        return character_types

    def copy_text(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.password.text())

    def toggle_theme(self):
        if self.theme_toggle.text() == "Dark":
            self.theme_toggle.setText("Light")
            theme = self.theme_toggle.text()
        else:
            self.theme_toggle.setText("Dark")
            theme = self.theme_toggle.text()

        self.apply_theme(theme.lower())

    def apply_theme(self, theme):
        self.main_stylesheet = f"""
            background-color: {themes[theme]["background-color"]};
            color: {themes[theme]["color"]};
            border: {themes[theme]["border"]};
            border-radius: {themes["general"]["border-radius"]};
            padding: {themes["general"]["padding"]};
            """
        self.widget_stylesheet = f"""
            background-color: {themes[theme]["widget-background-color"]};
            """
        self.setStyleSheet(self.main_stylesheet)
        self.password.setStyleSheet(self.widget_stylesheet)
        self.generate_password.setStyleSheet(self.widget_stylesheet)
        self.lowercase_letters.setStyleSheet(self.widget_stylesheet)
        self.uppercase_letters.setStyleSheet(self.widget_stylesheet)
        self.numbers.setStyleSheet(self.widget_stylesheet)
        self.symbols.setStyleSheet(self.widget_stylesheet)
        self.theme_toggle.setStyleSheet(self.widget_stylesheet)
        self.num_characters.setStyleSheet(self.widget_stylesheet)

        (
            self.theme_toggle.setText("Dark")
            if theme == "dark"
            else self.theme_toggle.setText("Light")
        )

    def set_font(self):
        font = QFont("Commit Mono Nerd Font", 9)

        self.setFont(font)
        self.generate_password.setFont(font)
        self.lowercase_letters.setFont(font)
        self.uppercase_letters.setFont(font)
        self.numbers.setFont(font)
        self.symbols.setFont(font)
        self.theme_toggle.setFont(font)
        self.num_characters.setFont(font)

    def set_font_password(self):
        min_font_size = 11
        current_font_size = 65
        font = QFont("Commit Mono Nerd Font")

        while current_font_size >= min_font_size:
            font.setPointSize(current_font_size)

            if (
                QFontMetrics(font).horizontalAdvance(self.password.text())
                < self.password.width() - 10
            ):
                self.password.setFont(font)
                return

            current_font_size -= 1


def main():
    app = QApplication(sys.argv)
    main_window = PsswdBox()  # noqa: F841
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
