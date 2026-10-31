# 07-04 §2 — 글로벌 용어 분할 보조 인덱스: 단일 샤드 읽기와 여러 인덱스 샤드에 닿는 쓰기.
# 사실 출처: 07-04 본문 §2(L42, L44~L46), DDIA 2판 Ch.7 Figure 7-10(원서 PDF 24쪽).
#   레코드·인덱스 값은 Figure 7-10 그림 글자 그대로(location 열과 그림의 "…" 칸은 뺐다).
#   쓰기 예는 그림의 점선 화살표가 나가는 레코드 893(color:silver → 인덱스 샤드 1, make:Audi → 인덱스 샤드 0).
#   color 경계 a~r / s~z 는 본문 L42, make 경계(f 와 h 사이)는 원서 24쪽 본문. 기본키 구간은 그림에 없어 적지 않는다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BY = 310
BH = 160
LEG = BY + BH + 30
H = LEG + 56

d = D(W, H, "07-04 §2 · GLOBAL SECONDARY INDEX", "글로벌 용어 분할 인덱스와 읽기·쓰기 경로",
      "용어 분할 글로벌 인덱스의 단일 샤드 읽기와 여러 인덱스 샤드에 닿는 쓰기를 보인다.",
      "용어별 인덱스 분할과 읽기·쓰기 경로 대조")

X0 = 24
X1 = 464
SW = 392
CX0 = X0 + SW / 2
CX1 = X1 + SW / 2

# 상단: 기본키 샤드 2개
PY = 96
PH = 120

d.box(X0, PY, SW, PH, PAPER2, RULE, 1.0)
d.tone(X0, PY, SW, 28, INFO, 4, "18", 1.0)
d.t(CX0, PY + 18, "기본키 샤드 0", 12, INK, KR, "middle", 600)
d.t(X0 + 12, PY + 46, "191 → {color: \"red\", make: \"Honda\"}", 11, INK, MONO, "start")
d.t(X0 + 12, PY + 72, "214 → {color: \"black\", make: \"Dodge\"}", 11, INK, MONO, "start")
d.t(X0 + 12, PY + 98, "306 → {color: \"red\", make: \"Ford\"}", 11, INK, MONO, "start")

d.box(X1, PY, SW, PH, PAPER2, RULE, 1.0)
d.tone(X1, PY, SW, 28, INFO, 4, "18", 1.0)
d.t(CX1, PY + 18, "기본키 샤드 1", 12, INK, KR, "middle", 600)
d.t(X1 + 12, PY + 46, "515 → {color: \"silver\", make: \"Ford\"}", 11, INK, MONO, "start")
d.t(X1 + 12, PY + 72, "768 → {color: \"red\", make: \"Volvo\"}", 11, INK, MONO, "start")
d.tone(X1 + 8, PY + 82, SW - 16, 24, WARN, 3, "1c", 1.0)
d.t(X1 + 12, PY + 98, "893 → {color: \"silver\", make: \"Audi\"}", 11, WARN, MONO, "start", 600)

# 중간: 읽기 질의 상자 · 쓰기 상자
MY = 232
MH = 38
d.box(X0, MY, SW, MH, PAPER2, OK, 1.1)
d.t(X0 + 12, MY + 16, "읽기: color = red", 11, INK, KR, "start")
d.t(X0 + 12, MY + 30, "인덱스 샤드 0 단일 질의 · fan-out 없음", 11, OK, KR, "start", 600)

d.box(X1, MY, SW, MH, PAPER2, WARN, 1.1)
d.t(X1 + 12, MY + 16, "쓰기: 893 추가 시 두 인덱스 샤드 갱신", 11, INK, KR, "start")
d.t(X1 + 12, MY + 30, "make:Audi(인덱스 0) · color:silver(인덱스 1)", 11, WARN, KR, "start", 600)

d.arrow([(CX1, PY + PH), (CX1, MY - 2)], WARN, "warn", 1.2)

# 하단: 글로벌 인덱스 샤드 2개
d.box(X0, BY, SW, BH, PAPER2, RULE, 1.0)
d.tone(X0, BY, SW, 28, MUTED, 4, "18", 1.0)
d.t(CX0, BY + 18, "인덱스 샤드 0 (color a~r · make a~f)", 12, INK, KR, "middle", 600)
d.t(X0 + 12, BY + 46, "color:black → [214]", 11, MUTED, MONO, "start")
d.tone(X0 + 8, BY + 56, SW - 16, 24, ACC, 3, "22", 1.2)
d.t(X0 + 12, BY + 72, "color:red   → [191, 306, 768]", 11, ACC, MONO, "start", 600)
d.tone(X0 + 8, BY + 82, SW - 16, 24, WARN, 3, "1c", 1.0)
d.t(X0 + 12, BY + 98, "make:Audi   → [893]", 11, WARN, MONO, "start", 600)
d.t(X0 + 12, BY + 124, "make:Dodge  → [214]", 11, INK, MONO, "start")
d.t(X0 + 12, BY + 146, "make:Ford   → [306, 515]", 11, INK, MONO, "start")

d.box(X1, BY, SW, BH, PAPER2, RULE, 1.0)
d.tone(X1, BY, SW, 28, MUTED, 4, "18", 1.0)
d.t(CX1, BY + 18, "인덱스 샤드 1 (color s~z · make h~z)", 12, INK, KR, "middle", 600)
d.tone(X1 + 8, BY + 30, SW - 16, 24, WARN, 3, "1c", 1.0)
d.t(X1 + 12, BY + 46, "color:silver → [515, 893]", 11, WARN, MONO, "start", 600)
d.t(X1 + 12, BY + 72, "color:yellow → []", 11, SOFT, MONO, "start")
d.t(X1 + 12, BY + 98, "make:Honda   → [191]", 11, INK, MONO, "start")
d.t(X1 + 12, BY + 124, "make:Volvo   → [768]", 11, INK, MONO, "start")

# 읽기 화살표
d.arrow([(CX0, MY + MH), (CX0, BY - 2)], OK, "ok", 1.5)

# 쓰기 화살표 (점선)
d.arrow([(X1, MY + 19), (440, MY + 19), (440, 290), (300, 290), (300, BY - 2)], WARN, "warn", 1.3, dash="4 4")
d.t(370, 284, "make:Audi", 11, WARN, MONO, "middle")

d.arrow([(CX1, MY + MH), (CX1, BY - 2)], WARN, "warn", 1.3, dash="4 4")
d.t(CX1 + 6, MY + MH + 18, "color:silver", 11, WARN, MONO, "start")

d.legend(LEG, [("기본키 샤드", INFO), ("검색 일치 (color:red)", ACC), ("단일 샤드 읽기", OK), ("쓰기가 닿는 인덱스", WARN)])
d.save("07-04.global-secondary-index.svg")
