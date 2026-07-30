"""
[해답 09] 투 포인터(Two Pointers) - 두 수의 합 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 이중 for문 vs 투 포인터:
   - 이중 for문을 이용하면 모든 쌍을 검사하므로 $O(N^2)$ 시간이 걸려 $N=100,000$인 경우 시간 초과가 발생합니다.
   - 이미 정렬된 배열이라는 성질을 활용하여 왼쪽 끝 포인터(`left`)와 오른쪽 끝 포인터(`right`)를 
     양 끝단에 두고 조건에 따라 포인터를 좁혀나가면 $O(N)$ 시간 만에 완벽히 탐색할 수 있습니다.

2. 포인터 이동 조건:
   - `numbers[left] + numbers[right] == M`: 조건 만족! `count += 1`, `left += 1`, `right -= 1`
   - `numbers[left] + numbers[right] < M`: 합이 M보다 작으므로 더 큰 값을 만들기 위해 `left += 1`
   - `numbers[left] + numbers[right] > M`: 합이 M보다 크므로 더 작은 값을 만들기 위해 `right -= 1`
"""

import sys

def main():
    n, m = map(int, sys.stdin.readline().split())
    numbers = list(map(int, sys.stdin.readline().split()))

    left = 0
    right = n - 1
    count = 0

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == m:
            count += 1
            left += 1
            right -= 1
        elif current_sum < m:
            left += 1
        else:
            right -= 1

    print(count)

if __name__ == "__main__":
    main()
