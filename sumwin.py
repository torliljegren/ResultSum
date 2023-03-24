# import time
import tkinter as tk
import tkinter.ttk as ttk

import focused
import vscroll
from gradetemplate import GradeTemplate
from student import Student
from student_test_entry import StudentTestEntry
from test import Test
from student_row import StudentRow
from edit_student_tests_win import EditStudentTestsWin
from testinfo import TestInfo
from statwin import StatWin
from student_stat_win import StudentStatWin
import platform
from testheading import TestHeading
from edittestwin import EditTestWin
from changeCourseGroupDialog import ChangeCourseGroupDialog
import csv
from tkinter.messagebox import showerror, showinfo
import tkinter.filedialog
import pyperclip
from tktooltip import ToolTip
from vscroll import ScrollableFrame


class SumWin(object):
    def __init__(self, testtitles: tuple[str] = ('Prov 1', 'Prov 2', 'NP'), students: tuple[Student] = None,
                 root=None, filepath=None, master=None, group: str = '', course: str = ''):
        if root:
            self.win = root
        else:
            self.win = tk.Tk()

        self.testtitles = testtitles

        self.master = master

        if filepath:
            self.filepath = filepath
        else:
            self.filepath = ""

        self.group: str = group
        self.course: str = course

        self.win.wm_protocol('WM_DELETE_WINDOW', self.on_close)
        s = ttk.Style()
        s.configure('ButtonFrame.TFrame', relief='groove')
        s.configure('Grade.TEntry', font=(None, 10, 'bold'), background='linen')
        s.configure('EditedGrade.TEntry', font=(None, 10, 'bold'), background='light goldenrod')
        if platform.system() == 'Linux':
            s.theme_use('clam')
            s.configure('Content.TFrame', background='white')
            s.configure('Content.TLabel', background='white', font=(None, 10, 'bold'))
            s.configure('TestHeading.TLabel', background='white', font=(None, 12, 'bold'))
        elif platform.system() == 'Windows':
            s.configure('Content.TFrame', background='white')
            s.configure('Content.TLabel', background='white', font=(None, 10, 'bold'))
            s.configure('TestHeading.TLabel', background='white', font=(None, 12, 'bold'))
        else:
            s.configure('Content.TLabel', font=(None, 14, 'bold'))
            s.configure('TestHeading.TLabel', background='white', font=(None, 15, 'bold'))
            s.configure('Grade.TEntry', font=(None, 12, 'bold'), background='linen')
            s.configure('EditedGrade.TEntry', font=(None, 12, 'bold'), background='light goldenrod')

        self.students = list(students) if students is not None else [Student('Elev 1', None),
                                                                     Student('Elev 2', None)]

        self.masterframe = ttk.Frame(self.win, style='Content.TFrame')

        btnpad_x = (0, 5)
        btnpad_y = 5
        ibtnpad_y = 0
        self.topframe = ttk.Frame(self.masterframe)  # style='ButtonFrame.TFrame')
        self.topframe['relief'] = 'ridge'
        self.topframe['borderwidth'] = '2'
        # self.topframe.grid(row=0, column=0, pady=0, padx=0, sticky=tk.EW)

        # self.topframe.pack(side='top', expand=True, pady=(0,10))
        self.saveimg = tk.PhotoImage(file='save.png', master=self.win)
        self.savebutton = ttk.Button(master=self.topframe, command=self.cmd_save, image=self.saveimg)
        self.savebutton.grid(row=0, column=0, padx=5, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.savebutton, msg='Spara', delay=0.7)

        self.saveasimg = tk.PhotoImage(file='saveas.png', master=self.win)
        self.saveasbutton = ttk.Button(master=self.topframe, command=self.cmd_saveas, image=self.saveasimg)
        self.saveasbutton.grid(row=0, column=1, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.saveasbutton, msg='Spara som', delay=0.7)

        self.loadimg = tk.PhotoImage(file='open.png', master=self.win)
        self.loadbutton = ttk.Button(master=self.topframe, command=self.cmd_open, image=self.loadimg)
        self.loadbutton.grid(row=0, column=2, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.loadbutton, msg='Öppna', delay=0.7)

        self.pasteimg = tk.PhotoImage(file='paste.png', master=self.win)
        self.pastebutton = ttk.Button(master=self.topframe, command=self.cmd_paste, image=self.pasteimg)
        self.pastebutton.grid(row=0, column=3, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.pastebutton, msg='Klistra in till klasslistan', delay=0.7)

        self.nrowimg = tk.PhotoImage(file='newstudent.png', master=self.win)
        self.nrowbutton = ttk.Button(master=self.topframe, command=self.newstudent, image=self.nrowimg)
        self.nrowbutton.grid(row=0, column=4, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.nrowbutton, msg='Lägg till elevrad', delay=0.7)

        self.drowimg = tk.PhotoImage(file='deletestudent.png', master=self.win)
        self.drowbutton = ttk.Button(master=self.topframe, command=self.removestudent, image=self.drowimg)
        self.drowbutton.grid(row=0, column=5, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.drowbutton, msg='Ta bort understa elevraden', delay=0.7)

        self.ncolimg = tk.PhotoImage(file='newtest.png', master=self.win)
        self.ncolbutton = ttk.Button(master=self.topframe, command=self.newtest, image=self.ncolimg)
        self.ncolbutton.grid(row=0, column=6, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.ncolbutton, msg='Lägg till prov', delay=0.7)

        self.dcolimg = tk.PhotoImage(file='deletetest.png', master=self.win)
        self.dcolbutton = ttk.Button(master=self.topframe, command=self.removetest, image=self.dcolimg)
        self.dcolbutton.grid(row=0, column=7, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.dcolbutton, msg='Ta bort högersta provet', delay=0.7)

        self.upimage = tk.PhotoImage(file='up.png', master=self.win)
        self.upbutton = ttk.Button(master=self.topframe, command=lambda: self.moveup(self.win.focus_get()),
                                   image=self.upimage)
        self.upbutton.grid(row=0, column=8, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.upbutton, msg='Flytta upp elev', delay=0.7)

        self.downimage = tk.PhotoImage(file='down.png', master=self.win)
        self.downbutton = ttk.Button(master=self.topframe, command=lambda: self.movedown(self.win.focus_get()),
                                     image=self.downimage)
        self.downbutton.grid(row=0, column=9, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.downbutton, msg='Flytta ner elev', delay=0.7)

        self.clrallimage = tk.PhotoImage(file='clearall.png', master=self.win)
        self.clrallbutton = ttk.Button(master=self.topframe, image=self.clrallimage, command=self.cmd_clearall)
        self.clrallbutton.grid(row=0, column=11, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.clrallbutton, msg='Rensa alla elever och poäng', delay=0.7)

        self.clrimage = tk.PhotoImage(file='clrentries.png', master=self.win)
        self.clrbutton = ttk.Button(master=self.topframe, image=self.clrimage, command=self.cmd_clear)
        self.clrbutton.grid(row=0, column=10, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.clrbutton, msg='Rensa elevens poäng', delay=0.7)

        self.infoimage = tk.PhotoImage(file='info.png', master=self.win)
        self.infobutton = ttk.Button(master=self.topframe, image=self.infoimage, command=self.cmd_info)
        self.infobutton.grid(row=0, column=12, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.infobutton, msg='Redigera kurs och klass', delay=0.7)

        self.leftimage = tk.PhotoImage(file='left.png', master=self.win)
        self.leftbutton = ttk.Button(master=self.topframe, image=self.leftimage, command=self.cmd_move_test_left)
        self.leftbutton.grid(row=0, column=13, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.leftbutton, msg='Flytta provet till vänster', delay=0.7)

        self.rightimage = tk.PhotoImage(file='right.png', master=self.win)
        self.rightbutton = ttk.Button(master=self.topframe, image=self.rightimage, command=self.cmd_move_test_right)
        self.rightbutton.grid(row=0, column=14, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.rightbutton, msg='Flytta provet till höger', delay=0.7)

        self.statimage = tk.PhotoImage(file='stat.png', master=self.win)
        self.statbutton = ttk.Button(master=self.topframe, image=self.statimage, command=lambda: StatWin(self))
        self.statbutton.grid(row=0, column=15, padx=btnpad_x, pady=btnpad_y, ipady=ibtnpad_y)
        ToolTip(self.statbutton, msg='Visa statistik', delay=0.7)

        self.scrollframe = ScrollableFrame(self.masterframe, hscroll=False, vscroll=True, bg='white')#, style='Content.TFrame')
        # self.scrollframe.grid(row=1, column=0, sticky=tk.NSEW)
        self.contentframe = self.scrollframe
        # self.win.columnconfigure(index=0, pad=0)
        # self.contentframe.config(style='Content.TFrame')
        # self.contentframe.columnconfigure(0, weight=1)
        # self.contentframe.pack(side='bottom', expand=True)

        # create the test titles and headings
        self.headingsvars: list[tk.StringVar] = [tk.StringVar(self.contentframe, value=tt) for tt in testtitles]
        self.headingslabels: list[TestHeading] = \
            [TestHeading(master=self.contentframe, textvariable=hv, sumwin=self) for hv in self.headingsvars]
        self.infoheadings: list[TestInfo] = [TestInfo(self.contentframe) for _ in self.headingsvars]

        # grid the test titles
        testnr = 0
        for hlabel in self.headingslabels:
            hlabel.grid(row=0, column=1 + testnr * 5, columnspan=5, sticky=tk.W, padx=(10, 0), pady=(15, 0))
            testnr += 1

        testnr = 0
        for infh in self.infoheadings:
            infh.grid(row=1, startcol=1 + testnr * 5)
            print(f'sumwin.__init__(): grid infoheading for test {testnr} at column {1 + testnr * 5} to'
                  f' {1 + testnr * 5 + 4}')
            testnr += 1

        print(f'sumwin.__init__(): grid percentage headings at column {len(testtitles) * 5 + 1}')

        ttk.Label(master=self.contentframe, text='%E', style='Content.TLabel').grid(row=1,
                                                                                    column=len(testtitles) * 5 + 1)
        ttk.Label(master=self.contentframe, text='%C', style='Content.TLabel').grid(row=1,
                                                                                    column=len(testtitles) * 5 + 2)
        ttk.Label(master=self.contentframe, text='%A', style='Content.TLabel').grid(row=1,
                                                                                    column=len(testtitles) * 5 + 3)
        ttk.Label(master=self.contentframe, text='%TOT', style='Content.TLabel').grid(row=1,
                                                                                      column=len(testtitles) * 5 + 4)

        # fill the list of students
        self.student_rows = []
        row = 2
        for stu in self.students:
            test_entries = []
            for stutest in stu.tests:
                te = StudentTestEntry(self.contentframe, stutest)
                test_entries.append(te)
            sturow = StudentRow(self.contentframe, row, stu, tuple(test_entries))
            sturow.bind_up_down(self)
            sturow.grid(row, 0)
            self.student_rows.append(sturow)
            row += 1

        # calculate the percentages in the last columns
        for sturow in self.student_rows:
            sturow.update_percent()

        # start a thread that updates percentages
        # self.run_thread = True
        # perc_thread = t.Thread(target=self.update_perc, daemon=True)
        # perc_thread.start()

        self.win.update_idletasks()
        print(f'Height of scrollframe is {self.contentframe.winfo_reqheight()}')
        self.contentframe.resize(vscroll.FIT_HEIGHT)

        self.topframe.pack(side=tk.TOP, fill='x', expand=True, anchor='n')
        self.scrollframe.pack(side=tk.TOP, fill='both', expand=True, anchor='s')
        self.masterframe.pack(fill='both', expand=True)



        self.win.title(self.generate_window_title())

    def generate_window_title(self) -> str:
        # name = str()
        if not self.filepath:
            name = 'Nytt dokument.dat'
        elif '\"' in self.filepath:
            name = self.filepath.split('\"')[-1]
        else:
            name = self.filepath.split('/')[-1]

        print(f'generate_window_title(): generated window title: {name} from file path: {self.filepath}')

        return f'{self.course} ({self.group}) | {name}' if self.course and self.group else name

    def update_window_title(self):
        self.win.title(self.generate_window_title())

    def heading_click_callback(self, e, widget):
        # find out which test was clicked
        i = 0
        for heading in self.headingslabels:
            if heading == widget:
                break
            i += 1
        # find an ordinary test to use as template
        tst = None
        for sturow in self.student_rows:
            if sturow.student.tests[i].standard:
                tst = sturow.student.tests[i]
        if tst is None:
            showerror('Sökfel', 'Kunde inte hitta provet {}.'.format(widget.textvariable.get()))
        else:
            # the editwin modifies the test t
            editwin = EditTestWin(self.win, tst, index=i)
            self.win.wait_window(editwin.win)
            # update all tests at column i
            if editwin.pressed == 'save':
                self.update_tests(i, tst)
                showinfo('Klar', 'Uppdaterade provet och elevomdömen.')
            else:
                pass

    def update_tests(self, index, tst: Test):
        for sturow in self.student_rows:
            test_entry = sturow.test_entries[index]
            if test_entry.test.standard:
                # update the test
                test_entry.test.title = tst.title
                self.headingslabels[index].textvariable.set(tst.title)
                test_entry.test.gradetemplate = tst.gradetemplate
                test_entry.test.max = tst.max
                test_entry.update_grade()

    def cmd_open(self):
        fpath = tkinter.filedialog.askopenfilename(defaultextension='dat', filetypes=(('Bedömningsfil', '*.dat'),),
                                                   parent=self.win)
        result = 0
        swin = tk.Toplevel(master=self.master)
        if fpath:
            result = self.load_session(win=swin, master=self.master, filepath=fpath)

        # if opening file failed
        if result == -1:
            swin.destroy()
            self.master.deiconify()
            self.master.focus_set()

    def cmd_save(self):
        if self.filepath:
            self.save_session(self.filepath)
        else:
            self.cmd_saveas()

    def cmd_saveas(self):
        fpath = tkinter.filedialog.asksaveasfilename(defaultextension='dat', filetypes=(('Bedömningsfil', '*.dat'),),
                                                     parent=self.win, confirmoverwrite=True)
        if fpath:
            self.filepath = fpath
            self.save_session(fpath)
            self.update_window_title()

    def cmd_info(self):
        dia = ChangeCourseGroupDialog(self.win, 'Ändra info')
        if dia.result is not None:
            self.course = dia.result[0] if dia.result[0] != '' else self.course
            self.group = dia.result[1] if dia.result[1] != '' else self.group
            self.update_window_title()

    def cmd_move_test_left(self):
        testnr = self.focused_index_from_widget_name(focused.FOCUSED)[1]
        print(f'testnr is {testnr}')
        if testnr != 0 and testnr != -1:
            self.swap_tests(testnr, testnr - 1)

    def cmd_move_test_right(self):
        testnr = self.focused_index_from_widget_name(focused.FOCUSED)[1]
        if testnr != len(self.student_rows[0].test_entries) - 1 and testnr != -1:
            self.swap_tests(testnr, testnr + 1)

    def update_sums(self):
        for row in self.student_rows:
            for entry in row.test_entries:
                entry.point_entry_callback()

    # row: int is 1-indexed
    def up_keypress(self, w):
        w.widget.icursor(tk.END)
        w.widget.select_clear()
        row, testnr, kind = self.focused_index(w)
        # print(f'Up pressed on row {row}, test nr {testnr}, of kind {kind}')
        if row == 1:
            return

        if kind == -1:  # nameentry is focused
            self.student_rows[row - 2].nameentry.focus_set()
            self.student_rows[row - 2].nameentry.select_range(0, tk.END)
        elif kind == 0:  # Eentry is focused
            self.student_rows[row - 2].test_entries[testnr].Eentry.focus_set()
            self.student_rows[row - 2].test_entries[testnr].Eentry.select_range(0, tk.END)
        elif kind == 1:  # Centry is focused
            self.student_rows[row - 2].test_entries[testnr].Centry.focus_set()
            self.student_rows[row - 2].test_entries[testnr].Centry.select_range(0, tk.END)
        elif kind == 2:  # Aentry is focused
            self.student_rows[row - 2].test_entries[testnr].Aentry.focus_set()
            self.student_rows[row - 2].test_entries[testnr].Aentry.select_range(0, tk.END)


    # row: int is 1-indexed
    def down_keypress(self, w):
        w.widget.icursor(tk.END)
        w.widget.select_clear()
        row, testnr, kind = self.focused_index(w)
        # print(f'Down pressed on row {row}, test nr {testnr}, of kind {kind}')
        if row == len(self.student_rows):
            return

        if kind == -1:  # nameentry is focused
            self.student_rows[row].nameentry.focus_set()
            self.student_rows[row].nameentry.select_range(0, tk.END)
        elif kind == 0:  # Eentry is focused
            self.student_rows[row].test_entries[testnr].Eentry.focus_set()
            self.student_rows[row].test_entries[testnr].Eentry.select_range(0, tk.END)
        elif kind == 1:  # Centry is focused
            self.student_rows[row].test_entries[testnr].Centry.focus_set()
            self.student_rows[row].test_entries[testnr].Centry.select_range(0, tk.END)
        elif kind == 2:  # Aentry is focused
            self.student_rows[row].test_entries[testnr].Aentry.focus_set()
            self.student_rows[row].test_entries[testnr].Aentry.select_range(0, tk.END)

    def return_keypress(self, w):
        # select the text in the entry
        w.widget.icursor(tk.END)
        w.widget.select_clear()

        row, testnr, kind = self.focused_index(w)

        # dont transverse the list if at the bottom
        if row == len(self.student_rows):
            return

        # set focus on the name if the entry is not a point entry
        if kind == -1:
            self.student_rows[row].nameentry.focus_set()
        else:
            self.student_rows[row].test_entries[testnr].Eentry.focus_set()
            self.student_rows[row].test_entries[testnr].Eentry.select_range(0, tk.END)


    def shift_return_keypress(self, w):
        w.widget.icursor(tk.END)
        w.widget.select_clear()
        row, testnr, kind = self.focused_index(w)

        if row == 1:
            return

        if kind == -1:
            self.student_rows[row - 2].nameentry.focus_set()
        else:
            self.student_rows[row - 2].test_entries[testnr].Eentry.focus_set()
            self.student_rows[row].test_entries[testnr].Eentry.select_range(0, tk.END)

    # the triggering widget w.widget is searched for. Returned is a tuple of
    # (row, test number (col), kind (E=0 C=1 A=2))
    def focused_index(self, w):
        # print(w.widget, 'is in focus')
        index = -1
        for row in self.student_rows:
            if row.nameentry is w.widget or str(row.nameentry) == str(w):
                print('focused row:', row.row, row.nameentry.get())
                return row.row - 1, -1, -1
            else:
                testnr = 0
                for entry in row.test_entries:
                    if entry.Eentry is w.widget or str(entry.Eentry) == str(w):
                        print('focused row:', row.row - 1, row.nameentry.get())
                        return row.row - 1, testnr, 0
                    elif entry.Centry is w.widget or str(entry.Centry) == str(w):
                        print('focused row:', row.row - 1, row.nameentry.get())
                        return row.row - 1, testnr, 1
                    elif entry.Aentry is w.widget or str(entry.Aentry) == str(w):
                        print('focused row:', row.row - 1, row.nameentry.get())
                        return row.row - 1, testnr, 2
                    testnr += 1
        return -1, -1, -1

    def focused_index_from_widget_name(self, n):
        """
        Get the index of the focused row. Observe that the index is 1-indexed.
        :param n: the name of the widget in Tk:s naming
        :return: 1-indexed row number that is in focus
        """
        # print(w.widget, 'is in focus')
        index = -1
        for row in self.student_rows:
            if str(row.nameentry) == str(n):
                print('focused row:', row.row, row.nameentry.get())
                return row.row - 1, -1, -1
            else:
                testnr = 0
                for entry in row.test_entries:
                    if str(entry.Eentry) == str(n):
                        print('focused row:', row.row - 1, row.nameentry.get())
                        return row.row - 1, testnr, 0
                    elif str(entry.Centry) == str(n):
                        print('focused row:', row.row - 1, row.nameentry.get())
                        return row.row - 1, testnr, 1
                    elif str(entry.Aentry) == str(n):
                        print('focused row:', row.row - 1, row.nameentry.get())
                        return row.row - 1, testnr, 2
                    testnr += 1
        return -1, -1, -1

    def infolabel_clicked(self, e: tk.Event):
        row = 0
        name = ''
        widget = None
        # find the row that was clicked by id:ing the calling widget and get the name of the student
        for sturow in self.student_rows:
            if e.widget == sturow.infolabel or e.widget == sturow.stuchartlabel:
                widget = e.widget
                name = sturow.namevar.get()
                break
            else:
                row += 1

        print(f'clicked index {row + 1} with name {name}')

        if widget == self.student_rows[row].infolabel:
            editwin = EditStudentTestsWin(self.win,
                                               tuple([stest.test for stest in self.student_rows[row].test_entries]),
                                               self.find_standard_tests(), name)
            self.win.wait_window(editwin.win)
            print(f'editwin: {editwin.pressed} pressed')

            if editwin.pressed == 'cancel':
                return
            elif editwin.pressed == 'restore':
                st_tests = self.find_standard_tests()
                i = 0
                for tst in editwin.tests:
                    tst.gradetemplate = st_tests[i].gradetemplate
                    tst.standard = True
                    i += 1

            i = 0
            for testentry in self.student_rows[row].test_entries:
                testentry.test = editwin.tests[i]
                print(f'{name}s new grade template on test {i + 1}: {testentry.test.gradetemplate}')
                testentry.update_grade()
                if not testentry.test.standard:
                    testentry.gradeentry.config(style='EditedGrade.TEntry')
                else:
                    testentry.gradeentry.config(style='Grade.TEntry')
                i += 1
        else:
            stustatswin = StudentStatWin(self.win, tuple([stest.test for stest in self.student_rows[row].test_entries]),
                                         name)

    def find_standard_tests(self) -> tuple[Test]:
        st_tests = list()
        taken_tests = list()
        test_index = 0
        for stu in self.student_rows:
            for entry in stu.test_entries:
                if entry.test.standard and test_index not in taken_tests:
                    st_tests.append(entry.test.copy())
                    taken_tests.append(test_index)
                    test_index += 1
            if len(st_tests) == len(self.student_rows[0].test_entries):
                break
        return tuple(st_tests)

    def moveup(self, w):
        print(focused.FOCUSED, 'was in focus')
        print(w, 'is in focus')
        index = -1
        for row in self.student_rows:
            if focused.FOCUSED == str(row.nameentry):
                index = row.row
                break
            else:
                for entry in row.test_entries:
                    if focused.FOCUSED == str(entry.Eentry):
                        print('focused row:', row.row)
                        index = row.row
                        break
                    elif focused.FOCUSED == str(entry.Centry):
                        print('focused row:', row.row)
                        index = row.row
                        break
                    elif focused.FOCUSED is str(entry.Aentry):
                        print('focused row:', row.row)
                        index = row.row
                        break
        if index == -1:
            return        # current    above
        self.swap_entries(index - 2, index - 3)
        row, _, __ = self.focused_index_from_widget_name(focused.FOCUSED)
        self.student_rows[row - 2].nameentry.focus_set()

    def movedown(self, w):
        print(focused.FOCUSED, 'was in focus')
        print(w, 'is in focus')
        index = -1
        for row in self.student_rows:
            if focused.FOCUSED == str(row.nameentry):
                index = row.row
                break
            else:
                for entry in row.test_entries:
                    if focused.FOCUSED == str(entry.Eentry):
                        print('focused row:', row.row)
                        index = row.row
                        break
                    elif focused.FOCUSED == str(entry.Centry):
                        print('focused row:', row.row)
                        index = row.row
                        break
                    elif focused.FOCUSED == str(entry.Aentry):
                        print('focused row:', row.row)
                        index = row.row
                        break
        if index == -1:
            return
        elif index - 2 == len(self.student_rows) - 1:
            return
        self.swap_entries(index - 2, index - 1)
        row, _, __ = self.focused_index_from_widget_name(focused.FOCUSED)
        self.student_rows[row].nameentry.focus_set()

    def cmd_clearall(self):
        for stu in self.student_rows:
            stu.clear_entries()

    def cmd_clear(self):
        row, name, kind = self.focused_index_from_widget_name(focused.FOCUSED)
        self.student_rows[row-1].clear_entries()

    def swap_entries(self, index1, index2):
        entries1 = self.student_rows[index1].test_entries
        entries2 = self.student_rows[index2].test_entries
        name1 = self.student_rows[index1].namevar.get()
        self.student_rows[index1].namevar.set(self.student_rows[index2].namevar.get())
        self.student_rows[index2].namevar.set(name1)

        for i in range(len(entries1)):
            tempE = entries1[i].Evar.get()
            tempC = entries1[i].Cvar.get()
            tempA = entries1[i].Avar.get()
            tempsum = entries1[i].sumvar.get()
            tempgrade = entries1[i].gradevar.get()

            entries1[i].Evar.set(entries2[i].Evar.get())
            entries1[i].Cvar.set(entries2[i].Cvar.get())
            entries1[i].Avar.set(entries2[i].Avar.get())
            entries1[i].sumvar.set(entries2[i].sumvar.get())
            entries1[i].gradevar.set(entries2[i].gradevar.get())

            entries2[i].Evar.set(tempE)
            entries2[i].Cvar.set(tempC)
            entries2[i].Avar.set(tempA)
            entries2[i].sumvar.set(tempsum)
            entries2[i].gradevar.set(tempgrade)

            # temptest1 = entries1[i].test
            # entries1[i].test = entries2[i].test
            # entries2[i].test = temptest1
        self.student_rows[index1].update_model_from_gui()
        self.student_rows[index2].update_model_from_gui()

        # self.update_students()

    def swap_tests(self, index1, index2):
        print(f'attempring to swap test {index1} and {index2}')
        # swap the titles
        heading1 = self.headingsvars[index1].get()
        self.headingsvars[index1].set(self.headingsvars[index2].get())
        self.headingsvars[index2].set(heading1)

        for row in self.student_rows:
            # swap results
            res1 = row.test_entries[index1].results()
            row.test_entries[index1].set_results( row.test_entries[index2].results() )
            row.test_entries[index2].set_results(res1)

            # swap tests
            test1 = row.test_entries[index1].test
            row.test_entries[index1].test = row.test_entries[index2].test
            row.test_entries[index2].test = test1

            row.update_model_from_gui()
            row.update_grades_and_sums()


    def newtest(self):
        stus = self.students
        tsts: list[str] = [tst.title for tst in stus[0].tests]
        tsts.append(f'Prov {len(tsts) + 1}')
        for stu in stus:
            stu.tests.append(Test(title=tsts[-1], max=(1, 1, 1), result=(0, 0, 0),
                                       grades=GradeTemplate(1, (1, 1), (1, 1), (1, 1), (1, 1))))
        s = SumWin(tuple(tsts), tuple(stus), master=self.master, root=tkinter.Toplevel(self.master), course=self.course,
                   group=self.group)
        s.filepath = self.filepath
        s.update_window_title()
        self.win.destroy()

    def removetest(self):
        stus = self.students
        tsts: list[str] = [tst.title for tst in stus[0].tests][:-1]
        for stu in stus:
            stu.tests = stu.tests[:-1]
        s = SumWin(tuple(tsts), tuple(stus), master=self.master,
                   root=tkinter.Toplevel(self.master), group=self.group, course=self.course)
        s.filepath = self.filepath
        s.update_window_title()
        self.win.destroy()

    def newstudent(self):
        stests = list()
        # give the new student the
        for tst in self.students[0].tests:
            stests.append(Test(title=tst.title, max=tst.max, result=(0, 0, 0), grades=tst.gradetemplate))
        self.students.append(Student(name='Ny elev', tests=tuple(stests)))
        # create a new student row with student entries
        entries = list()
        for tst in stests:
            entries.append(StudentTestEntry(self.contentframe, tst))
        newrow = StudentRow(self.contentframe, len(self.student_rows) + 2, self.students[-1], tuple(entries))
        newrow.bind_up_down(self)
        newrow.grid(row=newrow.row, startcolumn=0)
        self.student_rows.append(newrow)

    def removestudent(self):
        self.student_rows[-1].grid_forget()
        self.student_rows[-1].destroy()
        self.student_rows = self.student_rows[:-1]

    def update_students(self):
        for row in self.student_rows:
            index = 0
            for entry in row.test_entries:
                row.student.name = row.namevar.get()
                row.student.tests[index].result[0] = int(entry.Evar.get())
                row.student.tests[index].result[1] = int(entry.Cvar.get())
                row.student.tests[index].result[2] = int(entry.Avar.get())
            index += 1

    def cmd_paste(self):
        r = tk.messagebox.askyesno('Klistra in namn?', 'Vill du klistra in namnen till klasslistan? De nuvarande namnen'
                                                       'kommer att bytas ut.')
        if r == tk.NO:
            return

        # prepare and clean up the list
        print('cmd_paste(): attempting to paste names from clipboard')
        namelist_1 = [n.strip() for n in pyperclip.paste().split('\n') if '\n' not in n and n != '']
        print('cmd_paste(): found names:', namelist_1)
        namelist_2 = [n for n in namelist_1 if n != '']
        # write the names to the textarea
        namelist_2.sort()
        for i in range(len(namelist_2)):
            self.student_rows[i].namevar.set(namelist_2[i])

    def save_session(self, fpath):
        self.update_students()
        with open(fpath, 'w') as savefile:
            writer = csv.writer(savefile, dialect='excel', lineterminator='\n')
            writer.writerow(('PROVINFO', self.course, self.group))
            # get the tests
            index = 0
            tests = []
            for stu in self.students:
                for i in range(len(stu.tests)):
                    if len(tests) == len(stu.tests):
                        break
                    if stu.tests[index].standard:
                        tests.append(stu.tests[index])
                        index += 1
                if len(tests) == len(stu.tests):
                    break

            # write the tests info (title, max, gradetemplate)
            for tst in tests:
                writer.writerow((tst.title, *tst.max, tst.gradetemplate.E, *tst.gradetemplate.D,
                                 *tst.gradetemplate.C, *tst.gradetemplate.B, *tst.gradetemplate.A))
                print(f'save_session(): wrote {tst.title} to disk')

            # write the students and their results, as a list of results of their tests
            writer.writerow(('STUDENTER',))
            for row in self.student_rows:
                writedata = [row.namevar.get()]
                for tst in row.test_entries:
                    writedata.append(tst.Evar.get())
                    writedata.append(tst.Cvar.get())
                    writedata.append(tst.Avar.get())
                writer.writerow(writedata)
                print(f'save_session(): wrote {writedata} to disk')

            # search for non standard grade templates and save them to a tuple (row, col), 0-indexed
            print('searching for non standard grade templates')
            row = 0
            col = 0
            nonstandard = list()
            for stu in self.student_rows:
                col = 0
                for entry in stu.test_entries:
                    if not entry.test.standard:
                        print(f'found {self.students[row].name} on test {col}')
                        nonstandard.append((row, col))
                    col += 1
                row += 1
            writer.writerow(('REDIGERADE MALLAR',))
            # write the non standard templates if there are any, else 0 to indicate no non standard templates
            if len(nonstandard) > 0:
                for r, c in nonstandard:
                    tst = self.student_rows[r].test_entries[c].test
                    gtempl = tst.gradetemplate
                    #                0  1  2,3,4       5        6,7         8,9       10,11      12,13
                    writer.writerow((r, c, *tst.max, gtempl.E, *gtempl.D, *gtempl.C, *gtempl.B, *gtempl.A))
                print(f'wrote {len(nonstandard)} templates to disk')
            else:
                writer.writerow((0,))
                print('no non standard templates found')

    # CSV-format:
    # PROVINFO
    # [TEST TITLE], [MAX E], [MAX C], [MAX A], [POINTS FOR E], [POINTS FOR D], [C/A POINTS FOR D], [POINTS FOR C],
    # [C/A POINTS FOR C], [POINTS FOR B], [A POINTS FOR B], [POINTS FOR A], [A POINTS FOR A]
    # STUDENTER
    # [STUDENT NAME], [E POINTS ON TEST 1], [C POINTS ON TEST 1], [A POINTS ON TEST 1],...,[E POINTS ON TEST N],...
    @staticmethod
    def load_session(win, master, filepath: str = 'test.dat') -> int:
        # read the lines of the csv
        csv_rows = []
        with open(filepath, 'r') as opened_file:
            csvreader = csv.reader(opened_file, dialect='excel')
            for row in csvreader:
                csv_rows.append(row)

        course = str()
        group = str()

        # rudementary check if opened file is valid
        if len(csv_rows[0]) == 0:
            showerror('Filfel', 'Filen saknar innehåll.')
            return -1
        elif 'PROVINFO' not in csv_rows[0]:
            showerror('Filfel', 'Filen innehåller inte förväntad data.\n Är det verkligen en resultatfil?')
            return -1

        if len(csv_rows[0]) == 3:
            course = csv_rows[0][1]
            group = csv_rows[0][2]

        # find out the number of tests
        ntests = -1  # the loop will count row 0 as well so -1 is the correct start
        for row in csv_rows:
            if row[0] == 'STUDENTER':
                break
            else:
                ntests += 1
        print(f'load_session: found {ntests} tests')

        # create the test info
        tests_data = list()
        print('load_session(): parsing tests')
        for i in range(1, ntests + 1):
            row = csv_rows[i]
            test_data = dict()
            test_data['title'] = row[0]
            test_data['maxe'] = row[1]
            test_data['maxc'] = row[2]
            test_data['maxa'] = row[3]
            test_data['template'] = GradeTemplate(int(row[4]), (int(row[5]), int(row[6])),
                                                                (int(row[7]), int(row[8])), (int(row[9]), int(row[10])),
                                                                (int(row[11]), int(row[12])))
            q = test_data['template']
            print(f'load_session(): parsed {test_data} with gradetemplate: {q}')
            tests_data.append(test_data)
        print('load_session(): parsing tests done!')

        # extract the student rows
        # the first student has index ntests+2
        print('load_session(): parsing students and results')
        sturows = csv_rows[ntests + 2:]

        # create the student objects
        students: list[Student] = []
        # breakpnt is where the non standard grade templates begin
        breakpnt = 0
        for sturow in sturows:
            if sturow[0] == 'REDIGERADE MALLAR':
                break
            print(f'load_session(): parsing student: {sturow}')
            ttests: list[Test] = []
            for i in range(len(tests_data)):
                testdata = tests_data[i]
                ttests.append(Test(title=testdata['title'],
                                        max=(int(testdata['maxe']), int(testdata['maxc']), int(testdata['maxa'])),
                                        result=(int(sturow[3 * i + 1]), int(sturow[3 * i + 2]), int(sturow[3 * i + 3])),
                                        grades=testdata['template']))
            students.append(Student(name=sturow[0], tests=tuple(ttests)))
            breakpnt += 1
        print('load_session(): parsing students and results done!')

        print('load_session(): processing edited grade templates')
        gradetemplate_data = []

        for i in range(breakpnt + 1, len(sturows)):
            if len(sturows[i]) == 1:
                print('no edited grade templates found')
                break
            else:
                print(f'found {len(sturows[breakpnt + 1:])} non standard grade templates')
            print(
                f'parsing student #{int(sturows[i][0])} {students[int(sturows[i][0])].name}, test {int(sturows[i][1])}')
            #  0    1    2    3      4                  5  6,7  8,9  10,11   12,13
            # row, col, maxE, maxC, maxA, GradeTemplate(E,  D,   C,    B,      A)
            #                                   row             col
            gradetemplate_data.append((int(sturows[i][0]), int(sturows[i][1]),
                                       (int(sturows[i][2]), int(sturows[i][3]), int(sturows[i][4])),  # max
                                       GradeTemplate(int(sturows[i][5]),  # E
                                                                   (int(sturows[i][6]), int(sturows[i][7])),  # D
                                                                   (int(sturows[i][8]), int(sturows[i][9])),  # C
                                                                   (int(sturows[i][10]), int(sturows[i][11])),  # B
                                                                   (int(sturows[i][12]), int(sturows[i][13])))))  # A

        # modify the the students that should have a non standard grade template
        for data in gradetemplate_data:
            r = data[0]
            c = data[1]
            m = data[2]
            template = data[3]
            students[r].tests[c].max = m
            students[r].tests[c].gradetemplate = template
            students[r].tests[c].standard = False

        print('load_session(): opening a new document with loaded data')

        # feed the students to a new SumWin
        SumWin(testtitles=tuple([tst['title'] for tst in tests_data]), students=tuple(students),
               root=win, filepath=filepath, master=master, course=course, group=group)
        return 0


    def on_close(self):
        if self.master is not None:
            print(f'on_close(): destroying {self.generate_window_title()} and opening {self.win}')
            self.win.destroy()
            self.master.deiconify()
            self.master.lift()
            self.master.focus_set()
            self.master.entry_subject.focus_set()
        else:
            exit(0)
