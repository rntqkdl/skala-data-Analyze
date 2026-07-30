"""
[해답 05] 정렬(Sorting) 및 커스텀 키 조건 정렬 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 중복 제거 (`set` 자료구조):
   - 입력받은 단어들을 `set`에 넣으면 $O(1)$ 수준으로 중복을 제거할 수 있습니다.
   - 이후 정렬(sort) 연산을 위해 다시 `list`로 변환합니다.

2. Lambda 키(Key) 정렬:
   - `words.sort(key=lambda x: (len(x), x))`
   - 튜플 `(len(x), x)`를 리턴함으로써 1순위 조건인 '단어의 길이 `len(x)`', 
     2순위 조건인 '알파벳 사전순 `x`'에 따라 다중 조건 정렬을 한 번에 수행합니다.
"""

import sys

def main():
    n = int(sys.stdin.readline().strip())

    # 1. 단어 입력 및 중복 제거
    word_set = set()
    for _ in range(n):
        word_set.add(sys.stdin.readline().strip())

    words = list(word_set)

    # 2. 다중 조건 정렬 (1우선순위: 길이 len(x), 2우선순위: 사전순 x)
    words.sort(key=lambda x: (len(x), x))

    # 3. 결과 출력
    for word in words:
        print(word)

if __name__ == "__main__":
    main()
