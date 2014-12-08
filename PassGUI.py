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
		self.mainframe.grid(sticky=(N,E,S,W))


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
		self.tree.grid(row=0, column=0, sticky=(N,E,S,W))
		self.tree.column('#0', width=100, minwidth=75)
		self.tree.heading('#0', text='Service')
		tcolumns = ('Login', 'Password', 'Answer1', 'Answer2', 'Answer3',
			'Answer4', 'Answer5', 'Modified')
		self.tree['columns'] = tcolumns
		for colname in tcolumns:
			self.tree.column(colname, width=100, minwidth=75)
			self.tree.heading(colname, text=colname)

		# Scrollbars
		self.vscroll = Scrollbar(self.mainframe, orient=VERTICAL, command=self.tree.yview)
		self.xscroll = Scrollbar(self.mainframe, orient=HORIZONTAL, command=self.tree.xview)
		self.tree.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.xscroll.set)
		self.vscroll.grid(row=0, column=1, sticky=(N,S,W))
		self.xscroll.grid(row=1, column=0, sticky=(N,E,W))

		# Sizegrip
		Sizegrip(self.mainframe).grid(row=1, column=1, sticky=(E,S))

		# Make resizeable
		master.columnconfigure(0, weight=1)
		master.rowconfigure(0, weight=1)
		self.mainframe.columnconfigure(0, weight=1)
		self.mainframe.rowconfigure(0, weight=1)
			

	def AddPassBox(self):
		# GUI for adding a service and related password info to program
		PassBox = Toplevel(self.master)

	
	def placeholder(self, *args):
		print ('This is a placeholder')

if __name__ == '__main__':
	root = Tk()
	root.title('PassPhrase')
	app = App(root)
	root.mainloop()
