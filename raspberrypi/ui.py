#-*- encoding:utf-8 -*-
from Tkinter import *

class Dialog(Toplevel):
    """
        custom model dialog window
    """
    def __init__(self, parent, title = None, geometry = None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        if geometry is None:
            self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))
        else:
            self.geometry(geometry)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx = 5, pady = 5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.initial_focus.focus_set()

        self.wait_window(self)

    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        box = Frame(self)

        w = Button(box, text = "OK", width = 10, command = self.ok, default = ACTIVE)
        w.pack(side = LEFT, padx = 5, pady = 5)
        w = Button(box, text = "Cancel", width = 10, command = self.cancel)
        w.pack(side = LEFT, padx = 5, pady = 5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    # standard button semantics
    def ok(self, event = None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event = None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        pass # override

class StatusBar(Frame):
    """
        Application status bar
    """
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd = 1, relief = SUNKEN, anchor = W)
        self.label.pack(fill = X)

    def set(self, format, *args):
        if len(args) > 0:
            self.label.config(text = format % args)
        else:
            self.label.config(text = format)
        self.label.update_idletasks()
        
    def clear(self):
        self.label.config(text = "")
        self.label.update_idletasks()

def center(win):
    """
        centers a tkinter window
        :param win: the root or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def moveWinPosition(win, x, y):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
