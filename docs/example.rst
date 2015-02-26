Usage Example
-------------

    >>> from miditrack import Midi
    >>> midi = Midi()
    >>> midi.run()
    >>> print midi.config.keys()
    ['numChannels', 'buildGUID', 'mixBufferSize', 'filterEnabled', 'maxVoices',
    'libVersion', 'sampleRate', 'buildTimeStamp', 'checkedVersion']
    >>> print midi.config['sampleRate']
    22050
    >>> midi.write_short(0x90, 60, 127) # On middle C note with maximum velocity
    >>> import time ; time.sleep(2)
    >>> midi.write_short(0x80, 60, 127) # Off middle C note with maximum velocity
