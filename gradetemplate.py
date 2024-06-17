class GradeTemplate(object):
    # first element of tuple is total required points
    # second element of tuple is the amount of nivåpoäng needed
    # grade E only requires a total sum, hence E is an int
    def __init__(self, E: int, D: tuple[int, int], C: tuple[int, int], B: tuple[int, int], A: tuple[int, int]):
        self.E = E
        self.D = D
        self.C = C
        self.B = B
        self.A = A

    def copy(self) -> 'GradeTemplate':
        tempE = self.E
        tempD = (self.D[0], self.D[1])
        tempC = (self.C[0], self.C[1])
        tempB = (self.B[0], self.B[1])
        tempA = (self.A[0], self.A[1])

        return GradeTemplate(tempE, tempD, tempC, tempB, tempA, self.comment)

    def empty(self) -> bool:
        return self.E<1 and sum(self.D)<1 and sum(self.C)<1 and sum(self.B)<1 and sum(self.A)<1


    def __str__(self):
        return str(self.E)+str(self.D)+str(self.C)+str(self.B)+str(self.A)

    def __eq__(self, other):
        return self.E == other.E and self.D == other.D and self.C == other.C and self.B == other.B and self.A == other.A
