# 타입 스펙: type-architecture — Secret 이 사용자에서 etcd 를 거쳐 노드의 tmpfs 파일과 컨테이너로 가는 길 위에 다섯 기준을 붙인다. 넷은 충족하고 etcd 에서 저장 시 암호화만 구멍으로 남는다. focal 은 etcd.
# 사실 출처: 노트 L158~L164(기준 표 다섯), L166(etcd 에 base64, 복호화 키를 호스트에 두지 않도록), L190(노드의 마운트된 tmpfs)
# Layout conventions: 노드 128x64(y=144) stride 192(x=28+192k), 간격 64에 화살표, 노드 구역은 4·5번(x=588 폭 352), 기준 칩 y=256, 전송 칩 y=360. 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


W, H = 960, 464
d = D(W, H, "ARCHITECTURE · 12-01 §3",
      "Kubernetes Secret 은 다섯 기준 중 넷을 채우고 저장 시 암호화가 남습니다",
      "사용자가 만든 Secret 은 독립된 자원으로 etcd 에 base64 로 저장되고, 전송 중 암호화를 거쳐 노드의 tmpfs 파일로 컨테이너에 마운트된다. "
      "독립된 생애주기, 전송 중 암호화, 파일 방식, 최소 노출 네 기준은 충족하고 저장 시 암호화는 기본으로 꺼져 있다.",
      lead="etcd 에 base64 로만 저장되는 것이 구멍이고, 켠다 해도 복호화 키를 호스트에 두지 않아야 합니다")

NW, NH, NY = 128, 64, 144
NX = [28 + 192 * i for i in range(5)]
CXS = [x + NW // 2 for x in NX]
MIDY = NY + NH // 2

# 노드 구역(4·5번) — 노드/구역 순으로 아래에 깐다
d.o.append(f'<rect x="588" y="100" width="352" height="124" rx="8" fill="rgba(245,245,245,0.02)" '
           f'stroke="{RULE}" stroke-width="1" stroke-dasharray="6 5"/>')
d.t(604, 120, "노드", 12, MUTED, KR, "start", 600)

# 노드 사이 화살표와 라벨
EDGES = ["생성", "저장", "전송", "마운트"]
for i, lab in enumerate(EDGES):
    x1, x2 = NX[i] + NW + 2, NX[i + 1] - 2
    c, m = (OK, "ok") if lab == "전송" else (MUTED, "ar")
    d.arrow([(x1, MIDY), (x2, MIDY)], c, m, 1.4)
    d.t((x1 + x2) / 2, MIDY - 10, lab, 12, MUTED, KR, "middle")

# (제목, 부제, 기준 칩, 색)
NODES = [
    ("사용자", "RBAC 쓰기 전용", "최소 노출", OK),
    ("Secret", "독립된 자원", "독립 생애주기", OK),
    ("etcd", "base64 인코딩만", "저장 시 암호화", ACC),
    ("tmpfs 파일", "메모리에만 둠", "파일 방식", OK),
    ("컨테이너", "파일 마운트", None, None),
]
for x, cx, (title, sub, crit, c) in zip(NX, CXS, NODES):
    fit(title, 14, NW - 16)
    fit(sub, 12, NW - 16)
    if title == "etcd":
        d.tone(x, NY, NW, NH, ACC, 6, "1F", 1.6)
    else:
        d.box(x, NY, NW, NH)
    d.t(cx, NY + 28, title, 14, INK, kr(title), "middle", 600)
    d.t(cx, NY + 50, sub, 12, MUTED, kr(sub), "middle")
    if crit:
        d.line(cx, NY + NH + 2, cx, 246, c, 1.1)
        d.chip(cx, 256, crit, c, 12, 7)

# etcd 구멍 설명
for i, (txt, col) in enumerate((("기본은 꺼짐", MUTED), ("명시적으로 켜야 함", MUTED), ("복호화 키는 호스트 밖에", ACC))):
    fit(txt, 12, 168)
    d.t(CXS[2], 292 + i * 18, txt, 12, col, KR, "middle")

# 전송 중 암호화는 노드가 아니라 etcd 에서 노드로 가는 화살표에 붙는다
EDGE_X = (NX[2] + NW + NX[3]) // 2
d.line(EDGE_X, MIDY + 4, EDGE_X, 350, OK, 1.1)
d.chip(EDGE_X, 360, "전송 중 암호화", OK, 12, 7)

d.legend(H - 56, [("충족한 기준", OK), ("남는 구멍", ACC)])
d.save(str(ASSETS / "12-01.k8s-secrets.svg"))
print("ok 12-01 k8s-secrets")
