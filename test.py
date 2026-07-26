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
"""

import sys
a,b = sys.stdin.readline().strip().split()
a = int(a)
b = int(b)
print(a*b)