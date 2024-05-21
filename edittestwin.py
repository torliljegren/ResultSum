import tkinter as tk
import tkinter.ttk as ttk
from test import Test
from tkinter.messagebox import showerror
from platform import system
import threading
import time

class EditTestWin(object):
    """
    Takes a test and modifies it to the users liking.
    Usage:
    etw = EditTestWin(parent, test)
    parent.waitWindow(etw)
    edited_test = etw.test
    """
    def __init__(self, parent, test: Test, name=None, index=0):
        # TODO: implement parameter test_index and result stats
        self.parent = parent
        self.test = test
        self.name = name
        self.index = index
        self.win = tk.Toplevel(master=parent)
        self.win.title(f'Redigera {test.title}')
        self.win.wm_protocol('WM_DELETE_WINDOW', self.cancel)
        self.pressed = ""

        s = ttk.Style(self.parent)
        s.configure('Heading.TLabel', font=((None, 14, 'bold') if system() == 'Darwin' else (None, 11, 'bold')))

        self.bgframe = ttk.Frame(master=self.win)
        self.bgframe.pack()

        self.topframe = ttk.Frame(self.bgframe)
        titlefont = (None, 15, 'bold') if system() == 'Darwin' else (None, 12, 'bold')
        self.titlevar = tk.StringVar(master=self.topframe, value=self.test.title)
        self.titleentry = ttk.Entry(self.topframe, textvariable=self.titlevar, font=titlefont, justify='center')
        self.titleentry.grid(row=1, column=0, pady=(20, 30))
        if self.name is not None:
            namelabel = ttk.Label(self.topframe, text='Elev: ' + self.name, style='Heading.TLabel')
            namelabel.grid(row=0, column=0)
            self.titleentry.config(state='disabled')
        self.topframe.grid(row=0, column=0)
        yp = 10
        self.middleframe = ttk.Frame(self.bgframe)

        ttk.Label(self.middleframe, text='Maxpoäng', style='Heading.TLabel').grid(row=0, column=0, padx=(0, 15))
        ttk.Label(self.middleframe, text='E-poäng').grid(row=0, column=1)
        ttk.Label(self.middleframe, text='C-poäng').grid(row=0, column=2)
        ttk.Label(self.middleframe, text='A-poäng').grid(row=0, column=3)
        ttk.Label(self.middleframe, text='Totalpoäng').grid(row=0, column=4)
        self.Emaxvar = tk.StringVar(self.topframe, value=str(test.max[0]))
        self.Cmaxvar = tk.StringVar(self.topframe, value=str(test.max[1]))
        self.Amaxvar = tk.StringVar(self.topframe, value=str(test.max[2]))
        self.sumvar = tk.StringVar(self.topframe, value=str(test.max[0]+test.max[1]+test.max[2]))
        self.Emaxentry = ttk.Entry(self.middleframe, textvariable=self.Emaxvar, width=4)
        self.Emaxentry.grid(row=1, column=1, pady=(0, yp))
        self.Cmaxentry = ttk.Entry(self.middleframe, textvariable=self.Cmaxvar, width=4)
        self.Cmaxentry.grid(row=1, column=2, pady=(0, yp))
        self.Amaxentry = ttk.Entry(self.middleframe, textvariable=self.Amaxvar, width=4)
        self.Amaxentry.grid(row=1, column=3, pady=(0, yp))
        self.sumentry = ttk.Entry(self.middleframe, textvariable=self.sumvar, width=4)
        self.sumentry.grid(row=1, column=4, pady=(0, yp))

        ttk.Label(self.middleframe, text='E-gräns', style='Heading.TLabel').grid(row=2, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=2, column=1)
        self.Etotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.E))
        self.Etotentry = ttk.Entry(self.middleframe, textvariable=self.Etotvar, width=4)
        self.Etotentry.grid(row=3, column=1, pady=(0, yp))

        ttk.Label(self.middleframe, text='D-gräns', style='Heading.TLabel').grid(row=4, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=4, column=1)
        ttk.Label(self.middleframe, text='varav C/A-Poäng').grid(row=4, column=2, columnspan=2)
        # create Stringvars and entries
        self.Dtotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.D[0]))
        self.DCvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.D[1]))
        self.Dtotentry = ttk.Entry(self.middleframe, textvariable=self.Dtotvar, width=4)
        self.DCentry = ttk.Entry(self.middleframe, textvariable=self.DCvar, width=4)
        self.Dtotentry.grid(row=5, column=1, pady=(0, yp))
        self.DCentry.grid(row=5, column=2, pady=(0, yp))

        ttk.Label(self.middleframe, text='C-gräns', style='Heading.TLabel').grid(row=6, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=6, column=1)
        ttk.Label(self.middleframe, text='varav C/A-Poäng').grid(row=6, column=2, columnspan=2)
        # create Stringvars and entries
        self.Ctotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.C[0]))
        self.CCvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.C[1]))
        self.Ctotentry = ttk.Entry(self.middleframe, textvariable=self.Ctotvar, width=4)
        self.CCentry = ttk.Entry(self.middleframe, textvariable=self.CCvar, width=4)
        self.Ctotentry.grid(row=7, column=1, pady=(0, yp))
        self.CCentry.grid(row=7, column=2, pady=(0, yp))

        ttk.Label(self.middleframe, text='B-gräns', style='Heading.TLabel').grid(row=8, column=0, columnspan=2)
        ttk.Label(self.middleframe, text='Poäng').grid(row=8, column=1)
        ttk.Label(self.middleframe, text='varav A-Poäng').grid(row=8, column=2, columnspan=2)
        # create Stringvars and entries
        self.Btotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.B[0]))
        self.BAvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.B[1]))
        self.Btotentry = ttk.Entry(self.middleframe, textvariable=self.Btotvar, width=4)
        self.BAentry = ttk.Entry(self.middleframe, textvariable=self.BAvar, width=4)
        self.Btotentry.grid(row=9, column=1, pady=(0, yp))
        self.BAentry.grid(row=9, column=2, pady=(0, yp))

        ttk.Label(self.middleframe, text='A-gräns', style='Heading.TLabel').grid(row=10, column=0)
        ttk.Label(self.middleframe, text='Poäng').grid(row=10, column=1)
        ttk.Label(self.middleframe, text='varav A-Poäng').grid(row=10, column=2, columnspan=2)
        # create Stringvars and entries
        self.Atotvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.A[0]))
        self.AAvar = tk.StringVar(self.topframe, value=str(test.gradetemplate.A[1]))
        self.Atotentry = ttk.Entry(self.middleframe, textvariable=self.Atotvar, width=4)
        self.AAentry = ttk.Entry(self.middleframe, textvariable=self.AAvar, width=4)
        self.Atotentry.grid(row=11, column=1, pady=(0, yp))
        self.AAentry.grid(row=11, column=2, pady=(0, yp))

        self.bottomframe = ttk.Frame(self.bgframe)
        self.savebutton = ttk.Button(self.bottomframe, command=self.save_test, text='Spara')
        self.savebutton.grid(row=0, column=2)
        ttk.Label(master=self.bottomframe, text='    ').grid(row=0, column=1)
        self.cancelbutton = ttk.Button(self.bottomframe, command=self.cancel, text='Avbryt')
        self.cancelbutton.grid(row=0, column=0)

        self.middleframe.grid(row=1, column=0, padx=30)
        self.bottomframe.grid(row=2, column=0, pady=15, padx=30)

        self.sumthread = threading.Thread(target=self.sumtot, daemon=True)
        self.sumthread.start()

    def save_test(self):
        # check for input errors
        Emax = 0
        try:
            Emax = int(self.Emaxvar.get())
        except ValueError:
            Emax = -1

        Cmax = 0
        try:
            Cmax = int(self.Cmaxvar.get())
        except ValueError:
            Cmax = -1

        Amax = 0
        try:
            Amax = int(self.Amaxvar.get())
        except ValueError:
            Amax = -1

        eca_max = Emax + Cmax + Amax

        Etot = 0
        try:
            Etot = int(self.Etotvar.get())
        except ValueError:
            Etot = -1
        if Etot > Emax:
            Etot = -1

        Dtot = 0
        try:
            Dtot = int(self.Dtotvar.get())
        except ValueError:
            Dtot = -1

        DC = 0
        try:
            DC = int(self.DCvar.get())
        except ValueError:
            DC = -1

        Ctot = 0
        try:
            Ctot = int(self.Ctotvar.get())
        except ValueError:
            Ctot = -1

        CC = 0
        try:
            CC = int(self.CCvar.get())
        except ValueError:
            CC = -1

        Btot = 0
        try:
            Btot = int(self.Btotvar.get())
        except ValueError:
            Btot = -1

        BA = 0
        try:
            BA = int(self.BAvar.get())
        except ValueError:
            BA = -1

        Atot = 0
        try:
            Atot = int(self.Atotvar.get())
        except ValueError:
            Atot = -1

        AA = 0
        try:
            AA = int(self.AAvar.get())
        except ValueError:
            AA = -1

        if Emax < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för max E-poäng.')
        elif Cmax < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för max C-poäng.')
        elif Amax < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för max A-poäng.')
        elif Etot < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för E-poäng för betyget E.')
        elif Dtot < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för totalpoäng för betyget D.')
        elif DC < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för C/A-poäng för betyget D.')
        elif Ctot < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för totalpoäng för betyget C.')
        elif CC < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för C/A-poäng för betyget C.')
        elif Btot < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för totalpoäng för betyget B.')
        elif BA < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för A-poäng för betyget B.')
        elif Atot < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för totalpoäng för betyget A.')
        elif AA < 0:
            showerror('Fel', 'Felaktig inmatning i rutan för A-poäng för betyget A.')
        elif self.titlevar.get() == '':
            showerror('Fel', 'Fältet för provtitel är tom. Ange en provtitel.')
        else:
            # change self.test to user edits from the GUI:s entries
            tst = self.test
            tst.title = self.titlevar.get()
            tst.max = (Emax, Cmax, Amax)
            tst.gradetemplate.E = Etot
            tst.gradetemplate.D = (Dtot, DC)
            tst.gradetemplate.C = (Ctot, CC)
            tst.gradetemplate.B = (Btot, BA)
            tst.gradetemplate.A = (Atot, AA)

            self.pressed = 'save'
            if self.parent is not None:
                self.parent.focus_set()
            self.win.destroy()

    def cancel(self):
        self.pressed = 'cancel'
        if self.parent is not None:
            self.parent.focus_set()
        self.win.destroy()

    def sumtot(self):
        while not self.pressed:
            try:
                time.sleep(0.5)
                # print('threading!')
                self.sumvar.set(str(int(self.Emaxvar.get())+int(self.Cmaxvar.get())+int(self.Amaxvar.get())))
            except ValueError:
                self.sumvar.set('???')
        # print('threading ends')
