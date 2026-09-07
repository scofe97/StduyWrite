# 04-01 §3 — 원문 Figure 4.4 의 라우터 구조. 네 구성 요소와 두 시간 척도.
# 5.12 ns 는 원문의 100 Gbps · 64바이트 계산을 검산한 값이고, 제어 평면의 ms~s 도 원문 서술 그대로다.
# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 평면을 묶고 관계에 시간 척도를 단다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 620
PW, PH = 168, 62
IN_X, FAB_X, OUT_X = 132, 500, 868
ROWS = [214, 300, 386]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §3",
      "라우터의 네 부분",
      "원문 Figure 4.4. 입력 포트·스위칭 패브릭·출력 포트는 하드웨어이고 라우팅 프로세서만 소프트웨어다.",
      "데이터 평면은 나노초, 제어 평면은 밀리초에서 초입니다")

# 제어 평면 zone
d.o.append(f'<rect x="24" y="96" width="{W-72}" height="76" rx="8" fill="{INFO}08" '
           f'stroke="{INFO}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(36, 90, "제어 평면 — 밀리초에서 초 · 소프트웨어", 11, INFO, KR, "start")
d.box(FAB_X - 210, 110, 420, 50, PAPER2, INFO, 1.2, 6)
d.t(FAB_X, 132, "라우팅 프로세서", 12, INFO, KR, "middle", 600)
d.t(FAB_X, 150, "라우팅 프로토콜 실행 · 포워딩 테이블 계산 · SDN 이면 컨트롤러와 통신", 11, SOFT, KR)

# 데이터 평면 zone
d.o.append(f'<rect x="24" y="188" width="{W-72}" height="266" rx="8" fill="{INK}05" '
           f'stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(36, 182, "데이터 평면 — 나노초 · 하드웨어", 11, SOFT, KR, "start")

for i, y in enumerate(ROWS):
    focal = i == 1
    if focal:
        d.tone(IN_X - PW / 2, y, PW, PH, ACC, 6, "14", 1.4)
    else:
        d.box(IN_X - PW / 2, y, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(IN_X, y + 26, f"입력 포트 {i+1}", 12, ACC if focal else INK, KR, "middle", 600)
    d.t(IN_X, y + 46, "종단 · 링크 층 · 조회", 11, SOFT, KR)
    d.box(OUT_X - PW / 2, y, PW, PH, PAPER2, RULE, 1.0, 6)
    d.t(OUT_X, y + 26, f"출력 포트 {i+1}", 12, INK, KR, "middle", 600)
    d.t(OUT_X, y + 46, "저장 · 스케줄 · 송신", 11, SOFT, KR)
    d.path(f"M {IN_X + PW/2 + 4} {y + PH/2} L {FAB_X - 106} {y + PH/2}", MUTED, 1.2, m="ar")
    d.path(f"M {FAB_X + 106} {y + PH/2} L {OUT_X - PW/2 - 10} {y + PH/2}", MUTED, 1.2, m="ar")

d.box(FAB_X - 100, ROWS[0], 200, ROWS[2] + PH - ROWS[0], PAPER2, RULE, 1.0, 6)
d.t(FAB_X, 288, "스위칭 패브릭", 12, INK, KR, "middle", 600)
d.t(FAB_X, 310, "라우터 안의 망", 11, SOFT, KR)
d.t(FAB_X, 334, "메모리 · 버스 · 크로스바", 11, SOFT, MONO)

d.path(f"M {FAB_X} 162 L {FAB_X} {ROWS[0] - 8}", INFO, 1.3, m="info", dash="5 4")
d.t(FAB_X + 12, 190, "포워딩 테이블을 라인 카드로 복사", 11, INFO, KR, "start")

d.tone(IN_X - PW / 2, 476, 300, 56, ACC, 6, "14", 1.2)
d.t(IN_X - PW / 2 + 16, 500, "64바이트 / 100 Gbps = 5.12 ns", 12, ACC, MONO, "start", 600)
d.t(IN_X - PW / 2 + 16, 520, "다음 데이터그램이 오기까지의 시간", 11, SOFT, KR, "start")

d.t(400, 500, "포트가 N 개 묶인 라인 카드라면 처리 파이프라인이 N 배 빨라야 합니다.", 11, MUTED, KR, "start")
d.t(400, 522, "소프트웨어로는 불가능해서 이 셋이 거의 언제나 하드웨어입니다.", 11, MUTED, KR, "start")

d.legend(H - 44, [("조회가 일어나는 자리", ACC), ("제어 평면", INFO), ("데이터 평면", MUTED)])
d.save("04-01.router-anatomy.svg")
