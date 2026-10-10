# 타입 스펙: type-data-flow — 서비스 100개를 더한 뒤 iptables 모드와 KPR 의 규칙 수·패킷 경로 비교. 배정된 비교 타입 이름이 스펙 목록에 없어 흐름 문법의 이 타입으로 바꿨다
# 사실 출처: 추출본 cil6.txt 줄 133-197(787), 384-392·469-486(KPR 0), 220-231(맵 조회)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 372
d = D(W, H, "CILIUM UP AND RUNNING · 06-01 §2", "서비스 100개를 더한 뒤의 규칙",
      "iptables 는 규칙이 늘고 체인을 순서대로 훑으며, KPR 은 맵을 키로 조회합니다",
      "예시 kind 클러스터 · 워커 노드 kind-worker")

LBL_X, LBL_W = 12, 168
BX = [200, 450, 700]
BW, BH = 200, 76
HDR_Y = 100
for x, t in zip(BX, ["클러스터 설정", "KUBE-SEP 줄 수", "패킷 처리"]):
    d.t(x + BW / 2, HDR_Y, t, 12, SOFT, KR, "middle", 600)

rows = [
    ("kube-proxy", "kindnet · iptables", WARN,
     ("kubeProxyMode:", "iptables", MONO), ("787 줄", "wc -l", WARN), ("체인을 위에서 아래로", "규칙 하나씩 비교", WARN)),
    ("Cilium KPR", "kube-proxy 없음", OK,
     ("kubeProxyMode:", "\"none\"", MONO), ("0 줄", "wc -l", OK), ("맵 키 조회", "10.96.45.144:80", OK)),
]
for i, (nm, sub, c, c1, c2, c3) in enumerate(rows):
    y = 116 + i * 112
    d.box(LBL_X, y, LBL_W, BH, PAPER2, RULE, 0.9)
    d.t(LBL_X + 14, y + 32, nm, 13, INK, MONO, "start", 600)
    d.t(LBL_X + 14, y + 54, sub, 11, MUTED, KR, "start")
    for j, (a, b, *rest) in enumerate([c1, c2, c3]):
        x = BX[j]
        tone = c if j > 0 else INFO
        d.tone(x, y, BW, BH, tone, r=6, op="12" if j != 1 else "18", sw=1.0 if j != 1 else 1.5)
        fam = MONO if j == 0 else KR
        d.t(x + BW / 2, y + 34, a, 13 if j else 12, tone, fam, "middle", 600)
        d.t(x + BW / 2, y + 58, b, 11, MUTED, MONO if (j == 0 or b[0].isdigit() or b == "wc -l") else KR)
    cy = y + BH / 2
    d.arrow([(BX[0] + BW, cy), (BX[1], cy)], MUTED, "ar", 1.5)
    d.arrow([(BX[1] + BW, cy), (BX[2], cy)], MUTED, "ar", 1.5)
    d.t((BX[0] + BW + BX[1]) / 2, cy - 8, "×100", 11, MUTED, MONO)

d.legend(H - 56, [("iptables 모드", WARN), ("KPR", OK), ("설정", INFO)])
d.save("06-01.iptables-vs-kpr-rules.svg")
