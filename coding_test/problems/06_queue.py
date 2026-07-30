"""
[문제 06] 큐(Queue)와 collections.deque를 이용한 요세푸스 문제 (Josephus Problem)

■ 문제 설명
1번부터 N번까지 N명의 사람이 원을 이루면서 앉아있고, 양의 정수 K(≤ N)가 주어집니다.
이제 순서대로 K번째 사람을 제거합니다. 한 사람이 제거되면 남은 사람들로 이루어진 원을 따라 이 과정을 계속해 나갑니다.
이 과정은 N명의 사람이 모두 제거될 때까지 계속됩니다. 
원에서 사람들이 제거되는 순서를 (N, K)-요세푸스 순열이라고 합니다.

N과 K가 주어질 때 요세푸스 순열을 구하는 프로그램을 작성하세요.
(단, 시간 초과 방지를 위해 collections.deque를 활용해야 합니다.)

■ 입력 예시
7 3

■ 출력 예시
<3, 6, 2, 7, 5, 1, 4>

(설명: 1, 2, 3(제거), 4, 5, 6(제거), 7, 1, 2(제거)... 순으로 제거됨)
"""

import sys
from collections import deque

def main():
    # 입력 처리: N과 K
    n, k = map(int, sys.stdin.readline().split())

    # TODO: 1부터 N까지의 숫자로 deque를 만드세요.
    # q = deque(range(1, n + 1))

    result = []

    # TODO: K번째 사람을 회전/추출하여 result 리스트에 순서대로 담으세요.
    # while q:
    #     ...

    # 출력 양식: <3, 6, 2, 7, 5, 1, 4>
    print("<" + ", ".join(map(str, result)) + ">")

if __name__ == "__main__":
    main()
