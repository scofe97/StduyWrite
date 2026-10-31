# 07-03 §1 — 요청 라우팅 세 가지 방식 (임의 노드 접속, 라우팅 티어, 클라이언트 인지)의 요청 전달 경로 및 샤드 매핑 보유 위치 비교.
# 사실 출처: 07-03 본문 §1(L23~L36) — 방식별 시스템(Cassandra·Riak, mongos, Cassandra 드라이버)은 본문 L30·L32·L34 근거
#   (원서는 방식별 시스템을 적지 않는다)
# 원서 대목: Ch.7 PDF p.19 세 방식 목록, Figure 7-7 (PDF p.20) — get "foo", node 0 임의 선택, "foo" lives on node 2
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
PH = 380
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "07-03 · SECTION 1", "요청 라우팅 세 가지 방식",
      "클라이언트가 특정 키를 가진 샤드 노드를 찾는 세 가지 경로: 임의 노드 포워딩, 라우팅 티어, 클라이언트 직접 접속.",
      "어느 컴포넌트가 샤드→노드 매핑 정보를 갖는지에 따른 요청 전달 경로 비교")

X0 = 24
CW = 264
GAP = 20

panels = [
    ("1", "임의 노드 접속", "노드 간 포워딩", INFO, False),
    ("2", "라우팅 티어", "포워드만 담당", ACC, True),
    ("3", "클라이언트 인지", "중간 단계 없이 직접 접속", OK, False),
]

