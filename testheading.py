from tkinter.ttk import Label
from tkinter import StringVar

class TestHeading(Label):
    def __init__(self, master, sumwin, textvariable:StringVar):
        super().__init__(master, textvariable=textvariable, style='TestHeading.TLabel')
        self.sumwin = sumwin
        self.textvariable = textvariable
        self.bind('<Button-1>', lambda e: self.sumwin.heading_click_callback(e, self))