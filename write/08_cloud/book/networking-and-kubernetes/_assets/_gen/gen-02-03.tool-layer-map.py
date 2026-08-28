# 02-03.tool-layer-map — 도구마다 보는 계층 범위가 다르고, 수사 순서는 그 범위 순서가 아니다
# 본문 요구: "도구가 보는 계층 — 수사 순서와 같지 않다" 소절. 막대 길이가 그 도구가 실제로
#           관측하는 계층 범위이고, 칸의 숫자가 본문이 정한 수사 순서다. 둘이 어긋나는 것이 논지.
# 타입 스펙: type-gantt.md — 막대 길이가 곧 구간. 계약이 "내려오는 선의 길이가 제각각"을
#           이 타입으로 지정한다. 가로 시간축 대신 세로 OSI 계층축을 쓴 회전 배치다.
# 이력: 2026-08-28 명령 갱신 — `netstat` 열을 빼고 `dig` 를 넣었다(관문 1 이 그림에 없었다),
#       `arp` 는 `ip neigh` 로. 번호도 도구 일련번호에서 사다리의 관문 번호로 바꿔 두 도식의 축을 맞췄다.
#       관문 1 이 최상위 계층이라는 것이 "순서와 계층이 어긋난다"는 논지의 가장 선명한 근거다.
#       2026-08-28 신설. 생성기 없이 손으로 만들어져 타입 선택 단계를 건너뛴 자산이었다
#       (러너 "생성기가 없는 SVG 는 만들지 않는다"). 좌표·값·색을 기존 SVG 그대로 옮겼다.
# 좌표: 열 stride 128 · 행 stride 54 하나로 고정. 막대는 행 중심 ±16 에서 시작해 54 씩 늘어난다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 1296, 508
COL_X0, COL_W, COL_STRIDE = 234, 118, 128
ROW_X, ROW_W, ROW_Y0, ROW_H, ROW_STRIDE = 12, 210, 176, 48, 54
BAR_W, HALF = 26, 16

LAYERS = ["L7 Application", "L6/5 Presentation·Session", "L4 Transport", "L3 Network", "L2 Data Link"]
# (도구, 관문 번호, 첫 행, 마지막 행, 색)
# 번호는 triage-ladder 의 관문 번호와 같은 것을 쓴다 — 두 도식이 같은 축을 말해야
# "관문 순서와 계층 순서가 어긋난다"는 논지가 두 그림 사이에서 확인된다.
TOOLS = [("dig", "관문 1", 0, 0, OK),
         ("ping", "관문 2", 3, 3, INFO), ("traceroute", "관문 2", 3, 3, INFO),
         ("ss", "관문 3", 2, 2, WARN),
         ("openssl s_client", "관문 4", 0, 2, ACC), ("cURL", "관문 4", 0, 2, ACC),
         ("tcpdump", "관문 밖", 0, 4, MUTED), ("ip neigh", "관문 밖", 4, 4, SOFT)]

d = D(W, H, "SPAN MATRIX · 02-03 DIAGNOSIS",
      "도구가 보는 계층 — 수사 순서는 계층 순서가 아니다",
      "진단 도구 여덟 개가 각각 어느 OSI 계층을 관측하는지 세로 스팬으로 표시한 행렬. "
      "내려오는 선의 길이가 제각각이며, 수사 순서는 계층을 위에서 아래로 훑는 것이 아니라 "
      "끊길 가능성이 큰 곳부터 싼 검사로 짚는 순서다.",
      lead="막대 길이가 그 도구가 실제로 보는 계층 범위입니다 — 번호는 수사 사다리의 관문 번호입니다.")

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

d.legend(464, [("관문 1 이름", OK), ("관문 2 도달", INFO), ("관문 3 포트", WARN),
               ("관문 4 대화", ACC), ("전 계층 캡처", MUTED), ("L2 주소 조회", SOFT)])
d.save("02-03.tool-layer-map.svg")
print("ok tool-layer-map")
