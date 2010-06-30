# coding=cp949
from data import birthdays

def inputnum(prompt):
    while True: # 무한반복 (사용에 주의!)
        line = raw_input(prompt)
        try:
            return int(line)
        except:
            print '숫자를 입력하시죠.'

def printnames(birthdays):
    names = [p.name for p in birthdays]
    names.sort()
    print ', '.join(names)

def printbirthdays(birthdays):
    for p in birthdays: print p

def printbyname(birthdays):
    name = raw_input('이름을 입력하세요: ')
    filtered = [p for p in birthdays if p.name == name]
    printbirthdays(filtered)

def printbyyear(birthdays):
    year = inputnum('생년을 입력하세요: ')
    filtered = [p for p in birthdays if p.year == year]
    printbirthdays(filtered)

CHOICES = {1: printnames, 2: printbirthdays,
           3: printbyname, 4: printbyyear}
def showmenu():
    print '---- 메뉴 ----'
    print '1. 이름 보기'
    print '2. 이름과 생년월일 보기'
    print '3. 이름으로 찾기'
    print '4. 생년으로 찾기'
    print '0. 끝내기'
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

