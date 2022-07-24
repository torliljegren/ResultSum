import test
import gradetemplate
import student_row
import student_test_entry
import xlsxwriter as xlw

class ExcelExporter(object):

    def __init__(self, fname: str, student_rows: list[student_row.StudentRow], tests: tuple[test.Test], course: str,
                 group: str):
        wb = xlw.Workbook(filename=fname)
        ws = wb.add_worksheet()

        # write course and class info on row 0
        ws.write(0, 0, f'{course} med {group}')

        # write headings at row 2
        colcounter = 0
        for tst in tests:
            ws.write(2, colcounter, tst.title)
            colcounter += 1

        # write names starting on row 3
        rowcounter = 3
        for sturow in student_rows:
            ws.write(rowcounter, 0, sturow.namevar.get())
            rowcounter += 1

        # write test data starting at row 3
        rowcounter = 3
        for sturow in student_rows:
            colcounter = 0
            for entry in sturow.test_entries:
                colcounter += 1
            rowcounter += 1
