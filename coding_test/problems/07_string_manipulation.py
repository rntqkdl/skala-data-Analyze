"""
[문제 07] 문자열 정제 및 팰린드롬(Palindrome, 회문) 판별

■ 문제 설명
팰린드롬(Palindrome)이란 거꾸로 읽어도 같은 단어나 문장을 의미합니다.
주어진 문장에서 영문자와 숫자만 남기고(공백, 구두점, 특수문자 제거), 
대소문자를 구분하지 않았을 때 해당 문장이 팰린드롬인지 판별하는 프로그램을 작성하세요.

팰린드롬이면 "True", 아니면 "False"를 출력하세요.

■ 입력 예시 1
A man, a plan, a canal: Panama
■ 출력 예시 1
True

■ 입력 예시 2
race a car
■ 출력 예시 2
False
"""

import sys

def is_palindrome(s: str) -> bool:
    # TODO: 1. 영문자와 숫자만 추출하고 모두 소문자로 변환하세요 (char.isalnum(), char.lower() 활용).
    # clean_str = ...
    
    # TODO: 2. 정제된 문자열과 뒤집은 문자열(clean_str[::-1])을 비교하여 팰린드롬 여부를 반환하세요.
    return True

def main():
    s = sys.stdin.readline().strip()
    print(is_palindrome(s))

if __name__ == "__main__":
    main()
