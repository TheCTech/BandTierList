from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock


class ProfileScreen(Screen):
    def __init__(self, saved_data=None, **kwargs):
        super().__init__(**kwargs)

        self.saved_data = saved_data

        self.artist = None
        self.edit_mode = False
        self.referrer = "home_screen"

        self.delete_confirmation_awaiting = False

        root = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=12
        )

        top_bar = BoxLayout(
            size_hint=(1, None),
            height=60,
            spacing=10
        )

        self.edit_btn = Button(
            text="\U0001F58D",
            font_name="NotoEmoji-Regular.ttf",
            size_hint=(None, None),
            width=60,
            height=60
        )
        self.edit_btn.bind(on_press=self.toggle_edit_mode)

        self.close_btn = Button(
            text="Close",
            size_hint=(None, None),
            width=125,
            height=50
        )
        self.close_btn.bind(on_press=self.go_back)

        top_bar.add_widget(self.edit_btn)
        top_bar.add_widget(Label())
        top_bar.add_widget(self.close_btn)

        self.name_label = Label(
            text="Artist Name",
            size_hint=(1, None),
            height=60,
            font_size=48
        )

        self.position_label = Label(
            text="#0",
            size_hint=(1, None),
            height=30
        )

        self.edit_row = BoxLayout(
            size_hint=(1, None),
            height=50,
            spacing=10
        )

        self.edit_row.add_widget(Label())

        self.save_btn = Button(
            text="Save",
            size_hint=(None, 1),
            width=200
        )
        self.save_btn.bind(on_press=self.save_artist)

        self.move_btn = Button(
            text="Move",
            size_hint=(None, 1),
            width=200
        )
        self.move_btn.bind(on_press=self.move_artist)

        self.delete_btn = Button(
            text="Delete",
            size_hint=(None, 1),
            width=200
        )
        self.delete_btn.bind(on_press=self.delete_artist)

        self.edit_row.add_widget(self.save_btn)
        self.edit_row.add_widget(self.move_btn)
        self.edit_row.add_widget(self.delete_btn)

        self.edit_row.add_widget(Label())

        notes_title = Label(
            text="Notes",
            size_hint=(1, None),
            height=30,
            halign="left",
            valign="middle"
        )
        notes_title.bind(size=lambda inst, val: setattr(inst, "text_size", val))

        self.notes_input = TextInput(
            multiline=True,
            disabled=True
        )

        root.add_widget(top_bar)
        root.add_widget(self.name_label)
        root.add_widget(self.position_label)
        root.add_widget(self.edit_row)
        root.add_widget(notes_title)
        root.add_widget(self.notes_input)

        self.add_widget(root)

    def load_artist(self, artist):
        self.artist = artist

        name = artist.get("name", "Unknown")

        self.name_label.text = name

        pos = self.saved_data._find_artist_index(name)
        self.position_label.text = f"#{pos + 1}"

        self.notes_input.text = artist.get("notes", "")

        self.edit_mode = False
        self.notes_input.disabled = True

        self.edit_row.opacity = 0
        self.edit_row.disabled = True

    def toggle_edit_mode(self, instance):
        self.edit_mode = not self.edit_mode

        self.notes_input.disabled = not self.edit_mode

        if self.edit_mode:
            self.edit_row.opacity = 1
            self.edit_row.disabled = False
            Clock.schedule_once(lambda dt: setattr(self.notes_input, "focus", True), 0.1)
        else:
            self.edit_row.opacity = 0
            self.edit_row.disabled = True
            self.save_artist(self.save_btn)

    def go_back(self, instance):
        self.manager.current = self.referrer

    def save_artist(self, instance):
        if not self.artist:
            return

        self.artist["notes"] = self.notes_input.text

        self.saved_data.set_artist_notes(
            self.artist["name"],
            self.artist["notes"]
        )

        self.add_feedback("Saved")

    def delete_artist(self, instance):
        if not self.artist:
            return
        
        def reset_delete_button():
            self.delete_confirmation_awaiting = False
            self.delete_btn.text = "Delete"
            self.delete_btn.background_color=(1, 1, 1, 1)

        if not self.delete_confirmation_awaiting:
            self.delete_confirmation_awaiting = True
            self.delete_btn.text = "CONFIRM"
            self.delete_btn.background_color=(1, 0, 0, 1)
            Clock.schedule_once(lambda dt: reset_delete_button(), 3)
            return

        name = self.artist["name"]

        artists = self.saved_data.get("artists")
        artists[:] = [a for a in artists if a["name"] != name]

        self.saved_data.save()

        self.add_feedback("Deleted")

        home = self.manager.get_screen("home_screen")
        home.update_progress()

        self.manager.current = "home_screen"

    def move_artist(self, instance):
        list_screen = self.manager.get_screen("list_screen")

        list_screen.set_edit_mode(True, self.artist["name"])

        self.manager.current = "list_screen"

    def add_feedback(self, message):
        self.close_btn.text = message

        Clock.schedule_once(lambda dt: setattr(self.close_btn, "text", "Close"), 2)