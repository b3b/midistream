import os
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder

Builder.load_file(os.path.join(os.path.dirname(__file__), 'error_message.kv'))

class ErrorMessage(Popup):
    title = StringProperty('Bang!')
    message = StringProperty('')
