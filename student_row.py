from student import Student
from student_test_entry import StudentTestEntry
from tkinter import StringVar, END, PhotoImage
from tkinter.ttk import Entry, Label
import focused
import sumwin
# from sumwin import SumWin

class StudentRow(object):
    def __init__(self, master, row: int, student: Student, test_entries: tuple[StudentTestEntry]):
        self.master = master
        self.row = row
        self.student = student
        self.test_entries: list[StudentTestEntry] = list(test_entries)
        # pass self to each test entry to allow callback to update the student rows percentages
        for entry in self.test_entries:
            entry.student_row = self

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

        # this are replaced by two separate (i) and chart icons
        # self.var_row = StringVar(master=self.master, value='[#'+str(self.row-1)+']')
        # self.label_row = Label(master=self.master, textvariable=self.var_row, style='Content.TLabel')

        self.infoimage = PhotoImage(file='info.png', master=self.master, height=22)
        self.infolabel = Label(self.master, image=self.infoimage, style='Content.TLabel')

        self.stuchartimage = PhotoImage(file='stuchart.png', master=self.master, height=22)
        self.stuchartlabel = Label(self.master, image=self.stuchartimage, style='Content.TLabel')

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

            self.infolabel.bind('<Button-1>', win.infolabel_clicked)
            self.stuchartlabel.bind('<Button-1>', win.infolabel_clicked)

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

    def update_percent(self):
        valid = True
        # keep track of the tests total point sums
        Etot = 0
        Ctot = 0
        Atot = 0
        # keep track of the students point sums
        sumE = 0
        sumC = 0
        sumA = 0
        for entry in self.test_entries:
            try:
                sumE += int(entry.Evar.get())
                sumC += int(entry.Cvar.get())
                sumA += int(entry.Avar.get())
                if sumE + sumC + sumA > 0:  # only count the test if the student actually participated
                    Etot += entry.test.max[0]
                    Ctot += entry.test.max[1]
                    Atot += entry.test.max[2]
            except ValueError:
                valid = False
                break
        # print(f'calc_perc(): {sturow.namevar.get()} has Etot={Etot}, Ctot={Ctot}, Atot={Atot}')
        if valid:
            try:
                self.var_percentE.set(str(round(sumE / Etot * 100)) + '%')
            except ZeroDivisionError:
                self.var_percentE.set('?%')

            try:
                self.var_percentC.set(str(round(sumC / Ctot * 100)) + '%')
            except ZeroDivisionError:
                self.var_percentC.set('?%')

            try:
                self.var_percentA.set(str(round(sumA / Atot * 100)) + '%')
            except ZeroDivisionError:
                self.var_percentA.set('?%')

            try:
                self.var_percentTOT.set(str(round((sumE + sumC + sumA) / (Etot + Ctot + Atot) * 100)) + '%')
            except ZeroDivisionError:
                self.var_percentTOT.set('?%')
        else:
            self.var_percentE.set('-%')
            self.var_percentC.set('-%')
            self.var_percentA.set('-%')
            self.var_percentTOT.set('-%')

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
        # self.label_row.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 5)
        self.infolabel.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 5)
        self.stuchartlabel.grid(row=row, column=startcolumn+len(self.test_entries)*5 + 6)


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
        self.entry_percentTOT.grid_forget()

        self.infolabel.grid_forget()
        self.stuchartlabel.grid_forget()

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
