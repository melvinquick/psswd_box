from PySide6.QtCore import QSettings, Signal
from PySide6.QtWidgets import QCheckBox, QFrame, QGridLayout, QLabel, QVBoxLayout


class CharacterOptions(QFrame):
    changed = Signal()

    def __init__(self, settings: QSettings, parent=None):
        super().__init__(parent)
        self.setObjectName("Section")
        self.settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        section_title = QLabel("Character options")
        section_title.setObjectName("SectionTitle")
        layout.addWidget(section_title)

        self.lowercase = QCheckBox("Lowercase letters")
        self.uppercase = QCheckBox("Uppercase letters")
        self.numbers = QCheckBox("Numbers")
        self.symbols = QCheckBox("Symbols")

        for cb in [self.lowercase, self.uppercase, self.numbers, self.symbols]:
            cb.stateChanged.connect(lambda _: self.changed.emit())

        option_grid = QGridLayout()
        option_grid.setSpacing(12)
        option_grid.setColumnStretch(0, 1)
        option_grid.setColumnStretch(1, 1)

        option_grid.addWidget(self.lowercase, 0, 0)
        option_grid.addWidget(self.uppercase, 0, 1)
        option_grid.addWidget(self.numbers, 1, 0)
        option_grid.addWidget(self.symbols, 1, 1)

        layout.addLayout(option_grid)
        self.reload_from_settings()

    def reload_from_settings(self):
        for cb in [self.lowercase, self.uppercase, self.numbers, self.symbols]:
            cb.blockSignals(True)

        self.lowercase.setChecked(
            self.settings.value("chars/lowercase", True, type=bool)
        )
        self.uppercase.setChecked(
            self.settings.value("chars/uppercase", True, type=bool)
        )
        self.numbers.setChecked(self.settings.value("chars/numbers", True, type=bool))
        self.symbols.setChecked(self.settings.value("chars/symbols", True, type=bool))

        for cb in [self.lowercase, self.uppercase, self.numbers, self.symbols]:
            cb.blockSignals(False)

    def get_types(self):
        return (
            self.lowercase.isChecked(),
            self.uppercase.isChecked(),
            self.numbers.isChecked(),
            self.symbols.isChecked(),
        )
