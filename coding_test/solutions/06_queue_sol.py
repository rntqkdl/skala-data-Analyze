"""
[해답 06] 큐(Queue)와 collections.deque를 이용한 요세푸스 문제 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 일반 리스트 `pop(0)`의 문제점:
   - 파이썬의 일반 리스트에서 `pop(0)`을 사용하면 맨 앞 요소를 지울 때마다 나머지 요소들이 
     한 칸씩 이동하므로 $O(N)$의 시간이 소요되어 전체 $O(N^2)$ 시간초과가 발생합니다.
   - 반면 `collections.deque`의 `popleft()` 및 `rotate()`는 $O(1)$ 원소 이동을 보장합니다.

2. 풀이 방식:
   - 방법 1 (rotate): `deque.rotate(-(k - 1))`을 통해 K번째 사람을 맨 앞으로 이동시킨 후 `popleft()` 수행
   - 방법 2 (popleft 반복): 앞의 K-1 명을 `popleft()`하여 뒤로 `append()`한 뒤, K번째 사람을 `popleft()`
"""

import sys
from collections import deque

def main():
    n, k = map(int, sys.stdin.readline().split())

    # 1. deque 생성 (1부터 N까지)
    q = deque(range(1, n + 1))
    result = []

    # 2. 요세푸스 순열 계산
    while q:
        # K-1 명을 뽑아서 뒤로 보냄 (원형 큐 순회)
        q.rotate(-(k - 1))
        # K번째 사람 제거 및 결과 저장
        result.append(q.popleft())

    # 3. 형식에 맞춰 출력
    print("<" + ", ".join(map(str, result)) + ">")

if __name__ == "__main__":
    main()
