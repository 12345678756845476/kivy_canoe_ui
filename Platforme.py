#!/usr/bin/env python3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.core.window import Window
import os

# ====== Palette Lear ======
LEAR_RED = (0.85, 0.05, 0.15, 1)
DARK_TEXT = (0.08, 0.08, 0.1, 1)
LIGHT_BG = (0.95, 0.96, 0.97, 1)
WHITE = (1, 1, 1, 1)
BORDER = (0.86, 0.87, 0.9, 1)

class ChipButton(Button):
    """Badge type 'Progress Test' (fond rouge, angles arrondis)."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = LEAR_RED
        self.color = WHITE
        self.bold = True
        self.font_size = 16
        self.size_hint = (None, None)
        self.height = 42
        self.padding = (18, 8)
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*LEAR_RED)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[12])

class RedButton(Button):
    """Boutons rouges style Lear."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = LEAR_RED
        self.color = WHITE
        self.bold = True
        self.font_size = 16
        self.size_hint_y = None
        self.height = 46
        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*LEAR_RED)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[8])

class CardArea(Widget):
    """Grande zone blanche avec bordure gris clair à droite."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.canvas.before.clear()
        with self.canvas.before:
            # Fond blanc
            Color(*WHITE)
            Rectangle(pos=self.pos, size=self.size)
            # Bordure
            Color(*BORDER)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=1.2)

class LearUI(App):
    def build(self):
        # Fenêtre
        Window.clearcolor = LIGHT_BG
        Window.size = (1280, 720)

        root = BoxLayout(orientation='vertical', padding=12, spacing=12)

        # ================== HEADER ==================
        header = BoxLayout(orientation='horizontal', size_hint_y=0.14, padding=[6, 6, 6, 6], spacing=10)

        # Logo (à gauche)
        logo_source = "assets/Lear.png"  # Mets l'image dans le dossier assets/
        logo_box = BoxLayout(size_hint_x=0.2, padding=[6, 0, 6, 0])
        logo = Image(source=logo_source, allow_stretch=True, keep_ratio=True)
        logo_box.add_widget(logo)
        header.add_widget(logo_box)

        # Titre centré (en rouge Lear)
        title_box = BoxLayout(orientation='vertical')
        title = Label(
            text="[b] Automated Execution Testing Platform[/b]",
            markup=True,
            font_size=30,
            color=LEAR_RED,            # <<< Titre en rouge
            halign='center',
            valign='middle'
        )
        # S’assurer que le texte s’aligne correctement
        title.bind(size=lambda inst, val: setattr(inst, 'text_size', val))
        title_box.add_widget(Widget(size_hint_y=0.2))  # petit espace top
        title_box.add_widget(title)
        title_box.add_widget(Widget(size_hint_y=0.2))  # petit espace bottom
        header.add_widget(title_box)

        # Badge Progress + cloche (à droite)
        right_box = BoxLayout(orientation='horizontal', size_hint_x=0.25, spacing=8, padding=[0, 4, 0, 4])
        progress = ChipButton(text="Progress Test")
        # Ajuste la largeur du chip en fonction du texte
        progress.width = max(160, len(progress.text) * 9 + 28)

        # --- Icône cloche.png comme image ---
        bell_icon_path = "assets/cloche.png"
        if os.path.exists(bell_icon_path):
            bell = Image(
                source=bell_icon_path,
                size_hint=(None, None),
                size=(42, 42),
                allow_stretch=True,
                keep_ratio=True
            )
        else:
            # fallback si l'image n'est pas trouvée
            bell = Label(text="🔔", font_size=28, size_hint=(None, None), size=(42, 42))

        right_box.add_widget(progress)
        right_box.add_widget(bell)
        header.add_widget(right_box)

        root.add_widget(header)

        # ================== CONTENU ==================
        content = BoxLayout(orientation='horizontal', spacing=18)

        # ----- Colonne gauche (boutons) -----
        left = BoxLayout(orientation='vertical', size_hint_x=0.42, spacing=14, padding=[8, 8, 8, 8])

        btn_import_xml = RedButton(text="Import XML Test File")
        btn_import_cfg = RedButton(text="Import Configuration File")
        btn_push = RedButton(text="Push")

        # On positionne comme sur l’image : 2 boutons en haut, espace, Push au milieu, espace, 2 boutons bas
        left.add_widget(btn_import_xml)
        left.add_widget(btn_import_cfg)

        left.add_widget(Widget(size_hint_y=0.35))  # espace vertical

        # Centrer le bouton Push (en insérant un BoxLayout horizont.)
        center_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=46)
        center_row.add_widget(Widget(size_hint_x=0.35))
        center_row.add_widget(btn_push)
        center_row.add_widget(Widget(size_hint_x=0.35))
        left.add_widget(center_row)

        left.add_widget(Widget(size_hint_y=0.35))  # espace vertical

        bottom_row = BoxLayout(orientation='horizontal', spacing=14, size_hint_y=None, height=46)
        bottom_row.add_widget(RedButton(text="History Tester Actions"))
        bottom_row.add_widget(RedButton(text="Checks General Condition"))
        left.add_widget(bottom_row)

        content.add_widget(left)

        # ----- Grande zone blanche à droite -----
        right = BoxLayout(orientation='vertical', padding=[0, 0, 0, 0])
        panel = CardArea()
        right.add_widget(panel)
        content.add_widget(right)

        root.add_widget(content)

        return root


if __name__ == "__main__":
    LearUI().run()