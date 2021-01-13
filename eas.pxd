cdef extern from "Python.h":
    object PyBytes_FromStringAndSize(char *, Py_ssize_t)
    char* PyBytes_AsString(object)

cdef extern:
    ctypedef long EAS_RESULT

    ctypedef unsigned long EAS_U32
    ctypedef long EAS_I32
    ctypedef unsigned EAS_BOOL
    ctypedef char EAS_CHAR
    ctypedef short EAS_PCM

    ctypedef struct S_EAS_LIB_CONFIG:
        EAS_U32 libVersion
        EAS_BOOL checkedVersion
        EAS_I32 maxVoices
        EAS_I32 numChannels
        EAS_I32 sampleRate
        EAS_I32 mixBufferSize
        EAS_BOOL filterEnabled
        EAS_U32 buildTimeStamp
        EAS_CHAR *buildGUID

    EAS_RESULT EAS_Init(void *ppEASData)
    EAS_RESULT EAS_Shutdown(void * pEASData)
    S_EAS_LIB_CONFIG *EAS_Config()
    EAS_RESULT EAS_OpenMIDIStream(void *pEASData, void *pStreamHandle, void *streamHandle)
    EAS_RESULT EAS_CloseMIDIStream(void *pEASData, void *midiHandle)
    EAS_RESULT EAS_WriteMIDIStream(void *pEASData, void *streamHandle, void *pBuffer, EAS_I32 count)
    EAS_RESULT EAS_Render(void * pEASData, void *pOut, EAS_I32 numRequested, EAS_I32 *pNumGenerated)
    EAS_RESULT EAS_SetParameter(void *pEASData, EAS_I32 module, EAS_I32 param, EAS_I32 value)
