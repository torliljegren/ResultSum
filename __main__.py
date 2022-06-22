import sumwin
import student
import test
import gradetemplate

tpl = gradetemplate.GradeTemplate(10, (25, 10), (35, 15), (45, 10), (55, 15))
dummy_test1 = test.Test('Prov 1', (20, 18, 12), (0, 0, 0), tpl)
dummy_test2 = test.Test('Prov 2', (22, 20, 15), (0, 0, 0), tpl)
dummy_test3 = test.Test('NP', (26, 24, 18), (0, 0, 0), tpl)

students = []
for i in range(33):
    students.append(student.Student('Elev %i'%(i+1), (dummy_test1, dummy_test2, dummy_test3)))

s = sumwin.SumWin(('Prov 1', 'Prov 2', 'NP'), tuple(students))
s.win.mainloop()