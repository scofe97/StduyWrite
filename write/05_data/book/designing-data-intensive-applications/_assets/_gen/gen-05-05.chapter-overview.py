# 05-05 개요 — 워크플로우·이벤트 기반 데이터플로우와 5장 인코딩·호환성 전체 지도.
# 본문 L21: §1 은 서비스 기반 아키텍처의 워크플로우, §2·§3 이 비동기 메시지의 이벤트 기반이다. §1 을 "비동기"로 묶지 않는다.
# 사실 출처: 05-05 본문 도입부(L17~L21), §1(L29~L42), §2(L46~L61), §3(L69~L74), §4(L82~L93).
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
PY = 96
LEG = 420
H = LEG + 56

d = D(W, H, "05-05 · CHAPTER OVERVIEW", "워크플로우·이벤트 기반과 5장 종합 지형",
      "서비스 기반 워크플로우의 durable execution, 메시지 브로커의 비동기 버퍼링, 분산 액터 모델을 통한 데이터플로우와 5장 전체의 인코딩·호환성 종합을 보여준다.",
      "durable execution · 메시지 브로커 · 분산 actor 와 5장 인코딩·호환성 종합")

# 루트 노드 (5장 비동기 데이터플로우 & 종합 지형)
RX, RY, RW, RH = 250, 96, 380, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2)
d.t(440, 118, "워크플로우·이벤트 기반과 5장", 14, INK, KR, "middle", 600)
d.t(440, 134, "프로세스 간 데이터 이동 · 인코딩 호환성 종합", 12, MUTED, KR, "middle")

# 4개 컬럼 기하 (CW=200, GAP=12, X0=20)
CW = 200
GAP = 12
X0 = 20
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]
# cx: [120, 332, 544, 756]

# 루트 → 4개 컬럼 직각 버스 배선
BUS_Y = 164
d.line(440, RY + RH, 440, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[3], BUS_Y, RULE, 1.2)
for i in range(3):
    d.line(cx[i], BUS_Y, cx[i], 180, RULE, 1.2)
d.line(cx[3], BUS_Y, cx[3], 180, ACC, 1.4)

# 4개 카드 (y = 180, height = 216)
Y_CARD = 180
H_CARD = 216

cards = [
    ("durable execution", "05-05 §1", [
        "여러 서비스 호출의 태스크 그래프",
        "RPC · 상태 변경 WAL 로깅",
        "실패한 태스크 재실행",
        "성공 호출은 이전 결과로"
    ], INFO, False),
    ("메시지 브로커", "05-05 §2", [
        "송신자 · 수신자 비동기 분리",
        "과부하 완충 버퍼 · 장애 재전달",
        "큐(1:1) vs 토픽(1:N) 패턴",
        "스키마 레지스트리 호환 검사"
    ], INFO, False),
    ("분산 actor 모델", "05-05 §3", [
        "로컬 상태 · 한 번에 메시지 하나",
        "비동기 메시지 전달",
        "같은·다른 노드에 같은 메커니즘",
        "location transparency 적합"
    ], INFO, False),
    ("5장 인코딩 · 종합", "05-05 §4", [
        "언어별 · 텍스트 · 스키마 이진",
        "DB · RPC/REST · 이벤트 기반",
        "backward · forward 호환성",
        "무중단 롤링 업그레이드 지원"
    ], ACC, True),
]

for i, (title, section, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, Y_CARD, CW, H_CARD, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y_CARD, CW, H_CARD, PAPER2, RULE, 1.0)

    # 카드 헤더
    d.t(cx[i], Y_CARD + 24, title, 13, INK if not is_focal else ACC, KR, "middle", 600)
    d.chip(cx[i], Y_CARD + 48, section, color, 11)

    # 구분선
    d.line(x + 12, Y_CARD + 66, x + CW - 12, Y_CARD + 66, RULE, 0.8)

    # 항목 4줄
    for j, item in enumerate(items):
        item_y = Y_CARD + 92 + j * 28
        d.t(cx[i], item_y, item, 12, INK, KR, "middle")

d.legend(LEG, [("워크플로우 · 이벤트 기반 (§1~§3)", INFO), ("5장 인코딩·호환성 종합 (§4)", ACC)])
d.save("05-05.chapter-overview.svg")
