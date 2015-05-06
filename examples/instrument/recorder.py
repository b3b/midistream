import os
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ListProperty, OptionProperty, ObjectProperty
import threading
import time
from collections import deque
from helpers import midi_command_increase_channel, midi_program_change

Builder.load_file(os.path.join(os.path.dirname(__file__), 'recorder.kv'))


class Recorder(BoxLayout):
    instrument = ObjectProperty()
    reproducer = ObjectProperty()
    state = StringProperty("")
    position = NumericProperty(0)
    rec_start_time = NumericProperty(0)
    rec_prev_time = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        super(Recorder, self).__init__(*args, **kwargs)
        self.commands = deque()
        self.session = 0

    def on_instrument(self, instance, value):
        self.instrument.bind(command=self.record_command)

    def toggle_recording(self, *args):
        self.session += 1
        if self.state == 'rec':
            self.stop_recording()
        elif self.state == 'play':
            self.stop_playing()
        self.state = 'rec' if self.state != 'rec' else ''
        if self.state == 'rec':
            self.commands.clear()
            self.rec_start_time = self.rec_prev_time = time.time()
            self.program = self.instrument.program

    def toggle_play(self, *args):
        self.session += 1
        if self.state == 'rec':
            self.stop_recording()
        self.state = 'play' if self.state != 'play' else ''
        if self.state == 'play' and self.commands:
            self.position = 0
            self.play_prev_time = time.time()
            player = threading.Thread(target=self.play_loop)
            player.daemon = True
            player.start()
        elif self.state != 'play':
            self.stop_playing()

    def stop_recording(self):
        if self.reproducer:
            # record program change
            cmd = midi_program_change(self.program,
                                      self.instrument.channel)
        else:
            cmd = None # record pause
        self.record_command(self.reproducer, cmd)

    def stop_playing(self):
        reproducer = self.reproducer or self.instrument
        for note in self.instrument.played_notes:
            reproducer.note_off(note)

    def play_loop(self):
        session = self.session
        commands = self.commands_iter()
        reproducer = self.reproducer or self.instrument
        reproducer.program = self.program
        while self.state == 'play' and self.session == session:
            command, t = commands.next()
            if t:
                time.sleep(t)
            if self.state == 'play' and self.session == session:
                if command:
                    reproducer.command = command
                self.position += 1

    def commands_iter(self):
        while True:
            for command, t in self.commands:
                yield command, t

    def get_command(self, position=None):
        count = len(self.commands)
        if position is None:
            position = self.position
        if count:
            command, t = self.commands[self.position % count]
            return command, t

    def record_command(self, instrument, command):
        if self.state == 'rec':
            current = time.time()
            if self.commands:
                t = current - self.rec_prev_time
            else:
                t = 0
                self.rec_prev_time = current
            self.rec_prev_time = current
            if self.reproducer != self.instrument:
                inc = self.reproducer.channel - self.instrument.channel
                command = midi_command_increase_channel(command, inc)
            self.commands.append((command, t))
