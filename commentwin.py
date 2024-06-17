from tkinter.ttk import Frame
from tkinter import Text, Toplevel
from student import Student

class CommentWin(object):
    def __init__(self, master, student):
        super().__init__()
        self.master = master
        self.student = student

        self.win = Toplevel(master)
        self.win.title(self.student.name)
        self.mainframe = Frame(master=self.win)
        self.textarea = Text(master=self.mainframe)

    def generate_text(self):
        text = f'Kommentarer för {self.student.name}: \n'
        self.textarea.insert(0, text)