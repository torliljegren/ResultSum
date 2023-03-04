# encoding: utf-8
import tkinter
from tkinter import Tk
from tkinter import StringVar
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk as ttk
import platform
from sumwin import SumWin
from student import Student
from test import Test
from gradetemplate import GradeTemplate

class StartWin(Tk):
    def __init__(self):

        super().__init__()
        self.TITLE_FONT = (None, 14, 'bold')
        self.HEADING_FONT = (None, 12, 'bold')
        self.sumwin: SumWin = None
        self.destroyed = False
        self.withdraw()
        self.attributes('-alpha', 0)
        self.title("Bedömningsmall")
        self.resizable(False, False)

        self.style = tkinter.ttk.Style()
        if platform.system() == "Linux":
            self.style.theme_use("clam")
            self.style.configure('TButton', background='snow2')
        else:
            self.style.configure('TButton', background='snow2' if platform.system() == 'Linux' else None)

        # Create GUI elements

        self.mainframe = ttk.Frame(self)
        self.entry_strip = ttk.Frame(self.mainframe)
        self.button_strip = ttk.Frame(self.mainframe)

        self.label_heading = ttk.Label(self.mainframe, text="Ny bedömningsmall", font=self.TITLE_FONT)

        self.label_subject = ttk.Label(self.entry_strip, text="Kursnamn: ", font=self.HEADING_FONT)
        self.var_subject = StringVar(self.entry_strip)
        self.entry_subject = ttk.Entry(self.entry_strip, textvariable=self.var_subject)

        self.label_class = ttk.Label(self.entry_strip, text="Klass: ", font=self.HEADING_FONT)
        self.var_class = StringVar(self.entry_strip)
        self.entry_class = ttk.Entry(self.entry_strip, textvariable=self.var_class)

        self.label_students = ttk.Label(self.entry_strip, text="Antal elever: ", font=self.HEADING_FONT)
        self.var_students = StringVar(self.entry_strip, value='33')
        self.entry_students = ttk.Entry(self.entry_strip, textvariable=self.var_students)
        self.entry_students.icursor(tkinter.END)

        self.label_tests = ttk.Label(self.entry_strip, text="Antal prov: ", font=self.HEADING_FONT)
        self.var_tests = StringVar(self.entry_strip, value='3')
        self.entry_tests = ttk.Entry(self.entry_strip, textvariable=self.var_tests)
        self.entry_tests.icursor(tkinter.END)

        self.button_ok = ttk.Button(self.button_strip, text="Klar", width=10, command=self.ok_press,
                                    style='EditTestWin.TButton')
        self.button_load = ttk.Button(self.button_strip, text="Öppna", width=10, command=self.load_press,
                                      style='EditTestWin.TButton')


        self.setup_info_gui()

        self.bind("<Return>", lambda u: self.ok_press())
        self.bind('<FocusIn>', self.handle_focus)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        # center the window
        # avoid unwanted "flashing" by making window transparent until fully ready
        self.update_idletasks()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 6) #- (h / 2)
        self.geometry('+%d+%d' % (x, y))
        self.attributes('-alpha', 1)
        self.deiconify()

    def setup_info_gui(self):
        # Layout GUI elements
        paddy=4
        self.mainframe.grid(row=0, column=0, sticky="nsew")
        self.entry_strip.grid(row=1, column=1, padx=60)
        self.button_strip.grid(row=2,column=1, columnspan=2, pady=20)

        self.label_heading.grid(row=0, column=1, pady=20, padx=10, columnspan=2)

        self.label_subject.grid(row=2, column=1, sticky="E")
        self.entry_subject.grid(row=2, column=2, pady=paddy)

        self.label_class.grid(row=3, column=1, sticky="E")
        self.entry_class.grid(row=3, column=2, pady=paddy)

        self.label_students.grid(row=4, column=1, sticky="E")
        self.entry_students.grid(row=4, column=2, pady=paddy)

        self.label_tests.grid(row=5, column=1, sticky="E")
        self.entry_tests.grid(row=5, column=2, pady=paddy)

        self.button_ok.grid(row=1, column=1, padx=10, pady=10)
        self.button_load.grid(row=1, column=2,padx=10,pady=10)

    def handle_focus(self, e: tkinter.Event):
        if e.widget == self:
            print('startwin in focus')
            self.attributes("-topmost", True)
            self.focus_set()
            self.entry_subject.focus_set()
            self.attributes("-topmost", False)

    def on_quit(self):
        if self.destroyed:
            pass
        else:
            self.destroyed = True
            self.destroy()

    def ok_press(self):
        # Create the subject from info from entries
        s_name = self.entry_subject.get()
        group = self.entry_class.get()
        start = 0
        end = 0
        try:
            numstus = int(self.var_students.get())
        except ValueError:
            tkinter.messagebox.showerror(title="Fel antal elever", message="Antalet elever som angavs: "+self.var_students.get()+
                                                                         " är inte ett giltigt tal.")
            return

        try:
            numtests = int(self.entry_tests.get())
        except ValueError:
            tkinter.messagebox.showerror(title="Fel antal prov", message="Antalet prov som angavs: "+self.var_tests.get()+
                                                                        " är inte ett giltigt tal.")
            return

        if numstus<1:
            tkinter.messagebox.showerror(title="Fel antal elever", message="Antalet elever kan inte vara negativt.")
            return
        elif numtests<1:
            tkinter.messagebox.showerror(title="Fel antal prov", message="Antalet prov kan inte vara negativt.")
            return

        self.iconify()
        self.open_sumwin()

    def open_sumwin(self):
        ntests = int(self.var_tests.get())
        nstus = int(self.var_students.get())

        students = list()
        dummy_tests = list()
        for stuindex in range(nstus):
            for testindex in range(ntests):
                dummy_tests.append(Test(f'Prov {testindex + 1}', (0, 0, 0), (0, 0, 0),
                                             GradeTemplate(1, (1, 1), (1, 1), (1, 1), (1, 1))
                                             )
                                   )
            students.append(Student('Elev '+str(stuindex+1), tuple(dummy_tests)))
            dummy_tests = list()

        s = SumWin(tuple([tst.title for tst in students[0].tests]), tuple(students), master=self,
                          root=tkinter.Toplevel(self), course=self.var_subject.get(), group=self.var_class.get())
        self.clear_entries()


    def load_press(self):
        fpath = tkinter.filedialog.askopenfilename(filetypes=(('Bedömningsmall', '*.dat'),), parent=self)
        if fpath:
            sw = tkinter.Toplevel(master=self)
            sw.iconify()
            status = SumWin.load_session(win=sw, filepath=fpath, master=self)
            if status != -1:
                sw.deiconify()
                self.iconify()
                self.clear_entries()
            else:
                sw.destroy()


    def clear_entries(self):
        self.var_tests.set("3")
        self.var_subject.set("")
        self.var_class.set("")
        self.var_students.set("33")


# ENTRY POINT
if __name__ == "__main__":
    # open the start window
    app_start = StartWin()
    app_start.mainloop()
