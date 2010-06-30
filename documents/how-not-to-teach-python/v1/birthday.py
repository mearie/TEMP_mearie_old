# coding=cp949
from data import birthdays

def printnames(birthdays):
    print 'TODO: 이름 목록을 출력'

def printbirthdays(birthdays):
    print 'TODO: 이름과 생년월일 출력'

def printbyname(birthdays):
    print 'TODO: 이름을 입력받아 해당하는 생년월일을 출력'

def printbyyear(birthdays):
    print 'TODO: 생년을 입력받아 해당하는 목록을 출력'

def showmenu():
    print '---- 메뉴 ----'
    print '1. 이름 보기'
    print '2. 이름과 생년월일 보기'
    print '3. 이름으로 찾기'
    print '4. 생년으로 찾기'
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

