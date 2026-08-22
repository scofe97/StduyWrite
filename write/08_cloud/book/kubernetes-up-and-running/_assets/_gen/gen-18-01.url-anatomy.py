# 18-01 §랩 1 — API 서버가 HTTP 서버라는 것을 직접 봅니다
# 본문이 이 도식의 규격을 적어 둔다 — "세 줄의 차이가 이 장이 프로그래밍할 때 중요해진다고
# 말한 두 개념" 이고, 그 둘을 "API 그룹" 과 "네임스페이스 범위" 로 이름 붙인다. 그러니 세
# URL 을 나란한 문장으로 늘어놓으면 안 되고, *같은 자리* 가 세로로 맞은 격자여야 한다.
# 열이 맞아야 "여기가 비어 있다" 가 형태로 보인다 — Namespace 행의 네임스페이스 칸이 그것이다.
# 마지막 열에 클라이언트 메서드 이름을 붙이는 이유도 같다. 이름이 URL 에서 나왔다는 게
# 본문의 주장이므로, 주장과 근거가 한 행에 있어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 580
d = D(W, H, "KUBERNETES UP AND RUNNING · 18-01",
      "URL 한 줄에 두 축이 적혀 있다",
      "API 서버는 HTTP 서버이고 클라이언트도 그렇게 본다. 그래서 경로를 읽으면 어느 API "
      "그룹인지와 네임스페이스에 속하는지가 그대로 나온다.",
      "kind 로컬 클러스터 실측 — kubectl v1.34.1 · 서버 v1.35.0 · kubectl get <리소스> --v=6")

# 열을 고정한다. 같은 자리가 세로로 맞아야 빈 칸이 형태로 보인다.
COLS = [("API 그룹", 24, 250), ("네임스페이스 범위", 286, 268),
        ("리소스", 566, 170), ("Python 클라이언트", 748, 468)]
HDR_Y, Y0, RH, GAP = 128, 148, 74, 10

for name, x, w in COLS:
    d.t(x, HDR_Y, name, 9, SOFT, KR, "start")

ROWS = [
    ("Pod", "/api/v1", INFO, "/namespaces/default", ACC, "/pods", OK,
     "CoreV1Api.list_namespaced_pod(ns)"),
    ("Deployment", "/apis/apps/v1", INFO, "/namespaces/kube-system", ACC, "/deployments", OK,
     "AppsV1Api.list_namespaced_deployment(ns)"),
    ("Namespace", "/api/v1", INFO, None, None, "/namespaces", OK,
     "CoreV1Api.list_namespace()"),
]

for i, (label, grp, gc, ns, nc, res, rc, method) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    focal = ns is None
    for j, (cell, c) in enumerate(((grp, gc), (ns, nc), (res, rc))):
        _, cx, cw = COLS[j]
        if cell is None:
            # 빈 칸을 그리지 않고 비우면 실수처럼 보인다. 없다는 것을 적어 둔다.
            d.o.append(f'<rect x="{cx}" y="{y}" width="{cw}" height="{RH}" rx="6" '
                       f'fill="{PAPER}" stroke="{WARN}" stroke-width="1.2" stroke-dasharray="4 4"/>')
            d.t(cx + cw / 2, y + RH / 2 + 5, "이 마디가 없다", 11, WARN, KR)
            continue
        d.tone(cx, y, cw, RH, c, 6, "10", 1.2)
        d.t(cx + cw / 2, y + RH / 2 + 5, ddx.fit(cell, 13, cw - 24, cell), 13, c, MONO)
    _, mx, mw = COLS[3]
    d.box(mx, y, mw, RH, PAPER2, ACC if focal else RULE, 1.3 if focal else 1.0, 6)
    d.t(mx + 16, y + 28, label, 11, INK, KR, "start", 600)
    d.t(mx + 16, y + 50, ddx.fit(method, 11, mw - 32, method), 11,
        ACC if focal else MUTED, MONO, "start")

BY = Y0 + 3 * (RH + GAP) + 14
d.line(24, BY, W - 48, BY, RULE, 0.8)

NOTES = [
    ("core 는 /api/v1, 나머지는 /apis/<그룹>/<버전>", INFO,
     "YAML 의 apiVersion 이 경로에 나타난 것이다"),
    ("이 마디가 있으면 이름에 namespaced 가 붙는다", ACC,
     "Namespace 나열은 네임스페이스 안에서 하는 일이 아니다"),
    ("API 그룹이 클라이언트 객체를 가른다", OK,
     "경로가 갈리는 것이 타입으로 올라온 것이다"),
]
NW, NG = 388, 18
for i, (head, c, sub) in enumerate(NOTES):
    x = 24 + i * (NW + NG)
    d.o.append(f'<rect x="{x}" y="{BY+22}" width="{NW}" height="62" rx="6" '
               f'fill="{c}0C" stroke="{c}" stroke-width="1.1"/>')
    d.t(x + 16, BY + 46, ddx.fit(head, 12, NW - 32, head), 12, c, KR, "start", 600)
    d.t(x + 16, BY + 68, ddx.fit(sub, 10, NW - 32, sub), 10, MUTED, KR, "start")

d.legend(BY + 104, [("API 그룹", INFO), ("네임스페이스 범위", ACC),
                    ("리소스", OK), ("마디가 빠지는 자리", WARN)])
d.save("../18-01.url-anatomy.svg")
print("필요 h:", BY + 104 + 48, "· 실제:", H)
