cdef extern:
    ctypedef long EAS_RESULT
    ctypedef unsigned char EAS_U8
    ctypedef unsigned long EAS_U32
    ctypedef long EAS_I32
    ctypedef unsigned EAS_BOOL
    ctypedef char EAS_CHAR
    ctypedef short EAS_PCM

    ctypedef struct S_EAS_LIB_CONFIG:
        EAS_U32 libVersion
        EAS_BOOL checkedVersion
        EAS_I32 ma3xVoices
        EAS_I32 numChannels
        EAS_I32 sampleRate
        EAS_I32 mixBufferSize
        EAS_BOOL filterEnabled
        EAS_U32 buildTimeStamp
        EAS_CHAR *buildGUID

    S_EAS_LIB_CONFIG *EAS_Config()

    # Bill Farmer MidiDriver methods
    EAS_U8 midi_init()
    EAS_U8 midi_shutdown()
    EAS_U8 midi_write(EAS_U8 *bytes, EAS_I32 length)
    EAS_U8 midi_setVolume(EAS_I32 volume)
