import tkinter as tk
import tkinter.ttk as ttk
from sumwin import SumWin
from student_row import StudentRow
from student_test_entry import StudentTestEntry

# constants for painting the bar chart
RECTANGLE_WIDTH = 10
RECTANGLE_MAX_HEIGHT = 100
INVALID_COLOR = 'red'
F_COLOR = 'orange'
E_COLOR = 'yellow'
D_COLOR = 'green'
C_COLOR = 'blue'
B_COLOR = 'indigo'
A_COLOR = 'violet'

class StatWin(object):
    def __init__(self, sumwin: SumWin):
        self.sumwin = sumwin
        self.win = tk.Toplevel(master=self.sumwin)
        self.mainframe = ttk.Frame(self.win)
        self.mainfram.grid(row=0, column=0)

        nr_of_tests = len(self.sumwin.student_rows[0].test_entries)

        # create a grid of canvases and frames for each test
        self.titleframes = list()
        self.chartframes = list()
        for i in range(nr_of_tests):
            cf = ttk.Frame(self.mainframe)
            cf.grid(row=0, column=i)
            tf = ttk.Frame(self.mainframe)
            ttk.Label(master=tf, text=self.sumwin.testtitles[i]).grid(row=0, column=0)
            tf.grid(row=1, column=i)

    def draw_barchart(self, chartframe: ttk.Frame, stats: dict):
        pass

    # returns a tuple of dicts with the number of each grade in each test, and an empty tuple if no tests are defined
    # tuple structure:
    # ( {'invalid':int, 'E':int, 'D':int...}, ... ) i.e. a dict for each test
    def grade_tuple(self) -> tuple:
        # list of dicts to hold the number of each grade
        nr_of_tests = len(self.sumwin.student_rows[0].test_entries)
        stats = [{'-':0,
                  'F':0,
                  'E':0,
                  'D':0,
                  'C':0,
                  'B':0,
                  'A':0} for i in range(nr_of_tests)]

        # iterate through all students tests and increment the grade counts
        valid_grades = ('F', 'E', 'D', 'C', 'B', 'A')
        for row in self.sumwin.student_rows:
            testnr = 0
            for testentry in row.test_entries:
                g = testentry.gradeentry.get()
                if g in valid_grades:
                    stats[testnr][g] += 1
                else:
                    stats[testnr]['-'] += 1
                testnr += 1
        return tuple(stats)
