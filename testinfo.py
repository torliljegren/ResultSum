import tkinter as tk
import tkinter.ttk as ttk
from platform import system

class TestInfo(object):
    def __init__(self, master):
        if system() != 'Darwin':
            labelstyle = 'Content.TLabel'
        else:
            labelstyle = None

        self.Elabel = ttk.Label(master, text='E', style=labelstyle)
        self.Clabel = ttk.Label(master, text='C', style=labelstyle)
        self.Alabel = ttk.Label(master, text='A', style=labelstyle)
        self.sumlabel = ttk.Label(master, text='Σ', style=labelstyle)
        self.gradelabel = ttk.Label(master, text='omd', style=labelstyle)

    def grid(self, row: int, startcol: int):
        self.Elabel.grid(row=row, column=startcol)
        self.Clabel.grid(row=row, column=startcol + 1)
        self.Alabel.grid(row=row, column=startcol + 2)
        self.sumlabel.grid(row=row, column=startcol + 3)
        self.gradelabel.grid(row=row, column=startcol + 4)

    def destroy(self):
        self.Elabel.destroy()
        self.Clabel.destroy()
        self.Alabel.destroy()
        self.sumlabel.destroy()
        self.gradelabel.destroy()
