import logging
import os 

import re
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.button import Button

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '300')

class LoginScreen(FloatLayout):

	def __init__(self, **kwargs):
		super(LoginScreen, self).__init__(**kwargs)

		logging.info(os.getcwd())
		logging.info(os.listdir())

		logging.info(os.listdir('./images'))

		self.logo_path = './images/icon-256.png'
		self.logo = Image(source=self.logo_path)

		self.layout = BoxLayout(orientation='vertical', padding=(15,15))
		self.layout.add_widget(self.logo)

		self.data_layout = GridLayout(padding=(20,10))
		self.data_layout.cols = 2
		self.data_layout.add_widget(Label(text='Email address: '))
		self.data_layout.email = TextInput(multiline=False)
		self.data_layout.email.bind(on_text_validate=self.validate_email)

		self.data_layout.add_widget(self.data_layout.email)
		self.data_layout.add_widget(Label(text='Password: '))
		self.data_layout.password = TextInput(multiline=False, password=True)
		self.data_layout.add_widget(self.data_layout.password)

		self.layout.add_widget(self.data_layout)

		submit_buttom = Button(text='Sign In', on_press=self.sign_in)
		self.layout.add_widget(submit_buttom)

		self.add_widget(self.layout)


	def sign_in(self, instance):
		if self.validate_email(self.data_layout.email):
			self.email = self.data_layout.email.text
			self.password = self.data_layout.password.text
			logging.info(self.email)
			logging.info(self.password)

	def show_error(self, msg):
		error_layout = BoxLayout(orientation='vertical')
		error_msg_label = Label(text=msg)
		error_layout.add_widget(error_msg_label)
		self.layout.add_widget(error_layout)


	def validate_email(self, instance):
		logging.info(instance.text)

		if is_email(instance.text):
			logging.info('Is an email')
			return True
		logging.info('Not an email')
		self.show_error('Invalid email. Try again')
		return False


def is_email(text):
	'''
	Uses Regex to verify that the text is an email address
	'''
	email_re = re.compile(r'[a-zA-Z0-9]+[@][a-zA-Z0-9]+[\.][a-z]')
	if email_re.match(text):
		return True
	return False

class MyApp(App):
	def build(self):
		return LoginScreen()

if __name__=='__main__':
	MyApp().run()

