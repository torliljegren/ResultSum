from tkinter import Toplevel, Canvas
from tkinter.constants import BOTH, W
from tkinter.ttk import Frame, Label, LabelFrame, Button
from test import Test
from constants import *

RESULT_RECTANGLE_MAX_HEIGHT = 500



class StudentStatWin(object):

    def __init__(self, sumwin, stutests: tuple, stuname: str):
        self.win = Toplevel(sumwin)
        self.win.title(stuname)
        self.progframe = ProgressFrame(self.win, stutests)
        self.progframe.pack(fill=BOTH)

class ProgressFrame(Frame):

    """
    :param master: widget where this will be added
    :param stutests: tuple containing the tests to be charted
    """
    def __init__(self, master, stutests: tuple):
        super().__init__(master, height=RESULT_RECTANGLE_MAX_HEIGHT*1.3)
        self.chartcanvases = [Canvas(self, borderwidth=2, height=RESULT_RECTANGLE_MAX_HEIGHT*1.3, bg='white') for _ in stutests]

        i = 0
        for cvs in self.chartcanvases:
            Label(self, text=stutests[i].title, font=('helvetica', 14, 'bold')).grid(row=0, column=i, padx=(5,0),
                                                                                     pady=(35,0))
            self.draw_chart(cvs, stutests[i])
            cvs.grid(row=1, column=i, padx=(10,0) if i==0 else (60,0))
            if i==len(self.chartcanvases)-1:
                cvs.grid_configure(padx=(60,10))
            i += 1
        self.pack(fill=BOTH)

    def draw_chart(self, canvas: Canvas, stutest: Test):
        if stutest.gradetemplate.empty():
            return
        PADY = 0
        DASH = (2, 1)
        tlx = 50 # top left x
        tly = 0 # top left y
        bry = RESULT_RECTANGLE_MAX_HEIGHT + PADY # bottom right y
        testmaxpoints = sum(stutest.max)
        if testmaxpoints == 0:
            return

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
        canvas.create_text(tlx-20, bry-eheight-1, text=f'E({stutest.gradetemplate.E})')
        canvas.create_line(tlx, bry-dheight, tlx+RECTANGLE_WIDTH, bry-dheight, dash=DASH)
        canvas.create_text(tlx-20, bry-dheight-1, text=f'D({stutest.gradetemplate.D[0]})')
        canvas.create_line(tlx, bry-cheight, tlx+RECTANGLE_WIDTH, bry-cheight, dash=DASH)
        canvas.create_text(tlx-20, bry-cheight-1, text=f'C({stutest.gradetemplate.C[0]})')
        canvas.create_line(tlx, bry-bheight, tlx+RECTANGLE_WIDTH, bry-bheight, dash=DASH)
        canvas.create_text(tlx-20, bry-bheight-1, text=f'B({stutest.gradetemplate.B[0]})')
        canvas.create_line(tlx, bry-aheight, tlx+RECTANGLE_WIDTH, bry-aheight, dash=DASH)
        canvas.create_text(tlx-20, bry-aheight-1, text=f'A({stutest.gradetemplate.A[0]})')

        # BAR FOR C POINTS #
        # draw the bar and its text
        rheight = (stutest.result[1] + stutest.result[2]) / stutest.max[1] * RESULT_RECTANGLE_MAX_HEIGHT
        if rheight > RESULT_RECTANGLE_MAX_HEIGHT-5:
            rheight = RESULT_RECTANGLE_MAX_HEIGHT-5 # prevent the bar to reach over the top
        tly = bry - rheight
        tlx += 2.5*RECTANGLE_WIDTH
        canvas.create_rectangle(tlx, tly+PADY, tlx + RECTANGLE_WIDTH, bry, fill='linen')
        bottom_text = f'{stutest.result[1]+stutest.result[2]} CAp'
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry+12, text=bottom_text)
        # draw the lines corresponding to the grade criterias that C points enable
        dheight = stutest.gradetemplate.D[1] / stutest.max[1] * RESULT_RECTANGLE_MAX_HEIGHT
        cheight = stutest.gradetemplate.C[1] / stutest.max[1] * RESULT_RECTANGLE_MAX_HEIGHT
        canvas.create_line(tlx, bry-dheight, tlx+RECTANGLE_WIDTH, bry-dheight, dash=DASH)
        canvas.create_text(tlx-20, bry-dheight-1, text=f'D({stutest.gradetemplate.D[1]})')
        canvas.create_line(tlx, bry-cheight, tlx+RECTANGLE_WIDTH, bry-cheight, dash=DASH)
        canvas.create_text(tlx-20, bry-cheight-1, text=f'C({stutest.gradetemplate.C[1]})')

        # BAR FOR A POINTS #
        # draw the bar and its text
        rheight = stutest.result[2] / stutest.max[2] * RESULT_RECTANGLE_MAX_HEIGHT
        if rheight > RESULT_RECTANGLE_MAX_HEIGHT-5:
            rheight = RESULT_RECTANGLE_MAX_HEIGHT-5 # prevent the bar to reach over the top
        tly = bry - rheight
        tlx += 2.5*RECTANGLE_WIDTH
        canvas.create_rectangle(tlx, tly+PADY, tlx + RECTANGLE_WIDTH, bry, fill='linen')
        bottom_text = f'{stutest.result[2]} Ap'
        canvas.create_text(tlx+0.5*RECTANGLE_WIDTH, bry+12, text=bottom_text)
        # draw the lines corresponding to the grade criterias that C points enable
        bheight = stutest.gradetemplate.B[1] / stutest.max[2] * RESULT_RECTANGLE_MAX_HEIGHT
        aheight = stutest.gradetemplate.A[1] / stutest.max[2] * RESULT_RECTANGLE_MAX_HEIGHT
        canvas.create_line(tlx, bry-bheight, tlx+RECTANGLE_WIDTH, bry-bheight, dash=DASH)
        canvas.create_text(tlx-20, bry-bheight-1, text=f'B({stutest.gradetemplate.B[1]})')
        canvas.create_line(tlx, bry-aheight, tlx+RECTANGLE_WIDTH, bry-aheight, dash=DASH)
        canvas.create_text(tlx-20, bry-aheight-1, text=f'A({stutest.gradetemplate.A[1]})')

        # draw a bottom line for the bars to stand on
        canvas.create_line(0, bry, tlx+RECTANGLE_WIDTH, bry)

        # draw a top line representing the max number of points in any category
        canvas.create_line(0, 5, tlx+RECTANGLE_WIDTH, 5, dash=(1,2))

        canvas.config(width=tlx+RECTANGLE_WIDTH+1)

