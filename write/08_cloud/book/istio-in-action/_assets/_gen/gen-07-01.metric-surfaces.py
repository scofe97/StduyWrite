# 07-01 §2 메트릭을 묻는 네 표면과 각각의 응답.
# 본문: "저자가 이 장에서 두드리는 표면은 넷입니다. 앞의 셋은 데이터 플레인 프록시가 열어 두고,
#       마지막 하나는 컨트롤 플레인이 엽니다." 이름이 점으로 갈라지는 계층이 아니라 소유 주체의 계층이다.
# 타입 스펙: type-tree — 뿌리 하나에서 소유 주체로 갈라지고 그 아래 엔드포인트가 잎이 된다. 깊이 3, 최대 폭 4,
#           연결선은 직각 엘보(대각선 금지), accent 는 노드 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 500
d = D(W, H, "ISTIO IN ACTION · 07-01 §2",
      "메트릭을 어디에 묻고 무엇을 돌려받는가",
      "같은 프록시가 포트와 경로를 여럿 열어 두고, 같은 계열의 값을 다른 형식으로 두 번 낸다. "
      "색이 붙은 잎이 Prometheus 가 실제로 긁어 가는 곳이다.",
      "앞의 셋은 사이드카가, 마지막 하나는 istiod 가 엽니다")

LW, LH = 204, 56
LY = 336
def leaf_x(i): return 40 + i * 244
leaves = [
    ("Envoy 형식 통계", ":15000/stats", False),
    ("엔드포인트별 통계", ":15000/clusters", False),
    ("Prometheus 형식", ":15090/stats/prometheus", True),
    ("컨트롤 플레인 통계", ":15014/metrics", False),
]
TW, TH = 224, 60
TY = 208
tiers = [("istio-proxy 사이드카", "앱 파드마다 하나", 394 - TW / 2),
         ("istiod", "istio-system", 882 - TW / 2)]
RW, RH = 260, 60
RX, RY = 638 - RW / 2, 100

# 연결선 먼저 — 직각 엘보
d.path(f"M 638 {RY + RH} L 638 178 L 394 178 L 394 {TY - 2}", MUTED, 1.0, m="ar")
d.path(f"M 638 {RY + RH} L 638 178 L 882 178 L 882 {TY - 2}", MUTED, 1.0, m="ar")
for i in range(3):
    cx = leaf_x(i) + LW / 2
    col = ACC if leaves[i][2] else MUTED
    mk = "acc" if leaves[i][2] else "ar"
    d.path(f"M 394 {TY + TH} L 394 300 L {cx} 300 L {cx} {LY - 2}", col, 1.2 if leaves[i][2] else 1.0, m=mk)
d.path(f"M 882 {TY + TH} L 882 {LY - 2}", MUTED, 1.0, m="ar")

# 뿌리
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0, 6)
d.t(RX + RW / 2, RY + 26, "메트릭을 묻는 곳", 13, INK, KR, "middle", 600)
d.t(RX + RW / 2, RY + 46, "kubectl exec + curl", 9, MUTED, MONO, "middle")

# 중간 계층
for name, sub, tx in tiers:
    d.box(tx, TY, TW, TH, PAPER2, RULE, 1.0, 6)
    d.t(tx + TW / 2, TY + 26, name, 12, INK, KR, "middle", 600)
    d.t(tx + TW / 2, TY + 46, sub, 9, MUTED, MONO, "middle")

# 잎
for i, (name, port, focal) in enumerate(leaves):
    x = leaf_x(i)
    if focal:
        d.o.append(f'<rect x="{x}" y="{LY}" width="{LW}" height="{LH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, LY, LW, LH, PAPER2, RULE, 0.9, 6)
    d.t(x + LW / 2, LY + 24, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + LW / 2, LY + 44, port, 9, ACC if focal else MUTED, MONO, "middle")

d.t(36, 424, "distroless 이미지에는 curl 이 없어 pilot-agent request GET stats 로 같은 값을 꺼낸다", 11, SOFT, KR, "start")
d.legend(444, [("Prometheus 가 긁는 곳", ACC)])
d.save("07-01.metric-surfaces.svg")
