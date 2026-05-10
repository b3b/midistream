"""Midistream demo app."""

import traceback

from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.properties import StringProperty

import midistream
from midistream import MIDIException, ReverbPreset, Synthesizer
from midistream.helpers import (
    Control,
    midi_control_change,
    midi_instruments,
    midi_note_off,
    midi_note_on,
    midi_program_change,
    note_name,
    parse_note,
)


DEMO_START = "MIDISTREAM_DEMO_START"
DEMO_PASS = "MIDISTREAM_DEMO_PASS"
DEMO_FAIL = "MIDISTREAM_DEMO_FAIL"


class DemoApp(App):
    status = StringProperty("Starting")

    def build(self):
        self.title = "Midistream Demo"
        self.midi = None
        self.note = 60
        self.program = 0
        self.active_notes = set()
        self.log_lines = []
        root = self.root
        self.log("MIDISTREAM_APP_BUILD")
        return root

    def on_start(self):
        Clock.schedule_once(lambda _dt: self.run_checks(), 0)

    def on_stop(self):
        for note in list(self.active_notes):
            try:
                self.write(midi_note_off(note), "note_off on stop")
            except Exception as exc:
                self.log(
                    "MIDISTREAM_STOP_NOTE_OFF_ERROR=%s: %s" % (type(exc).__name__, exc)
                )
        if self.midi is not None:
            try:
                self.log("MIDISTREAM_CLOSE")
                self.midi.close()
            except Exception as exc:
                self.log("MIDISTREAM_CLOSE_ERROR=%s: %s" % (type(exc).__name__, exc))
            finally:
                self.midi = None

    def log(self, message):
        line = str(message)
        Logger.info("midistream-demo: %s", line)
        print(line)
        self.log_lines.append(line)
        self.log_lines = self.log_lines[-200:]
        if hasattr(self, "log_output"):
            self.log_output.text = "\n".join(self.log_lines)

    def fail(self, message):
        self.status = "FAIL"
        self.log("%s %s" % (DEMO_FAIL, message))

    def pass_step(self, name):
        self.log("MIDISTREAM_TEST_%s=PASS" % name)

    def run_checks(self, *_args):
        self.status = "Running"
        self.log(DEMO_START)
        self.log("MIDISTREAM_VERSION=%s" % midistream.__version__)

        try:
            self.midi = Synthesizer()
            self.pass_step("INIT")

            self.log("MIDISTREAM_CONFIG=%r" % (self.midi.config,))
            self.pass_step("CONFIG")

            self.midi.volume = 70
            self.log("MIDISTREAM_VOLUME=%s" % self.midi.volume)
            self.volume_slider.value = self.midi.volume
            self.pass_step("VOLUME")

            for preset in ReverbPreset:
                self.midi.reverb = preset
                self.log("MIDISTREAM_REVERB=%s" % preset.name)
            self.pass_step("REVERB")

            self.write(midi_program_change(0), "program_change")
            self.write(midi_control_change(Control.volume, 90), "control_change")
            self.write(midi_note_on(60, velocity=64), "note_on")
            self.write(midi_note_off(60), "note_off")
            self.pass_step("WRITE")
        except Exception as exc:
            self.fail("%s: %s" % (type(exc).__name__, exc))
            self.log(traceback.format_exc())
            return

        self.status = "PASS"
        self.log(DEMO_PASS)

    def write(self, command, description):
        if self.midi is None:
            raise MIDIException("Synthesizer is not initialized.")
        self.log("MIDISTREAM_WRITE_%s=%r" % (description.upper(), command))
        self.midi.write(command)

    def parse_note_input(self):
        text = self.note_input.text.strip()
        if not text:
            raise ValueError("Note is empty.")
        try:
            note = int(text)
        except ValueError:
            note = parse_note(text)
        if not 0 <= note <= 127:
            raise ValueError("Note must be in MIDI range 0..127.")
        self.note = note
        self.note_input.text = note_name(note)
        return note

    def set_note_from_input(self, *_args):
        try:
            note = self.parse_note_input()
        except Exception as exc:
            self.fail("%s: %s" % (type(exc).__name__, exc))
        else:
            self.log("MIDISTREAM_NOTE=%s" % note)

    def note_on(self, *_args):
        try:
            note = self.parse_note_input()
            self.write(midi_note_on(note, velocity=90), "manual_note_on")
            self.active_notes.add(note)
        except Exception as exc:
            self.fail("%s: %s" % (type(exc).__name__, exc))

    def note_off(self, *_args):
        try:
            note = self.parse_note_input()
            self.write(midi_note_off(note), "manual_note_off")
            self.active_notes.discard(note)
        except Exception as exc:
            self.fail("%s: %s" % (type(exc).__name__, exc))

    def on_program_selected(self, _spinner, text):
        try:
            program = int(text.split(":", 1)[0])
            self.program = program
            if self.midi is None:
                return
            self.write(midi_program_change(program), "manual_program_change")
        except Exception as exc:
            self.fail("%s: %s" % (type(exc).__name__, exc))

    def on_reverb_selected(self, _spinner, text):
        try:
            preset = ReverbPreset[text]
            if self.midi is None:
                return
            self.midi.reverb = preset
            self.log("MIDISTREAM_MANUAL_REVERB=%s" % preset.name)
        except Exception as exc:
            self.fail("%s: %s" % (type(exc).__name__, exc))

    def on_volume_touch_up(self, _slider, _touch):
        try:
            if not _slider.collide_point(*_touch.pos):
                return
            if self.midi is None:
                raise MIDIException("Synthesizer is not initialized.")
            volume = int(self.volume_slider.value)
            self.midi.volume = volume
            self.log("MIDISTREAM_MANUAL_VOLUME=%s" % volume)
        except Exception as exc:
            self.fail("%s: %s" % (type(exc).__name__, exc))

    @staticmethod
    def program_label(program):
        return "%03d: %s" % (program, midi_instruments[program])

    @property
    def program_labels(self):
        return [self.program_label(n) for n in sorted(midi_instruments)]

    @property
    def reverb_labels(self):
        return [preset.name for preset in ReverbPreset]

    @property
    def note_input(self):
        return self.root.ids.note_input

    @property
    def volume_slider(self):
        return self.root.ids.volume_slider

    @property
    def log_output(self):
        return self.root.ids.log_output


if __name__ == "__main__":
    DemoApp().run()
