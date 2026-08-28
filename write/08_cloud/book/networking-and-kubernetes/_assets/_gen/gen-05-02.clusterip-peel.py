# 05-02.clusterip-peel — ClusterIP 가 추상화한 것을 네 번에 걸쳐 벗긴다
# 본문 요구: 1 veth 짝 찾기 → 2 netns 확인 → 3 프로세스 둘(웹 서버·/pause) → 4 iptables
#           KUBE-SVC·KUBE-SEP 의 DNAT. 결론은 "DNS 레코드 + DNAT 체인 + Endpoints 삼위일체".
# 타입 스펙: type-dp-security-matrix.md — 열 머리가 "치는 명령"과 "드러나는 것", 행이 명령 넷 — 세로 대조가 논지
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 604   # 행 4개가 520 에서 끝난다
d = D(W, H, "ClusterIP · PEELING THE ABSTRACTION",
      "명령 넷으로 ClusterIP 를 끝까지 벗기면",
      "veth 짝에서 시작해 네임스페이스와 pause 를 거쳐 iptables DNAT 까지 내려간다.",
      lead="서비스라는 말의 실체는 DNS 레코드와 DNAT 체인과 Endpoints 목록 셋이다")

LX, LW, RX, RW, RY, RH, GAP = 32, 384, 448, 520, 152, 76, 12
STEPS = [
    ("ip a (Pod · 노드)", "eth0@if5 와 짝이 되는 veth45d1f3e8@if5", INFO),
    ("ip netns list", "Pod 의 네트워크 네임스페이스 cni-...", INFO),
    ("ip netns pid", "웹 서버 프로세스와 네임스페이스를 쥔 /pause", INFO),
    ("iptables -t nat -L", "KUBE-SVC → KUBE-SEP 가 Pod IP:8080 으로 DNAT", ACC),
]
d.t(LX + LW // 2, 140, "치는 명령", 12, SOFT, KR, "middle", 600)
d.t(RX + RW // 2, 140, "드러나는 것", 12, SOFT, KR, "middle", 600)
for i, (cmd, out, c) in enumerate(STEPS):
    y = RY + i * (RH + GAP)
    d.box(LX, y, LW, RH, PAPER2, RULE, 0.9, 6)
    d.t(LX + 20, y + 34, f"{i+1}", 11, SOFT, MONO, "start")
    d.t(LX + LW // 2, y + 46, cmd, 12, INK if c is not ACC else ACC, MONO, "middle", 600)
    if c is ACC:
        d.tone(RX, y, RW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(RX, y, RW, RH, PAPER2, c, 1.1, 6)
    d.t(RX + RW // 2, y + 46, ddx.fit(out, 12, RW - 24, out), 12,
        ACC if c is ACC else MUTED, KR)
    if i < 3:
        d.path(f"M {LX+LW//2} {y+RH+2} L {LX+LW//2} {y+RH+GAP-2}", MUTED, 1.2, m="ar")

FY = RY + 4 * (RH + GAP) + 16
d.t(36, FY + 24, "접근 경로 셋(서비스 이름 DNS · ClusterIP · Pod IP:8080)이 같은 Pod 에 닿는다 — 서비스는 그 셋의 합이다",
    12, MUTED, KR, "start")
d.legend(FY + 36, [("벗겨 나가는 층", INFO), ("실제로 주소를 바꾸는 자리", ACC)])
d.save("05-02.clusterip-peel.svg")
print("ok clusterip-peel")
