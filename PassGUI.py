#! /usr/bin/python3

# This is the GUI to the PassPhrase program
# It's purpose is to show the users password information
# an an easy to read way. The GUI will be constructed in
# Tkinter.

from tkinter import *
from tkinter.ttk import *
import Passes

class App():

	def __init__(self, master):
		# Create a instance binding to master (root) window
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
		filemenu.add_command(label='Import', command=self.placeholder)
		filemenu.add_separator()
		filemenu.add_command(label='Exit', command=self.placeholder)
		menubar.add_cascade(menu=filemenu, label='File')
		editmenu = Menu(menubar)
		editmenu.add_command(label='Add', command=self.AddPassBox)
		editmenu.add_command(label='Remove', command=self.placeholder)
		editmenu.add_command(label='Modify', command=self.placeholder)
		menubar.add_cascade(menu=editmenu, label='Edit')
		helpmenu = Menu(menubar)
		helpmenu.add_command(label='Help', command=self.placeholder)
		menubar.add_cascade(menu=helpmenu, label='Help')

		# Treeview widget
		self.tree = Treeview(self.mainframe)
		self.tree.grid(row=0, column=0, sticky=(N,E,S,W))
		self.tree.column('#0', width=90, minwidth=50, anchor='center')
		self.tree.heading('#0', text='Service')
		tcolumns = ('Login', 'Password', 'Answer1', 'Answer2', 'Answer3',
			'Answer4', 'Answer5', 'Modified')
		self.tree['columns'] = tcolumns
		for colname in tcolumns:
			self.tree.column(colname, width=90, minwidth=50, anchor='center')
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

		# Instantiate password data. (Not really gui related)
		self.PassData = Passes.Phrase()
			

	def AddPassBox(self):
		# GUI for adding a service and related password info to program
		PassBox = Toplevel(self.master)
		# Create list for getting args from PassBox
		fields = ['Service', 'Login', 'Password', 'Answer 1', 'Answer 2', 'Answer 3',
			'Answer 4', 'Answer 5']
		self.ndata = [1, 2, 3, 4, 5, 6, 7, 8]
		for index in range(0, 8):
			self.ndata[index] = StringVar()
			Label(PassBox, text=fields[index]).grid(column=0, row=index)
			Entry(PassBox, textvariable=self.ndata[index]).grid(column=1, row=index)
		butframe = Frame(PassBox); butframe.grid(column=1, row=8, sticky=EW)
		Button(butframe, text='Ok', command=lambda: self.AddPass(PassBox)).grid(column=0, row=0, sticky=EW)
		Button(butframe, text='Cancel', command=lambda: PassBox.destroy()).grid(column=1, row=0, sticky=EW)

	def AddPass(self, Caller):
		data = []
		for field in self.ndata:
			data.append(field.get())

		self.PassData.Add(data[0], data[1], data[2], data[3], data[4], data[5], data [6], data[7])
		self.tree.insert('', 'end', text=data[0], values=(data[1], data[2], data[3], data[4],
			data[5], data[6], data[7]))
		Caller.destroy()


	def placeholder(self, *args):
		print ('This is a placeholder')

if __name__ == '__main__':
	# Instantiate GUI Stuff
	root = Tk()
	root.title('PassPhrase')
	app = App(root)
	root.mainloop()

