import sumwin
import startwin
from sumwin import SumWin
from tkinter import Tk, Toplevel

if __name__ == '__main__':
    st = startwin.StartWin()
    SumWin.load_session(Toplevel(st), st, 'na20c.dat')
    st.mainloop()
