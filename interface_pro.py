#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.uix.widget import Widget
from tkinter import Tk, filedialog
import os

# LEAR CORPORATE COLORS - Professional Design
COLOR_LEAR_RED = (0.85, 0.05, 0.15, 1)      # Primary Brand Color
COLOR_DARK_GRAY = (0.15, 0.15, 0.18, 1)     # Dark Professional Gray
COLOR_LIGHT_GRAY = (0.95, 0.95, 0.97, 1)    # Light Background
COLOR_WHITE = (1, 1, 1, 1)                  # Pure White
COLOR_TEXT_PRIMARY = (0.2, 0.2, 0.2, 1)     # Primary Text
COLOR_TEXT_SECONDARY = (0.5, 0.5, 0.5, 1)   # Secondary Text
COLOR_BORDER = (0.85, 0.85, 0.87, 1)        # Border Color
COLOR_SUCCESS = (0.13, 0.55, 0.13, 1)       # Success Green
COLOR_HOVER = (0.95, 0.08, 0.18, 1)         # Hover State

# Configure window
Window.size = (1200, 800)
Window.title = "LEAR Corporation - Regression Test Framework"
Window.clearcolor = COLOR_LIGHT_GRAY


class ProfessionalButton(Button):
    """Custom professional button with shadow and hover effect"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.background_normal = ''
        self.color = COLOR_WHITE
        self.bold = True
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # Shadow effect
            Color(0.8, 0.8, 0.8, 0.3)
            RoundedRectangle(
                pos=(self.x + 2, self.y - 2),
                size=self.size,
                radius=[8]
            )
            # Main button background
            Color(*COLOR_LEAR_RED)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[8]
            )


class StatusCard(BoxLayout):
    """Professional status card widget"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 25
        self.spacing = 15
        self.bg_color = COLOR_WHITE  # Default background color
        self.bind(size=self.update_graphics, pos=self.update_graphics)
        
    def update_graphics(self, *args):
        self.canvas.before.clear()   
        with self.canvas.before:
            # Card background
            Color(*self.bg_color)
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[12]
            )
            # Border
            Color(*COLOR_BORDER)
            Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, 12),
                width=1.2
            )
    
    def set_background_color(self, color):
        """Change the background color of the card"""
        self.bg_color = color
        self.update_graphics()


