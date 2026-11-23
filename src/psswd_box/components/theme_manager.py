class ThemeManager:
    # Set to "sugar_goth" for PNF, Psswd Box, Scramble, Wttrman
    # Set to "phaino_dusk" for Phaino
    DEFAULT_THEME = "sugar_goth"

    def __init__(self, themes, qss_template):
        self.general = themes.pop("general", {})
        self.themes = themes
        self.qss_template = qss_template

    def get_display_name(self, theme_key):
        return (
            theme_key.replace("phaino_dusk", "Phaino Dusk")
            .replace("phaino_dawn", "Phaino Dawn")
            .replace("_", " ")
            .title()
        )

    def get_available_themes(self):
        valid_themes = list(self.themes.keys())
        
        def sort_key(key):
            display = self.get_display_name(key)
            base_name = (
                display.replace(" Dark", "")
                .replace(" Light", "")
                .replace(" Dusk", "")
                .replace(" Dawn", "")
            )
            if " Dark" in display or " Dusk" in display:
                weight = 0
            else:
                weight = 1
            return (base_name, weight)
            
        return sorted(valid_themes, key=sort_key)

    def resolve(self, theme_name):
        if theme_name in self.themes:
            return theme_name
        return self.DEFAULT_THEME

    def render(self, theme_name):
        name = self.resolve(theme_name)
        tokens = {**self.general, **self.themes[name]}
        
        qss = self.qss_template
        for key, value in tokens.items():
            qss = qss.replace(f"{{{{{key}}}}}", str(value))
            
        import re
        return re.sub(r"\{\{[^}]+\}\}", "", qss)