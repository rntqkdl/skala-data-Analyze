"""
[해답 01] 빠른 입출력 및 조건별 합계 구하기 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. sys.stdin.readline():
   - input() 함수는 입력값이 많아질 경우 속도가 저하되므로, sys.stdin.readline()을 사용하면 
     입력 속도를 획기적으로 개선할 수 있습니다.
   - 개행문자(\n)가 포함되므로 보통 .strip() 또는 .split()과 함께 사용합니다.

2. map(int, sys.stdin.readline().split()):
   - 공백 단위로 쪼개진 문자열 리스트를 정수(int)형으로 일괄 변환하여 리스트로 만듭니다.
"""

import sys

def main():
    # 1. 정수 N 입력받기
    n = int(sys.stdin.readline().strip())
    
    # 2. N개의 정수 리스트로 입력받기
    numbers = list(map(int, sys.stdin.readline().split()))

    # 3. 홀수합과 짝수합 계산
    odd_sum = sum(x for x in numbers if x % 2 != 0)
    even_sum = sum(x for x in numbers if x % 2 == 0)

    # 4. 결과 출력
    print(f"{odd_sum} {even_sum}")

if __name__ == "__main__":
    main()
