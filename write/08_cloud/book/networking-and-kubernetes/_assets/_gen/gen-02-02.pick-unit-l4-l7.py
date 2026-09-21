# 02-02.pick-unit-l4-l7 — 백엔드를 고를 기회가 몇 번인가
# 본문 요구: "IPVS 는 Linux 의 L4 연결 로드밸런서"(02-02 §4 533줄) · "연결이 맺어지면 그 연결의
#           모든 요청은 종료까지 같은 Pod 로 간다"(04-02 §4 315줄) · "요청 하나하나를 나누려면
#           L7 로 올라가야 한다"(04-02 §4 326줄). L7 의 두 일(같은 풀에 요청 분배 / 경로로 서비스
#           선택)을 레인으로 갈라, "URL 라우팅"과 겹쳐 읽히지 않게 한다.
# 타입 스펙: type-swimlane — 가로 레인 셋이 같은 전제(연결 하나에 요청 셋)를 공유하고,
#           첫 칸이 "무엇을 보고 몇 번 고르는가"를, 나머지 세 칸이 그 결과를 보인다.
#           노드는 가로 한 줄이라 화살표가 전부 수평이다. 레인 구분은 1px hairline.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, BAD, INFO, OK, PAPER, PAPER2, KR, MONO

W, H = 920, 472
d = D(W, H, "L4 VS L7 · HOW OFTEN A BACKEND IS PICKED",
      "백엔드를 고를 기회가 몇 번인가",
      "L4 는 연결이 맺어질 때 5-tuple 로 한 번만 백엔드를 고르므로 그 연결 위의 요청은 전부 같은 "
      "Pod 로 가고, L7 은 요청마다 고르므로 같은 연결 위 요청들이 서로 다른 곳으로 갈린다. "
      "L7 이 하는 일은 같은 풀에 요청을 나누는 것과 경로로 서비스를 고르는 것 둘로 갈린다.",
      lead="세 레인 모두 TCP 연결 하나 위에 요청 셋을 실어 보낸다")

HX, HW = 140, 120                        # 첫 칸(고르는 근거) x · 폭
CX, CW, STRIDE = 276, 192, 208           # 결과 칸 첫 x · 폭 · 간격
COL = [CX + i * STRIDE for i in range(3)]
BANDS = [104, 208, 312]
BH, CELLH = 84, 60
LABEL_X = 12


def cell(x, y, w, top, sub, c, sub_c, focal=False):
    d.tone(x, y, w, CELLH, ACC if focal else c, 6, "14" if focal else "12", 1.4 if focal else 1.2)
    d.t(x + w / 2, y + 26, top, 13, ACC if focal else c, KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 12, sub_c, MONO)


def lane(band, label, sublabel, head, rows, c, focal=False):
    y = band + (BH - CELLH) // 2
    d.t(LABEL_X, band + 34, label, 12, c, MONO, "start", 600)
    d.t(LABEL_X, band + 52, sublabel, 12, SOFT, KR, "start")
    cell(HX, y, HW, head[0], head[1], WARN if not focal else ACC, MUTED, focal)
    for i, (top, sub) in enumerate(rows):
        cell(COL[i], y, CW, top, sub, c, MUTED)
        prev = HX + HW if i == 0 else COL[i - 1] + CW
        d.arrow([(prev + 6, y + CELLH // 2), (COL[i] - 8, y + CELLH // 2)],
                c, "info" if c is INFO else "ok", 1.4)


lane(BANDS[0], "L4", "kube-proxy · IPVS", ("5-tuple", "연결당 1회"),
     [("요청 1", "Pod A"), ("요청 2", "Pod A"), ("요청 3", "Pod A")], INFO, focal=True)
d.line(12, 196, W - 12, 196, RULE, 1.0)

lane(BANDS[1], "L7 · 분배", "같은 백엔드 풀", ("HTTP 요청", "요청마다"),
     [("요청 1", "Pod A"), ("요청 2", "Pod B"), ("요청 3", "Pod C")], OK)
d.line(12, 300, W - 12, 300, RULE, 1.0)

lane(BANDS[2], "L7 · 라우팅", "경로로 서비스 선택", ("URL 경로", "요청마다"),
     [("GET /api", "api 서비스"), ("GET /img", "img 서비스"), ("GET /api", "api 서비스")], OK)

d.t(HX + HW / 2, 408, "여기가 갈리는 축", 12, ACC, KR, "middle", 600)

d.legend(428, [("연결당 한 번", ACC), ("요청마다", WARN), ("고정된 목적지", INFO), ("갈리는 목적지", OK)])
d.save("02-02.pick-unit-l4-l7.svg")
print("ok pick-unit-l4-l7")
