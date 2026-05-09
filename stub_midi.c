/*
 * Stub MidiDriver library for local development and tests.
 *
 * Build with:
 *   gcc -shared -fPIC stub_midi.c -o libmidi.so
 *
 * Run Python with LD_LIBRARY_PATH pointing at the directory containing
 * libmidi.so so midistream.mididriver can load it with ctypes.
 */
#include <stdint.h>
#include <stdio.h>

typedef uint8_t EAS_U8;
typedef uint32_t EAS_U32;
typedef int32_t EAS_I32;
typedef uint32_t EAS_BOOL;
typedef char EAS_CHAR;

typedef struct {
    EAS_U32 libVersion;
    EAS_BOOL checkedVersion;
    EAS_I32 maxVoices;
    EAS_I32 numChannels;
    EAS_I32 sampleRate;
    EAS_I32 mixBufferSize;
    EAS_BOOL filterEnabled;
    EAS_U32 buildTimeStamp;
    EAS_CHAR *buildGUID;
} S_EAS_LIB_CONFIG;

static S_EAS_LIB_CONFIG config = {
    .libVersion = 0xAABBCCDD,
    .checkedVersion = 1,
    .maxVoices = 64,
    .numChannels = 16,
    .sampleRate = 44100,
    .mixBufferSize = 256,
    .filterEnabled = 0,
    .buildTimeStamp = 0,
    .buildGUID = "stub-libmidi",
};

S_EAS_LIB_CONFIG *EAS_Config(void)
{
    puts("EAS_Config()");
    fflush(stdout);
    return &config;
}

EAS_U8 midi_init(void)
{
    puts("midi_init()");
    fflush(stdout);
    return 1;
}

EAS_U8 midi_shutdown(void)
{
    puts("midi_shutdown()");
    fflush(stdout);
    return 1;
}

EAS_U8 midi_write(EAS_U8 *bytes, EAS_I32 length)
{
    printf("midi_write length=%d bytes=", length);
    for (EAS_I32 i = 0; i < length; i++) {
        printf("%02X ", bytes[i]);
    }
    putchar('\n');
    fflush(stdout);
    return 1;
}

EAS_U8 midi_setVolume(EAS_I32 volume)
{
    printf("midi_setVolume(%d)\n", volume);
    fflush(stdout);
    return 1;
}

EAS_U8 midi_setReverb(EAS_I32 preset)
{
    printf("midi_setReverb(%d)\n", preset);
    fflush(stdout);
    return 1;
}
