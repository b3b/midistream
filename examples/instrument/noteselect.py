import os
from kivy.lang import Builder
from kivy.uix.popup import Popup
from helpers import midi_instruments, midi_notes, note_name
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty
from kivy.uix.stacklayout import StackLayout

Builder.load_file(os.path.join(os.path.dirname(__file__), 'noteselect.kv'))


class SelectableButton(ToggleButton):
    value = NumericProperty(0)

    def select(self):
        if self.state != 'down':
            self._do_press()

class NoteButton(SelectableButton):
    def format_text(self):
        return "{}{}".format(self.value, note_name(self.value))

class InstrumentButton(SelectableButton):
    title = StringProperty('')

    def format_text(self):
        return "{}".format(self.title)

class ButtonsLayout(StackLayout):
    selection = NumericProperty(0)
    default_selection = 0

    def __init__(self, *args, **kwargs):
        super(ButtonsLayout, self).__init__(*args, **kwargs)
        self.selection = self.default_selection
        self.buttons = []
        self.add_buttons()

    def select(self, value):
        for button in self.buttons:
            if button.value == value:
                button.select()
                break

class NotesLayout(ButtonsLayout):
    default_selection = 60

    def add_buttons(self):
        for n in midi_notes:
            button = NoteButton(value=n)
            self.buttons.append(button)
            self.add_widget(button)

class InstrumentsLayout(ButtonsLayout):

    default_selection = midi_instruments.keys()[0]

    def add_buttons(self):
        for n, title in midi_instruments.items():
            button = InstrumentButton(value=n, title=title)
            self.buttons.append(button)
            self.add_widget(button)

class NoteSelectPopup(Popup):
    instruments = ObjectProperty()
    notes = ObjectProperty()
    instruments = ObjectProperty()
    panel = ObjectProperty()
    notes_tab = ObjectProperty()
    instruments_tab = ObjectProperty()

    selected_action = ObjectProperty()
    selected_note = NumericProperty(0)
    selected_instrument = NumericProperty(1)

    def open(self, target=None, position=None):
        self.target = target
        self.target_position = position
        if target:
            note = getattr(target, 'note', self.selected_note)
            instrument = getattr(target, 'program', self.selected_instrument)
            is_new_button = False
        else:
            note = self.selected_note
            instrument = self.selected_instrument
            is_new_button = True
        self.update_actions(is_new_button)
        self.notes.select(note)
        self.instruments.select(instrument)
        self.selected_note = note
        self.selected_instrument = instrument
        self.panel.switch_to(self.notes_tab)
        super(NoteSelectPopup,self).open()

    def update_actions(self, is_new_button=False):
        if not getattr(self, 'actions_buttons', None):
            actions = ('add', 'update', 'delete', 'cancel')
            self.actions_buttons = {name: self.ids[name].__self__ for name in actions}

        self.actions.clear_widgets()
        buttons = self.actions_buttons
        if is_new_button:
            self.actions.add_widget(buttons['add'])
        else:
            self.actions.add_widget(buttons['update'])
            self.actions.add_widget(buttons['delete'])
        self.actions.add_widget(buttons['cancel'])

    def set_action(self, action):
        self.selected_action = {'action': action,
                                'target': self.target,
                                'instrument': self.selected_instrument,
                                'note': self.selected_note,
                                'position': self.target_position}
        self.dismiss()
