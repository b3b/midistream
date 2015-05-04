import os
try:
    import cPickle as pickle
except:
    import pickle
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivy.logger import Logger
from helpers import midi_channels
from instrument import Instrument
from joystick import Joystick, JoystickButton
from recorder import Recorder
from controls import VelocitySlider, ControlsLayout


class DummyMidi(object):

    def start(self):
        Logger.info('midi start')

    def stop(self):
        Logger.info('midi stop')

    def write_short(self, *args):
        message = "midi: write_shord({})".format(args)
        Logger.info(message)


if platform == 'android':
    from midistream import Midi
else:
    Midi = DummyMidi


class Reproducer(BoxLayout, Instrument):
    pass

class MainLayout(BoxLayout):
    pass

class InstrumentApp(App):

    def build(self):
        self.midi = Midi()
        self.instruments = []
        self.channels = midi_channels()
        return MainLayout()

    def on_start(self):
        self.midi.start()
        self.load_state()

    def on_stop(self):
        self.save_state()
        self.midi.stop()

    def register_instrument(self, instrument):
        '''Connect instrument to synthesizer

        :returns: allocated MIDI channel
        '''
        self.instruments.append(instrument)
        channel = self.channels.next()
        instrument.bind(command=self.on_midi_command)
        return channel

    def on_midi_command(self, instrument, command):
        self.midi.write_short(*command)

    @property
    def state_path(self):
        return os.path.join(
            os.path.abspath(self.directory),
            'state.cfg')

    def load_state(self, path=None):
        if path is None:
            path = self.state_path
        if os.path.exists(path):
            with open(path, 'rb') as f:
                try:
                    state = pickle.load(f)
                except EOFError:
                    return
            for instrument in self.instruments:
                try:
                    istate = state[instrument.name]
                except KeyError:
                    pass
                else:
                    instrument.load_state(istate)

    def save_state(self, path=None):
        if path is None:
            path = self.state_path
        with open(path, 'wb') as f:
            pickle.dump(self.get_state(), f)

    def get_state(self):
        return {i.name: i.get_state() for i in self.instruments if i.name}


if __name__ == '__main__':
    InstrumentApp().run()
