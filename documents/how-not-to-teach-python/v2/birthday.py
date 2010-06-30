# coding=cp949
from data import birthdays

def inputnum(prompt):
    while True: # ���ѹݺ� (��뿡 ����!)
        line = raw_input(prompt)
        try:
            return int(line)
        except:
            print '���ڸ� �Է��Ͻ���.'

def names(birthdays):
    result = []
    for name, _, _, _ in birthdays:
        result.append(name)
    result.sort()
    return result

def filterbyname(birthdays, targetname):
    return [(name, year, month, day)
            for name, year, month, day
            in birthdays
            if name == targetname]

def filterbyyear(birthdays, targetyear):
    return [(name, year, month, day)
            for name, year, month, day
            in birthdays
            if year == targetyear]

def printnames(birthdays):
    print ', '.join(names(birthdays))

def printbirthdays(birthdays):
    for name, _, month, day in birthdays:
        print '%s - %d�� %d�ϻ�' % (name, month, day)

def printbyname(birthdays):
    name = raw_input('�̸��� �Է��ϼ���: ')
    filtered = filterbyname(birthdays, name)
    printbirthdays(filtered)

def printbyyear(birthdays):
    year = inputnum('������ �Է��ϼ���: ')
    filtered = filterbyyear(birthdays, year)
    printbirthdays(filtered)

def showmenu():
    print '---- �޴� ----'
    print '1. �̸� ����'
    print '2. �̸��� ������� ����'
    print '3. �̸����� ã��'
    print '4. �������� ã��'
    print '0. ������'
    return inputnum('>>> ')

def main():
    choice = showmenu()
    if choice == 1:
        printnames(birthdays)
    elif choice == 2:
        printbirthdays(birthdays)
    elif choice == 3:
        printbyname(birthdays)
    elif choice == 4:
        printbyyear(birthdays)

if __name__ == '__main__': main()

