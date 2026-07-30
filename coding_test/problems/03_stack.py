"""
[문제 03] 스택(Stack)을 이용한 올바른 괄호 문자열(VPS) 검사

■ 문제 설명
괄호 문자열(Parenthesis String, PS)은 두 개의 괄호 기호인 '(' 와 ')' 만으로 구성되어 있는 문자열입니다. 
그 중에서 괄호의 모양이 바르게 구성된 문자열을 올바른 괄호 문자열(Valid PS, VPS)이라고 부릅니다.
예를 들어 "(())()"나 "(())"는 올바른 괄호 문자열이지만, "(()("나 ")("는 올바르지 않은 괄호 문자열입니다.

문자열 한 줄이 입력으로 주어질 때, 이 문자열이 올바른 괄호 문자열이면 "YES", 아니면 "NO"를 출력하는 프로그램을 작성하세요.
(힌트: 파이썬의 리스트를 스택으로 활용하여 '('는 append(), ')'는 pop()을 사용하여 처리해보세요.)

■ 입력 예시 1
(())()
■ 출력 예시 1
YES

■ 입력 예시 2
(()(
■ 출력 예시 2
NO
"""

import sys

def check_vps(s: str) -> str:
    stack = []
    
    # TODO: 스택을 활용하여 괄호 문자열 s가 올바른지 검사하는 로직을 작성하세요.
    for char in s:
        pass

    # TODO: 최종 스택 상태에 따라 "YES" 또는 "NO" 반환
    return "YES"

def main():
    s = sys.stdin.readline().strip()
    print(check_vps(s))

if __name__ == "__main__":
    main()
