try:
    from kivy.utils import platform
except ImportError:
    pass
else:
    if platform == "android":
        from .midistream import EASException, Midi
        __all__ = [EASException, Midi]
