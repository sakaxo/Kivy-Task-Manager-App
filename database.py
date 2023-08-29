import sqlite3


class Database(	):
	"""	"""
	def __init__(self):
		self.conn = sqlite3.connect("sakaxo-task-database.db")
		self.cursor = self.conn.cursor()
		self.create_task_table()

	def create_task_table(self):
		'''Create db table and do nothing if table already exists'''

		self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(100) NOT NULL, due_date varchar(50) NOT NULL, due_time varchar(50) NOT NULL)")
		self.conn.commit()
		# self.conn.close()

	def create_task(self,task,due_date,due_time):
		'''create/save new task'''

		self.cursor.execute("INSERT INTO tasks(task, due_date, due_time) VALUES(?,?,?)",(task, due_date, due_time))
		self.conn.commit()
		# self.conn.close()

	def get_tasks(self):
		return self.cursor.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
		# self.conn.close()

	def delete_task(self,taskid):
		# try:
		self.cursor.execute("DELETE FROM tasks WHERE id=?",(taskid))
		self.conn.commit()
		# except Exception as e:
		# 	print(f"=========== {e} ==========")
		
		# self.conn.close()

	# def 


