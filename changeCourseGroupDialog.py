from tkinter import *
from tkinter.simpledialog import Dialog

class ChangeCourseGroupDialog(Dialog):

    def body(self, master):

        Label(master, text="Kurs:").grid(row=0)
        Label(master, text="Klass:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def apply(self):
        self.result = (self.e1.get(), self.e2.get())


if __name__ == '__main__':
    root = Tk()
    dia = ChangeCourseGroupDialog(root, 'Ändra info')
    print(dia.result)
