"""
[문제 09] 투 포인터(Two Pointers) - 두 수의 합 (Sum of Two Numbers)

■ 문제 설명
오름차순으로 정렬된 N개의 서로 다른 양의 정수가 주어집니다. 
이 중에서 두 수의 합이 타겟 값 M이 되는 양의 정수 쌍 (A, B)의 개수를 구하는 프로그램을 작성하세요.

첫째 줄에 정수의 개수 N과 타겟 값 M이 공백으로 주어집니다 (1 ≤ N ≤ 100,000, 1 ≤ M ≤ 2,000,000).
둘째 줄에 오름차순으로 정렬된 N개의 정수가 공백으로 주어집니다.

(단, 이중 for문을 이용한 O(N^2) 풀이는 시간 초과가 발생하므로, 양 끝단에서 탐색하는 O(N) 투 포인터 알고리즘을 사용하세요.)

■ 입력 예시
6 10
1 3 5 7 9 11

■ 출력 예시
2

(설명: 합이 10이 되는 쌍은 (1, 9), (3, 7) 로 총 2개입니다.)
"""

import sys

def main():
    n, m = map(int, sys.stdin.readline().split())
    numbers = list(map(int, sys.stdin.readline().split()))

    left = 0
    right = n - 1
    count = 0

    # TODO: left < right 조건 동안 투 포인터를 이동하며 합이 m이 되는 쌍의 개수를 세세요.
    # sum_val = numbers[left] + numbers[right]
    # sum_val == m 인 경우 count += 1, left += 1, right -= 1
    # sum_val < m 인 경우 left += 1
    # sum_val > m 인 경우 right -= 1

    print(count)

if __name__ == "__main__":
    main()
