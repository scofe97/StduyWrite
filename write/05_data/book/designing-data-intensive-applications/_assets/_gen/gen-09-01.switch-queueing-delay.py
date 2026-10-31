# 09-01 §5 — 스위치 포트 큐잉 혼잡(원서 Figure 9-2)과 다계층 버퍼 중첩 지연 데이터 흐름도.
# 사실 출처: 09-01 본문 §5(L84~L94), 원서 Ch.9 Unreliable Networks — Figure 9-2
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, BAD, KR, MONO

W = 880
LEG = 636
H = LEG + 56

d = D(W, H, "09-01 · §5 NETWORK DELAYS & QUEUEING", "스위치 포트 큐잉과 다계층 버퍼 지연 구조",
      "단일 목적지로 집중되는 스위치 큐잉 혼잡과 패킷 교환망의 4단계 버퍼 지연 구조.",
      "입력 포트 집중 · 스위치 출력 큐 · 패킷 드롭 · OS 수신 큐 · VM 일시 정지 · TCP 혼잡 제어")

# 상단 패널: 원서 Figure 9-2 스위치 포트 큐잉
d.box(24, 104, W - 48, 236, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(40, 130, "스위치 포트 큐잉 혼잡", 13, INK, KR, "start", 600)
d.t(360, 130, "여러 입력 포트가 동일 목적지 링크로 동시 전송 시 버퍼 포화 발생", 11, SOFT, KR, "start")

# 좌측 3개 머신 포트
ports = [
    ("포트 1 입력", 152),
    ("포트 2 입력", 210),
    ("포트 4 입력", 268),
]
for name, py in ports:
    d.box(40, py, 140, 44, fill=PAPER, stroke=RULE, sw=0.9)
    d.t(110, py + 20, name, 12, INK, KR, "middle", 600)
    d.t(110, py + 36, "패킷 동시 송신", 11, MUTED, KR, "middle")
    d.arrow([(180, py + 22), (280, py + 22)], MUTED, "ar", 1.2)

# 중앙 스위치 버퍼
d.box(280, 152, 290, 160, fill=PAPER, stroke=ACC, sw=1.3)
d.t(425, 174, "스위치 출력 큐 버퍼", 12, ACC, KR, "middle", 600)

slots = [
    ("대기열 1: 포트 1 패킷", 188),
    ("대기열 2: 포트 2 패킷", 216),
    ("대기열 3: 포트 4 패킷", 244),
]
for lab, sy in slots:
    d.box(296, sy, 160, 22, fill=PAPER2, stroke=INFO, sw=0.8)
    d.t(376, sy + 15, lab, 11, INFO, KR, "middle")

d.t(505, 230, "순서대로 처리", 11, WARN, KR, "middle")

# 포화 드롭 슬롯
d.box(296, 272, 258, 26, fill=BAD + "18", stroke=BAD, sw=1.1)
d.t(425, 289, "버퍼 포화: 패킷 폐기 (Drop)", 11, BAD, KR, "middle", 600)

# 출력 링크 및 목적지 머신
d.arrow([(570, 232), (660, 232)], MUTED, "ar", 1.4)
d.box(660, 172, 176, 120, fill=PAPER, stroke=RULE, sw=1.0)
d.t(748, 198, "목적지 머신 (포트 3)", 12, INK, KR, "middle", 600)
d.t(748, 222, "단일 목적지 링크", 11, MUTED, KR, "middle")
d.t(748, 246, "순서대로 수신", 11, MUTED, KR, "middle")
d.t(748, 270, "드롭 시 재전송 지연", 11, BAD, KR, "middle")

# 하단 패널: 4단계 큐잉 중첩 구조
d.box(24, 356, W - 48, 216, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(40, 382, "여러 계층의 큐잉 지점", 13, INK, KR, "start", 600)
d.t(360, 382, "계층마다 큐 대기 · 지연 변동의 원인", 11, SOFT, KR, "start")

stages = [
    (0, "1. 스위치 출력 큐", "스위치 버퍼 큐잉",
     [("동시 전송 집중", "같은 목적지로 송신"),
      ("패킷 폐기", "큐 가득 차면 드롭")],
     ACC, True),
    (1, "2. OS 수신 큐", "목적지 머신 큐잉",
     [("CPU 포화 대기", "모든 코어 점유"),
      ("요청 큐잉", "OS 가 큐에 보관")],
     WARN, False),
    (2, "3. 가상화 VM", "다른 VM 의 CPU 사용",
     [("CPU 양보 중단", "VM 일시 정지"),
      ("정지 시간", "수십 밀리초")],
     BAD, False),
    (3, "4. 송신 측 TCP 큐", "혼잡 제어 큐잉",
     [("혼잡 제어", "송신자 측 큐잉"),
      ("송신 전 대기", "전송 전 버퍼")],
     WARN, False),
]

BW = 170
GAP = 40
X0 = 40

for idx, title, sub_t, items, col_c, is_focal in stages:
    bx = X0 + idx * (BW + GAP)
    by = 404
    
    if is_focal:
        d.box(bx, by, BW, 150, fill=PAPER, stroke=ACC, sw=1.4)
    else:
        d.box(bx, by, BW, 150, fill=PAPER, stroke=RULE, sw=0.9)
    
    d.chip(bx + BW / 2, by + 18, title, col_c, 11)
    d.t(bx + BW / 2, by + 40, sub_t, 11, SOFT, KR, "middle")
    d.line(bx + 12, by + 50, bx + BW - 12, by + 50, RULE, 0.8)
    
    iy0 = by + 68
    for i_idx, (head, sub_txt) in enumerate(items):
        iy = iy0 + i_idx * 40
        d.box(bx + 10, iy - 12, BW - 20, 34, fill=PAPER2, stroke=RULE, sw=0.6)
        d.t(bx + BW / 2, iy + 2, head, 11, INK, KR, "middle", 600)
        d.t(bx + BW / 2, iy + 16, sub_txt, 11, MUTED, KR, "middle")
    

# 하단 배너: 비용/편익 트레이드오프 요약
d.tone(24, 584, W - 48, 34, INFO, 4, "12", 0.9)
d.t(W / 2, 605, "여유 용량: 큐 즉시 소진 및 안정 지연 · 용량 포화: 버퍼 적재 및 지연 변동성 급증", 12, INK, KR, "middle", 600)

d.legend(LEG, [
    ("병목·혼잡 (focal)", ACC),
    ("패킷 흐름", INFO),
    ("대기·제약", WARN),
    ("폐기·정지", BAD),
])

d.save("09-01.switch-queueing-delay.svg")
