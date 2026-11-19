# 06-03 §4 environ 환경 목록 — printenv 출력 다섯 줄을 가리키는 포인터 배열과 NULL 종단.
# 본문 근거: 이 노트 「4. C 프로그램의 환경 조작 인터페이스」의 첫 소절 「environ 전역 변수와 순회」.
# 값 근거: 다섯 환경 문자열은 노트의 printenv 출력 블록과 같다(TLPI 6.7 의 mtk 계정 예시). environ[5] 는 NULL 종단(environ(7) 「The last pointer in this array has the value NULL」).
# 타입 스펙: type-architecture — 포인터 칸(왼쪽)이 문자열 칸(오른쪽)을 가리키는 구조. argv 도식과 같은 형태라 같은 타입과 같은 좌표를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, INFO, KR, MONO

W, H = 880, 620
d = D(W, H, "TLPI · 06-03 §4",
      "environ 은 NAME=value 문자열을 가리키는 포인터 배열이다",
      "전역 변수 environ 이 포인터 배열의 시작을 가리키고, 각 칸은 NAME=value 형태의 널 종료 문자열을 가리킨다. 배열은 NULL 칸으로 끝나고 개수를 담은 변수는 없다.",
      lead="왼쪽 칸은 포인터, 오른쪽 칸은 NAME=value 문자열입니다. 문자열 순서는 정해져 있지 않습니다.")

# environ 변수
d.box(40, 104, 200, 48, PAPER, RULE, 0.9, 6)
d.t(56, 134, "environ", 14, ACC, MONO, "start", 600)
d.t(224, 134, "char **", 13, MUTED, MONO, "end")
d.t(40, 190, "포인터 배열", 13, MUTED, KR, "start")
d.t(560, 190, "가리키는 문자열", 13, MUTED, KR, "middle")

ENV = [
    "LOGNAME=mtk\\0",
    "SHELL=/bin/bash\\0",
    "HOME=/home/mtk\\0",
    "PATH=/usr/local/bin:/usr/bin:/bin:.\\0",
    "TERM=xterm\\0",
]
Y0, STRIDE = 204, 52
for i, val in enumerate(ENV):
    y = Y0 + i * STRIDE
    d.box(40, y, 200, 40, PAPER, ACC, 0.9, 4)
    d.t(56, y + 26, f"environ[{i}]", 14, INK, MONO, "start", 600)
    d.arrow([(240, y + 20), (356, y + 20)], ACC, "acc", 1.4)
    d.tone(360, y, 480, 40, INFO, 4, "14", 1.1)
    d.t(600, y + 26, val, 14, INFO, MONO, "middle", 600)

y = Y0 + len(ENV) * STRIDE
d.box(40, y, 200, 40, PAPER, MUTED, 0.9, 4)
d.t(56, y + 26, f"environ[{len(ENV)}]", 14, INK, MONO, "start", 600)
d.line(240, y + 20, 356, y + 20, MUTED, 1.0, "3 3")
d.box(360, y, 480, 40, PAPER2, RULE, 0.8, 4)
d.t(600, y + 26, "NULL — 배열의 끝. 개수 변수는 없음", 13, MUTED, KR, "middle")

d.legend(H - 56, [("포인터 칸", ACC), ("환경 문자열", INFO), ("배열 끝", MUTED)])
d.save("06-03.environ-array.svg")
print("ok 06-03 environ-array")
