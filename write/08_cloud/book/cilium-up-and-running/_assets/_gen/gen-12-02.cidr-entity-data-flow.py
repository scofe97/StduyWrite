# 타입 스펙: type-data-flow — Pod 외부 트래픽이 노드 eBPF 에서 목적지 IP 확인, ipcache 의 CIDR identity 조회, toCIDR 규칙 판정을 거쳐 성공/차단되는 데이터 흐름.
# 사실 출처: Cilium Up and Running 12장 cil12.txt 줄 936-946(ipcache 새 identity 매핑), 947-975(toCIDR 1.1.1.1/32, curl 1.1.1.2 타임아웃, curl 1.1.1.1 HTTP 301)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 410
CW, GAPX, X0 = 196, 32, 24
XS = [X0 + i * (CW + GAPX) for i in range(4)]
RH, Y0, STRIDE = 100, 148, 126

d = D(W, H, "CILIUM UP AND RUNNING · 12-02 §3", "외부 목적지 IP 의 CIDR 신원 조회와 정책 판정",
      "ipcache 에 등록된 CIDR 대역은 고유 identity 로 변환되어 toCIDR 규칙과 대조된다",
      "ipcache 에 등록된 CIDR 대역은 고유 identity 로 변환되어 toCIDR 규칙과 대조된다")

for x, nm in zip(XS, ["출발지 Pod", "노드 ipcache", "Cilium 정책 맵", "판정 결과"]):
    d.box(x, 96, CW, 32, PAPER2, SOFT, 1.0)
    d.t(x + CW / 2, 117, nm, 13, INK, KR, "middle", 600)

rows = [
    (
        ["test 라벨 Pod", "curl 1.1.1.1"],
        ["1.1.1.1/32 대역 조회", "CIDR identity 매핑"],
        ["toCIDR 일치 확인", "규칙 매칭 성공"],
        ["HTTP 301 성공", "트래픽 전달 허용"],
        OK, False
    ),
    (
        ["test 라벨 Pod", "curl 1.1.1.2"],
        ["1.1.1.2 대역 조회", "world identity 부여"],
        ["toCIDR 불일치", "기본 거부 적용"],
        ["연결 타임아웃", "패킷 드롭 차단"],
        BAD, True
    ),
]

for i, (p_pod, p_ipc, p_pol, p_res, col, focal) in enumerate(rows):
    y = Y0 + i * STRIDE
    stages = [p_pod, p_ipc, p_pol, p_res]
    for j, lines in enumerate(stages):
        x = XS[j]
        if j == 3:
            d.tone(x, y, CW, RH, col, r=6, op="14", sw=1.3)
        else:
            d.box(x, y, CW, RH, PAPER2, RULE, 0.9)
        y1 = y + 38
        for k, ln in enumerate(lines):
            c_text = col if (j == 3 and k == 0) else (INK if k == 0 else MUTED)
            fam = KR if any("가" <= c <= "힣" for c in ln) else MONO
            d.t(x + CW / 2, y1 + k * 24, ln, 12, c_text, fam, "middle", 600 if k == 0 else 400)
    for j in range(3):
        d.arrow([(XS[j] + CW + 4, y + RH / 2), (XS[j + 1] - 6, y + RH / 2)], MUTED, "ar", 1.5)

d.save("12-02.cidr-entity-data-flow.svg")
