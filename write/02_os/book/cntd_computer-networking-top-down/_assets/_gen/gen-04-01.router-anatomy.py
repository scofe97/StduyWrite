# 04-01 §3 — 원문 Figure 4.4 의 라우터 구조. 네 구성 요소와 두 시간 척도.
# 5.12 ns 는 원문의 100 Gbps · 64바이트 계산을 검산한 값이고, 제어 평면의 ms~s 도 원문 서술 그대로다.
# 2026-09-14 재구성: 5.12 ns 를 도식 아래 별도 사각형으로 띄워 두면 패킷 흐름과 끊긴다는 지적을 받아
#   (1) 입력 링크 위의 패킷 간격으로 5.12 ns 를 보이고 (2) 그 간격 안에서 입력 포트가 도는 단계를 시간축으로 펼쳤다.
# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 평면을 묶고 관계에 시간 척도를 단다.
#   축약: 아래 확대 패널의 세 단계 칸 너비는 균등 분할이다. 원문이 단계별 소요 시간을 주지 않으므로
#         너비가 비율로 읽히지 않게 캡션에 그 사실을 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 812

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §3",
      "라우터의 네 부분",
      "원문 Figure 4.4. 입력 포트·스위칭 패브릭·출력 포트는 하드웨어이고 라우팅 프로세서만 소프트웨어다. "
      "입력 링크의 패킷 간격이 곧 입력 포트가 쓸 수 있는 시간 예산이다.",
      "패킷은 5.12 ns 마다 들어오고, 판단은 그 사이에 끝나야 합니다")

# ── 제어 평면 ──
d.o.append(f'<rect x="24" y="100" width="928" height="76" rx="8" fill="{INFO}08" '
           f'stroke="{INFO}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(36, 94, "제어 평면 — 밀리초에서 초 · 소프트웨어", 12, INFO, KR, "start")
d.box(290, 112, 420, 52, PAPER2, INFO, 1.2, 6)
d.t(500, 134, "라우팅 프로세서", 13, INFO, KR, "middle", 600)
d.t(500, 154, "라우팅 프로토콜 · 링크 상태 반응 · 컨트롤러 통신 · 관리", 12, SOFT, KR)

d.path("M 500 176 L 500 224", INFO, 1.3, m="info", dash="5 4")
d.t(512, 202, "포워딩 테이블을 라인 카드로 복사", 12, INFO, KR, "start")

# ── 데이터 평면 ──
d.o.append(f'<rect x="24" y="228" width="928" height="176" rx="8" fill="{INK}05" '
           f'stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(36, 222, "데이터 평면 — 나노초 · 하드웨어", 12, SOFT, KR, "start")

# 입력 링크 위의 패킷 줄 — 간격이 곧 5.12 ns
d.t(40, 272, "100 Gbps · 64바이트", 12, SOFT, MONO, "start")
for i in range(3):
    px = 40 + i * 72
    d.o.append(f'<rect x="{px}" y="285" width="32" height="22" rx="3" '
               f'fill="{ACC}22" stroke="{ACC}" stroke-width="1.1"/>')
d.line(40, 315, 40, 335, ACC, 1.0)
d.line(112, 315, 112, 335, ACC, 1.0)
d.line(40, 325, 112, 325, ACC, 1.0)
d.t(76, 352, "5.12 ns", 12, ACC, MONO)
d.path("M 220 296 L 252 296", ACC, 1.3, m="acc")

d.box(256, 258, 176, 76, PAPER2, RULE, 1.0, 6)
d.t(344, 286, "입력 포트", 13, INK, KR, "middle", 600)
d.t(344, 308, "종단 · 링크 층 · 조회", 12, SOFT, KR)
d.path("M 436 296 L 468 296", MUTED, 1.2, m="ar")

d.box(472, 258, 176, 76, PAPER2, RULE, 1.0, 6)
d.t(560, 286, "스위칭 패브릭", 13, INK, KR, "middle", 600)
d.t(560, 308, "라우터 안의 망", 12, SOFT, KR)
d.path("M 652 296 L 684 296", MUTED, 1.2, m="ar")

d.box(688, 258, 176, 76, PAPER2, RULE, 1.0, 6)
d.t(776, 286, "출력 포트", 13, INK, KR, "middle", 600)
d.t(776, 308, "저장 · 스케줄 · 송신", 12, SOFT, KR)
d.path("M 868 296 L 900 296", MUTED, 1.2, m="ar")
d.o.append(f'<rect x="908" y="285" width="32" height="22" rx="3" '
           f'fill="{MUTED}22" stroke="{MUTED}" stroke-width="1.1"/>')

d.path("M 344 338 L 344 432", ACC, 1.2, m="acc", dash="5 4")
d.t(356, 388, "이 안을 시간으로 펼치면", 12, ACC, KR, "start")

# ── 확대 — 입력 포트 안의 5.12 ns ──
d.o.append(f'<rect x="24" y="440" width="928" height="264" rx="8" fill="{ACC}06" '
           f'stroke="{ACC}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(36, 434, "입력 포트 안 — 다음 데이터그램이 오기 전에 끝나야 하는 일", 12, ACC, KR, "start")

SEG = [("1", "물리 층 종단", "링크 층 처리", False),
       ("2", "헤더 검사", "버전 · 체크섬 · TTL", False),
       ("3", "포워딩 테이블 조회", "최장 접두 일치", True)]
SX, SW = 88, 264
for i, (num, l1, l2, focal) in enumerate(SEG):
    x = SX + i * SW
    if focal:
        d.tone(x, 496, SW, 72, ACC, 6, "14", 1.4)
    else:
        d.box(x, 496, SW, 72, PAPER2, RULE, 1.0, 6)
    c = ACC if focal else INK
    d.t(x + SW / 2, 518, num, 11, SOFT, MONO)
    d.t(x + SW / 2, 540, l1, 13, c, KR, "middle", 600)
    d.t(x + SW / 2, 560, l2, 12, SOFT, KR)

d.line(88, 592, 880, 592, MUTED, 1.0)
d.line(88, 584, 88, 600, MUTED, 1.0)
d.line(880, 584, 880, 600, MUTED, 1.0)
d.t(88, 616, "0 ns", 12, SOFT, MONO)
d.t(880, 616, "5.12 ns", 12, ACC, MONO)
d.line(880, 476, 880, 584, ACC, 1.4, "4 4")
d.t(872, 470, "다음 데이터그램 도착", 12, ACC, KR, "end")

d.t(88, 646, "칸 너비는 균등 분할 — 원문은 단계별 비용을 말하지 않음", 13, MUTED, KR, "start")
d.t(88, 668, "합 > 5.12 ns → 뒤 패킷이 입력에서 밀림 · 포트 N 개면 파이프라인도 N 배", 13, MUTED, KR, "start")
d.t(88, 690, "셋 다 하드웨어 · 제어 평면만 소프트웨어 (밀리초~초)", 13, INK, KR, "start")

d.legend(H - 44, [("5.12 ns 예산과 조회", ACC), ("제어 평면 — 초", INFO), ("데이터 평면 — 나노초", MUTED)])
d.save("04-01.router-anatomy.svg")
print("ok router-anatomy")
