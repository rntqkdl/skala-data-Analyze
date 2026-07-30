"""
[해답 03] 스택(Stack)을 이용한 올바른 괄호 문자열(VPS) 검사 - 정답 코드 및 해설

■ 핵심 개념 및 해설
1. 스택(Stack)의 LIFO(Last-In-First-Out) 성질 활용:
   - 여는 괄호 '('를 만나면 스택에 넣습니다(`stack.append('(')`).
   - 닫는 괄호 ')'를 만나면 스택에서 여는 괄호를 짝지어 꺼냅니다(`stack.pop()`).
   - 만약 닫는 괄호를 만났는데 스택이 비어 있다면, 짝이 맞지 않으므로 즉시 "NO"를 반환합니다.
   - 모든 문자열을 순회한 후 스택에 여는 괄호가 남아있다면 짝이 맞지 않은 것이므로 "NO", 스택이 완전히 비어있다면 "YES"를 반환합니다.

2. 시간 복잡도:
   - 문자열의 길이를 N이라 할 때 $O(N)$의 시간에 탐색이 가능합니다.
"""

import sys

def check_vps(s: str) -> str:
    stack = []
    
    for char in s:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:  # 짝이 될 여는 괄호가 없는 경우
                return "NO"
            stack.pop()

    # 모든 검사 후 스택에 남아있는 여는 괄호가 없어야 올바른 괄호임
    return "YES" if not stack else "NO"

def main():
    s = sys.stdin.readline().strip()
    print(check_vps(s))

if __name__ == "__main__":
    main()
