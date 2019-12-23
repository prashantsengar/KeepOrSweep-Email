import logging
import os 
import threading
import imaplib

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
		self.initialize_login_screen()

	def initialize_login_screen(self):
		self.logo_path = './images/icon-256.png'
		self.logo = Image(source=self.logo_path)

		self.layout = BoxLayout(orientation='vertical', padding=(15,15))
		self.layout.add_widget(self.logo)

		self.data_layout = GridLayout(padding=(20,10))
		self.data_layout.cols = 2
		self.data_layout.add_widget(Label(text='Email address: '))
		self.data_layout.email = TextInput(multiline=False)

		self.data_layout.add_widget(self.data_layout.email)
		self.data_layout.add_widget(Label(text='Password: '))
		self.data_layout.password = TextInput(multiline=False, password=True)
		self.data_layout.add_widget(self.data_layout.password)

		self.layout.add_widget(self.data_layout)

		submit_buttom = Button(text='Sign In', on_press=self.on_sign_in)
		self.layout.add_widget(submit_buttom)

		self.add_widget(self.layout)

	def clear_screen(self):
		self.remove_widget(self.layout)

	def show_loading(self):
		self.clear_screen()
		self.loading_image = Image(source='./images/loading.gif')
		self.layout = BoxLayout()
		self.layout.add_widget(self.loading_image)
		self.add_widget(self.layout)


	def on_sign_in(self, instance):
		if is_email(self.data_layout.email.text):
			email = self.data_layout.email.text
			password = self.data_layout.password.text
			self.show_loading()
			sign_in_thread = threading.Thread(target=sign_in_util, args=(self, email, password,))
			sign_in_thread.start()

			logging.info(email)
			logging.info(password)
		else:
			self.clear_screen()
			self.initialize_login_screen()
			self.show_error('Invalid email. Try again')


	def show_error(self, msg):
		self.clear_screen()
		self.initialize_login_screen()
		error_layout = BoxLayout(orientation='vertical')
		error_msg_label = Label(text=msg)
		error_layout.add_widget(error_msg_label)
		self.layout.add_widget(error_layout)



def sign_in_util(instance, email, password):
	server = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	try:
		server.login(email, password)
	except imaplib.IMAP4.error as e:
		logging.error(e)
		# logging.error(e.__str__)
		instance.show_error('Invalid email/password combination. Try again')
		return
	server.select('Inbox')
	typ, data = server.search(None, 'ALL')
	for i in range(5):
		print(data[i])

	
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

