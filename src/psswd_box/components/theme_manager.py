class ThemeManager:
    DEFAULT_THEME = "psswd_box_dark"

    def __init__(self, themes, qss_template):
        self.themes = themes
        self.template = qss_template
        self._polish_targets = []

    def register(self, widget):
        if widget not in self._polish_targets:
            self._polish_targets.append(widget)

    def resolve(self, theme_name):
        return theme_name if theme_name in self.themes else self.DEFAULT_THEME

    def get_available_themes(self):
        # Filter out the 'general' block and return sorted keys
        return sorted([k for k in self.themes if k != "general"])

    def get_display_name(self, theme_key):
        # Converts "psswd_box_dark" to "Psswd Box Dark"
        return theme_key.replace("_", " ").title()

    def build_stylesheet(self, theme_name):
        name = self.resolve(theme_name)
        tokens = {**self.themes[name], **self.themes["general"]}
        stylesheet = self.template
        for key, value in tokens.items():
            stylesheet = stylesheet.replace("{{" + key + "}}", str(value))
        return stylesheet

    def apply(self, widget, theme_name):
        name = self.resolve(theme_name)
        widget.setStyleSheet(self.build_stylesheet(name))
        self._repolish_all()
        return name

    @staticmethod
    def _repolish(widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _repolish_all(self):
        for widget in self._polish_targets:
            self._repolish(widget)
