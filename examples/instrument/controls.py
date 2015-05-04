import os
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder

Builder.load_file(os.path.join(os.path.dirname(__file__), 'controls.kv'))

class VelocitySlider(Slider):
    instrument = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(VelocitySlider, self).__init__(*args, **kwargs)

    def on_instrument(self, instance, value):
        self.value = self.instrument.velocity
        self.instrument.bind(velocity=self.on_instrument_velocity)
        self.bind(value=self.on_velocity)

    def on_instrument_velocity(self, instrument, value):
        if value != self.value:
            self.value = value

    def on_velocity(self, instance, value):
        if self.instrument.velocity != value:
            self.instrument.velocity = value

class ConfirmPopup(GridLayout):
    '''make popup yes no with kivy
    https://gist.github.com/rohman/5300469
    '''
    text = StringProperty()

    def __init__(self,**kwargs):
        self.register_event_type('on_answer')
        super(ConfirmPopup,self).__init__(**kwargs)

    def on_answer(self, *args):
        pass	

class ControlsLayout(BoxLayout):
    controls = ObjectProperty()
    edit_mode_controls = ObjectProperty()
    instrument = ObjectProperty()
    popup = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(ControlsLayout, self).__init__(*args, **kwargs)

        content = ConfirmPopup(text='Remove all the notes?')
        content.bind(on_answer=self.on_clear_confirmed)
        self.popup = Popup(title="Confirmation",
                      content=content,
                      size_hint=(None, None),
                      size=(480,400),
                      auto_dismiss=False)
        
    def switch_mode(self, edit):
        if edit:
            self.remove_widget(self.controls)
            self.add_widget(self.edit_mode_controls)
        else:
            self.remove_widget(self.edit_mode_controls)
            self.add_widget(self.controls)

    def confirm_clear(self):
        self.popup.open()

    def on_clear_confirmed(self, confirmation, answer):
        if answer == 'yes':
            self.instrument.clear_state()
        self.popup.dismiss()

