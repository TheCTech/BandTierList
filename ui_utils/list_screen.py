from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class ListScreen(Screen):
    def __init__(self, saved_data=None, **kwargs):
        super().__init__(**kwargs)

        self.saved_data = saved_data
        self.edit_mode = False
        self.edit_mode_artist = None

        root = BoxLayout(
            orientation="vertical"
        )

        top_bar = BoxLayout(
            size_hint=(1, None),
            height=75,
            padding=5
        )

        title = Label(text="Artists List")

        close_btn = Button(
            text="Close",
            size_hint=(None, 1),
            width=125
        )
        close_btn.bind(on_press=self.go_back)

        top_bar.add_widget(title)
        top_bar.add_widget(close_btn)

        scroll = ScrollView()

        self.list_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            spacing=5,
            padding=10
        )

        self.list_layout.bind(
            minimum_height=self.list_layout.setter("height")
        )

        scroll.add_widget(self.list_layout)

        root.add_widget(top_bar)
        root.add_widget(scroll)

        self.add_widget(root)

    def go_back(self, instance):
        if not self.edit_mode:
            self.manager.current = "home_screen"
            return

        self.saved_data.save()

        profile = self.manager.get_screen("profile_screen")
        profile.load_artist(self.saved_data.get_artist(self.edit_mode_artist))

        self.set_edit_mode(False)

        profile.referrer = "list_screen"
        self.manager.current = "profile_screen"

    def refresh_list(self):
        self.list_layout.clear_widgets()

        if not self.saved_data:
            return

        artists = self.saved_data.get("artists")

        for i, artist in enumerate(artists, start=1):
            row = BoxLayout(
                size_hint_y=None,
                height=50,
                spacing=10
            )

            row.add_widget(
                Label(
                    text=str(i),
                    size_hint=(None, 1),
                    width=60
                )
            )

            name_label = Label(text=artist["name"])

            row.add_widget(name_label)

            if not self.edit_mode:
                edit_btn = Button(
                    text="\U0001F464",
                    font_name="NotoEmoji-Regular.ttf",
                    size_hint=(None, None),
                    width=50,
                    height=50
                )

                edit_btn.bind(
                    on_press=lambda instance, a=artist: self.edit_artist(a)
                )

                row.add_widget(edit_btn)

            elif artist["name"] == self.edit_mode_artist:
                name_label.bold = True

                up_btn = Button(
                    text="\U0001F53C",
                    background_color=(0, 0, 0, 0),
                    font_name="NotoEmoji-Regular.ttf",
                    size_hint=(None, 1),
                    width=50
                )
                up_btn.bind(
                    on_press=lambda instance, idx=i - 1: self.move_up(idx)
                )

                down_btn = Button(
                    text="\U0001F53D",
                    background_color=(0, 0, 0, 0),
                    font_name="NotoEmoji-Regular.ttf",
                    size_hint=(None, 1),
                    width=50
                )
                down_btn.bind(
                    on_press=lambda instance, idx=i - 1: self.move_down(idx)
                )

                row.add_widget(up_btn)
                row.add_widget(down_btn)

            self.list_layout.add_widget(row)

    def edit_artist(self, artist):
        profile = self.manager.get_screen("profile_screen")

        profile.load_artist(artist)

        profile.referrer = "list_screen"
        self.manager.current = "profile_screen"

    def set_edit_mode(self, state, artist_name=None):
        self.edit_mode = state
        self.edit_mode_artist = artist_name
        self.refresh_list()

    def move_up(self, index):
        self.saved_data.move_artist(index, index - 1)
        self.refresh_list()

    def move_down(self, index):
        self.saved_data.move_artist(index, index + 1)
        self.refresh_list()