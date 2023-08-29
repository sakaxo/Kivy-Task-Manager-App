import kivy
kivy.require("2.1.0")
import webbrowser as web
from kivymd.app import MDApp
from datetime import datetime
from kivy.lang import Builder
from database import Database
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.pickers import MDDatePicker, MDTimePicker

from kivy.properties import StringProperty

db = Database()

Window.size = (350, 550)
Builder.load_file('design.kv')



class RefreshMainWindow(Screen):
	""" This an empty screen widget which does nothing.
		I added it as a way to help me refresh my main 
		window(MainWindow class) anytime an item is deleted.
		
		The main window screen does not refresh when an item is
		deleted, so in the method that deletes an item I first of
		all change the screen to this RefreshMainWindow class which
		is a screen and then in the same method change the screen
		to the main screen.
		
		I understand this approach is not the right way to do this
		but hmmmmm, this also works. I think kivy recycleview will
		do but it wasn't working when I tried it.
	
	"""
	pass 


class AddNewTaskWindow(Screen):
	"""Screen for creating tasks"""
	def on_pre_enter(self):
		# clear textfields
		self.ids.task_input.text = ""
		self.ids.date.text = ""
		self.ids.time.text = "Set time"

	def show_main_window(self):
		'''switch from this app screen to main application screen'''

		self.manager.transition.direction = 'left'
		self.manager.current = 'mainwindow'


	def on_save(self, instance, value, date_range):
		'''update date text field when date is saved(ok button pressed)'''

		yy, mm, dd  = str(value).split('-')
		self.ids.date.text = f"{yy}/{mm}/{dd}"


	def on_cancel(self, instance, value):
		'''Do nothing when date dialog is cancel(cancel button pressed)'''
		pass


	def show_date_picker(self):
		'''show date picker dialog'''

		date_picker = MDDatePicker(
			title_input="Input Due Date",
			title="Select Due Date",
			)

		date_picker.bind(on_save=self.on_save, on_cancel=self.on_cancel)
		date_picker.open() #open date dialog


	def get_time(self, instance, time):
		time = str(time).split(':') #(h, m, s)
		self.ids.time.text = f"{time[0]}:{time[1]}" 

	def show_time_picker(self):
		'''show time picker dialog'''
		now = datetime.now()
		time_now = datetime.strptime(now.strftime('%H:%M'), '%H:%M').time()
		time_dialog = MDTimePicker()
		time_dialog.set_time(time_now) #set time to current time
		time_dialog.bind(time=self.get_time)
		time_dialog.open() #open time dialog

	def reset_time(self):
		self.ids.time.text = "Reset time"

	def save_task(self):
		success = True # flag to save task in db
		task = self.ids.task_input
		date = self.ids.date
		due_time = self.ids.time
		
		if task.text == "":
			task.error = True
			task.helper_text_mode: "persistent"
			task.helper_text = "Provide task"
			success = False

		if date.text != "": 
			# yyyy/mm/dd
			# validate date in before save, use regex
			validated = True
			if validated:
				success = True
			else:
				date.error = True 
				success = False

		if due_time.text != "":
			t = due_time.text.split(":")
			try:
				if int(t[0]) > 12:
					# time is pm
					due_time.text = f"{int(t[0])-12}:{t[1]} pm"
				else:
					# time is am
					due_time.text = due_time.text + " am"

			except ValueError :
				due_time.text = ""
				
			


		if success:
			if due_time.text == "Reset time" or due_time.text == "Set time":
				due_time.text = ""

			db.create_task(task=task.text, due_date=date.text, due_time=due_time.text) #task,due_date,due_time
			self.manager.transition.direction = 'left'
			self.manager.current = 'mainwindow'

			



class BuyMeCoffeeDialogContent(MDBoxLayout):
	"""Buy me coffee dialog content"""

	def buy_coffee_now(self):
		# print(f"Email: {self.ids.email.text}")
		# print(f"Phone: {self.ids.phone.text}")
		# print(f"Amount: {self.ids.amount.text}")

		self.ids.email.text = ''
		self.ids.phone.text = ''
		self.ids.amount.text = ''


