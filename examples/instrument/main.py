import os
import traceback
try:
    import cPickle as pickle
except:
    import pickle
from kivy.base import runTouchApp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger
from midistream.helpers import midi_channels
from instrument import Instrument
from joystick import Joystick, JoystickButton
from recorder import Recorder
from controls import VelocitySlider, ControlsLayout, ReverbDropdown
from error_message import ErrorMessage

from midistream import ReverbPreset, Synthesizer


class Reproducer(BoxLayout, Instrument):
    pass

class MainLayout(BoxLayout):
    pass

class InstrumentApp(App):

    def build(self):
        self.midi = None
        self.instruments = []
        self.channels = midi_channels()
        return MainLayout()

    def on_start(self):
        self.midi = Synthesizer()
        self.load_state()

    def on_stop(self):
        self.save_state()
        self.midi.close()

    def run(self):
        try:
            super(InstrumentApp, self).run()
        except Exception as e:
            msg = "Error: {type}{args}".format(type=type(e),
                                               args=e.args)
            Logger.exception(msg)
            if not getattr(self, 'exeption_state', False):
                self.exeption_state = True
                msg = '\n'.join((msg, traceback.format_exc()))
                message = ErrorMessage(message=msg)

                def raise_exception(*args, **kwargs):
                    raise Exception(msg)

                message.bind(on_dismiss=raise_exception)
                message.open()
                try:
                    runTouchApp()
                except:
                    pass

    def register_instrument(self, instrument):
        '''Connect instrument to synthesizer

        :returns: allocated MIDI channel
        '''
        self.instruments.append(instrument)
        channel = next(self.channels)
        instrument.bind(command=self.on_midi_command)
        return channel

    def on_midi_command(self, instrument, command):
        self.midi.write(command)

    def reverb(self, preset):
        self.midi.reverb = {
            'disabled': ReverbPreset.OFF,
            'large hall': ReverbPreset.LARGE_HALL,
            'hall': ReverbPreset.HALL,
            'chamber': ReverbPreset.CHAMBER,
            'room': ReverbPreset.ROOM,
        }[preset]

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
