# 08-01 §6 — 트랜잭션 커밋 성공 후 네트워크 응답 유실 시 클라이언트의 abort 오판단과 재시도 중복 실행 함정 흐름도.
# 사실 출처: 08-01 §6(L70~L79), 원서 Ch.8 Single-Object and Multi-Object Operations — Retrying aborted transactions(PDF p.13)
# 타입 스펙: type-flowchart
# 검증(10-31 cc-ddia-dverify08): "(focal)" 본문 라벨 제거, 원서에 없는 "이중 결제" 제거, 멱등 키 → 본문·원서(p.13) 의 "애플리케이션 수준 중복 제거", 클라이언트 칸은 원서 "timed out from the client's point of view"
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 688
H = LEG + 56

d = D(W, H, "08-01 · §6 ABORT & RETRY HAZARD", "네트워크 타임아웃과 abort 재시도 중복 실행 함정 흐름",
      "트랜잭션 커밋 성공 후 응답 유실 시 클라이언트 관점 타임아웃과 중복 제거 없는 재시도로 인한 중복 실행 함정.",
      "커밋 성공 · 응답 유실 타임아웃 · 재시도 · 중복 제거 유무 분기 · 중복 실행 오염")

CX = 340

# 1. 시작 노드: 커밋 요청
d.box(CX - 110, 104, 220, 36, fill=PAPER2, stroke=INFO, sw=1.1, r=18)
d.t(CX, 127, "트랜잭션 커밋 요청", 12, INK, KR, "middle", 600)

d.arrow([(CX, 140), (CX, 172)], MUTED, "ar", 1.2)

# 2. 단계: DB 커밋 성공
d.box(CX - 140, 172, 280, 44, fill=PAPER, stroke=RULE, sw=0.9, r=6)
d.t(CX, 190, "데이터베이스 트랜잭션 커밋", 12, INK, KR, "middle", 600)
d.t(CX, 206, "트랜잭션 실제 성공", 11, MUTED, KR, "middle")

d.arrow([(CX, 216), (CX, 248)], MUTED, "ar", 1.2)

# 3. 결정 1: 성공 응답 수신?
CY1, DW1, DH1 = 280, 240, 64
d.o.append(f'<path d="M {CX} {CY1 - DH1 / 2} L {CX + DW1 / 2} {CY1} '
           f'L {CX} {CY1 + DH1 / 2} L {CX - DW1 / 2} {CY1} Z" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(CX, CY1 + 4, "성공 ACK 응답 수신?", 12, INK, KR, "middle", 600)

# 분기 1-1: 예 (우측) -> 정상 완료
d.arrow([(CX + DW1 / 2, CY1), (580, CY1)], OK, "ok", 1.2)
d.chip(510, CY1 - 10, "예", OK, 11)

d.box(580, CY1 - 18, 230, 36, fill=PAPER2, stroke=OK, sw=1.2, r=18)
d.t(695, CY1 + 5, "정상 완료 (추가 재시도 없음)", 12, OK, KR, "middle", 600)

# 분기 1-2: 아니오 (하단) -> 타임아웃
d.arrow([(CX, CY1 + DH1 / 2), (CX, 348)], WARN, "warn", 1.2)
d.chip(CX + 28, 328, "아니오 (유실)", WARN, 11)

# 4. 단계: 타임아웃 및 abort 오판단
d.box(CX - 150, 348, 300, 48, fill=PAPER2, stroke=WARN, sw=1.1, r=6)
d.t(CX, 366, "네트워크 타임아웃 발생", 12, WARN, KR, "middle", 600)
d.t(CX, 384, "클라이언트 관점에서 실패", 11, MUTED, KR, "middle")

d.arrow([(CX, 396), (CX, 428)], MUTED, "ar", 1.2)

# 5. 단계: 동일 트랜잭션 재시도
d.box(CX - 130, 428, 260, 44, fill=PAPER, stroke=RULE, sw=0.9, r=6)
d.t(CX, 446, "동일 트랜잭션 재시도 트리거", 12, INK, KR, "middle", 600)
d.t(CX, 462, "단순 재시도 규칙 실행", 11, MUTED, KR, "middle")

d.arrow([(CX, 472), (CX, 508)], MUTED, "ar", 1.2)

# 6. 결정 2: 멱등 키 존재?
CY2, DW2, DH2 = 540, 240, 64
d.o.append(f'<path d="M {CX} {CY2 - DH2 / 2} L {CX + DW2 / 2} {CY2} '
           f'L {CX} {CY2 + DH2 / 2} L {CX - DW2 / 2} {CY2} Z" '
           f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1.2"/>')
d.t(CX, CY2 + 4, "앱 수준 중복 제거 존재?", 12, INK, KR, "middle", 600)

# 분기 2-1: 예 (우측) -> 안전 완료
d.arrow([(CX + DW2 / 2, CY2), (580, CY2)], OK, "ok", 1.2)
d.chip(510, CY2 - 10, "예", OK, 11)

d.box(580, CY2 - 18, 230, 36, fill=PAPER2, stroke=OK, sw=1.2, r=18)
d.t(695, CY2 + 5, "중복 감지 및 안전 완료", 12, OK, KR, "middle", 600)

# 분기 2-2: 아니오 (하단) -> 중복 실행 함정 (focal)
d.arrow([(CX, CY2 + DH2 / 2), (CX, 608)], BAD, "bad", 1.4)
d.chip(CX + 28, 588, "아니오 (부재)", BAD, 11)

# 7. 종료 노드: 중복 실행 함정 (focal)
d.box(CX - 160, 608, 320, 48, fill=PAPER2, stroke=ACC, sw=1.5, r=22)
d.t(CX, 626, "동일 작업 2회 중복 실행", 12, ACC, KR, "middle", 600)
d.t(CX, 644, "중복·잘못된 데이터", 11, BAD, KR, "middle")

d.legend(LEG, [
    ("중복 함정 (focal)", ACC),
    ("안전 완료", OK),
    ("진행 단계", INFO),
    ("타임아웃", WARN),
    ("오염 위험", BAD),
])

d.save("08-01.abort-retry-timeout.svg")
