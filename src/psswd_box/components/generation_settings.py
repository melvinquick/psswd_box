from PySide6.QtCore import QSettings, Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSlider,
    QSpinBox,
    QVBoxLayout,
)


class GenerationSettings(QFrame):
    changed = Signal()

    def __init__(self, settings: QSettings, parent=None):
        super().__init__(parent)
        self.setObjectName("Section")
        self.settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        section_title = QLabel("Generation settings")
        section_title.setObjectName("SectionTitle")
        layout.addWidget(section_title)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(10, 100)
        self.slider.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.slider.valueChanged.connect(lambda _: self._on_slider_changed())

        self.spin = QSpinBox()
        self.spin.setRange(10, 100)
        self.spin.setSuffix(" characters")
        self.spin.valueChanged.connect(lambda _: self._on_spin_changed())

        length_row = QHBoxLayout()
        length_row.setSpacing(12)
        length_row.addWidget(self.slider, 1)
        length_row.addWidget(self.spin)
        layout.addLayout(length_row)

        self.auto_copy = QCheckBox("Copy automatically after generation")
        self.auto_copy.stateChanged.connect(lambda _: self.changed.emit())
        layout.addWidget(self.auto_copy)

        self.reload_from_settings()

    def reload_from_settings(self):
        self.slider.blockSignals(True)
        self.spin.blockSignals(True)
        self.auto_copy.blockSignals(True)

        default_len = int(self.settings.value("length/default", 24))
        self.slider.setValue(default_len)
        self.spin.setValue(default_len)
        self.auto_copy.setChecked(self.settings.value("auto_copy", True, type=bool))

        self.slider.blockSignals(False)
        self.spin.blockSignals(False)
        self.auto_copy.blockSignals(False)

    def _on_slider_changed(self):
        if self.spin.value() != self.slider.value():
            self.spin.setValue(self.slider.value())
        self.changed.emit()

    def _on_spin_changed(self):
        if self.slider.value() != self.spin.value():
            self.slider.setValue(self.spin.value())
        self.changed.emit()

    def get_length(self):
        return self.spin.value()

    def is_auto_copy_enabled(self):
        return self.auto_copy.isChecked()
