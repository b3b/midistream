"""Sequentially play all the MIDI instruments.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from itertools import cycle
from midistream import Syntesizer
from midistream.helpers import (
    midi_note_on,
    midi_note_off,
    midi_program_change,
    midi_instruments,
)


class MainLayout(BoxLayout):
    pass


class PlayAll(App):
    instrument = StringProperty("")
    note = NumericProperty(0)
    start_note = 60
    end_note = 64
    note_step = 2

    def build(self):
        return MainLayout()

    def on_start(self):
        self.midi = Syntesizer()
        self.instruments = cycle(midi_instruments.items())
        Clock.schedule_interval(self.change_note, 1)

    def change_note(self, *args):
        if self.note:
            self.midi.write(midi_note_off(self.note))
            self.note += self.note_step
            if self.note > self.end_note:
                self.change_instrument()
        else:
            self.change_instrument()
        self.midi.write(midi_note_on(self.note))

    def change_instrument(self, *args):
        program, title = next(self.instruments)
        self.midi.write(midi_program_change(program))
        self.instrument = title
        self.note = self.start_note


if __name__ == "__main__":
    PlayAll().run()
