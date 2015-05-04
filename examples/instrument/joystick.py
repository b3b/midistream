import os
from kivy.uix.scatter import Scatter
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty, OptionProperty, ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.lang import Builder
from helpers import note_name
from instrument import Instrument
from noteselect import NoteSelectPopup

Builder.load_file(os.path.join(os.path.dirname(__file__), 'joystick.kv'))

class JoystickButton(Scatter):
    program = NumericProperty(1, min=1, max=128)
    note = NumericProperty(60)
    title = StringProperty('')
    play = BooleanProperty(False)
    edit_mode = BooleanProperty(False)
    double_click = NumericProperty(0)
    color_normal = ListProperty([.3, .5, .6, .6])
    color_play = ListProperty([.3, .5, .6, .5])

    def get_state(self):
        return {
            'program': self.program,
            'note': self.note,
            'position':  self.bbox[0],
            'size':  self.bbox[1],
        }

    def load_state(self, state):
        self.program = state['program']
        self.note = state['note']
        self.pos = state['position']
        self.size = state['size']

    def on_touch_down(self, touch):
        if self.edit_mode:
            return super(JoystickButton, self).on_touch_down(touch)
        super(Scatter, self).on_touch_down(touch)
        self.on_touch(touch)

    def on_touch(self, touch):
        if not 'notes' in touch.ud:
            touch.ud['notes'] = []
        if self.collide_point(touch.x, touch.y):
            if not self in touch.ud['notes']:
                if not self.play:
                    self.play = True
                touch.ud['notes'].append(self)
        elif self in touch.ud['notes']:
            if self.play:
                self.play = False
            touch.ud['notes'].remove(self)

    def on_touch_up(self, touch):
        if self.edit_mode:
            if touch.is_double_tap and self.collide_point(touch.x, touch.y):
                if touch.ud['double_tap_handler'] is None:
                    self.double_click += 1
                    touch.ud['double_tap_handler'] = self
            return super(JoystickButton, self).on_touch_up(touch)
        super(Scatter, self).on_touch_up(touch)
        if self in touch.ud.get('notes', []):
            if self.play:
                self.play = False
            touch.ud['notes'].remove(self)

    def on_touch_move(self, touch):
        if self.edit_mode:
            return super(JoystickButton, self).on_touch_move(touch)
        super(Scatter, self).on_touch_move(touch)
        self.on_touch(touch)


class Joystick(FloatLayout, Instrument):
    edit_mode = BooleanProperty(False)
    buttons = ListProperty([])
    note_select = ObjectProperty()
    button_size = ListProperty([100, 100])

    def __init__(self, *args, **kwargs):
        super(Joystick, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.init, -1)

    def init(self, *args):
        self.note_select.bind(selected_action=self.on_note_selection)
        self.note_select.bind(selected_note=self.play_selected_note)
        self.note_select.bind(selected_instrument=self.play_selected_note)

    def on_touch_up(self, touch):
        if self.edit_mode and touch.is_double_tap:
            touch.ud['double_tap_handler'] = None
            super(Joystick, self).on_touch_up(touch)
            if touch.ud['double_tap_handler'] is None: # double click was not handled by buttons
                touch.ud['double_tap_handler'] = self
                w, h = self.button_size
                pos = (touch.pos[0]-w/2, touch.pos[1]-h/2)
                self.note_select.open(position=pos)
        else:
            return super(Joystick, self).on_touch_up(touch)

    def add_button(self, jb):
        self.add_widget(jb)
        self.buttons.append(jb)
        jb.bind(double_click=self.configure_button)
        jb.bind(play=self.on_button_play)
        jb.edit_mode = self.edit_mode
        return jb

    def on_note_selection(self, popup, action):
        if action['action'] == 'add':
            w, h = self.button_size
            jb = JoystickButton(note=action['note'],
                                program=action['instrument'],
                                pos=action['position'])
            jb.size = (w, h)
            self.add_button(jb)
        elif action['action'] == 'del':
            button = action['target']
            self.buttons.remove(button)
            self.remove_widget(button)
        elif action['action'] == 'update':
            button = action['target']
            button.note = action['note']
            button.program = action['instrument']

    def on_edit_mode(self, instance, value):
        for button in self.buttons:
            if button.play:
                button.play = False
            button.edit_mode = value

    def configure_button(self, button, *args):
        self.note_select.open(target=button)

    def on_button_play(self, button, value):
        if value and self.program != button.program:
            self.program = button.program
        self.toggle_note(button.note, value)

    def get_state(self):
        return {
            'buttons': [b.get_state() for b in self.buttons],
            'velocity': self.velocity
        }

    def load_state(self, state):
        self.velocity = state['velocity']
        for bstate in state['buttons']:
            jb = JoystickButton()
            self.add_button(jb)
            jb.load_state(bstate)

    def clear_state(self):
        self.clear_widgets()
        self.buttons = []

    def play_selected_note(self, instance, value):
        program = self.note_select.selected_instrument
        note = self.note_select.selected_note
        self.program =  program
        self.note_on(note)
        Clock.schedule_once(lambda t: self.note_off(note), 1)
