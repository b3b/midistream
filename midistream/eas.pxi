EAS_SUCCESS = 0

EAS_MODULE_REVERB = 2

(EAS_PARAM_REVERB_BYPASS,
 EAS_PARAM_REVERB_PRESET,
 EAS_PARAM_REVERB_WET,
 EAS_PARAM_REVERB_DRY) = range(4)

(EAS_PARAM_REVERB_LARGE_HALL,
 EAS_PARAM_REVERB_HALL,
 EAS_PARAM_REVERB_CHAMBER,
 EAS_PARAM_REVERB_ROOM) = range(4)

cdef class EAS:

    cdef:
       void *eas_handle
       void *eas_stream_handle

       EAS_U32 sample_size
       EAS_U32 eas_buffer_size_samples
       EAS_U32 num_buffers
       EAS_U32 out_buffer_size

       char *out
       bytes out_bytes
       object fout

    def __cinit__(self):
        self.num_buffers = 1

    @property
    def config(self):
        cdef S_EAS_LIB_CONFIG *pLibConfig
        pLibConfig = EAS_Config()
        return pLibConfig[0]

    @property
    def buffer_size(self):
        return self.out_buffer_size

    def init(self, output):
        cdef EAS_RESULT result
        result = EAS_Init(&self.eas_handle)
        if result != EAS_SUCCESS:
            raise EASException('EAS_INIT', result)
        cfg = self.config
        self.eas_buffer_size_samples = cfg['mixBufferSize']
        self.sample_size = cfg['numChannels'] * sizeof(EAS_PCM)
        self.out_buffer_size = self.eas_buffer_size_samples * self.sample_size * self.num_buffers
        self.fout = output

    def shutdown(self):
        EAS_Shutdown(self.eas_handle)

    def open_stream(self):
        cdef EAS_RESULT result
        cfg = self.config
        result = EAS_OpenMIDIStream(self.eas_handle,
                           &self.eas_stream_handle,
                           NULL)
        if result != EAS_SUCCESS:
            raise EASException('EAS_OpenMIDIStream',  result)
        self.out_bytes = PyBytes_FromStringAndSize(NULL,
                                                   self.out_buffer_size)
        self.out = PyBytes_AsString(self.out_bytes)

    def close_stream(self):
        cdef EAS_RESULT result
        result = EAS_CloseMIDIStream(self.eas_handle,
                                     self.eas_stream_handle)
        if result != EAS_SUCCESS:
            raise EASException('EAS_CloseMIDIStream',  result)

    def write_command(self, status, data1=None, data2=None):
        cdef:
            EAS_RESULT result
            unsigned char msg[3]
        msg[0] = status
        msg[1] = data1 or 0
        msg[2] = data2 or 0

        msg_len = 1
        if data1 is not None:
            msg_len += 1 + (data2 is not None)

        result = EAS_WriteMIDIStream(self.eas_handle, self.eas_stream_handle, msg, msg_len)
        if result != EAS_SUCCESS:
            raise EASException('EAS_WriteMIDIStream', result,
                               message_len=msg_len,
                               status=status,
                               data1=data1,
                               data2=data2)

    def set_parameter(self, module, parameter, value):
        result = EAS_SetParameter(self.eas_handle, module, parameter, value)
        if result != EAS_SUCCESS:
            raise EASException('EAS_SetParameter', result,
                               module=module, parameter=parameter, value=value)

    def render(self, sample):
        cdef:
            EAS_I32 count
            EAS_RESULT result
        result = EAS_Render(self.eas_handle, self.out, self.eas_buffer_size_samples, &count)
        if result != EAS_SUCCESS:
            raise EASException('EAS_Render', result,
                               numRequested=self.eas_buffer_size_samples)
        out_len = count * self.sample_size
        if out_len < self.out_buffer_size:
            sample.write(self.out_bytes[:out_len])
            if self.fout:
                self.fout.write(self.out_bytes[:out_len])
        else:
            sample.write(self.out_bytes)
            if self.fout:
                self.fout.write(self.out_bytes)
        return out_len