class BuyMeCoffeeDialog(MDBoxLayout):
	"""Buy me coffee dialog"""

	def __init__(self, **kwargs):
		super(BuyMeCoffeeDialog, self).__init__(**kwargs)

		self.dialog = MDDialog(
			title ="Buy me a coffee?",
			type ="custom",
			content_cls = BuyMeCoffeeDialogContent(),
			)

		self.dialog.open()



class AboutToDoApp(Screen):
	app_description = StringProperty("")
	msg = "Version 1.0.0 of the TaskManager app. It allows you to create a task and delete when done. "
	msg = msg + "More features will be added in future release.\n\nSupport me by following me on social media,"
	msg = msg + " you can also support by sending me some few dollars or cedis on +233-559-037-977.\n\n"
	msg = msg + "Click on the three vertical dots on the home screen to follow me on social media.\n\n"
	msg = msg + "Contact me over social media to hire me."
	app_description = msg
	

class MainWindow(Screen):
	"""Handle design in kv file and logic here"""
	def direct_to_about_app_screen(self):
		# Direct to the about screen of the app
		self.manager.transition.direction = 'right'
		self.manager.current = "about_app"


	def open_media_link_in_browser(self, media_type=None):
		if media_type != None:

			if media_type == 'l':
				web.open("https://www.linkedin.com/in/sakaxo/")

			elif media_type == 'f':
				web.open("https://web.facebook.com/sakax0/")

			elif media_type == 't':
				web.open("https://twitter.com/sakaxo_")

			else:
				web.open("https://www.instagram.com/sakaxo_")

	@property
	def share_app(self):
		# print("sharing now")
		pass 

	@property
	def send_feedback(self):
		# print("sending feedback now")
		pass 


	def show_buy_coffee_dialog(self):
		BuyMeCoffeeDialog()

	def show_add_task_window(self):
		self.manager.transition.direction = 'right'
		self.manager.current = 'addtask'
					

	def delete_task_id(self, instance):
		'''Delete task item with instance id (id of pressed button)'''
		db.delete_task(taskid=instance.id)
		self.manager.current = "refresh"
		self.manager.current = "mainwindow"
		
	
	def on_pre_enter(self):
		self.ids.container.clear_widgets() # clear previous  widgets before adding new one
		tasks = db.get_tasks()
		for task in tasks:
			print(task)
			box_root = MDBoxLayout(orientation="vertical",)
			box_root.add_widget(MDLabel(text= task[1], bold= True,))

			# both date and time empty
			if task[2] == "" and task[3]== "":
				box_root.add_widget(MDLabel(text="",))

			# date not empty but time is empty
			if task[2] != "" and task[3] == "":
				box_root.add_widget(MDLabel(text=task[2], markup=True,))

			# date empty but time is not
			if task[2] == "" and task[3] != "":
				box_root.add_widget(MDLabel(text=task[3], markup=True,))

			# date and time has value
			if task[2] != "" and task[3] != "": #[size=<size>][/size]
				box_root.add_widget(MDLabel(text=f"{task[2]} [color=556B2F] | [/color] {task[3]}", markup=True,))

			grid_root = MDGridLayout(cols=2,)
			grid_root.add_widget(box_root)

			btn = MDIconButton(
				id= str(task[0]),
				icon = "delete-outline",
				theme_icon_color = "Custom",
				icon_color = (1,0.1,0.2,0.8),
				)

			btn.bind(on_release= self.delete_task_id)
			grid_root.add_widget(btn)
				
			add_task = MDCard(
				size_hint= (0.9, None),
				height="70dp",
				pos_hint= {'center_x': 0.5},
				padding= ("20dp", "10dp", "10dp","10dp"),
				)

			add_task.add_widget(grid_root)
			self.ids.container.add_widget(add_task)


class ToDOApp(MDApp):
	"""ToDo application base class"""

	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "Blue"
		# self.theme_cls.primary_hue = "900"

		self.sm = ScreenManager()
		self.sm.add_widget(MainWindow(name="mainwindow"))
		self.sm.add_widget(AddNewTaskWindow(name="addtask"))
		self.sm.add_widget(RefreshMainWindow(name="refresh"))
		self.sm.add_widget(AboutToDoApp(name="about_app"))
		return self.sm
	

if __name__ == '__main__':
	ToDOApp().run()
	