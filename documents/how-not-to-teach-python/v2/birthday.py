# coding=cp949
from data import birthdays

def inputnum(prompt):
    while True: # 무한반복 (사용에 주의!)
        line = raw_input(prompt)
        try:
            return int(line)
        except:
            print '숫자를 입력하시죠.'

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
        print '%s - %d월 %d일생' % (name, month, day)

def printbyname(birthdays):
    name = raw_input('이름을 입력하세요: ')
    filtered = filterbyname(birthdays, name)
    printbirthdays(filtered)

def printbyyear(birthdays):
    year = inputnum('생년을 입력하세요: ')
    filtered = filterbyyear(birthdays, year)
    printbirthdays(filtered)

def showmenu():
    print '---- 메뉴 ----'
    print '1. 이름 보기'
    print '2. 이름과 생년월일 보기'
    print '3. 이름으로 찾기'
    print '4. 생년으로 찾기'
    print '0. 끝내기'
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

