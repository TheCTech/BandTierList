from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.label import Label
from kivy.clock import Clock

from artists_list import BANDS


class HomeScreen(Screen):
    def __init__(self, saved_data=None, **kwargs):
        super().__init__(**kwargs)

        self.saved_data = saved_data

        root = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        add_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=60,
            spacing=10
        )

        self.add_artist_input = TextInput(
            hint_text="Artist name",
            multiline=False,
            height = 60
        )

        add_button = Button(
            text="Add",
            size_hint=(None, 1),
            width=100
        )
        add_button.bind(on_press=self.on_add_artist)

        add_row.add_widget(self.add_artist_input)
        add_row.add_widget(add_button)

        list_button = Button(
            text="See List",
            size_hint=(1, None),
            height=50
        )
        list_button.bind(on_press=self.on_see_list)

        search_row = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=60,
            spacing=10
        )

        self.search_input = TextInput(
            hint_text="Search artist",
            multiline=False,
            height = 60
        )

        search_button = Button(
            text="Search",
            size_hint=(None, 1),
            width=150
        )
        search_button.bind(on_press=self.on_search_artist)

        search_row.add_widget(self.search_input)
        search_row.add_widget(search_button)

        progress_text_label = Label(
            text="Progress",
            size_hint=(1, None),
            height=30
        )

        self.progress_label = Label(
            text="(0/0)",
            size_hint=(1, None),
            height=20
        )

        self.progress_bar = ProgressBar(
            max=len(BANDS),
            value=0,
        )

        self.update_progress()

        root.add_widget(add_row)
        root.add_widget(list_button)
        root.add_widget(search_row)
        root.add_widget(progress_text_label)
        root.add_widget(self.progress_label)
        root.add_widget(self.progress_bar)

        self.add_widget(root)

    def on_add_artist(self, instance):
        name = self.add_artist_input.text.strip()

        if not name:
            return

        self.add_artist_input.text = ""
        Clock.schedule_once(lambda dt: setattr(self.add_artist_input, "hint_text", "Artist name"), 3)

        if name not in BANDS:
            self.add_artist_input.hint_text = "Does not play (check spelling?)"
            return

        if self.saved_data._find_artist_index(name) is not None:
            self.add_artist_input.hint_text = "Already exists"
            return

        self.saved_data.add_artist(name, notes="")

        self.add_artist_input.hint_text = "Added"
        self.update_progress()

        list_screen = self.manager.get_screen("list_screen")
        list_screen.set_edit_mode(True, name)
        self.manager.current = "list_screen"

    def on_see_list(self, instance):
        self.manager.get_screen("list_screen").refresh_list()
        self.manager.current = "list_screen"

    def on_search_artist(self, instance):
        query = self.search_input.text

        self.search_input.text = ""

        Clock.schedule_once(lambda dt: setattr(self.search_input, "hint_text", "Search artist"), 3)

        artist_id = self.saved_data._find_artist_index(query)

        if artist_id == None and query not in BANDS:
            self.search_input.hint_text = "Does not play (check spelling?)"
            return
        
        if artist_id == None and query in BANDS:
            self.search_input.hint_text = "Not added yet (consider doing it)"
            return

        profile = self.manager.get_screen("profile_screen")

        profile.load_artist(self.saved_data.get("artists")[artist_id])

        profile.referrer = "home_screen"
        self.manager.current = "profile_screen"
    
    def update_progress(self):
        artists_len = len(self.saved_data.get("artists"))

        self.progress_label.text = f"({artists_len}/{len(BANDS)})"
        self.progress_bar.value = artists_len