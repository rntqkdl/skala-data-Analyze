"""
[해답 08] 그리디(Greedy, 탐욕법) 알고리즘 - 최소 동전 개수 구하기 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 그리디 알고리즘(탐욕법):
   - 매 순간 최적의 선택(가장 가치가 큰 동전 선택)을 하는 알고리즘입니다.
   - 이 문제에서 그리디가 최적해를 보장하는 이유는 "동전의 가치가 이전 동전 가치의 배수"라는 
     조건이 존재하기 때문입니다.

2. 계산 최적화:
   - 큰 동전부터 순회할 때 1씩 뺴는 뺄셈 반복문 대신 몫(`K // coin`)과 나머지(`K % coin`) 연산을 
     사용하면 $O(N)$ 시간 만에 해결할 수 있습니다.
"""

import sys

def main():
    n, k = map(int, sys.stdin.readline().split())
    coins = [int(sys.stdin.readline().strip()) for _ in range(n)]

    count = 0

    # 가치가 가장 큰 동전부터 확인하기 위해 내림차순 탐색
    for coin in reversed(coins):
        if k == 0:
            break
        
        # 현재 동전으로 거슬러 줄 수 있는 개수 누적
        count += k // coin
        # 남은 금액 갱신
        k %= coin

    print(count)

if __name__ == "__main__":
    main()
