API
---

.. py:module:: midistream

.. py:class:: Midi
                             
    MIDI rendering and playback thread

    .. py:attribute:: exception

        :class:`EASException` instance, None if no errors have occurred yet

    .. py:attribute:: config

        Syntesizer configuration dictionary

    .. py:attribute:: reverb

       Reverberation effect, could be set to:
         * "large hall"
         * "hall"
         * "chamber"
         * "room"
         * *None* - no effect

    .. py:method:: start()

        Start MIDI rendering and playback

    .. py:method:: stop()

        Stop MIDI rendering and playback

    .. py:method:: write_short(status, data1=None, data2=None)

        Write MIDI command to syntesizer stream

        :param status: Status byte
        :param data1: Optional data byte
        :param data2: Optional second data byte
        :raise EASException: error has occurred during processing of previous commands


.. py:class:: EASException
                      
    Syntesizer exception
