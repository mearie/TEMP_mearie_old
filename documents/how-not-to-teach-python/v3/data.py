# coding=cp949

class person(object):
    def __init__(self, name, year,
                 month, day):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
    def __str__(self):
        return '%s - %d�� %d�ϻ�' % \
               (self.name, self.month, self.day)

birthdays = [
    person('������', 1987, 9, 13),
    person('���缺', 1987, 2, 23),
    person('���ر�', 1987, 5, 12),
    person('�Ⱥ���', 1989, 10, 14),
    person('��ö', 1990, 3, 11),
    person('������', 1991, 3, 13),
    person('������', 1990, 4, 18),
    person('�赵��', 1990, 3, 11),
]
