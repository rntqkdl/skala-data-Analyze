# 🐍 Python 코딩 테스트 종합 문제집 (Coding Test Practice)

본 폴더는 `test.py`에 정리된 기초 파이썬 코딩 테스트 패턴을 바탕으로, 실전에서 자주 출제되는 핵심 자료구조 및 알고리즘 문제들을 **문제(Problem)**와 **해답(Solution)**으로 분리하여 학습할 수 있도록 구성된 문제집입니다.

---

## 📂 폴더 구조 (Directory Structure)

```text
coding_test/
├── README.md                          # 본 학습 가이드 파일
├── problems/                          # 📝 문제 및 코드 작성용 템플릿
│   ├── 01_input_output.py             # 1. 빠른 입출력 및 조건별 합계
│   ├── 02_list_comprehension.py      # 2. 리스트 컴프리헨션 및 조건 필터링
│   ├── 03_stack.py                    # 3. 스택(LIFO) - 올바른 괄호 문자열(VPS)
│   ├── 04_dictionary.py               # 4. 딕셔너리/Counter - 완주하지 못한 선수 (해시)
│   ├── 05_sorting.py                  # 5. 정렬 - 조건부 커스텀 정렬 및 중복 제거
│   ├── 06_queue.py                    # 6. 큐(FIFO)/deque - 요세푸스 문제
│   ├── 07_string_manipulation.py      # 7. 문자열 처리 - 팰린드롬 검사
│   ├── 08_greedy.py                   # 8. 그리디(Greedy) - 최소 동전 개수 구하기
│   └── 09_two_pointers.py             # 9. 투 포인터(Two Pointers) - 두 수의 합
└── solutions/                         # 💡 정답 코드 및 상세 풀이 해설
    ├── 01_input_output_sol.py
    ├── 02_list_comprehension_sol.py
    ├── 03_stack_sol.py
    ├── 04_dictionary_sol.py
    ├── 05_sorting_sol.py
    ├── 06_queue_sol.py
    ├── 07_string_manipulation_sol.py
    ├── 08_greedy_sol.py
    └── 09_two_pointers_sol.py
```

---

## 📑 문제 커리큘럼 (Curriculum)

| 번호 | 주제 | 난이도 | 핵심 키워드 |
| :---: | :--- | :---: | :--- |
| **01** | 빠른 입출력 (Input/Output) | ⭐☆☆☆☆ | `sys.stdin.readline`, `map`, `split` |
| **02** | 리스트 컴프리헨션 | ⭐☆☆☆☆ | List Comprehension, Filtering |
| **03** | 스택 (Stack) | ⭐⭐☆☆☆ | LIFO, `append()`, `pop()`, 괄호 검사 |
| **04** | 딕셔너리 (Dictionary) | ⭐⭐☆☆☆ | Hash Table, `collections.Counter` |
| **05** | 정렬 (Sorting) | ⭐⭐☆☆☆ | `sort(key=lambda ...)`, 중복 제거 `set` |
| **06** | 큐 (Queue) | ⭐⭐☆☆☆ | FIFO, `collections.deque`, `popleft()` |
| **07** | 문자열 처리 (String) | ⭐⭐☆☆☆ | `isalnum()`, `lower()`, Slicing `[::-1]` |
| **08** | 그리디 (Greedy) | ⭐⭐⭐☆☆ | 탐욕법, 거스름돈 최소화 |
| **09** | 투 포인터 (Two Pointers) | ⭐⭐⭐☆☆ | 정렬된 배열, $O(N)$ 조작 |

---

## 🎯 학습 방법 (How to Study)

1. `problems/` 폴더 안의 문제를 먼저 확인합니다.
2. 각 문제 파일의 주석에 기술된 **[문제 설명]**, **[입력 조건]**, **[출력 조건]**을 읽고 빈 칸(`TODO` 및 템플릿 코드)에 직접 풀이 코드를 작성합니다.
3. 문제 풀이가 완료되었거나 어려움이 있을 때는 `solutions/` 폴더 내의 해답 및 상세 해설(`*_sol.py`)을 참고하여 학습합니다.
