# 09-02 §5 — 프로세스 일시 중단으로 리스가 만료된 뒤 잘못된 쓰기가 실행되는 흐름도.
# 사실 출처: 09-02 §5(L69~L73), 원서 Ch.9 Process Pauses(p.196~205) 및 Figure 9-4(잘못된 분산 락 구현으로 인한 파일 오염)
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 660
H = LEG + 56

d = D(W, H, "09-02 · §5 PROCESS PAUSE & LEASE EXPIRATION", "프로세스 일시 중단 중 리스 만료와 잘못된 쓰기 흐름",
      "시각 확인과 처리 사이 프로세스 멈춤으로 리스가 만료된 뒤에도 자신이 리더라 믿고 쓰기를 수행하는 과정.",
      "리스 만료 시각 확인 · 15초 멈춤 · 리스 만료 · 다른 노드가 리더 · 만료된 리스로 쓰기")

CX = 340

# 1. 시작 노드: 요청 수신 및 리스 확인
d.box(CX - 120, 104, 240, 36, fill=PAPER2, stroke=INFO, sw=1.1, r=18)
d.t(CX, 127, "리스 만료 시각 확인", 12, INK, KR, "middle", 600)

d.arrow([(CX, 140), (CX, 168)], MUTED, "ar", 1.2)

# 2. 결정 다이아몬드: 리스 유효성 확인
CY1, DW1, DH1 = 200, 240, 60
d.o.append(f'<path d="M {CX} {CY1 - DH1 / 2} L {CX + DW1 / 2} {CY1} '
           f'L {CX} {CY1 + DH1 / 2} L {CX - DW1 / 2} {CY1} Z" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(CX, CY1 + 4, "리스 유효?", 12, INK, KR, "middle", 600)

# 분기 2-1: 아니오 (좌측) -> 거부/갱신
d.arrow([(CX - DW1 / 2, CY1), (170, CY1)], INFO, "info", 1.2)
d.chip(200, CY1 - 10, "아니오", INFO, 11)

d.box(28, CY1 - 18, 142, 36, fill=PAPER2, stroke=INFO, sw=1.1, r=18)
d.t(99, CY1 + 5, "처리하지 않음", 11.5, INFO, KR, "middle", 600)

# 분기 2-2: 예 (하단) -> 진입 허가
d.arrow([(CX, CY1 + DH1 / 2), (CX, 256)], OK, "ok", 1.2)
d.chip(CX + 24, 242, "예 (유효)", OK, 11)

# 3. 단계: 요청 처리 진입 허가
d.box(CX - 140, 256, 280, 44, fill=PAPER, stroke=RULE, sw=0.9, r=6)
d.t(CX, 274, "처리 계속 결정", 12, INK, KR, "middle", 600)
d.t(CX, 290, "현재 시각 < 리스 만료 시각", 11, OK, KR, "middle")

d.arrow([(CX, 300), (CX, 330)], MUTED, "ar", 1.2)

# 4. 단계: 예기치 않은 프로세스 일시 중단 (15초)
d.box(CX - 150, 330, 300, 48, fill=PAPER2, stroke=WARN, sw=1.3, r=6)
d.t(CX, 348, "프로세스 일시 중단 발생 (15초 정지)", 12, WARN, KR, "middle", 600)
d.t(CX, 366, "GC STW · VM 마이그레이션 · I/O 대기", 11, MUTED, KR, "middle")

# 외부 세계로의 화살표
d.arrow([(CX + 150, 354), (570, 354)], BAD, "bad", 1.3)
d.chip(530, 342, "시간 경과", BAD, 11)

# 외부 세계 상태 박스 (우측)
d.box(570, 320, 280, 68, fill=PAPER2, stroke=BAD, sw=1.2, r=6)
d.t(710, 342, "리스 만료", 12, BAD, KR, "middle", 600)
d.t(710, 364, "다른 노드가 리더가 됨", 11.5, INK, KR, "middle")

d.arrow([(CX, 378), (CX, 418)], MUTED, "ar", 1.2)

# 5. 단계: 프로세스 재개 (정지 인지 불가)
d.box(CX - 140, 418, 280, 44, fill=PAPER, stroke=RULE, sw=0.9, r=6)
d.t(CX, 436, "프로세스 실행 재개", 12, INK, KR, "middle", 600)
d.t(CX, 452, "스레드는 자신이 멈춘 사실을 모름", 11, MUTED, KR, "middle")

d.arrow([(CX, 462), (CX, 498)], BAD, "bad", 1.3)

# 6. 단계: 만료된 리스로 요청 처리 및 쓰기 실행
d.box(CX - 150, 498, 300, 46, fill=PAPER2, stroke=BAD, sw=1.2, r=6)
d.t(CX, 516, "만료된 리스로 요청 처리 및 쓰기 실행", 12, BAD, KR, "middle", 600)
d.t(CX, 533, "자신이 리더라고 믿음", 11, MUTED, KR, "middle")

# 외부 세계 쓰기와 충돌을 잇는 파선 화살표
d.path(f"M 710 388 L 710 521 L {CX + 150} 521", BAD, 1.2, m="bad", dash="4 3")
d.t(630, 511, "두 리더 공존", 11, BAD, KR, "middle")

d.arrow([(CX, 544), (CX, 584)], BAD, "bad", 1.4)

# 7. 종료 노드: 재앙 결과 (focal)
d.box(CX - 170, 584, 340, 48, fill=PAPER2, stroke=ACC, sw=1.6, r=22)
d.t(CX, 602, "자신이 리더라 믿고 쓰기 수행", 12, ACC, KR, "middle", 600)
d.t(CX, 620, "리스 만료 뒤의 잘못된 쓰기", 11, BAD, KR, "middle")

d.legend(LEG, [
    ("잘못된 쓰기 (focal)", ACC),
    ("정상 판정", OK),
    ("진행 단계", INFO),
    ("프로세스 정지", WARN),
    ("리스 만료", BAD),
])

d.save("09-02.process-pause-lease.svg")
