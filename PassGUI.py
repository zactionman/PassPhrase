#! /usr/bin/python3

# This is the GUI to the PassPhrase program
# It's purpose is to show the users password information
# an an easy to read way. The GUI will be constructed in
# Tkinter.

from tkinter import *
from tkinter.ttk import *

class App():

	def __init__(self, master):
		self.master = master

		# Main content frame
		self.mainframe = Frame(master)
		self.mainframe.grid()


		# Make Menus
		root.option_add('*tearOff', FALSE)
		menubar = Menu(master)
		master['menu'] = menubar
		filemenu = Menu(menubar)
		filemenu.add_command(label='Save', command=self.placeholder)
		filemenu.add_command(label='Exit', command=self.placeholder)
		menubar.add_cascade(menu=filemenu, label='File')
		editmenu = Menu(menubar)
		editmenu.add_command(label='Add', command=self.placeholder)
		editmenu.add_command(label='Remove', command=self.placeholder)
		editmenu.add_command(label='Modify', command=self.placeholder)
		menubar.add_cascade(menu=editmenu, label='Edit')
		helpmenu = Menu(menubar)
		helpmenu.add_command(label='Help', command=self.placeholder)
		menubar.add_cascade(menu=helpmenu, label='Help')

		# Treeview widget
		self.tree = Treeview(self.mainframe)
		self.tree.grid()
		self.tree.column('#0', width=80)
		self.tree.heading('#0', text='Service')
		tcolumns = ('Login', 'Password', 'Answer1', 'Answer2', 'Answer3',
			'Answer4', 'Answer5', 'Modified')
		self.tree['columns'] = tcolumns
		for colname in tcolumns:
			self.tree.column(colname, width=80)
			self.tree.heading(colname, text=colname)
			

	def placeholder(self, *args):
		print ('This is a placeholder')

root = Tk()
root.title('PassPhrase')
app = App(root)
root.mainloop()
