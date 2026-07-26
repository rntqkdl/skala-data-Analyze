"""
python 코테 준비
1. input()은 데이터가 커지면 느려서 sys.stdin.readline()을 쓰는게 좋다.

# 1. 데이터 단일로 입력받기.
n = int(input())
print(f"data: {n}")

# 2. 데이터 여러개 입력받기.
a,b = map(int, input().split())
print(a+b)

# sys.stdin.readline()
import sys
text = sys.stdin.readline().strip()  # rstrip()을 붙여서 개행문자 제거
print(text)

4. 두 정수 A와 B가 주어졌을 때, A와 B를 곱하는 프로그램을 작성하시오.
단, sys.stdin.readline()을 사용하여 입력을 받아야 한다.

import sys
a,b = sys.stdin.readline().strip().split()
a = int(a)
b = int(b)
print(a*b)
"""

# 한 줄에 입력 된 여러 개의 숫자를 공백 기준으로 쪼개서 정수형 리스트에 저장하기. 
import sys
numbers = list(map(int, sys.stdin.readline().split())) # 10 20 30 40 50 -> ['10', '20', '30', '40', '50'] =-> [10, 20, 30, 40, 50]

print(numbers)

# 응용 해보기 첫 줄에 여러 개의 정수들이 공백으로 구분되어 주어집니다. 이 정수들 중에서 가장 큰 값을 찾아 출력 하는 프로그램을 만드시오.
print(max(numbers))