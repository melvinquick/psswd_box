from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)


class PreferencesDialog(QDialog):
    settings_changed = Signal()

    def __init__(self, settings: QSettings, theme_manager, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.theme_manager = theme_manager
        self.setWindowTitle("Preferences")
        self.setObjectName("MainWindow")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowCloseButtonHint)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        # --- 1. APPEARANCE ---
        appearance_section = QFrame()
        appearance_section.setObjectName("Section")
        appearance_layout = QVBoxLayout(appearance_section)
        appearance_layout.setContentsMargins(18, 18, 18, 18)
        appearance_layout.setSpacing(12)

        title = QLabel("Appearance")
        title.setObjectName("SectionTitle")
        appearance_layout.addWidget(title)

        theme_row = QHBoxLayout()
        theme_row.setSpacing(12)

        theme_label = QLabel("Theme:")
        theme_label.setFixedWidth(60)

        self.theme_combo = QComboBox()

        # Dynamically load themes
        current_theme_key = self.settings.value(
            "theme", self.theme_manager.DEFAULT_THEME
        )
        current_theme_key = self.theme_manager.resolve(current_theme_key)

        for key in self.theme_manager.get_available_themes():
            display_name = self.theme_manager.get_display_name(key)
            self.theme_combo.addItem(display_name, key)  # Store the key as item data
            if key == current_theme_key:
                self.theme_combo.setCurrentIndex(self.theme_combo.count() - 1)

        self.theme_combo.currentTextChanged.connect(self._save)

        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.theme_combo, 1)
        appearance_layout.addLayout(theme_row)
        root_layout.addWidget(appearance_section)

        # --- 2. DEFAULTS ---
        gen_section = QFrame()
        gen_section.setObjectName("Section")
        gen_layout = QVBoxLayout(gen_section)
        gen_layout.setContentsMargins(18, 18, 18, 18)
        gen_layout.setSpacing(12)

        title2 = QLabel("Defaults")
        title2.setObjectName("SectionTitle")
        gen_layout.addWidget(title2)

        len_row = QHBoxLayout()
        len_label = QLabel("Length:")
        len_label.setFixedWidth(60)
        self.len_spin = QSpinBox()
        self.len_spin.setRange(10, 100)
        self.len_spin.setValue(int(self.settings.value("length/default", 24)))
        self.len_spin.setSuffix(" chars")
        self.len_spin.valueChanged.connect(self._save)
        len_row.addWidget(len_label)
        len_row.addWidget(self.len_spin, 1)
        gen_layout.addLayout(len_row)

        self.auto_copy_cb = QCheckBox("Copy automatically after generation")
        self.auto_copy_cb.setChecked(self.settings.value("auto_copy", True, type=bool))
        self.auto_copy_cb.stateChanged.connect(self._save)
        gen_layout.addWidget(self.auto_copy_cb)
        root_layout.addWidget(gen_section)

        # --- 3. DEFAULT CHARACTER OPTIONS ---
        char_section = QFrame()
        char_section.setObjectName("Section")
        char_layout = QVBoxLayout(char_section)
        char_layout.setContentsMargins(18, 18, 18, 18)
        char_layout.setSpacing(12)

        title3 = QLabel("Default Character Options")
        title3.setObjectName("SectionTitle")
        char_layout.addWidget(title3)

        char_grid = QGridLayout()
        char_grid.setSpacing(12)

        self.cb_lower = QCheckBox("Lowercase letters")
        self.cb_lower.setMinimumWidth(180)
        self.cb_lower.setChecked(
            self.settings.value("chars/lowercase", True, type=bool)
        )
        self.cb_lower.stateChanged.connect(self._save)

        self.cb_upper = QCheckBox("Uppercase letters")
        self.cb_upper.setMinimumWidth(180)
        self.cb_upper.setChecked(
            self.settings.value("chars/uppercase", True, type=bool)
        )
        self.cb_upper.stateChanged.connect(self._save)

        self.cb_numbers = QCheckBox("Numbers")
        self.cb_numbers.setMinimumWidth(180)
        self.cb_numbers.setChecked(
            self.settings.value("chars/numbers", True, type=bool)
        )
        self.cb_numbers.stateChanged.connect(self._save)

        self.cb_symbols = QCheckBox("Symbols")
        self.cb_symbols.setMinimumWidth(180)
        self.cb_symbols.setChecked(
            self.settings.value("chars/symbols", True, type=bool)
        )
        self.cb_symbols.stateChanged.connect(self._save)

        char_grid.addWidget(self.cb_lower, 0, 0)
        char_grid.addWidget(self.cb_upper, 0, 1)
        char_grid.addWidget(self.cb_numbers, 1, 0)
        char_grid.addWidget(self.cb_symbols, 1, 1)
        char_layout.addLayout(char_grid)
        root_layout.addWidget(char_section)

        root_layout.addStretch()

        # --- 4. FOOTER ---
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 8, 0, 0)
        footer_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setObjectName("PrimaryButton")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)

        footer_layout.addWidget(close_btn)
        root_layout.addLayout(footer_layout)

        self.setMinimumWidth(500)
        self.adjustSize()

    def _save(self):
        # Pull the actual theme key from the combobox data
        theme_key = self.theme_combo.currentData()
        self.settings.setValue("theme", theme_key)
        self.settings.setValue("length/default", self.len_spin.value())
        self.settings.setValue("auto_copy", self.auto_copy_cb.isChecked())
        self.settings.setValue("chars/lowercase", self.cb_lower.isChecked())
        self.settings.setValue("chars/uppercase", self.cb_upper.isChecked())
        self.settings.setValue("chars/numbers", self.cb_numbers.isChecked())
        self.settings.setValue("chars/symbols", self.cb_symbols.isChecked())
        self.settings.sync()
        self.settings_changed.emit()