class LearProfessionalApp(App):
    """LEAR Corporation Professional Regression Framework"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.xml_loaded = False
        self.config_loaded = False
    
    def build(self):
        """Build the professional interface"""
        main_layout = BoxLayout(orientation='vertical', padding=0, spacing=0)
        
        # ============ PROFESSIONAL HEADER ============
        header = BoxLayout(size_hint_y=0.12, padding=[30, 15], spacing=25)
        with header.canvas.before:
            Color(*COLOR_WHITE)
            Rectangle(size=header.size, pos=header.pos)
            # Bottom border for header
            Color(*COLOR_LEAR_RED)
            Rectangle(size=(header.width, 3), pos=(header.x, header.y))
        
        # Logo Section
        logo_container = BoxLayout(size_hint_x=0.2, orientation='horizontal', spacing=15)
        logo = Image(source='assets/Lear.png', size_hint_x=1, allow_stretch=True, keep_ratio=True)
        logo_container.add_widget(logo)
        header.add_widget(logo_container)
        
        # Title Section - CENTERED
        title_layout = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=5)
        
        main_title = Label(
            text='Regression Test Framework',
            font_size='32sp',
            bold=True,
            halign='center',
            valign='middle'
        )
        main_title.color = COLOR_TEXT_PRIMARY
        main_title.bind(size=main_title.setter('text_size'))
        title_layout.add_widget(main_title)
        
        subtitle = Label(
            text='CANoe Automated Execution Testing Platform',
            font_size='20sp',
            halign='center',
            valign='middle'
        )
        subtitle.color = COLOR_LEAR_RED
        subtitle.bind(size=subtitle.setter('text_size'))
        title_layout.add_widget(subtitle)
        
        header.add_widget(title_layout)
        
        # Empty space for balance
        empty_space = BoxLayout(size_hint_x=0.2)
        header.add_widget(empty_space)
        
        main_layout.add_widget(header)
        
        # ============ MAIN CONTENT AREA ============
        content = BoxLayout(orientation='horizontal', padding=40, spacing=40, size_hint_y=0.88)
        
        # LEFT PANEL - ACTION BUTTONS
        left_panel = BoxLayout(orientation='vertical', size_hint_x=0.45, spacing=25)
        
        # Section Title
        actions_title = Label(
            text='Import & Configuration',
            font_size='20sp',
            bold=True,
            size_hint_y=0.08,
            halign='left'
        )
        actions_title.color = COLOR_DARK_GRAY
        actions_title.bind(size=actions_title.setter('text_size'))
        left_panel.add_widget(actions_title)
        
        # Button Container
        buttons_container = BoxLayout(orientation='vertical', spacing=20, size_hint_y=0.92)
        
        # Button 1: Import XML
        xml_card = BoxLayout(orientation='vertical', size_hint_y=0.5, padding=25, spacing=15)
        xml_card.bind(size=self._update_xml_card, pos=self._update_xml_card)
        
        xml_icon_label = Label(
            text='📄',
            font_size='52sp',
            size_hint_y=0.35
        )
        xml_card.add_widget(xml_icon_label)
        
        xml_title = Label(
            text='Import XML Test File',
            font_size='19sp',
            bold=True,
            size_hint_y=0.25
        )
        xml_title.color = COLOR_TEXT_PRIMARY
        xml_card.add_widget(xml_title)
        
        xml_desc = Label(
            text='Load test cases and scenarios',
            font_size='13sp',
            size_hint_y=0.2
        )
        xml_desc.color = COLOR_TEXT_SECONDARY
        xml_card.add_widget(xml_desc)
        
        btn_import_xml = ProfessionalButton(
            text='SELECT XML FILE',
            font_size='15sp',
            size_hint_y=0.2
        )
        btn_import_xml.bind(on_press=self.import_xml)
        xml_card.add_widget(btn_import_xml)
        
        buttons_container.add_widget(xml_card)
        
        # Button 2: Import Configuration
        config_card = BoxLayout(orientation='vertical', size_hint_y=0.5, padding=25, spacing=15)
        config_card.bind(size=self._update_config_card, pos=self._update_config_card)
        
        config_icon_label = Label(
            text='⚙️',
            font_size='52sp',
            size_hint_y=0.35
        )
        config_card.add_widget(config_icon_label)
        
        config_title = Label(
            text='Import Configuration',
            font_size='19sp',
            bold=True,
            size_hint_y=0.25
        )
        config_title.color = COLOR_TEXT_PRIMARY
        config_card.add_widget(config_title)
        
        config_desc = Label(
            text='CANoe and hardware settings',
            font_size='13sp',
            size_hint_y=0.2
        )
        config_desc.color = COLOR_TEXT_SECONDARY
        config_card.add_widget(config_desc)
        
        btn_import_config = ProfessionalButton(
            text='SELECT CONFIG FILE',
            font_size='15sp',
            size_hint_y=0.2
        )
        btn_import_config.bind(on_press=self.import_config)
        config_card.add_widget(btn_import_config)
        
        buttons_container.add_widget(config_card)
        
        left_panel.add_widget(buttons_container)
        
        content.add_widget(left_panel)
        
        # RIGHT PANEL - STATUS & INFO
        right_panel = BoxLayout(orientation='vertical', size_hint_x=0.55, spacing=25)
        
        # System Status Card
        self.status_card = StatusCard(size_hint_y=1.0)
        self.status_card_widget = self.status_card  # Keep reference for color updates
        
        status_header = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        
        status_title = Label(
            text='System Status',
            font_size='20sp',
            bold=True,
            halign='left'
        )
        status_title.color = COLOR_DARK_GRAY
        status_title.bind(size=status_title.setter('text_size'))
        status_header.add_widget(status_title)
        
        self.status_indicator = Label(
            text='●',
            font_size='24sp',
            size_hint_x=0.1
        )
        self.status_indicator.color = COLOR_TEXT_SECONDARY
        status_header.add_widget(self.status_indicator)
        
        self.status_card.add_widget(status_header)
        
        # Status Details
        self.status_text = Label(
            text='[b]Ready to Initialize[/b]\n\n'
                 '[size=14sp][b]XML File:[/b] [color=#999999]Not Loaded[/color][/size]\n\n'
                 '[size=14sp][b]Configuration:[/b] [color=#999999]Not Loaded[/color][/size]\n\n\n'
                 '[size=13sp][color=#666666]Please import required files to begin the regression testing process.[/color][/size]',
            markup=True,
            font_size='15sp',
            halign='left',
            valign='top',
            size_hint_y=0.85
        )
        self.status_text.color = COLOR_TEXT_PRIMARY
        self.status_text.bind(size=self.status_text.setter('text_size'))
        self.status_card.add_widget(self.status_text)
        
        right_panel.add_widget(self.status_card)
        
        content.add_widget(right_panel)
        
        main_layout.add_widget(content)
        
        return main_layout
    
    def _update_xml_card(self, instance, value):
        """Update XML card graphics with shadow and gradient"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            # Shadow effect
            Color(0.7, 0.7, 0.7, 0.2)
            RoundedRectangle(
                pos=(instance.x + 3, instance.y - 3),
                size=instance.size,
                radius=[12]
            )
            # Main card background
            Color(*COLOR_WHITE)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[12]
            )
            # Top accent border
            Color(*COLOR_LEAR_RED)
            RoundedRectangle(
                pos=(instance.x, instance.y + instance.height - 5),
                size=(instance.width, 5),
                radius=[12, 12, 0, 0]
            )
            # Border
            Color(*COLOR_BORDER)
            Line(
                rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 12),
                width=1.5
            )
    
    def _update_config_card(self, instance, value):
        """Update Config card graphics with shadow and gradient"""
        instance.canvas.before.clear()
        with instance.canvas.before:
            # Shadow effect
            Color(0.7, 0.7, 0.7, 0.2)
            RoundedRectangle(
                pos=(instance.x + 3, instance.y - 3),
                size=instance.size,
                radius=[12]
            )
            # Main card background
            Color(*COLOR_WHITE)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[12]
            )
            # Top accent border
            Color(*COLOR_LEAR_RED)
            RoundedRectangle(
                pos=(instance.x, instance.y + instance.height - 5),
                size=(instance.width, 5),
                radius=[12, 12, 0, 0]
            )
            # Border
            Color(*COLOR_BORDER)
            Line(
                rounded_rectangle=(instance.x, instance.y, instance.width, instance.height, 12),
                width=1.5
            )
    
    def import_xml(self, instance):
        """Import XML file with native Windows file dialog"""
        # Hide Tkinter root window
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        # Open native file dialog
        filepath = filedialog.askopenfilename(
            title='Select XML Test File',
            filetypes=[('XML Files', '*.xml'), ('All Files', '*.*')],
            initialdir=os.path.expanduser('~')
        )
        
        root.destroy()
        
        if filepath:
            self.xml_loaded = True
            filename = os.path.basename(filepath)
            
            # Update status card background to light green
            self.status_card.set_background_color((0.9, 0.98, 0.9, 1))  # Light green
            
            self.status_text.text = (
                f'[b]XML File Loaded Successfully[/b]\n\n'
                f'[size=14sp][b]XML File:[/b] [color=#228B22]{filename}[/color][/size]\n\n'
                f'[size=14sp][b]Configuration:[/b] [color=#999999]Not Loaded[/color][/size]\n\n\n'
                f'[size=12sp][color=#666666]File Path:[/color]\n{filepath}[/size]\n\n'
                f'[size=13sp][color=#228B22][b]Status:[/b] Ready to parse test cases[/color]\n'
                f'[color=#666666][b]Next Step:[/b] Import configuration file[/color][/size]'
            )
            self.status_indicator.color = (1, 0.65, 0, 1)  # Orange - partial ready
            
            # Check if both files loaded
            self._check_all_loaded()
    
    def import_config(self, instance):
        """Import configuration file with native Windows file dialog"""
        # Hide Tkinter root window
        root = Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        # Open native file dialog
        filepath = filedialog.askopenfilename(
            title='Select Configuration File',
            filetypes=[
                ('Configuration Files', '*.json;*.cfg;*.config'),
                ('JSON Files', '*.json'),
                ('Config Files', '*.cfg'),
                ('All Files', '*.*')
            ],
            initialdir=os.path.expanduser('~')
        )
        
        root.destroy()
        
        if filepath:
            self.config_loaded = True
            filename = os.path.basename(filepath)
            
            # Update status based on what's loaded
            if self.xml_loaded:
                # Both files loaded - GREEN background
                self.status_card.set_background_color((0.85, 0.98, 0.85, 1))  # Bright green
                self.status_indicator.color = COLOR_SUCCESS
                
                self.status_text.text = (
                    f'[b][color=#228B22]All Files Loaded Successfully[/color][/b]\n\n'
                    f'[size=14sp][b]XML File:[/b] [color=#228B22]Loaded ✓[/color][/size]\n\n'
                    f'[size=14sp][b]Configuration:[/b] [color=#228B22]{filename} ✓[/color][/size]\n\n\n'
                    f'[size=12sp][color=#666666]Config Path:[/color]\n{filepath}[/size]\n\n'
                    f'[size=14sp][b][color=#228B22]● System Ready[/color][/b]\n'
                    f'[color=#666666]All components initialized successfully.[/color][/size]'
                )
            else:
                # Only config loaded - Light green background
                self.status_card.set_background_color((0.9, 0.98, 0.9, 1))
                self.status_indicator.color = (1, 0.65, 0, 1)  # Orange
                
                self.status_text.text = (
                    f'[b]Configuration Loaded Successfully[/b]\n\n'
                    f'[size=14sp][b]XML File:[/b] [color=#999999]Not Loaded[/color][/size]\n\n'
                    f'[size=14sp][b]Configuration:[/b] [color=#228B22]{filename}[/color][/size]\n\n\n'
                    f'[size=12sp][color=#666666]File Path:[/color]\n{filepath}[/size]\n\n'
                    f'[size=13sp][color=#228B22][b]Status:[/b] Configuration ready[/color]\n'
                    f'[color=#666666][b]Next Step:[/b] Import XML test file[/color][/size]'
                )
            
            self._check_all_loaded()
    
    def _check_all_loaded(self):
        """Check if all files are loaded and update status"""
        if self.xml_loaded and self.config_loaded:
            # Both files loaded - make background bright green
            self.status_card.set_background_color((0.85, 0.98, 0.85, 1))
            self.status_indicator.color = COLOR_SUCCESS


if __name__ == '__main__':
    app = LearProfessionalApp()
    app.run()