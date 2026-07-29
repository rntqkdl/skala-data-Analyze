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

# 한 줄에 입력 된 여러 개의 숫자를 공백 기준으로 쪼개서 정수형 리스트에 저장하기. 
import sys
numbers = list(map(int, sys.stdin.readline().split())) # 10 20 30 40 50 -> ['10', '20', '30', '40', '50'] =-> [10, 20, 30, 40, 50]

print(numbers)

# 응용 해보기 첫 줄에 여러 개의 정수들이 공백으로 구분되어 주어집니다. 이 정수들 중에서 가장 큰 값을 찾아 출력 하는 프로그램을 만드시오.
print(max(numbers))
"""
"""
# 첫 줄에는 데이터의 개수(N), 둘째 줄에는 N개의 숫자가 공백으로 주어지는 형태 다뤄보기.
(입력 예시)
5
10 20 30 40 50(입력 예시)


import sys
# 1. 데이터의 개수(N) 입력받기
n = int(sys.stdin.readline())

# 2. 두 번째 줄 : N개의 숫자를 리스트로 한 번에 입력받기
numbers = list(map(int, sys.stdin.readline().split()))

print(f"입력된 데이터의 개수: {n}")
print(f"입력된 리스트: {numbers}")
"""
"""
응용 해보기 (미니 실습)
첫 줄에 정수의 개수 $N$이 주어지고, 둘째 줄에는 $N개의 정수$가 공백으로 주어집니다.
이 $N개의 정수의 합(Sum)$을 구해서 출력하는 프로그램을 작성해 보세요.

import sys
n = int(sys.stdin.readline())

numbers = list(map(int, sys.stdin.readline().split()))

print(f"{sum(numbers)}")
"""

"""
리스트 컴프리 헨션
1. 개념 이해하기 입력 받은 값들을 특정 조건에 따라 변형 및 필터링 하여 리스트로 만들기. for 문과의 비교

# 1부터 5까지 제곱한 리스트 만들고 싶음.
result = []
for i in range(1,6):
    result.append(i*i)
print(result)

# 리스트 컴프리 헨션으로 바꾸기
# 대괄호 안에 [표현식 for 변수 in 반복가능 객체]를 넣는다.
result = [i*i for i in range(1,6)]
print(result)

# 리스트 컴프리 헨션으로 1부터 10까지의 수 중에서 짝수만 제곱한 리스트 만들기
result = [i * i for i in range(1,11) if i % 2 == 0]
print(result)

# 미니 실습

[문제]
공백으로 구분된 여러 개의 정수가 한 줄에 입력됩니다.
이 정수들 중에서 음수(-)는 모두 제외하고, 0 이상의 값들만 골라낸 뒤 각각 2를 곱한 결과를 리스트로 만들어 출력하는 프로그램을 작성해 보세요.
(예시 입력: -3 5 -1 0 4 -8 2 / 출력된 리스트: [10, 0, 8, 4])

import sys
numbers = list(map(int,sys.stdin.readline().split()))
result = [i * 2 for i in numbers if i >= 0]
print(result)


"""
"""
Stack : LIFO (Last-In-Firs-Out)
먼저들어온 것이 먼저나감 -> 데이터가 많아지면 pop() 사용 시 맨 앞의 값을 지울때마다 데이터들이 이동하면서 시간초과가 발생함.
-> collections.deque를 무조건 사용해야함

from collections import deque

# 덱 생성
q = deque([1,2,3])
q.append(4) # 오른쪽뒤에 삽입 -> 맨마지막자리에 (0(1))추가
left_val = q.popleft() # -> 왼쪽(맨앞)에서 추출 ()
print(q,left_val)

# 문제 -> 빈 스택(리스트) 하나를 만들고, 순서대로 10,20,30 을 append로 넣은 뒤 pop()을 두번 연속 하여 꺼내진 값들을출력
q = list()
q.append(10)
q.append(20)
q.append(30)
print(q.pop())
print(q.pop())
"""

"""
딕셔너리(Dictionary) 활용
1. 개념: Key-Value 쌍으로 데이터를 저장하는 자료구조. 해시 테이블을 기반으로 하여 데이터 검색, 삽입, 삭제가 평균적으로 O(1)의 시간 복잡도를 가짐.

# 미니 실습

[문제]
첫 줄에 여러 단어가 공백으로 구분되어 입력됩니다. 각 단어가 몇 번씩 나왔는지 세어서, "단어: 횟수" 형태로 출력하는 프로그램을 작성해 보세요.
(예시 입력: apple banana apple orange banana apple / 출력 예시: apple: 3, banana: 2, orange: 1)
(힌트: from collections import Counter 를 사용하면 더 쉽게 해결할 수 있습니다.)

import sys
from collections import Counter

words = sys.stdin.readline().strip().split()

# 방법 1: 기본 딕셔너리 사용
word_count = {}
for word in words:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

for word, count in word_count.items():
    print(f"{word}: {count}")

# 방법 2: collections.Counter 사용
counter = Counter(words)
for word, count in counter.items():
    print(f"{word}: {count}")
"""

"""
정렬(Sorting)
1. 개념: 데이터를 특정 기준에 따라 순서대로 나열하는 것. 파이썬에서는 list.sort() 메서드나 sorted() 내장 함수를 주로 사용.

# 미니 실습

[문제]
첫 줄에 정수의 개수 N이 주어지고, 둘째 줄에 N개의 정수가 공백으로 주어집니다.
이 정수들을 오름차순으로 정렬하여 한 줄에 공백으로 구분해 출력하세요.

import sys

n = int(sys.stdin.readline())
numbers = list(map(int, sys.stdin.readline().split()))

numbers.sort() # 원본 리스트를 직접 정렬

for num in numbers:
    print(num, end=' ')
"""

"""
큐(Queue) : FIFO (First-In-First-Out)
먼저 들어온 데이터가 먼저 나가는 구조. 스택과 달리 양쪽에서 데이터를 넣고 뺄 수 있는 `deque`를 사용해야 효율적.

# 미니 실습

[문제]
1부터 N까지의 번호가 붙은 카드가 순서대로 쌓여있습니다.
1. 제일 위의 카드를 버립니다.
2. 그 다음 제일 위의 카드를 제일 아래로 옮깁니다.
카드가 한 장 남을 때까지 이 과정을 반복할 때, 마지막에 남는 카드의 번호를 출력하세요. (N=4일 경우, 4가 남음)

from collections import deque
import sys

n = int(sys.stdin.readline())
card_deck = deque(range(1, n + 1))

while len(card_deck) > 1:
    card_deck.popleft() # 1. 제일 위 카드 버리기
    card_deck.append(card_deck.popleft()) # 2. 그 다음 카드를 뽑아 맨 뒤로 옮기기

print(card_deck[0])
"""