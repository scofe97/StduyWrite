# 03-02 / 11-01 §로드밸런싱 — 접속 경로가 분산 여부를 가른다
# 본문 실측(30회): 클러스터 안 curl → 13 (2vm7s, worker2) / 10 (8phwt, worker) / 7 (bhgc5, worker).
#   port-forward 는 Pod 하나에 직접 터널이라 30번 모두 같은 Pod 로 간다.
#   "이 kind 환경의 kube-proxy 는 iptables 모드였고, 설치된 규칙이 endpoint 를 확률적으로
#    선택했습니다. 30회처럼 표본이 작으면 13/10/7 정도의 편차가 날 수 있습니다."
# 타입 스펙: type-bar.md — 같은 30회가 경로에 따라 어떻게 갈리는지가 요점이라, 두 경로를 위아래로 두고
#           도착 분포를 막대 길이로 그린다 — 숫자가 본문에 있으므로 길이를 값에 비례해 둔다.
#           30 회를 파드별로 나눈 이산 수량을 막대 길이로 비교한다. 길이가 값에 비례하고(30 회 =
#           420px) 두 경로를 위아래 두 벌로 두어 같은 축에서 읽힌다 — 정본 계약 그대로다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

# 두 번째 패널의 마지막 막대가 521~547 을 쓴다 — 산문 y 를 그 아래에서 산출한다.
P2_Y0 = 400
BAR_BOT = P2_Y0 + 50 + 2 * 42 + 13          # 547
NOTE_Y, NOTE2_Y = BAR_BOT + 21, BAR_BOT + 45
BAND_Y1, LEG_Y = NOTE2_Y + 24, NOTE2_Y + 40
W, H = 1000, LEG_Y + 40
d = D(W, H, "KUBERNETES IN ACTION · 03-02",
      "같은 30회인데 경로에 따라 도착지가 갈린다",
      "port-forward 는 Pod 하나에 직접 터널을 뚫어 kube-proxy 를 거치지 않으므로 30번이 한 Pod 로 "
      "몰린다. 클러스터 안에서 ClusterIP 로 가면 새 연결마다 endpoint 가 선택된다.",
      lead="분산은 Service 가 아니라 노드의 데이터패스가 한다 — 그 경로를 지나야 발동한다")

BARX, BARMAX = 420, 420      # 30회 = 420px
POD_LABELS = ["bhgc5 (worker)", "8phwt (worker)", "2vm7s (worker2)"]

ddx.band(d, 104, BAND_Y1, "한 요청을 셋에 복제하는 것이 아니라 연결 하나가 하나로 간다")

def panel(y0, title, sub, counts, c):
    d.t(36, y0, title, 13, INK, KR, "start", 600)
    d.t(36, y0 + 20, sub, 10, SOFT, KR, "start")
    for i, (lab, n) in enumerate(zip(POD_LABELS, counts)):
        y = y0 + 50 + i * 42
        d.t(BARX - 16, y + 4, lab, 11, MUTED, MONO, "end")
        w = round(n / 30 * BARMAX)
        cc = c if n else RULE
        if w:
            d.o.append(f'<rect x="{BARX}" y="{y-13}" width="{w}" height="26" rx="4" '
                       f'fill="{cc}22" stroke="{cc}" stroke-width="1.0"/>')
        d.t(BARX + w + 12, y + 4, f"{n}회", 11, c if n else SOFT, MONO, "start")
    return y0 + 50 + 3 * 42

y = panel(196, "① kubectl port-forward — kube-proxy 를 안 거친다",
          "Pod 하나에 직접 터널을 뚫는다. svc/kiada 라 써도 마찬가지다.", [30, 0, 0], BAD)
d.chip(700, 196 + 8, "한 Pod 에 고정", BAD, 11)

y2 = panel(P2_Y0, "② 클러스터 안에서 ClusterIP 로 — 노드 데이터패스가 고른다",
           "새 연결마다 endpoint 하나를 골라 DNAT 한다. kube-proxy 가 미리 규칙을 깔아 둔다.",
           [7, 10, 13], OK)
d.chip(700, P2_Y0 + 8, "세 Pod 로 분산", OK, 11)

d.line(36, 372, 964, 372, RULE, 0.8)

d.t(36, NOTE_Y, "표본이 30회라 13/10/7 정도의 편차는 난다 — iptables 규칙이 확률적으로 고르기 때문이다.",
     12, MUTED, KR, "start")
d.t(36, NOTE2_Y, "그중 하나는 다른 노드(worker2)였다 — 분산은 노드 경계를 넘는다.", 12, MUTED, KR, "start")
d.legend(LEG_Y, [("분산이 발동하지 않는 경로", BAD), ("분산이 발동하는 경로", OK)])
d.save("03-02-loadbalancing-portforward-vs-clusterip.svg")
print("ok loadbalancing")
