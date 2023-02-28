from tkinter import Toplevel, Canvas, BOTH
from tkinter.ttk import Frame, Label, LabelFrame, Button
from test import Test
from constants import *

RESULT_RECTANGLE_MAX_HEIGHT = 500



class StudentStatWin(object):

    def __init__(self, sumwin, stutests: tuple):
        self.win = Toplevel(sumwin)
        self.progframe = ProgressFrame(self.win, stutests)
        self.progframe.pack(fill=BOTH)

class ProgressFrame(Frame):

    """
    :param master: widget where this will be added
    :param stutests: tuple containing the tests to be charted
    """
    def __init__(self, master, stutests: tuple):
        super().__init__(master, height=RESULT_RECTANGLE_MAX_HEIGHT*1.3)
        self.chartcanvases = [Canvas(self, borderwidth=2, height=RESULT_RECTANGLE_MAX_HEIGHT*1.3) for _ in stutests]

        i = 0
        for cvs in self.chartcanvases:
            Label(self, text=stutests[i].title, font=('helvetica', 14, 'bold')).grid(row=0, column=i)
            self.draw_chart(cvs, stutests[i])
            cvs.grid(row=1, column=i)
            i += 1
        self.pack(fill=BOTH)

    def draw_chart(self, canvas: Canvas, stutest: Test):
        PADY = 0
        DASH = (2, 1)
        tlx = 10 # top left x
        tly = 0 # top left y
        bry = RESULT_RECTANGLE_MAX_HEIGHT + PADY # bottom right y
        testmaxpoints = sum(stutest.max)

        # BAR FOR TOTAL POINTS #
        # draw the bar and its text
        rheight = sum(stutest.result) / testmaxpoints * RESULT_RECTANGLE_MAX_HEIGHT
        tly = bry - rheight
        canvas.create_rectangle(tlx, tly+PADY, tlx + RECTANGLE_WIDTH, bry, fill='linen')
        bottom_text = f'{sum(stutest.result)} Tp'
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry+12, text=bottom_text)
        # draw the lines corresponding to the grade criterias
        eheight = stutest.gradetemplate.E / testmaxpoints * RESULT_RECTANGLE_MAX_HEIGHT
        dheight = stutest.gradetemplate.D[0] / testmaxpoints * RESULT_RECTANGLE_MAX_HEIGHT
        cheight = stutest.gradetemplate.C[0] / testmaxpoints * RESULT_RECTANGLE_MAX_HEIGHT
        bheight = stutest.gradetemplate.B[0] / testmaxpoints * RESULT_RECTANGLE_MAX_HEIGHT
        aheight = stutest.gradetemplate.A[0] / testmaxpoints * RESULT_RECTANGLE_MAX_HEIGHT
        canvas.create_line(tlx, bry-eheight, tlx+RECTANGLE_WIDTH, bry-eheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-eheight-12, text='E')
        canvas.create_line(tlx, bry-dheight, tlx+RECTANGLE_WIDTH, bry-dheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-dheight-12, text='D')
        canvas.create_line(tlx, bry-cheight, tlx+RECTANGLE_WIDTH, bry-cheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-cheight-12, text='C')
        canvas.create_line(tlx, bry-bheight, tlx+RECTANGLE_WIDTH, bry-bheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-bheight-12, text='B')
        canvas.create_line(tlx, bry-aheight, tlx+RECTANGLE_WIDTH, bry-aheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-aheight-12, text='A')

        # BAR FOR C POINTS #
        # draw the bar and its text
        rheight = (stutest.result[1] + stutest.result[2]) / stutest.max[1] * RESULT_RECTANGLE_MAX_HEIGHT
        tly = bry - rheight
        tlx += 2*RECTANGLE_WIDTH
        canvas.create_rectangle(tlx, tly+PADY, tlx + RECTANGLE_WIDTH, bry, fill='linen')
        bottom_text = f'{stutest.result[1]+stutest.result[2]} CAp'
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry+12, text=bottom_text)
        # draw the lines corresponding to the grade criterias that C points enable
        dheight = stutest.gradetemplate.D[1] / stutest.max[1] * RESULT_RECTANGLE_MAX_HEIGHT
        cheight = stutest.gradetemplate.C[1] / stutest.max[1] * RESULT_RECTANGLE_MAX_HEIGHT
        canvas.create_line(tlx, bry-dheight, tlx+RECTANGLE_WIDTH, bry-dheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-dheight-12, text='D')
        canvas.create_line(tlx, bry-cheight, tlx+RECTANGLE_WIDTH, bry-cheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-cheight-12, text='C')

        # BAR FOR A POINTS #
        # draw the bar and its text
        rheight = stutest.result[2] / stutest.max[2] * RESULT_RECTANGLE_MAX_HEIGHT
        tly = bry - rheight
        tlx += 2*RECTANGLE_WIDTH
        canvas.create_rectangle(tlx, tly+PADY, tlx + RECTANGLE_WIDTH, bry, fill='linen')
        bottom_text = f'{stutest.result[2]} Ap'
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry+12, text=bottom_text)
        # draw the lines corresponding to the grade criterias that C points enable
        bheight = stutest.gradetemplate.B[1] / stutest.max[2] * RESULT_RECTANGLE_MAX_HEIGHT
        aheight = stutest.gradetemplate.A[1] / stutest.max[2] * RESULT_RECTANGLE_MAX_HEIGHT
        canvas.create_line(tlx, bry-bheight, tlx+RECTANGLE_WIDTH, bry-bheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-bheight-12, text='B')
        canvas.create_line(tlx, bry-aheight, tlx+RECTANGLE_WIDTH, bry-aheight, dash=DASH)
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry-aheight-12, text='A')

