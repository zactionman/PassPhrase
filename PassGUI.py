#! /usr/bin/python3

# This is the GUI to the PassPhrase program
# It's purpose is to show the users password information
# an an easy to read way. The GUI will be constructed in
# Tkinter.

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox as mbox
from tkinter import filedialog as fbox
import Passes

class App():
    """An object containing all the specifications for the Tkinter GUI"""


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
        # File Menu
        filemenu = Menu(menubar)
        filemenu.add_command(label='Save', command=self.GetEncr)
        filemenu.add_command(label='Import', command=self.ImExBox)
        filemenu.add_command(label='Export', command=lambda: self.ImExBox('Export'))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.Exit)
        menubar.add_cascade(menu=filemenu, label='File')
        # Edit Menu
        editmenu = Menu(menubar)
        editmenu.add_command(label='Copy', command=self.CopyPass)
        editmenu.add_command(label='Find', command=self.FindBox)
        editmenu.add_separator()
        editmenu.add_command(label='Add', command=self.AddPassBox)
        editmenu.add_command(label='Remove', command=self.RemPass)
        editmenu.add_command(label='Modify', command=self.ModPassBox)
        menubar.add_cascade(menu=editmenu, label='Edit')
        # Help Menu
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
        # Dictionary of tree item/text values
        self.treedict = {}

        # Scrollbars
        self.vscroll = Scrollbar(self.mainframe, orient=VERTICAL, command=self.tree.yview)
        self.xscroll = Scrollbar(self.mainframe, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.xscroll.set)
        self.vscroll.grid(row=0, column=1, sticky=(N,S,W))
        self.xscroll.grid(row=2, column=0, sticky=(N,E,W))

        # Sizegrip
        Sizegrip(self.mainframe).grid(row=2, column=1, sticky=(E,S))

        # Make resizeable
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        # Set protocol for when window is closed via window manager.
        # And set bindings
        master.protocol("WM_DELETE_WINDOW", self.Exit)
        master.bind("<Control-c>", lambda e: self.CopyPass())
        master.bind("<Control-f>", lambda e: self.FindBox())

        # Keep track of whether or not changes have been saved. (0=yes, 1=no)
        self.saved=0
        # Know whether find bar is open
        # Uses 1 for open 0 for closed
        self.findb='None'

        # Instantiate password data. (Not really gui related)
        self.PassData = Passes.Phrase()
        # Open data file if it exists
        if Passes.f.isfile(self.PassData.wfile) or Passes.f.isfile(self.PassData.wfile + '.enc'):
            self.GetEncr('open')    


    def AddPassBox(self):
        """Popup toplevel to get password/service info from user"""

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
        # Make buttons (grid them inside their own frame
        butframe = Frame(PassBox); butframe.grid(column=1, row=8, sticky=EW)
        b1 = Button(butframe, text='Ok', default='active', command=lambda: self.AddPass(PassBox))
        b1.grid(column=0, row=0, sticky=EW)
        Button(butframe, text='Cancel', command=lambda: PassBox.destroy()).grid(column=1, row=0, sticky=EW)
        # Bind the enter/return key to the 'Ok' button.
        PassBox.bind('<Return>', lambda e: b1.invoke())


    def AddPass(self, Caller):
        """Add user defined information to the program."""

        Caller.destroy()
        # Get all data needed from entry widgets
        data = []
        for field in self.ndata:
            data.append(field.get())

        # Insert data into underlying dict
        added = self.PassData.Add(data[0], data[1:])
        # Instert data into tree
        if added != None:
            item1 = self.tree.insert('', 'end', text=added[0], values=(tuple(added[1:])))
            self.treedict[added[0]] = item1
        # Mark that changes should be saved (should one exit before doing so)
        self.saved=1


    def RemPass(self):
        """Remove password data by getting selection from tree widget."""
        # Get the id's of selected nodes in tree.
        selection = self.tree.selection()
        # Get a list of service names
        remlist = [self.tree.item(serv, 'text') for serv in selection]
        # Remove stuff
        self.PassData.Remove(remlist)
        for serv, text in zip(selection, remlist):
            self.tree.delete(serv)
            del self.treedict[text]
        # Mark 'not saved'
        self.saved=1


    def ModPassBox(self):
        """Toplevel GUI for getting changes to a service from the user"""

        # Get currently selected item in tree
        selection = self.tree.selection()

        if len(selection) != 1:
            # Provide an error message if more or less than one item is selected
            self.Messages(0, "You must have exactly one item selected in the Tree")
        else:
            # Tuple containing the tree identification number and service name
            moditem = (selection[0], self.tree.item(selection[0], 'text'))

            # Create toplevel GUI
            ModBox = Toplevel(self.master)
            fields = ['Service', 'Login', 'Password', 'Answer1', 'Answer2', 
                    'Answer3', 'Answer4', 'Answer5']
            self.modata = [1, 2, 3, 4, 5, 6, 7]

            # Show which service is being modified in the topleve
            Label(ModBox, text=fields[0]).grid(row=0, column=0)
            Label(ModBox, text=moditem[1]).grid(row=0, column=1)

            for i in range(0, 7):
                # Build the Labels and Entry widgets for the toplevel
                self.modata[i] = StringVar()
                self.modata[i].set(self.PassData.Phrases[moditem[1]][i])
                Label(ModBox, text=fields[i+1]).grid(row=i+1, column=0)
                Entry(ModBox, textvariable=self.modata[i]).grid(
                      row=i+1, column=1)

            # Okay and Cancel button
            butframe = Frame(ModBox)
            butframe.grid(row=8, column=1, sticky='ew')
            b1 = Button(butframe, text='Ok', default='active',
                    command=lambda: self.ModPass(moditem, ModBox))
            b1.grid(row=0, column=0, sticky='ew')
            b2 = Button(butframe, text='Cancel',
                    command=lambda: ModBox.destroy())
            b2.grid(row=0, column=1, sticky='ew')

            # Bind Return to the Ok button (b1)
            ModBox.bind('<Return>', lambda e: b1.invoke())


    def ModPass(self, serv, caller):
        """Write out modified data to interal data structure and tree."""

        # Destroy toplevel widget
        caller.destroy()

        # Get the data from the entry widgets
        newdata = []
        for item in self.modata:
            newdata.append(item.get())
        
        # Pass new data to the internal data structure
        newdata = self.PassData.Modify(serv[1], newdata)

        # If modify was succesful writeout new data to the tree widget
        if newdata != None:
            self.tree.item(serv[0], values=tuple(newdata))
            # Mark that save is needed
            self.saved=1
        else:
            Messages(0, 'Oops: This service did not exist')


    def CopyPass(self):
        """Copy an items Password to the clipboard"""

        # Get current selection!
        selitem = self.tree.selection()

        # Get password for currently selected item.
        selvalues = self.tree.item(selitem[0], 'values')
        
        # Write the password to the clipboard
        self.master.clipboard_clear()
        self.master.clipboard_append(selvalues[1])


    def FindBox(self):
        """Draw a find bar at the bottom of the window"""
        
        if self.findb == 0:
            # Re-grid findframe if it's off screen
            self.findframe.grid()
            self.findb = 1
        elif self.findb == 1:
            # Remove find box if it's already on screen
            self.findframe.grid_remove()
            self.findb = 0
        else:
            # Draw initial frame for search stuff at start of program and hide it
            self.findframe = Frame(self.mainframe, relief='sunken')
            self.findframe.grid(row=1, column=0, sticky='ew')

            # Entry widgets and buttons for findbar
            search = StringVar()
            Entry(self.findframe, textvariable=search).grid(
                row=0, column=0, sticky='ew')
            Button(self.findframe, text='Find',
                command=lambda: self.FindPass(search)).grid(row=0, column=1)
            Button(self.findframe, text='Next', command=self.placeholder).grid(
                row=0, column=2)
            Button(self.findframe, text='Close', command=self.FindBox
                ).grid(row=0, column=3, sticky=E)

            self.findframe.columnconfigure(0, weight=1)

            # Set findframe to open
            self.findb = 1


    def FindPass(self, search):
        """Get a string from the user and use it to search for services"""

        results = self.PassData.Find(search.get())
        if results != []:
            # If matches were found find their tkinter id's and select them
            select = [self.treedict[x] for x in results]
            self.tree.selection('set', tuple(select))
            # Show if off screen
            self.tree.see(select[0])


    def SavePass(self, ekey1, ekey2, caller):
        """Get enccryption key and pass it to the save method of Passes.Phrase.
        
        SavePass is called by the GetEncr GUI which expects the user to type in an 
        encryption key. If SavePass is called with an empty encryption key it calls the
        Save method without providing a key for encryption - essentailly bypassing
        encryption alltogether.

        If SavePass is provided one (or two) non-empty encryption keys it first verifies
        that both encryption keys match and then passes the encryption key to the save
        method.
        """

        caller.destroy()
        if ekey1 == ekey2 and len(ekey1) > 0:
            self.PassData.Save(self.PassData.Phrases, self.PassData.wfile, ekey1)
            self.saved=0
        elif ekey1 != ekey2 and len(ekey1) > 0:
            mbox.showinfo(message="Error: Key1 and Key2 don't match.  Please retype them.")
            self.GetEncr()
        else:
            self.Messages(1)
            self.PassData.Save(self.PassData.Phrases, self.PassData.wfile)
            self.saved=0


    def OpenPass(self, ekey, caller):
        """Pass an encryption key to the open method of the internal data class.

        OpenPass is called by GetEncr and passes the encryption key input by the user
        to the open method of the internal data structure.  If the encryption key is
        incorrect the internal data structure should detect this and return false.  If
        this happens then OpenPass will provide an error message to the user and ask
        her to re-type the encryption key.
        """

        caller.destroy()
        if len(ekey) > 0:
            success = self.PassData.Open(self.PassData.wfile, ekey)
        else:
            success = self.PassData.Open(self.PassData.wfile)

        if success:
            #print (self.PassData.Phrases['Services'])
            for service in self.PassData.Phrases['Services']:
                servdata = tuple(self.PassData.Phrases[service])
                item1 = self.tree.insert('', 'end', text=service, values=servdata)
                self.treedict[service] = item1 
        else:
            self.Messages(3)
            self.GetEncr('open')


    def GetEncr(self, etype='save'):
        """Draw a toplevel GUI for getting encryption keys from the user.
        
        If called with the option 'open' GetEncr will provide only one entry field
        of which it will pass the contents to OpenPass.  If called with 'save' option
        then GetEncr will provide two entry fields the contents of which will be
        passed to SavePass (this is the default behavoir if no argument is provided).
        """

        toplevel = Toplevel(self.master)
        templevel = Frame(toplevel, padding=6); templevel.grid()
        getkey1, getkey2 = StringVar(), StringVar()
        Label(templevel, text='Entery Key/Password', anchor='center').grid(
                row=0, column=0, columnspan=2, sticky='ew')
        Entry(templevel, textvariable=getkey1, show='*').grid(
                row=1, column=1, sticky='ew')
        Label(templevel, text='Key: ').grid(row=1, column=0, sticky='e')
        toplevel.lift(self.master)
        if etype == 'open':
            # Call OpenPass method if passed the 'open' argument
            toplevel.protocol("WM_DELETE_WINDOW", lambda: self.Messages(2, '', toplevel))
            b1 = Button(templevel, text='Ok', default='active', command=lambda: self.OpenPass(
                        getkey1.get(), toplevel))
            b1.grid(row=2, column=1, sticky='ew')
        else:
            # If not passed an argument get key for encryption and create a second
            # entry widget for passphrase matching
            Entry(templevel, textvariable=getkey2, show='*').grid(
                    row=2, column=1, sticky='ew')
            Label(templevel, text='Re-Type: ', anchor='w').grid(
                    row=2, column=0, sticky='e')
            b1 = Button(templevel, text='Ok', default='active', command=lambda: self.SavePass(
                        getkey1.get(), getkey2.get(), toplevel))
            b1.grid(row=3, column=1, sticky='ew')

        # Bind the enter/return key to the 'Ok' button
        toplevel.bind('<Return>', lambda e: b1.invoke())

        
    def ImExBox(self, whatdo='Import'):
        """Provide a Toplevel gui for getting a delimiter for importing and exporting."""

        delimiter = StringVar()
        exbox = Toplevel(self.master)
        Label(exbox, text='Type custom delimiter').grid(row=0, column=0, columnspan=2, sticky='ew')
        Entry(exbox, textvariable=delimiter).grid(row=1, column=0, columnspan=2, sticky='ew')
        if whatdo == 'Export':
            # If passed 'Export' send the delimiter to the ExportPass method
            b1 = Button(exbox, text='Ok', default='active', command=lambda: self.ExportPass(delimiter.get(), exbox))
            b1.grid(row=2, column=0, sticky='ew')
        else:
            # If passed 'Import' send the delimiter to the ImportPass method (default).
            b1 = Button(exbox, text='Ok', default='active', command=lambda: self.ImportPass(delimiter.get(), exbox))
            b1.grid(row=2, column=0, sticky='ew')
        Button(exbox, text='Cancel', command=lambda: exbox.destroy()).grid(row=2, column=1, sticky='ew')
        exbox.bind('<Return>', lambda e: b1.invoke())


    def ImportPass(self, delim, caller):
        """Get a filename and pass it and a delimiter to Passes.Phrase.Import."""

        # Function to import data from text file
        caller.destroy()
        filname = fbox.askopenfilename()
        if filname != ():
            if len(delim) == 0:
                imported = self.PassData.Import(filname)
            else:
                imported = self.PassData.Import(filname, delim)
            for serv in imported:
                vals = tuple(self.PassData.Phrases[serv])
                self.tree.insert('', 'end', text=serv, values=vals)
                self.saved=1
            mbox.showinfo(message='Import Complete')
        else:
            mbox.showinfo(message='No filename provided - import not executed.')


    def ExportPass(self, delim, caller):
        """Get a filename and pass it and a delimiter to Passes.Phrase.Export."""

        # Function to export data to text file
        caller.destroy()
        filname = fbox.asksaveasfilename()
        if filname != ():
            if len(delim) == 0:
                self.PassData.Export(filname)
            else:
                self.PassData.Export(filname, delim)
        else:
            print ('filename box cancelled')

    
    def Exit(self):
        if self.saved == 0:
            self.master.destroy()
        else:
            cont = mbox.askyesno(
                message='Warning: Current changes not saved. Do you wish to Continue?',
                icon='warning', title='Exit')
            if cont:
                self.master.destroy()


    def Messages(self, messnum, mess='', caller=None):
        """Provide info/warning messages to the user when needed."""

        # A place for prebuilt messages that can be called. Or a way to build custom messages.
        if messnum == 0:
            mbox.showinfo(message=mess)
        elif messnum == 1:
            mbox.showinfo(message="Warning: no encryption key provided.  Not encrypting passwords file")
        elif messnum == 2:
            answer = mbox.askokcancel(message="""Warning: Open window closed.
This will cause PassPhrase to make a new password data file and, if saved, will overwrite any previously saved data""")
            if answer == True:
                caller.destroy()
            else:
                pass
        elif messnum == 3:
            mbox.showinfo(message="Failure opening or decrypting data file.  Please retype encryption key")
        else:
            print ('Please pass a valid message argument')


    def placeholder(self, *args):
        print ('This is a placeholder')


if __name__ == '__main__':
    # Instantiate GUI Stuff
    root = Tk()
    root.title('PassPhrase')
    app = App(root)
    root.mainloop()

