import tkinter as tk
import tkinter.ttk as ttk
import test as t
from tkinter.messagebox import showerror
from platform import system
import focused


class StudentTestEntry(object):
    def __init__(self, master, test: t.Test):
        self.master = master
        self.Evar = tk.StringVar(master, value=str(test.result[0]))
        self.Eentry = ttk.Entry(master, textvariable=self.Evar, width=3)
        self.Eentry.icursor(tk.END)
        self.Eentry.bind('<FocusOut>', lambda e: self.point_entry_callback(e, self.Eentry))

        self.Cvar = tk.StringVar(master, value=str(test.result[1]))
        self.Centry = ttk.Entry(master, textvariable=self.Cvar, width=3)
        self.Centry.icursor(tk.END)
        self.Centry.bind('<FocusOut>', lambda e:self.point_entry_callback(e,self.Centry))

        self.Avar = tk.StringVar(master, value=str(test.result[2]))
        self.Aentry = ttk.Entry(master, textvariable=self.Avar, width=3)
        self.Aentry.icursor(tk.END)
        self.Aentry.bind('<FocusOut>', lambda e:self.point_entry_callback(e,self.Aentry))

        self.sumvar = tk.StringVar(master, value=str(test.sum_result()))
        self.sumentry = ttk.Entry(master, textvariable=self.sumvar, width=3)
        self.sumentry.config(state='readonly', takefocus=False)

        fnt = (None,12,'bold') if system() == 'Darwin' else (None,10,'bold')
        ttk.Style().configure('Grade.TEntry', fieldbackground='linen')
        self.gradevar = tk.StringVar(master, value=test.grade())
        st = 'Grade.TEntry' if test.standard else 'EditedGrade.TEntry'
        self.gradeentry = ttk.Entry(master, textvariable=self.gradevar, width=3, style=st, font=fnt)
        self.gradeentry.config(state='readonly', takefocus=False)

        self.test = test


    def point_entry_callback(self, e=None, widget=None):
        focused.FOCUSED = str(e.widget)
        E = -1
        C = -1
        A = -1

        orgE = str(self.test.result[0])
        orgC = str(self.test.result[1])
        orgA = str(self.test.result[2])

        valid = True
        try:
            E = int(self.Evar.get())
            self.test.result[0] = E
        except ValueError:
            self.Evar.set(str(self.test.result[0]))
            valid = False

        try:
            C = int(self.Cvar.get())
            self.test.result[1] = C
        except ValueError:
            self.Cvar.set(str(self.test.result[1]))
            valid = False

        try:
            A = int(self.Avar.get())
            self.test.result[2] = A
        except ValueError:
            self.Avar.set(str(self.test.result[2]))
            valid = False

        # check that points given do not exceed maximum for the test
        if E > self.test.max[0]:
            showerror('Ogiltiga poäng', 'Antalet givna E-poäng överstiger provets totala E-poäng.')
            self.Evar.set("0")
            valid = False
        elif C > self.test.max[1]:
            showerror('Ogiltiga poäng', 'Antalet givna C-poäng överstiger provets totala C-poäng.')
            self.Cvar.set("0")
            valid = False
        elif A > self.test.max[2]:
            showerror('Ogiltiga poäng', 'Antalet givna A-poäng överstiger provets totala A-poäng.')
            self.Avar.set("0")
            valid = False

        if valid:
            self.gradevar.set(self.test.grade())
            self.sumvar.set(str(self.test.sum_result()))


    def update_grade(self):
        self.gradevar.set(self.test.grade())


    def grid(self, row, startcol: int):
        self.Eentry.grid(row=row, column=startcol)
        self.Centry.grid(row=row, column=startcol + 1)
        self.Aentry.grid(row=row, column=startcol + 2)
        self.sumentry.grid(row=row, column=startcol + 3)
        self.gradeentry.grid(row=row, column=startcol + 4)


    def grid_forget(self):
        self.Eentry.grid_forget()
        self.Centry.grid_forget()
        self.Aentry.grid_forget()
        self.sumentry.grid_forget()
        self.gradeentry.grid_forget()


    def destroy(self):
        self.Eentry.destroy()
        self.Centry.destroy()
        self.Aentry.destroy()
        self.sumentry.destroy()
        self.gradeentry.destroy()
