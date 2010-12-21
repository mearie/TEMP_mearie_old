# coding=cp949

class person(object):
    def __init__(self, name, year,
                 month, day):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
    def __str__(self):
        return '%s - %d월 %d일생' % \
               (self.name, self.month, self.day)

birthdays = [
    person('강성훈', 1987, 9, 13),
    person('정재성', 1987, 2, 23),
    person('김준기', 1987, 5, 12),
    person('안병욱', 1989, 10, 14),
    person('강철', 1990, 3, 11),
    person('유수형', 1991, 3, 13),
    person('조유정', 1990, 4, 18),
    person('김도국', 1990, 3, 11),
]
