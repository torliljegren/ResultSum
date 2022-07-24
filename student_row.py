import student as st
import student_test_entry as ste
from tkinter import StringVar, END
from tkinter.ttk import Entry, Label
import focused
import sumwin

class StudentRow(object):
    def __init__(self, master, row: int, student: st.Student, test_entries: tuple[ste.StudentTestEntry]):
        self.master = master
        self.row = row
        self.student = student
        self.test_entries : list[ste.StudentTestEntry] = list(test_entries)

        self.namevar = StringVar(master, value=student.name)
        self.nameentry = Entry(master, textvariable=self.namevar)
        # print('created', self.student.name, 'on row', row, 'with tests:')
        # print(*self.student.tests)
        self.nameentry.bind('<FocusOut>', self.nameentry_callback)
        self.nameentry.icursor(END)

        self.var_percentE = StringVar(master=self.master)
        self.entry_percentE = Entry(master=master, textvariable=self.var_percentE, width=4, takefocus=False)

        self.var_percentC = StringVar(master=self.master)
        self.entry_percentC = Entry(master=master, textvariable=self.var_percentC, width=4, takefocus=False)

        self.var_percentA = StringVar(master=self.master)
        self.entry_percentA = Entry(master=master, textvariable=self.var_percentA, width=4, takefocus=False)

        self.var_percentTOT = StringVar(master=self.master)
        self.entry_percentTOT = Entry(master=master, textvariable=self.var_percentTOT, width=4, takefocus=False)

        self.var_row = StringVar(master=self.master, value='[#'+str(self.row-1)+']')
        self.label_row = Label(master=self.master, textvariable=self.var_row, style='Content.TLabel')

    def bind_up_down(self, win: 'sumwin.SumWin'):
        self.nameentry.bind('<Up>', win.up_keypress)
        self.nameentry.bind('<Down>', win.down_keypress)
        self.nameentry.bind('<Shift-Return>', win.shift_return_keypress)
        self.nameentry.bind('<Return>', win.return_keypress)

        for entry in self.test_entries:
            entry.Eentry.bind('<Up>', win.up_keypress)
            entry.Eentry.bind('<Down>', win.down_keypress)
            entry.Eentry.bind('<Return>', win.return_keypress)
            entry.Eentry.bind('<Shift-Return>', win.shift_return_keypress)

            entry.Centry.bind('<Up>', win.up_keypress)
            entry.Centry.bind('<Down>', win.down_keypress)
            entry.Centry.bind('<Return>', win.return_keypress)
            entry.Centry.bind('<Shift-Return>', win.shift_return_keypress)

            entry.Aentry.bind('<Up>', win.up_keypress)
            entry.Aentry.bind('<Down>', win.down_keypress)
            entry.Aentry.bind('<Return>', win.return_keypress)
            entry.Aentry.bind('<Shift-Return>', win.shift_return_keypress)

            self.label_row.bind('<Button-1>', win.index_number_clicked)

    def nameentry_callback(self, e):
        focused.FOCUSED = str(self.test_entries[0].Eentry)

    def update_sums(self):
        for entry in self.test_entries:
            entry.update_sum()

    def update_grades(self):
        for entry in self.test_entries:
            entry.update_grade()

    def update_grades_and_sums(self):
        for entry in self.test_entries:
            entry.update_sum()
            entry.update_grade()

    def grid(self, row: int, startcolumn: int):
        self.nameentry.grid(row=row, column=startcolumn)
        entrycounter = startcolumn
        for entry in self.test_entries:
            entry.grid(row=row, startcol=entrycounter*5 + 1)
            entrycounter += 1

        self.entry_percentE.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 1)
        self.entry_percentC.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 2)
        self.entry_percentA.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 3)
        self.entry_percentTOT.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 4)
        self.label_row.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 5)


    def update_model_from_gui(self):
        self.student.name = self.namevar.get()
        testindex = 0
        for entry in self.test_entries:
            entry.test.result[0] = int(entry.Evar.get())
            entry.test.result[1] = int(entry.Cvar.get())
            entry.test.result[2] = int(entry.Avar.get())
            self.student.tests[testindex] = entry.test
            testindex += 1


    def grid_forget(self):
        for entry in self.test_entries:
            entry.grid_forget()

        self.entry_percentE.grid_forget()
        self.entry_percentC.grid_forget()
        self.entry_percentA.grid_forget()
        self.entry_percentTOT.grid()

    def clear_entries(self):
        self.namevar.set('')
        for entry in self.test_entries:
            entry.clear_entries()


    def destroy(self):
        self.nameentry.destroy()
        for entry in self.test_entries:
            entry.destroy()

        self.entry_percentE.destroy()
        self.entry_percentC.destroy()
        self.entry_percentA.destroy()
        self.entry_percentTOT.destroy()
