import math
import tkinter as tk
import tkinter.ttk as ttk
from constants import *

VALID_GRADES = ('F', 'E', 'D', 'C', 'B', 'A')

class StatWin(object):
    def __init__(self, sumwin):
        self.sumwin = sumwin
        self.win = tk.Toplevel(master=self.sumwin.win)
        self.win.title('Betygsstatistik')
        self.mainframe = ttk.Frame(self.win)
        self.mainframe.grid(row=0, column=0)

        tuple_of_tests = self.grade_tuple()
        max_num_grades_per_test = self.max_num_grades(tuple_of_tests)
        print(f'Max registered grades in a test is: {max_num_grades_per_test}')
        nr_of_tests = len(tuple_of_tests)

        # create a grid of canvases and frames for each test and place them horizontally. Between each, put a separator
        self.titleframes = list()
        self.chartcanvases = list()
        additional = 0  # each time a separator i placed, add that to the column in grid()
        for i in range(2*nr_of_tests - 1):
            if i%2 != 0:    # place a separator on odd columns
                ttk.Separator(master=self.mainframe, orient=tk.VERTICAL).grid(row=0, column=i, sticky=tk.NSEW,
                                                                              rowspan=2, padx=10)
                additional += 1
            else:   # place a title, barchart and stats on even columns
                cc = tk.Canvas(self.mainframe)
                self.chartcanvases.append(cc)
                self.draw_barchart(cc, tuple_of_tests[i-additional], max_num_grades_per_test[i-additional])
                cc.grid(row=1, column=i)
                tf = ttk.Frame(self.mainframe)
                self.titleframes.append(tf)
                ttk.Label(master=tf, text=self.sumwin.testtitles[i-additional], font=('helvetica', 14, 'bold')).\
                    grid(row=0, column=0,pady=(15,0))
                tf.grid(row=0, column=i)
                mean, std_dev = self.one_var_stats(tuple_of_tests[i-additional])
                ttk.Label(master=tf, text='Medelvärde: '+str(round(mean, 1))).grid(row=1, column=0)
                ttk.Label(master=tf, text='Stdavvikelse: '+str(round(std_dev, 1))).grid(row=2, column=0)
                framewidth = len(GRADE_COLORS)*RECTANGLE_WIDTH


                cc.configure(width=framewidth)
                tf.configure(width=framewidth)

    def draw_barchart(self, chartcanvas: tk.Canvas, stats: dict, maxnum: int):
        # num_individual_grades = sum(stats.values())
        print('Drawing barchart for:', stats)

        startx = 0
        for grade, numgrade in stats.items():
            height = numgrade/maxnum*RECTANGLE_MAX_HEIGHT*0.9
            chartcanvas.create_rectangle(startx, RECTANGLE_MAX_HEIGHT-height, startx + RECTANGLE_WIDTH, RECTANGLE_MAX_HEIGHT,
                                          fill=GRADE_COLORS[grade])
            chartcanvas.create_text(startx+RECTANGLE_WIDTH/2, RECTANGLE_MAX_HEIGHT-height-12, justify='center',
                                     text=('Ej' if grade=='-' else grade)+':'+str(stats[grade]))
            startx += RECTANGLE_WIDTH

    """
    returns a tuple on the format (mean, stddev)
    """
    def one_var_stats(self, stats: dict) -> tuple:
        # calculate the mean via the sum of all points of the grades
        point_sum = 0
        grade_sum = 0
        for grade, numgrade in stats.items():
            point_sum += numgrade * GRADE_POINTS[grade] if grade in VALID_GRADES else 0
            grade_sum += numgrade if grade in VALID_GRADES else 0
        print(f'Number of grades: {grade_sum}')
        print(f'Point sum of all grades: {point_sum}')
        mean = point_sum/grade_sum if grade_sum != 0 else 0
        print(f'Mean: {mean}')

        # calculate the standard deviation
        quadratic_difference = 0
        for grade, numgrade in stats.items():
            quadratic_difference += stats[grade] * ((GRADE_POINTS[grade] - mean) ** 2) if grade in VALID_GRADES else 0
        std_dev = math.sqrt(quadratic_difference/(grade_sum - 1)) if mean != 0 else 0

        return mean, std_dev


    # returns a tuple of dicts with the number of each grade in each test, and an empty tuple if no tests are defined
    # tuple structure:
    # ( {'invalid':int, 'E':int, 'D':int...}, {...} ... ) i.e. a dict for each test
    def grade_tuple(self) -> tuple:
        # tuple of dicts which hold the number of each grade
        nr_of_tests = len(self.sumwin.student_rows[0].test_entries)
        stats = [{'-':0,
                  'F':0,
                  'E':0,
                  'D':0,
                  'C':0,
                  'B':0,
                  'A':0} for _ in range(nr_of_tests)]

        # iterate through all students tests and increment the grade counts
        for row in self.sumwin.student_rows:
            testnr = 0
            for testentry in row.test_entries:
                g = testentry.gradeentry.get()
                if g in VALID_GRADES:
                    stats[testnr][g] += 1
                else:
                    stats[testnr]['-'] += 1
                testnr += 1
        return tuple(stats)

    """
    Given n tests in the gradetuple, determine the maximum number of a grade given
    """
    def max_num_grades(self, gradetuple: tuple) -> tuple:
        maxtestnums = list()
        for gr_t in gradetuple:
            max_g = 0
            for num in gr_t.values():
                if num > max_g:
                    max_g = num
            maxtestnums.append(max_g)
        return tuple(maxtestnums)

