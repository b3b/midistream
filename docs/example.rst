Usage Example
-------------

    >>> from midistream import ReverbPreset, Synthesizer
    >>> midi = Synthesizer()
    >>> midi.config
    {'libVersion': 50727438, 'checkedVersion': 0, 'ma3xVoices': 64, 'numChannels': 2, 'sampleRate': 22050, 'mixBufferSize': 128, 'filterEnabled': 1, 'buildTimeStamp': 1195621085, 'buildGUID': b'1feda229-b9a8-45e9-96f4-73c0a80e7220'}
    >>> midi.volume
    90
    >>> midi.volume = 70 # Set master volume
    >>> midi.reverb = ReverbPreset.LARGE_HALL # Enable reverb effect
    >>> midi.write([0x90, 60, 127]) # On middle C note with maximum velocity
    >>> import time ; time.sleep(2)
    >>> midi.write([0x80, 60, 127]) # Off middle C note with maximum velocity
    # Using helpers
    >>> from midistream.helpers import Note, midi_note_on
    >>> midi.write(midi_note_on(Note.C4) + midi_note_on(Note.Es5))
