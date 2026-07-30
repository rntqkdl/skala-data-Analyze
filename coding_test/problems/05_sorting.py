"""
[문제 05] 정렬(Sorting) 및 커스텀 키 조건 정렬

■ 문제 설명
첫 줄에 알파벳 소문자로 이루어진 단어의 개수 N이 주어집니다 (1 ≤ N ≤ 20,000).
둘째 줄부터 N개의 줄에 걸쳐 한 줄에 하나씩 단어가 주어집니다.

다음 조건에 따라 단어들을 정렬하여 출력하는 프로그램을 작성하세요.
1. 중복된 단어는 하나만 남기고 제거합니다.
2. 길이가 짧은 단어부터 앞에 오도록 정렬합니다.
3. 길이가 같은 단어가 여러 개 있다면 알파벳 사전 순으로 정렬합니다.

■ 입력 예시
5
banana
apple
dog
cat
banana

■ 출력 예시
cat
dog
apple
banana
"""

import sys

def main():
    # TODO: 첫 줄에서 단어의 개수 N을 입력받으세요.
    n = int(sys.stdin.readline().strip())

    # TODO: N개의 단어를 입력받고 중복을 제거하세요 (set 활용).
    words = []

    # TODO: 조건(1: 길이, 2: 사전순)에 따라 정렬을 수행하세요.
    # sort(key=lambda x: (...)) 사용

    # TODO: 정렬된 결과를 한 줄에 하나씩 출력하세요.
    pass

if __name__ == "__main__":
    main()
