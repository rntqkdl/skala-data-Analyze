"""
[해답 02] 리스트 컴프리헨션을 이용한 필터링 및 데이터 변환 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 리스트 컴프리헨션 문법:
   - 기본 구조: `[표현식 for 변수 in 반복가능객체 if 조건문]`
   - 여러 조건 연결: `if x % 3 == 0 and x % 2 == 0` 또는 `if x % 6 == 0` (3과 2의 최소공배수는 6)

2. for문과의 비교:
   - 일반 for문 대신 리스트 컴프리헨션을 사용하면 코드가 매우 간결해지고 파이썬 내부 C 구현으로 인해 
     실행 속도가 향상됩니다.
"""

import sys

def main():
    numbers = list(map(int, sys.stdin.readline().split()))

    # 리스트 컴프리헨션 작성
    # 3의 배수이면서 짝수 (즉, 6의 배수)인 값에 10을 더함
    result = [x + 10 for x in numbers if x % 3 == 0 and x % 2 == 0]

    print(result)

if __name__ == "__main__":
    main()
