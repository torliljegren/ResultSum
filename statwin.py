import tkinter as tk
import tkinter.ttk as ttk
# from sumwin import SumWin
from student_row import StudentRow
from student_test_entry import StudentTestEntry

# constants for painting the bar chart
RECTANGLE_WIDTH = 50
RECTANGLE_MAX_HEIGHT = 200
GRADE_COLORS = {"-" : "grey",
                "F" : "red",
                "E" : "limegreen",
                "D" : "green",
                "C" : "blue",
                "B" : "indigo",
                "A" : "violet"}

class StatWin(object):
    def __init__(self, sumwin):
        self.sumwin = sumwin
        self.win = tk.Toplevel(master=self.sumwin.win)
        self.mainframe = ttk.Frame(self.win)
        self.mainframe.grid(row=0, column=0)

        tuple_of_tests = self.grade_tuple()
        nr_of_tests = len(tuple_of_tests)

        # create a grid of canvases and frames for each test and place them horizontally
        self.titleframes = list()
        self.chartframes = list()
        for i in range(nr_of_tests):
            cf = ttk.Frame(self.mainframe, borderwidth=1)
            self.chartframes.append(cf)
            self.draw_barchart(cf, tuple_of_tests[i])
            cf.grid(row=0, column=i)
            tf = ttk.Frame(self.mainframe)
            self.titleframes.append(tf)
            ttk.Label(master=tf, text=self.sumwin.testtitles[i]).grid(row=0, column=0)
            tf.grid(row=1, column=i)

    def draw_barchart(self, chartframe: ttk.Frame, stats: dict):
        chart_canvas = tk.Canvas(chartframe)
        num_individual_grades = sum(stats.values())

        startx = 0
        for grade, numgrade in stats.items():
            chart_canvas.create_rectangle(startx, 0, startx + RECTANGLE_WIDTH,
                                          numgrade/num_individual_grades*RECTANGLE_MAX_HEIGHT,
                                          fill=GRADE_COLORS[grade])
            startx += RECTANGLE_WIDTH
            chart_canvas.pack()


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
