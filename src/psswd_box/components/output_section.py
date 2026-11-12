from PySide6.QtCore import Qt
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)

from .icons import COPY, EYE_CLOSED, EYE_OPEN, get_svg_icon
from .strength import classify, entropy_bits, percent


class OutputSection(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Section")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        section_title = QLabel("Generated password")
        section_title.setObjectName("SectionTitle")
        layout.addWidget(section_title)

        # --- INPUT CONTAINER ---
        self.input_container = QFrame()
        self.input_container.setObjectName("PasswordInput")

        container_layout = QVBoxLayout(self.input_container)
        container_layout.setContentsMargins(12, 12, 8, 12)

        input_row = QHBoxLayout()
        input_row.setSpacing(4)

        self.password_edit = QLineEdit()
        self.password_edit.setObjectName("PasswordEdit")
        self.password_edit.setReadOnly(True)
        self.password_edit.setPlaceholderText("Generate a password to see it here.")
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.password_edit.setMinimumHeight(40)
        self.password_edit.setMinimumWidth(500)

        font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        font.setPointSize(16)
        self.password_edit.setFont(font)

        self.visibility_btn = QPushButton()
        self.visibility_btn.setObjectName("IconButton")
        self.visibility_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.visibility_btn.setFixedSize(32, 32)

        self.copy_btn = QPushButton()
        self.copy_btn.setObjectName("IconButton")
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.setFixedSize(32, 32)
        self.copy_btn.setIcon(get_svg_icon(COPY, "#8B949E", 16))

        input_row.addWidget(self.password_edit, 1)
        input_row.addWidget(self.visibility_btn)
        input_row.addWidget(self.copy_btn)

        container_layout.addLayout(input_row)
        layout.addWidget(self.input_container)

        # --- STRENGTH BAR ---
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

        layout.addStretch(1)

    def update_theme_icons(self, theme_color):
        self.visibility_btn.setIcon(get_svg_icon(EYE_CLOSED, theme_color, 16))
        self.copy_btn.setIcon(get_svg_icon(COPY, theme_color, 16))

    def toggle_visibility(self, is_visible, theme_color):
        if is_visible:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.visibility_btn.setIcon(get_svg_icon(EYE_OPEN, theme_color, 16))
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.visibility_btn.setIcon(get_svg_icon(EYE_CLOSED, theme_color, 16))

    def update_strength(self, pool_size, length):
        if pool_size == 0:
            self.strength_label.setText("Strength: add at least one character type")
            self.strength_bar.setValue(0)
            return

        bits = entropy_bits(pool_size, length)
        level = classify(bits)
        label = {"weak": "Weak", "fair": "Fair", "strong": "Strong"}[level]

        self.strength_label.setText(f"Strength: {label} ({bits:.0f} bits)")

        # Only the fill length changes now, no dynamic property needed
        self.strength_bar.setValue(percent(bits))
