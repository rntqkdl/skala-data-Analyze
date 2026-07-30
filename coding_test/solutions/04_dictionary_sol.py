"""
[해답 04] 딕셔너리(Dictionary) 및 Counter를 이용한 해시 알고리즘 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 해시 테이블(Hash Table)과 딕셔너리:
   - 딕셔너리는 키(Key) 탐색, 삽입, 삭제가 $O(1)$로 매우 빠릅니다.
   - 참가자 수를 딕셔너리에 `+1` 카운팅하고, 완주자 명단을 보며 `-1` 카운팅하면 최종적으로 
     값이 `1`로 남아있는 선수가 완주하지 못한 선수입니다.

2. collections.Counter 활용:
   - `Counter(participant) - Counter(completion)` 연산을 수행하면 남아있는 요소의 Counter가 
     반환되어 단 한 줄로 해결할 수도 있습니다.
"""

import sys
from collections import Counter

def find_unfinished_player_dict(participant: list, completion: list) -> str:
    # 방법 1: 기본 딕셔너리 활용
    p_dict = {}
    for p in participant:
        p_dict[p] = p_dict.get(p, 0) + 1
        
    for c in completion:
        p_dict[c] -= 1

    for key, val in p_dict.items():
        if val > 0:
            return key

def find_unfinished_player_counter(participant: list, completion: list) -> str:
    # 방법 2: collections.Counter 활용 (추천)
    answer = Counter(participant) - Counter(completion)
    return list(answer.keys())[0]

def main():
    participant = sys.stdin.readline().strip().split()
    completion = sys.stdin.readline().strip().split()

    # 방법 2 사용
    result = find_unfinished_player_counter(participant, completion)
    print(result)

if __name__ == "__main__":
    main()
