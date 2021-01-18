from kivy.properties import (BooleanProperty, NumericProperty, BoundedNumericProperty,
                             StringProperty, ListProperty, OptionProperty)
from midistream.v1.helpers import (midi_note_on, midi_note_off, midi_program_change,
                                   midi_control_change)


class Instrument(object):
    name = StringProperty('')
    channel = NumericProperty(0, min=0, max=15)
    program = NumericProperty(1, min=1, max=128)
    velocity = BoundedNumericProperty(127, min=0, max=127)
    notes_on = set()
    played_notes = set()

    command = ListProperty([])
    '''current MIDI command'''

    def toggle_note(self, note, state, velocity=None):
        if velocity is None:
            velocity = self.velocity
        channel = self.channel
        if state:
            command = midi_note_on(note, channel, int(velocity))
            self.played_notes.add(note)
            self.notes_on.add(note)
        else:
            command = midi_note_off(note, channel)
            try:
                self.notes_on.remove(note)
            except KeyError:
                pass
        self.command = command

    def note_on(self, note, *args):
        self.toggle_note(note, True)

    def note_off(self, note, *args):
        self.toggle_note(note, False)

    def all_notes_off(self):
        for note in self.notes_on:
            self.note_off(note)
        self.notes_on.clear()

    def on_program(self, instrument, program):
        self.command = midi_program_change(program, self.channel)

    def toggle_control(self, control, value):
        self.command = midi_control_change(control, value,
                                           channel=self.channel)

    def get_state(self):
        '''Return instrument state as dict'''
        return {
            'program': self.program,
            'velocity': self.velocity
            }

    def load_state(self, state):
        '''Restore instrument state from dict'''
        self.program = state['program']
        self.velocity = state['velocity']

    def clear_state(self):
        '''Reset instrument to initial state'''
        self.program = 1
        self.velocity = 127
