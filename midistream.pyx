from eas cimport *
import threading
import Queue
from jnius import autoclass
from audiostream import get_output, AudioSample
from contextlib import contextmanager


class EASException(Exception):

    def __init__(self, eas_function, result, **function_kwargs):
        message = "{} return error: {}.".format(
            eas_function, result)
        if function_kwargs:
            message += ' Arguments: {}'.format(function_kwargs)
        super(EASException, self).__init__(message)


include "eas.pxi"

class Midi(threading.Thread, EAS):

    def __init__(self):
        super(Midi, self).__init__()
        self.daemon = True
        self._stop_thread = threading.Event()
        self._exit_thread = threading.Event()
        self.commands = Queue.Queue()
        self.eas = None
        self._exception = None
        self.lock = threading.RLock()

    @property
    def exception(self):
        return self._exception

    @property
    def config(self):
        if self.eas and not self._exception:
            return self.eas.config

    def write_short(self, status, data1=None, data2=None):
        if self._exception:
            raise self._exception
        self.commands.put((status, data1, data2))

    def run(self):
        self.eas = EAS()

        with self._eas_call():
            self.eas.init()

        if self._stop_thread.isSet():
            return

        cfg = self.config
        stream = get_output(channels=cfg['numChannels'],
                            rate=cfg['sampleRate'],
                            encoding=16,
                            buffersize=self.eas.buffer_size)

        sample = AudioSample()
        stream.add_sample(sample)
        sample.play()

        with self._eas_call():
            self.eas.open_stream()

        while not self._stop_thread.isSet():
            self._execute_commands()
            with self._eas_call():
                self.eas.render(sample)

        if self.eas:
            with self._eas_call():
                self.eas.close_stream()
                self.eas.shutdown()
                sample.stop()

        self._exit_thread.wait()

    def stop(self):
        self._stop_thread.set()

    def _execute_commands(self):
        while not self._stop_thread.isSet():
            try:
                cmd = self.commands.get_nowait()
            except Queue.Empty:
                return
            else:
                with self._eas_call():
                    self.eas.write_command(*cmd)

    @contextmanager
    def _eas_call(self):
        try:
            yield self.eas
        except Exception as ex:
            self._stop_thread.set()
            self._exception = ex
