"""
[해답 07] 문자열 정제 및 팰린드롬 판별 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 문자열 전처리 (Filtering & Lowercasing):
   - `char.isalnum()`: 알파벳 소문자/대문자 및 숫자인 경우 True를 반환합니다.
   - `char.lower()`: 대소문자 구분을 없애기 위해 모두 소문자로 일치시킵니다.
   - 리스트 컴프리헨션으로 정제: `clean_str = "".join([c.lower() for c in s if c.isalnum()])`

2. 슬라이싱 뒤집기 (`[::-1]`):
   - 파이썬에서 문자열 `s[::-1]`은 $O(N)$ 시간 만에 문자열 전체를 뒤집은 새 문자열을 반환합니다.
   - `clean_str == clean_str[::-1]` 비교로 팰린드롬 여부를 한 줄로 명확하게 판단합니다.
"""

import sys

def is_palindrome(s: str) -> bool:
    # 1. 알파벳과 숫자만 추출하여 소문자로 정제
    clean_str = "".join([c.lower() for c in s if c.isalnum()])
    
    # 2. 회문 비교 (원본 vs 뒤집은 문자열)
    return clean_str == clean_str[::-1]

def main():
    s = sys.stdin.readline().strip()
    print(is_palindrome(s))

if __name__ == "__main__":
    main()