for idx, (chip_txt, title, sub, col, is_focal) in enumerate(panels):
    x = X0 + idx * (CW + GAP)
    cx = x + CW / 2

    # 패널 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 헤더
    d.chip(x + 24, PY + 24, chip_txt, col, 11)
    d.t(x + CW / 2 + 10, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, sub, 11.5, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 클라이언트 상자
    client_y = PY + 68
    if idx == 2:
        d.tone(cx - 108, client_y, 216, 46, OK, 6, "1A", 1.2)
        d.t(cx, client_y + 20, "클라이언트 (Client)", 12, INK, KR, "middle", 600)
        d.t(cx, client_y + 37, "샤드→노드 매핑 직접 보유", 11.5, OK, KR, "middle")
    else:
        d.box(cx - 108, client_y, 216, 46, PAPER, RULE, 0.8)
        d.t(cx, client_y + 20, "클라이언트 (Client)", 12, INK, KR, "middle", 600)
        d.t(cx, client_y + 37, "샤드 정보 미보유", 11.5, MUTED, KR, "middle")

    # 중간 라우팅 티어 영역
    tier_y = PY + 144
    if idx == 1:
        d.tone(cx - 108, tier_y, 216, 46, ACC, 6, "22", 1.4)
        d.t(cx, tier_y + 20, "라우팅 티어 (Routing Tier)", 12, INK, KR, "middle", 600)
        d.t(cx, tier_y + 37, "샤드 매핑 보유 · mongos", 11.5, ACC, KR, "middle")
        # 클라이언트 -> 라우팅 티어 화살표
        d.arrow([(cx, client_y + 46), (cx, tier_y)], MUTED, "ar")
        d.t(cx + 34, tier_y - 8, 'get "foo"', 11, MUTED, MONO, "start")

    # 노드 클러스터 배치
    node_w = 68
    node_gap = 10
    node_x0 = x + (CW - (3 * node_w + 2 * node_gap)) / 2
    nx0 = node_x0 + node_w / 2
    nx1 = node_x0 + node_w + node_gap + node_w / 2
    nx2 = node_x0 + 2 * (node_w + node_gap) + node_w / 2
    ny = PY + 236
    nh = 48

    # 노드 3개 그리기
    for n_idx, (nx_val, n_name) in enumerate([(nx0, "Node 0"), (nx1, "Node 1"), (nx2, "Node 2")]):
        bx = nx_val - node_w / 2
        if idx == 0 and n_idx == 0:
            d.tone(bx, ny, node_w, nh, INFO, 4, "1C", 1.2)
            d.t(nx_val, ny + 20, n_name, 12, INK, MONO, "middle", 600)
            d.t(nx_val, ny + 37, "매핑 보유", 11.5, INFO, KR, "middle")
        elif idx == 0:
            d.box(bx, ny, node_w, nh, PAPER, RULE, 0.8)
            d.t(nx_val, ny + 20, n_name, 12, INK, MONO, "middle", 600)
            d.t(nx_val, ny + 37, "매핑 보유", 11.5, SOFT, KR, "middle")
        elif idx == 1 and n_idx == 2:
            d.tone(bx, ny, node_w, nh, ACC, 4, "14", 1.1)
            d.t(nx_val, ny + 20, n_name, 12, INK, MONO, "middle", 600)
            d.t(nx_val, ny + 37, "대상 노드", 11.5, ACC, KR, "middle")
        elif idx == 2 and n_idx == 2:
            d.tone(bx, ny, node_w, nh, OK, 4, "14", 1.1)
            d.t(nx_val, ny + 20, n_name, 12, INK, MONO, "middle", 600)
            d.t(nx_val, ny + 37, "대상 노드", 11.5, OK, KR, "middle")
        else:
            d.box(bx, ny, node_w, nh, PAPER, RULE, 0.8)
            d.t(nx_val, ny + 29, n_name, 12, INK, MONO, "middle", 600)

        # 스토리지 샤드 상자
        sy = ny + nh + 6
        if n_idx == 2:
            d.tone(bx, sy, node_w, 28, ACC if idx == 1 else (OK if idx == 2 else INFO), 4, "20", 1.0)
            d.t(nx_val, sy + 18, '"foo" 샤드', 11, INK, KR, "middle", 600)
        else:
            d.box(bx, sy, node_w, 28, PAPER, RULE, 0.6)
            d.t(nx_val, sy + 18, "샤드", 11, SOFT, KR, "middle")

    # 연결 경로 화살표
    if idx == 0:
        # 클라이언트 -> Node 0
        d.arrow([(cx - 40, client_y + 46), (cx - 40, ny - 34), (nx0, ny - 34), (nx0, ny)], MUTED, "ar")
        d.t(cx - 48, ny - 60, 'get "foo"', 11, MUTED, MONO, "end")
        # Node 0 -> Node 2 포워드 (직각 경유)
        d.arrow([(nx0 + 14, ny), (nx0 + 14, ny - 16), (nx2 - 14, ny - 16), (nx2 - 14, ny)], INFO, "info")
        d.t(nx1, ny - 22, '"foo" 포워드', 11.5, INFO, KR, "middle")
    elif idx == 1:
        # 라우팅 티어 -> Node 2 포워드
        d.arrow([(nx2, tier_y + 46), (nx2, ny)], ACC, "acc")
        d.t(nx2 - 8, (tier_y + 46 + ny) / 2 + 4, '"foo" 포워드', 11.5, ACC, KR, "end")
    elif idx == 2:
        # 클라이언트 -> Node 2 직접 연결 (직각 경유)
        d.arrow([(cx + 40, client_y + 46), (cx + 40, ny - 20), (nx2, ny - 20), (nx2, ny)], OK, "ok")
        d.t(cx + 32, ny - 60, 'get "foo" 직접 접속', 11.5, OK, KR, "end")

    # 하단 대표 시스템 칩
    chip_y = PY + PH - 30
    if idx == 0:
        d.chip(cx, chip_y, "Cassandra · Riak", INFO, 11)
    elif idx == 1:
        d.chip(cx, chip_y, "MongoDB mongos", ACC, 11)
    elif idx == 2:
        d.chip(cx, chip_y, "Cassandra 드라이버", OK, 11)

d.legend(LEG, [("매핑: 라우팅 티어", ACC), ("매핑: 노드", INFO), ("매핑: 클라이언트", OK), ("요청 전달 경로", MUTED)])
d.save("07-03.request-routing.svg")
