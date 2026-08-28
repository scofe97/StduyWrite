# 02-03.tool-layer-map — 도구마다 보는 계층 범위가 다르고, 수사 순서는 그 범위 순서가 아니다
# 본문 요구: "도구가 보는 계층 — 수사 순서와 같지 않다" 소절. 막대 길이가 그 도구가 실제로
#           관측하는 계층 범위이고, 칸의 숫자가 본문이 정한 수사 순서다. 둘이 어긋나는 것이 논지.
# 타입 스펙: type-gantt.md — 막대 길이가 곧 구간. 계약이 "내려오는 선의 길이가 제각각"을
#           이 타입으로 지정한다. 가로 시간축 대신 세로 OSI 계층축을 쓴 회전 배치다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어져 타입 선택 단계를 건너뛴 자산이었다
#       (러너 "생성기가 없는 SVG 는 만들지 않는다"). 좌표·값·색을 기존 SVG 그대로 옮겼다.
# 좌표: 열 stride 128 · 행 stride 54 하나로 고정. 막대는 행 중심 ±16 에서 시작해 54 씩 늘어난다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 1296, 508
COL_X0, COL_W, COL_STRIDE = 234, 118, 128
ROW_X, ROW_W, ROW_Y0, ROW_H, ROW_STRIDE = 12, 210, 176, 48, 54
BAR_W, HALF = 26, 16

LAYERS = ["L7 Application", "L6/5 Presentation·Session", "L4 Transport", "L3 Network", "L2 Data Link"]
# (도구, 수사 순서, 첫 행, 마지막 행, 색)
TOOLS = [("ping", "순서 1", 3, 3, INFO), ("traceroute", "순서 2", 3, 3, INFO),
         ("netstat", "순서 3", 2, 2, WARN), ("ss", "순서 3", 2, 2, WARN),
         ("openssl s_client", "순서 4", 0, 2, ACC), ("cURL", "순서 5", 0, 2, OK),
         ("tcpdump", "순서 —", 0, 4, MUTED), ("arp", "순서 —", 4, 4, SOFT)]

d = D(W, H, "SPAN MATRIX · 02-03 DIAGNOSIS",
      "도구가 보는 계층 — 수사 순서는 계층 순서가 아니다",
      "진단 도구 여덟 개가 각각 어느 OSI 계층을 관측하는지 세로 스팬으로 표시한 행렬. "
      "내려오는 선의 길이가 제각각이며, 수사 순서는 계층을 위에서 아래로 훑는 것이 아니라 "
      "끊길 가능성이 큰 곳부터 싼 검사로 짚는 순서다.",
      lead="막대 길이가 그 도구가 실제로 보는 계층 범위입니다 — 숫자는 본문의 수사 순서입니다.")

def row_cy(r):
    return ROW_Y0 + r * ROW_STRIDE + ROW_H // 2

# 계층 행 — 왼쪽 라벨 칸과 오른쪽으로 뻗는 기준선
for r, name in enumerate(LAYERS):
    y = ROW_Y0 + r * ROW_STRIDE
    d.box(ROW_X, y, ROW_W, ROW_H, "none", RULE, 0.9, 6)
    d.t(24, y + 29, name, 12, MUTED, KR, "start")
    d.line(230, row_cy(r), 1248, row_cy(r), RULE, 0.6, "3 6")

# 도구 열 머리 + 스팬 막대
for i, (name, order, r0, r1, c) in enumerate(TOOLS):
    x, cx = COL_X0 + i * COL_STRIDE, COL_X0 + i * COL_STRIDE + COL_W // 2
    d.box(x, 96, COL_W, 56, PAPER2, RULE, 0.9, 6)
    # `openssl s_client` 하나만 12px 로는 118px 칸을 넘는다 — 그 칸만 한 단 줄인다
    d.t(cx, 120, name, 12 if len(name) * 7.5 < COL_W - 12 else 11, INK, MONO, "middle", 600)
    d.t(cx, 140, order, 12, SOFT, KR)   # 한글은 12px 이상 (스타일 계약 타이포그래피)
    top = row_cy(r0) - HALF
    d.box(cx - BAR_W // 2, top, BAR_W, row_cy(r1) + HALF - top, f"{c}2E", c, 1.2, 5)

d.legend(464, [("도달 확인", INFO), ("포트·소켓", WARN), ("TLS", ACC),
               ("L7 응답", OK), ("전 계층 캡처", MUTED), ("L2 주소 조회", SOFT)])
d.save("02-03.tool-layer-map.svg")
print("ok tool-layer-map")
