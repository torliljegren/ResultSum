from gradetemplate import *


class Test(object):
    #                              (E, C, A)        (E, C, A)
    def __init__(self, title: str, max: tuple[int, int, int], result: tuple[int, int, int], grades: GradeTemplate,
                 active=True, standard=True):
        self.active:bool = active
        self.standard:bool = standard
        self.title:str = title
        self.max:tuple[int, int, int] = max
        self.result:list[int, int, int] = list(result) if result is not None else []
        self.gradetemplate = grades

    def sum_result(self) -> int:
        return sum(self.result)

    def sum_max(self) -> int:
        return sum(self.max)

    def grade(self) -> str:
        if self.result is None:
            return '-'
        elif sum(self.result) == 0:
            return '-'
        elif not self.active:
            return '-'

        res = self.sum_result()

        if res >= self.gradetemplate.A[0] and self.result[2] >= self.gradetemplate.A[1]:
            return 'A'
        elif res >= self.gradetemplate.B[0] and self.result[2] >= self.gradetemplate.B[1]:
            return 'B'
        elif res >= self.gradetemplate.C[0] and self.result[2] + self.result[1] >= self.gradetemplate.C[1]:
            return 'C'
        elif res >= self.gradetemplate.D[0] and self.result[2] + self.result[1] >= self.gradetemplate.D[1]:
            return 'D'
        elif res >= self.gradetemplate.E:
            return 'E'
        else:
            return 'F'

    def copy(self) -> 'Test':
        tempmax = (self.max[0], self.max[1], self.max[2])
        tempresult = [i for i in self.result]
        temptemplate = self.gradetemplate.copy()
        return Test(self.title, tempmax, tempresult, temptemplate, self.active, bool(self.standard))

    def __str__(self) -> str:
        if not self.result and not self.max:
            return 'tom'
        return '%s. Poäng: %d/%d/%d. Betyg: %s.' % (self.title, self.result[0], self.result[1],
                                                    self.result[2], self.grade())

    def __eq__(self, other):
        return self.title == other.title and self.max == other.max and self.result == other.result and\
                self.gradetemplate == other.gradetemplate


if __name__ == '__main__':
    g1 = GradeTemplate((12), (21, 5), (30, 11), (35, 3), (40, 5))
    g2 = GradeTemplate((12), (21, 5), (30, 11), (35, 3), (40, 5))
    maxp = (20, 20, 10)
    ta = Test('Prov A', maxp, (20, 18, 8), g1)
    tb = Test('Prov A', maxp, (20, 18, 8), g2)
    tc = Test('Prov F', maxp, (4, 1, 1), g1)
    tnone = Test('Prov ej', maxp, None, g2)
    print(f'ta==tb: {ta==tb}')
    print(ta)
    print(tb)
    print(tc)
