"""Helpers to work with MIDI messages.
"""
from enum import IntEnum
from typing import Dict, Generator, List


def midi_note_on(note: int, channel: int = 0, velocity: int = 64) -> List[int]:
    """MIDI 9nH message - note on.

    >>> midi_note_on(70)
    [144, 70, 64]
    >>> midi_note_on(70, velocity=127, channel=15)
    [159, 70, 127]
    """
    status = 0x90 + channel
    return [status, note, velocity]


def midi_note_off(note: int, channel: int = 0, velocity: int = 0) -> List[int]:
    """MIDI 8nH message - note off.

    >>> midi_note_off(70)
    [128, 70, 0]
    >>> midi_note_off(70, channel=15)
    [143, 70, 0]
    """
    status = 0x80 + channel
    return [status, note, velocity]


def midi_program_change(program: int, channel: int = 0) -> List[int]:
    """MIDI CnH message - program change.

    >>> midi_program_change(80, 1)
    [193, 80]
    """
    status = 0xC0 + channel
    return [status, program]


def midi_control_change(controller: int, value: int = 0, channel: int = 0) -> List[int]:
    """MIDI BnH message - control change.

    >>> midi_control_change(7, value=127, channel=1)
    [177, 7, 127]
    """
    status = 0xB0 + channel
    return [status, controller, value]


def midi_command_increase_channel(command: List[int], inc: int) -> List[int]:
    """Increase channel number of a given command.

    >>> command = [177, 7, 127]
    >>> midi_command_increase_channel(command, -7)
    [170, 7, 127]
    >>> command
    [177, 7, 127]
    """
    if command:
        command = command[:]
        command[0] += inc
    return command



class Control(IntEnum):
    """Control function number for Control Change messages.

    See: https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2
    """
    modulation = 1
    volume = 7
    pan = 10
    all_sound_off = 120


def midi_channels() -> Generator[int, None, None]:
    """Generator of MIDI channels numbers, with percussion (9) channel omited.

    >>> list(midi_channels())
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15]
    """
    for n in range(16):
        if n != 9:  #  MIDI channel 10 is reserver for percussion
            yield n


#: All MIDI notes list (from 0 to 127)
midi_notes: List[int] = list(range(128))


def note_name(note: int) -> str:
    """Return name for a given note number.

    >>> note_name(90)
    'F#'
    """
    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    return notes[note % len(notes)]


#: MIDI instruments number => name dictionary
midi_instruments: Dict[int, str] = {
    0: "Acoustic Grand Piano",
    1: "Bright Acoustic Piano",
    2: "Electric Grand Piano",
    3: "Honky-tonk Piano",
    4: "Electric Piano 1",
    5: "Electric Piano 2",
    6: "Harpsichord",
    7: "Clavi",
    8: "Celesta",
    9: "Glockenspiel",
    10: "Music Box",
    11: "Vibraphone",
    12: "Marimba",
    13: "Xylophone",
    14: "Tubular Bells",
    15: "Dulcimer",
    16: "Drawbar Organ",
    17: "Percussive Organ",
    18: "Rock Organ",
    19: "Church Organ",
    20: "Reed Organ",
    21: "Accordion",
    22: "Harmonica",
    23: "Tango Accordion",
    24: "Acoustic Guitar (nylon)",
    25: "Acoustic Guitar (steel)",
    26: "Electric Guitar (jazz)",
    27: "Electric Guitar (clean)",
    28: "Electric Guitar (muted)",
    29: "Overdriven Guitar",
    30: "Distortion Guitar",
    31: "Guitar harmonics",
    32: "Acoustic Bass",
    33: "Electric Bass (finger)",
    34: "Electric Bass (pick)",
    35: "Fretless Bass",
    36: "Slap Bass 1",
    37: "Slap Bass 2",
    38: "Synth Bass 1",
    39: "Synth Bass 2",
    40: "Violin",
    41: "Viola",
    42: "Cello",
    43: "Contrabass",
    44: "Tremolo Strings",
    45: "Pizzicato Strings",
    46: "Orchestral Harp",
    47: "Timpani",
    48: "String Ensemble 1",
    49: "String Ensemble 2",
    50: "SynthStrings 1",
    51: "SynthStrings 2",
    52: "Choir Aahs",
    53: "Voice Oohs",
    54: "Synth Voice",
    55: "Orchestra Hit",
    56: "Trumpet",
    57: "Trombone",
    58: "Tuba",
    59: "Muted Trumpet",
    60: "French Horn",
    61: "Brass Section",
    62: "SynthBrass 1",
    63: "SynthBrass 2",
    64: "Soprano Sax",
    65: "Alto Sax",
    66: "Tenor Sax",
    67: "Baritone Sax",
    68: "Oboe",
    69: "English Horn",
    70: "Bassoon",
    71: "Clarinet",
    72: "Piccolo",
    73: "Flute",
    74: "Recorder",
    75: "Pan Flute",
    76: "Blown Bottle",
    77: "Shakuhachi",
    78: "Whistle",
    79: "Ocarina",
    80: "Lead 1 (square)",
    81: "Lead 2 (sawtooth)",
    82: "Lead 3 (calliope)",
    83: "Lead 4 (chiff)",
    84: "Lead 5 (charang)",
    85: "Lead 6 (voice)",
    86: "Lead 7 (fifths)",
    87: "Lead 8 (bass + lead)",
    88: "Pad 1 (new age)",
    90: "Pad 3 (polysynth)",
    89: "Pad 2 (warm)",
    91: "Pad 4 (choir)",
    92: "Pad 5 (bowed)",
    93: "Pad 6 (metallic)",
    94: "Pad 7 (halo)",
    95: "Pad 8 (sweep)",
    96: "FX 1 (rain)",
    97: "FX 2 (soundtrack)",
    98: "FX 3 (crystal)",
    99: "FX 4 (atmosphere)",
    100: "FX 5 (brightness)",
    101: "FX 6 (goblins)",
    102: "FX 7 (echoes)",
    103: "FX 8 (sci-fi)",
    104: "Sitar",
    105: "Banjo",
    106: "Shamisen",
    107: "Koto",
    108: "Kalimba",
    109: "Bag pipe",
    110: "Fiddle",
    111: "Shanai",
    112: "Tinkle Bell",
    113: "Agogo",
    114: "Steel Drums",
    115: "Woodblock",
    116: "Taiko Drum",
    117: "Melodic Tom",
    118: "Synth Drum",
    119: "Reverse Cymbal",
    120: "Guitar Fret Noise",
    121: "Breath Noise",
    122: "Seashore",
    123: "Bird Tweet",
    124: "Telephone Ring",
    125: "Helicopter",
    126: "Applause",
    127: "Gunshot",
}
