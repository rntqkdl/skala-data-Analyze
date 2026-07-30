"""
[문제 04] 딕셔너리(Dictionary) 및 Counter를 이용한 해시 알고리즘 (완주하지 못한 선수)

■ 문제 설명
마라톤 경기에 참여한 선수들의 이름 목록과 완주한 선수들의 이름 목록이 주어집니다.
단 한 명의 선수를 제외하고는 모든 선수가 마라톤을 완주하였습니다.

첫째 줄에는 마라톤에 참여한 선수들의 이름이 공백으로 구분되어 주어집니다.
둘째 줄에는 완주한 선수들의 이름이 공백으로 구분되어 주어집니다.
완주하지 못한 단 한 명의 선수 이름을 출력하는 프로그램을 작성하세요.
(참고: 참가자 명단에는 동명이인이 있을 수 있습니다.)

■ 입력 예시
marleo kiki eden marleo
eden kiki marleo

■ 출력 예시
marleo

(설명: marleo가 2명 참가했으나 완주자 명단에는 1명만 있으므로 완주하지 못한 선수는 marleo입니다.)
"""

import sys
from collections import Counter

def find_unfinished_player(participant: list, completion: list) -> str:
    # TODO: 딕셔너리나 collections.Counter를 활용하여 완주하지 못한 선수를 찾으세요.
    pass

def main():
    participant = sys.stdin.readline().strip().split()
    completion = sys.stdin.readline().strip().split()

    result = find_unfinished_player(participant, completion)
    print(result)

if __name__ == "__main__":
    main()
