# 04-02.nine-step-check — Pod 에서 출발해 배선·규칙·상태·경로를 아홉 번에 이어 확인하는 순서
# 본문 요구: "1~2번은 배선, 3~5번은 규칙, 6번은 상태, 7~9번은 경로를 봅니다 … 어디서 끊기는지가 곧 어느 컴포넌트의 문제인지"
#           (전제: Calico CNI + kube-proxy iptables 모드)
# 타입 스펙: type-process — 단계 머리 + 같은 의미 슬롯(이름 · 명령 · 기대값)이 칸마다 같은 자리에 반복된다.
#           아홉 칸이 한 줄에 안 들어가 배선·규칙·상태 경로 세 줄로 접고, 줄을 접는 화살표는 읽는 순서만 나른다.
#           focal 은 서비스 주소가 Pod 주소로 바뀌는 5번 DNAT 칸. 2026-11-08 Mermaid 흐름도를 대체.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 576
d = D(W, H, "CALICO + IPTABLES MODE · NINE-STEP CHECK",
      "아홉 명령이 배선에서 경로까지 한 줄로 이어집니다",
      "1~2번은 Pod 의 배선, 3~5번은 kube-proxy 의 규칙이 서비스 주소를 Pod 주소로 바꾸는 과정, "
      "6번은 conntrack 상태, 7~9번은 바뀐 주소로 가는 경로를 확인한다. Calico BGP 비오버레이와 iptables 모드를 전제하며, "
      "8번의 PERMANENT 는 VXLAN 모드로 돌릴 때 vxlan.calico 이웃에 찍힌다. cali… 인터페이스는 호스트 네트워크가 아닌 Pod 마다 하나씩 생긴다. "
      "10.244.242.66 은 Calico 예시 클러스터의 CoreDNS Pod 주소이고 다른 도식의 주소와는 다른 클러스터 예시다.",
      lead="어디서 끊기는지가 곧 어느 컴포넌트의 문제인지를 가른다")

CW, CH, GAP = 200, 100, 16
BX0 = 124
ROWS = [
    ("배선", INFO, 112, [
        ("1 · Pod 의 길", ["kubectl exec probe", "-- ip route"], "default via 169.254.1.1"),
        ("2 · calico 인터페이스", ["ip link | grep cali"], "cali… = 비호스트망 Pod 수"),
    ]),
    ("규칙", WARN, 256, [
        ("3 · 진입 체인", ["iptables -t nat", "-L KUBE-SERVICES"], "10.96.0.10 → KUBE-SVC-…"),
        ("4 · 서비스 체인", ["iptables -t nat", "-L KUBE-SVC-…"], "random probability 0.5"),
        ("5 · 엔드포인트 체인", ["iptables -t nat", "-L KUBE-SEP-…"], "DNAT 10.244.242.66:53"),
    ]),
    ("상태 · 경로", OK, 400, [
        ("6 · conntrack 장부", ["conntrack -L | head -5"], "ASSURED · UDP 30·120초"),
        ("7 · 경로 예측", ["ip route get", "10.244.242.66"], "cali… 또는 via 노드 IP"),
        ("8 · 이웃 캐시", ["ip neigh"], ["REACHABLE", "(VXLAN 이면 PERMANENT)"]),
        ("9 · 실측", ["traceroute", "10.244.242.66"], "예측한 hop 과 일치"),
    ]),
]


def bx(j):
    return BX0 + j * (CW + GAP)


for band, bc, by, steps in ROWS:
    d.chip(68, by + CH // 2 - 4, band, bc, 11, 4)
    for j, (name, cmds, exp) in enumerate(steps):
        focal = name.startswith("5")
        c = ACC if focal else bc
        x = bx(j)
        d.tone(x, by, CW, CH, c, 6, "14", 1.4 if focal else 1.1)
        d.t(x + 12, by + 24, ddx.fit(name, 13, CW - 24, name), 13, c, KR, "start", 600)
        for k, ln in enumerate(cmds):
            d.t(x + 12, by + 46 + k * 16, ddx.fit(ln, 12, CW - 24, ln), 12, INK, MONO, "start")
        exps = exp if isinstance(exp, list) else [exp]
        for k, ln in enumerate(exps):
            d.t(x + 12, by + 90 - (len(exps) - 1 - k) * 16, ddx.fit(ln, 12, CW - 24, ln), 12, MUTED, MONO, "start")
        if j < len(steps) - 1:
            d.arrow([(x + CW + 2, by + CH // 2), (x + CW + GAP - 4, by + CH // 2)], SOFT, "soft", 1.3)

# 줄 바꿈 화살표 — 앞 줄 마지막 칸 아래에서 내려와 다음 줄 첫 칸 위로 들어간다
for (_, _, by, steps), (_, _, ny, _) in zip(ROWS, ROWS[1:]):
    xa = bx(len(steps) - 1) + CW // 2
    xb = bx(0) + CW // 2
    ym = by + CH + 22
    d.arrow([(xa, by + CH + 2), (xa, ym), (xb, ym), (xb, ny - 4)], SOFT, "soft", 1.3)

d.legend(528, [("배선 · 1~2번", INFO), ("규칙 · 3~5번", WARN), ("상태 · 경로 · 6~9번", OK), ("주소가 바뀌는 칸", ACC)])
d.save("04-02.nine-step-check.svg")
print("ok nine-step-check")
