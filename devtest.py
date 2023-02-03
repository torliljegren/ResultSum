import sumwin
from startwin import StartWin
from sumwin import SumWin
from tkinter import Tk, Toplevel

if __name__ == '__main__':
    st = StartWin()
    SumWin.load_session(Toplevel(st), st, 'na20c.dat')

    st.mainloop()
