# coding=cp949
from data import birthdays

def inputnum(prompt):
    while True: # ���ѹݺ� (��뿡 ����!)
        line = raw_input(prompt)
        try:
            return int(line)
        except:
            print '���ڸ� �Է��Ͻ���.'

def printnames(birthdays):
    names = [p.name for p in birthdays]
    names.sort()
    print ', '.join(names)

def printbirthdays(birthdays):
    for p in birthdays: print p

def printbyname(birthdays):
    name = raw_input('�̸��� �Է��ϼ���: ')
    filtered = [p for p in birthdays if p.name == name]
    printbirthdays(filtered)

def printbyyear(birthdays):
    year = inputnum('������ �Է��ϼ���: ')
    filtered = [p for p in birthdays if p.year == year]
    printbirthdays(filtered)

CHOICES = {1: printnames, 2: printbirthdays,
           3: printbyname, 4: printbyyear}
def showmenu():
    print '---- �޴� ----'
    print '1. �̸� ����'
    print '2. �̸��� ������� ����'
    print '3. �̸����� ã��'
    print '4. �������� ã��'
    print '0. ������'
    choice = inputnum('>>> ')
    if choice in CHOICES:
        return CHOICES[choice]

def main():
    while True:
        routine = showmenu()
        if not routine: return
        routine(birthdays)
        print

if __name__ == '__main__': main()

