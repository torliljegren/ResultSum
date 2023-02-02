from test import Test

class Student(object):
    def __init__(self, name: str, tests: tuple[Test]=None):
        self.name = name

        if tests is not None:
            self.tests = list(tests)
        else:
            self.tests = []

