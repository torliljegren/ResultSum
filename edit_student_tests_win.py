import tkinter as tk
from tkinter.messagebox import showerror
import tkinter.ttk as ttk
import test as t
from platform import system
import threading
import time


class TestFrame(ttk.Frame):
    """
    Takes a test and modifies it to the users liking.
    Usage:
    etw = EditTestWin(parent, test)
    parent.waitWindow(etw)
    edited_test = etw.test
    """
    # TODO: make every frame have a save and restore button, instead of the global ones
    def __init__(self, parent, test: t.Test, st_test: t.Test, title=None):
        super().__init__(master=parent, borderwidth=1)
        self.parent = parent
        self.test = test
        self.st_test = st_test
        self.title = title
        self.pressed = ""

        s = ttk.Style(self.parent)
        s.configure('Heading.TLabel', font=((None, 14, 'bold') if system() == 'Darwin' else (None, 11, 'bold')))

        self.bgframe = ttk.Frame(master=self)
        self.bgframe.pack()

        self.topframe = ttk.Frame(self.bgframe)
        titlefont = (None, 15, 'bold') if system() == 'Darwin' else (None, 12, 'bold')
        self.titlevar = tk.StringVar(master=self.topframe, value=self.test.title)
        self.titleentry = ttk.Entry(self.topframe, textvariable=self.titlevar, font=titlefont, justify='center')
        self.titleentry.grid(row=1, column=0, pady=(20, 30))
        self.titleentry.config(state='disabled')
        self.topframe.grid(row=0, column=0)
        yp = 10

        self.middleframe = ttk.Frame(self.bgframe)

        ttk.Label(self.middleframe, text='Elevens poäng:', style='Heading.TLabel').grid(row=0, column=0, padx=(0, 15))
        ttk.Label(self.middleframe, text='E-poäng').grid(row=0, column=1)
        ttk.Label(self.middleframe, text='C-poäng').grid(row=0, column=2)
        ttk.Label(self.middleframe, text='A-poäng').grid(row=0, column=3)
        ttk.Label(self.middleframe, text='Totalpoäng').grid(row=0, column=4)
        self.Estuvar = tk.IntVar(self.middleframe, test.result[0])
        self.Estu = ttk.Entry(self.middleframe, textvariable=self.Estuvar, width=4, state='readonly')
        self.Estu.grid(row=1, column=1, pady=(0, yp))
        self.Cstuvar = tk.IntVar(self.middleframe, test.result[1])
        self.Cstu = ttk.Entry(self.middleframe, textvariable=self.Cstuvar, width=4, state='readonly')
        self.Cstu.grid(row=1, column=2, pady=(0, yp))
        self.Astuvar = tk.IntVar(self.middleframe, test.result[2])
        self.Astu = ttk.Entry(self.middleframe, textvariable=self.Astuvar, width=4, state='readonly')
        self.Astu.grid(row=1, column=3, pady=(0, yp))
        self.sumstuvar = tk.IntVar(self.middleframe, test.result[0]+test.result[1]+test.result[2])
        self.sumstu = ttk.Entry(self.middleframe, textvariable=self.sumstuvar,
                                width=4, state='readonly')
        self.sumstu.grid(row=1, column=4, pady=(0, yp))

        ttk.Label(self.middleframe, text='Maxpoäng', style='Heading.TLabel').grid(row=2, column=0, padx=(0, 15))
        ttk.Label(self.middleframe, text='E-poäng').grid(row=2, column=1)
        ttk.Label(self.middleframe, text='C-poäng').grid(row=2, column=2)
        ttk.Label(self.middleframe, text='A-poäng').grid(row=2, column=3)
        ttk.Label(self.middleframe, text='Totalpoäng').grid(row=2, column=4)
        self.Emaxvar = tk.StringVar(self.topframe, value=str(test.max[0]))
        self.Cmaxvar = tk.StringVar(self.topframe, value=str(test.max[1]))
        self.Amaxvar = tk.StringVar(self.topframe, value=str(test.max[2]))
        self.sumvar = tk.StringVar(self.topframe, value=str(test.max[0]+test.max[1]+test.max[2]))
        self.Emaxentry = ttk.Entry(self.middleframe, textvariable=self.Emaxvar, width=4)
        self.Emaxentry.grid(row=3, column=1, pady=(0, yp))
        self.Cmaxentry = ttk.Entry(self.middleframe, textvariable=self.Cmaxvar, width=4)
        self.Cmaxentry.grid(row=3, column=2, pady=(0, yp))
        self.Amaxentry = ttk.Entry(self.middleframe, textvariable=self.Amaxvar, width=4)
        self.Amaxentry.grid(row=3, column=3, pady=(0, yp))
        self.sumentry = ttk.Entry(self.middleframe, textvariable=self.sumvar, width=4)
        self.sumentry.grid(row=3, column=4, pady=(0, yp))

        ttk.Label(self.middleframe, text='E-gräns', style='Heading.TLabel').grid(row=4, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=4, column=1)
        self.Etotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.E))
        self.Etotentry = ttk.Entry(self.middleframe, textvariable=self.Etotvar, width=4)
        self.Etotentry.grid(row=5, column=1, pady=(0, yp))

        ttk.Label(self.middleframe, text='D-gräns', style='Heading.TLabel').grid(row=6, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=6, column=1)
        ttk.Label(self.middleframe, text='C/A-Poäng').grid(row=6, column=2)
        # create Stringvars and entries
        self.Dtotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.D[0]))
        self.DCvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.D[1]))
        self.Dtotentry = ttk.Entry(self.middleframe, textvariable=self.Dtotvar, width=4)
        self.DCentry = ttk.Entry(self.middleframe, textvariable=self.DCvar, width=4)
        self.Dtotentry.grid(row=7, column=1, pady=(0, yp))
        self.DCentry.grid(row=7, column=2, pady=(0, yp))

        ttk.Label(self.middleframe, text='C-gräns', style='Heading.TLabel').grid(row=8, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=8, column=1)
        ttk.Label(self.middleframe, text='C/A-Poäng').grid(row=8, column=2)
        # create Stringvars and entries
        self.Ctotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.C[0]))
        self.CCvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.C[1]))
        self.Ctotentry = ttk.Entry(self.middleframe, textvariable=self.Ctotvar, width=4)
        self.CCentry = ttk.Entry(self.middleframe, textvariable=self.CCvar, width=4)
        self.Ctotentry.grid(row=9, column=1, pady=(0, yp))
        self.CCentry.grid(row=9, column=2, pady=(0, yp))

        ttk.Label(self.middleframe, text='B-gräns', style='Heading.TLabel').grid(row=10, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=10, column=1)
        ttk.Label(self.middleframe, text='A-Poäng').grid(row=10, column=2)
        # create Stringvars and entries
        self.Btotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.B[0]))
        self.BAvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.B[1]))
        self.Btotentry = ttk.Entry(self.middleframe, textvariable=self.Btotvar, width=4)
        self.BAentry = ttk.Entry(self.middleframe, textvariable=self.BAvar, width=4)
        self.Btotentry.grid(row=11, column=1, pady=(0, yp))
        self.BAentry.grid(row=11, column=2, pady=(0, yp))

        ttk.Label(self.middleframe, text='A-gräns', style='Heading.TLabel').grid(row=12, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=12, column=1)
        ttk.Label(self.middleframe, text='A-Poäng').grid(row=12, column=2)
        # create Stringvars and entries
        self.Atotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.A[0]))
        self.AAvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.A[1]))
        self.Atotentry = ttk.Entry(self.middleframe, textvariable=self.Atotvar, width=4)
        self.AAentry = ttk.Entry(self.middleframe, textvariable=self.AAvar, width=4)
        self.Atotentry.grid(row=13, column=1, pady=(0, yp))
        self.AAentry.grid(row=13, column=2, pady=(0, yp))

        self.middleframe.grid(row=1, column=0, padx=30)

        self.sumthread = threading.Thread(target=self.sumtot, daemon=True)
        self.sumthread.start()

    def validate(self) -> ttk.Entry | None:
        # check for input errors
        Emax = 0
        try:
            Emax = int(self.Emaxvar.get())
        except ValueError:
            return self.Emaxentry

        Cmax = 0
        try:
            Cmax = int(self.Cmaxvar.get())
        except ValueError:
            return self.Cmaxentry

        Amax = 0
        try:
            Amax = int(self.Amaxvar.get())
        except ValueError:
            return self.Amaxentry

        Etot = 0
        try:
            Etot = int(self.Etotvar.get())
        except ValueError:
            return self.Etotentry

        Dtot = 0
        try:
            Dtot = int(self.Dtotvar.get())
        except ValueError:
            return self.Dtotentry

        DC = 0
        try:
            DC = int(self.DCvar.get())
        except ValueError:
            return self.DCentry

        Ctot = 0
        try:
            Ctot = int(self.Ctotvar.get())
        except ValueError:
            return self.Ctotentry

        CC = 0
        try:
            CC = int(self.CCvar.get())
        except ValueError:
            return self.CCentry

        Btot = 0
        try:
            Btot = int(self.Btotvar.get())
        except ValueError:
            return self.Btotentry

        BA = 0
        try:
            BA = int(self.BAvar.get())
        except ValueError:
            return self.BAentry

        Atot = 0
        try:
            Atot = int(self.Atotvar.get())
        except ValueError:
            return self.Atotentry

        AA = 0
        try:
            AA = int(self.AAvar.get())
        except ValueError:
            return self.AAentry

        return None


    def sumtot(self):
        while not self.pressed:
            try:
                time.sleep(0.5)
                # print('threading!')
                self.sumvar.set(str(int(self.Emaxvar.get())+int(self.Cmaxvar.get())+int(self.Amaxvar.get())))
            except ValueError:
                self.sumvar.set('???')
        # print('threading ends')

    def update_test(self):
        Emax = int(self.Emaxvar.get())
        Cmax = int(self.Cmaxvar.get())
        Amax = int(self.Amaxvar.get())
        Etot = int(self.Etotvar.get())
        Dtot = int(self.Dtotvar.get())
        DC = int(self.DCvar.get())
        Ctot = int(self.Ctotvar.get())
        CC = int(self.CCvar.get())
        Btot = int(self.Btotvar.get())
        BA = int(self.BAvar.get())
        Atot = int(self.Atotvar.get())
        AA = int(self.AAvar.get())

        tst = self.test.copy()
        tst.title = self.titlevar.get()
        tst.max = (Emax, Cmax, Amax)
        tst.gradetemplate.E = Etot
        tst.gradetemplate.D = (Dtot, DC)
        tst.gradetemplate.C = (Ctot, CC)
        tst.gradetemplate.B = (Btot, BA)
        tst.gradetemplate.A = (Atot, AA)
        tst.standard = tst.gradetemplate == self.st_test.gradetemplate
        self.test = tst

