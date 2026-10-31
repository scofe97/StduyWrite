# 10-01 §2 — 레지스터 x의 읽기·쓰기·CAS 연산과 선형화 포인트(원자적 flip) 타임라인.
# 사실 출처: 10-01 §2(L38~L50), DDIA 2판 Ch.10 Linearizability(PDF p.6~8) 및 Figure 10-3, Figure 10-4(register x, flip 0->1, CAS)
# 타입 스펙: type-timeline
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 512
H = LEG + 52

d = D(W, H, "10-01 · §2 LINEARIZATION POINT", "원자적 flip과 선형화 포인트 타임라인",
      "레지스터 x에 대한 동시 쓰기·읽기·CAS 연산과 선형화 포인트 전후의 반환 값 규칙.",
      "원자적 flip 시점 · 동시 읽기 반환 규칙 · 새 값 관찰 후 역전 금지 · CAS 충돌 방지")

# 좌측 클라이언트 레인 헤더 박스
lanes = [
    ("Client C", "쓰기 주체", 160),
    ("Client A", "선행 읽기", 226),
    ("Client B", "후속 읽기", 292),
    ("Client D", "조건부 CAS", 358),
]

for name, role, ly in lanes:
    d.box(28, ly - 14, 116, 44, PAPER2, RULE, 0.9)
    d.t(86, ly + 4, name, 12, INK, MONO, "middle", 600)
    d.t(86, ly + 21, role, 11, MUTED, KR, "middle")
    d.box(152, ly - 14, W - 180, 44, PAPER, RULE, 0.4)

# 수직 선형화 포인트 (x_flip = 470)
X_FLIP = 470
d.line(X_FLIP, 136, X_FLIP, 410, OK, 1.5, dash="4,3")
d.chip(X_FLIP, 126, "선형화 포인트 (x: 0 → 1 flip)", OK, 11)

# 1. Client C: Write(x, 1) 막대 (300 ~ 620)
d.box(300, 154, 170, 30, PAPER2, WARN, 1.1)
d.t(385, 173, "Write(x, 1) 시작 (x=0)", 11, WARN, KR, "middle")
d.box(470, 154, 150, 30, OK + "22", OK, 1.2)
d.t(545, 173, "x=1 반영 · 이후 OK 반환", 11, OK, KR, "middle")

# 2. Client A: Read 1 (180 ~ 370) -> flip 이전 구 값 0 반환
d.box(180, 220, 190, 30, PAPER2, RULE, 0.9)
d.t(275, 239, "Read(x) ⇒ 0 (구 값 반환)", 11, INK, KR, "middle")

# 3. Client A: Read 2 (390 ~ 530) -> flip 이후 새 값 1 반환
d.box(390, 220, 140, 30, OK + "22", OK, 1.2)
d.t(460, 239, "Read(x) ⇒ 1 (새 값)", 11, OK, KR, "middle")

# 4. Client B: Read 1 (560 ~ 710) -> Client A의 Read 2 완료 후 시작 -> 반드시 1 반환
d.box(560, 286, 150, 30, OK + "22", ACC, 1.5)
d.t(635, 305, "Read(x) ⇒ 반드시 1", 11, ACC, KR, "middle", 600)

# Figure 10-3 시간 의존 화살표 (Client A Read 2 끝 -> Client B Read 1 시작)
d.arrow([(530, 235), (545, 235), (545, 301), (558, 301)], ACC, "acc", 1.4)
d.t(600, 272, "시간적 선행 의존 (역전 금지)", 11, ACC, KR, "start", 600)

# 5. Client D: cas(x, 0, 1) -> 590 ~ 790 -> x가 이미 1이므로 실패 Error
d.box(590, 352, 200, 30, BAD + "22", BAD, 1.2)
d.t(690, 371, "cas(x, 0, 1) ⇒ Error", 11, BAD, MONO, "middle", 600)
d.t(690, 396, "이미 x=1 로 변경되어 실패", 11, MUTED, KR, "middle")

# 하단 요약 패널
d.box(28, 424, W - 56, 54, PAPER2, RULE, 0.9)
d.t(W / 2, 446, "선형화 규칙: flip 이전에는 구 값(0) 허용, flip 이후에는 반드시 새 값(1)만 반환", 12, INK, KR, "middle", 600)
d.t(W / 2, 464, "새 값을 한 번이라도 관찰한 뒤에는 어떤 읽기도 구 값을 반환할 수 없음", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("선형화 포인트·성공", OK),
    ("새 값 고정 (focal)", ACC),
    ("진행 중·구 값 가능", WARN),
    ("CAS 실패·충돌 차단", BAD),
])

d.save("10-01.linearization-point.svg")
