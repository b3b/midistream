Usage Example
-------------

    >>> from midistream import Midi
    >>> midi = Midi('/mnt/sdcard/example.raw') # not only play, but also save output to example.raw
    >>> midi.start()
    >>> print midi.config.keys()
    ['numChannels', 'buildGUID', 'mixBufferSize', 'filterEnabled', 'maxVoices',
    'libVersion', 'sampleRate', 'buildTimeStamp', 'checkedVersion']
    >>> print(midi.config['numChannels'], midi.config['sampleRate'])
    2, 22050
    >>> midi.reverb = 'large hall' # Enable reverb effect
    >>> midi.write_short(0x90, 60, 127) # On middle C note with maximum velocity
    >>> import time ; time.sleep(2)
    >>> midi.write_short(0x80, 60, 127) # Off middle C note with maximum velocity
    >>> midi.reverb = None # Disable reverb effect


 Format of saved "example.raw" depends on system MIDI configuration.
 This example output could be lately converted to MP3 with avconv::

   avconv -f s16le -ac 2 -ar 22050 -i example.raw example.mp3