class EditStudentTestsWin(object):
    def __init__(self, parent, tests: tuple[t.Test], st_tests, name=None):
        self.buttonframe = None
        self.parent = parent
        self.tests = tests
        self.st_tests = st_tests
        self.restore = False
        self.name = name if name else 'Namnlös elev'
        self.pressed = ''

        self.test_frames = []
        self.win = tk.Toplevel(parent)
        self.win.title(self.name)
        print(f'There are {len(tests)} tests in {name}s testlist')
        self.initUI()

    def initUI(self):
        s = ttk.Style(self.parent)
        s.configure('Heading.TLabel', font=((None, 14, 'bold') if system() == 'Darwin' else (None, 11, 'bold')))

        bgframe = ttk.Frame(self.win)

        topframe = ttk.Frame(master=bgframe)
        ttk.Label(topframe, text=f'Redigera {self.name}s provmallar', style='Heading.TLabel').grid(row=0, column=0, pady=(10,20))
        topframe.grid(row=0, column=0)

        middleframe = ttk.Frame(master=bgframe)
        test_index = 0
        for i in range(1, len(self.tests)*2+1):
            if i%2 != 0:
                ttk.Separator(master=middleframe, orient=tk.VERTICAL).grid(row=0, column=i, sticky=tk.NSEW)
            else:
                self.test_frames.append(TestFrame(middleframe, self.tests[test_index], self.st_tests[test_index],
                                                  title=self.tests[test_index].title))
                self.test_frames[test_index].grid(row=0, column=i)
                test_index += 1

        middleframe.grid(row=1, column=0)

        buttonframe = ttk.Frame(master=bgframe)
        ttk.Button(buttonframe, command=self.save_test, text='Spara').grid(row=0, column=0, padx=10, pady=20)
        ttk.Button(buttonframe, command=self.cancel, text='Avbryt').grid(row=0, column=2, padx=10, pady=20)
        ttk.Button(buttonframe, command=self.restore_test, text='Återställ').grid(row=0, column=1, padx=10, pady=20)
        buttonframe.grid(row=2, column=0)
        topframe.grid_columnconfigure(0, weight=1)
        buttonframe.grid_columnconfigure(0, weight=1)

        bgframe.pack()

    def save_test(self):
        temptests: list[t.Test] = []
        for testframe in self.test_frames:
            err_entry = testframe.validate()
            if err_entry:
                showerror('Värdefel', 'Felaktig inmatning i en poängruta. Den rutan markeras nu')
                self.win.focus_set()
                err_entry.focus_set()
                return
            else:
                testframe.update_test()
                temptests.append(testframe.test)
        self.tests = temptests
        self.pressed = 'save'
        self.win.destroy()

    def restore_test(self):
        self.pressed = 'restore'
        self.win.destroy()


    def cancel(self):
        self.pressed = 'cancel'
        self.win.destroy()
