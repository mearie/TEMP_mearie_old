# coding=cp949
from data import birthdays

def printnames(birthdays):
    print 'TODO: �̸� ����� ���'

def printbirthdays(birthdays):
    print 'TODO: �̸��� ������� ���'

def printbyname(birthdays):
    print 'TODO: �̸��� �Է¹޾� �ش��ϴ� ��������� ���'

def printbyyear(birthdays):
    print 'TODO: ������ �Է¹޾� �ش��ϴ� ����� ���'

def showmenu():
    print '---- �޴� ----'
    print '1. �̸� ����'
    print '2. �̸��� ������� ����'
    print '3. �̸����� ã��'
    print '4. �������� ã��'
    return input('>>> ')

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

