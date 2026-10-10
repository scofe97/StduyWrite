# 타입 스펙: type-dp-security-matrix — 행 = 세 가지 외부 송신 방식(마스커레이딩 없음 · 노드 IP 마스커레이딩 · Egress Gateway), 열 = 출발지 IP · 외부 대상 IP · 외부에서 보이는 출발지 IP · 귀환 경로와 식별성 비교 행렬. 배정된 comparison 타입이 설치 목록에 없어 비교 행렬 문법을 가진 이 타입으로 선언했다. 셀 1개만 focal.
# 사실 출처: Cilium Up and Running 11장 cil11.txt 줄 56-60(Figure 11-1 10.244.1.3 → 172.18.0.3), 348-356(Figure 11-3 Pod 10.1.2.106 · 노드 172.18.0.3 · Egress IP 10.0.3.42 · 외부 10.0.4.2) / docs.cilium.io v1.20.2 network/egress-gateway/
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 424
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 210, 12, 216, 14
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 52, 60
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(3)]

d = D(W, H, "CILIUM UP AND RUNNING · 11-01", "외부 트래픽 송신 방식과 출발지 IP",
      "마스커레이딩 해제 · 노드 IP SNAT · Egress Gateway 의 출발지 변환과 식별성 비교",
      "마스커레이딩 해제 · 노드 IP SNAT · Egress Gateway 의 출발지 변환과 식별성 비교")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "송신 구성", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "egress mode", 11, MUTED, MONO)

cols = [
    ("원본 출발지 · 목적지", "src & dst"),
    ("외부에서 본 출발지", "observed src"),
    ("귀환 경로와 식별성", "routing & identity")
]
for j, (nm, code) in enumerate(cols):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, code, 11, MUTED, MONO)

rows = [
    ("마스커레이딩 해제", "masq: false", [
        ("10.1.2.106 → 10.0.4.2", "변환 없음", None),
        ("10.1.2.106", "Pod IP 유지", BAD),
        ("경로 부재로 응답 유실", "통신 실패", BAD)]),
    ("노드 IP 마스커레이딩", "기본 SNAT", [
        ("10.1.2.106 → 10.0.4.2", "노드 IP 로 변환", None),
        ("172.18.0.3", "노드 IP 로 치환", OK),
        ("응답 가능 · 식별 불가", "워크로드 출처 은폐", WARN)]),
    ("Egress Gateway", "CEGP 정책", [
        ("10.1.2.106 → 10.0.4.2", "게이트웨이 노드 전달", None),
        ("10.0.3.42", "고정 egress IP", "focal"),
        ("응답 가능 · 테넌트 식별", "감사 추적 충족", OK)]),
]

for i, (name, hint, cells) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 12, y + 22, name, 13, INK, KR, "start", 600)
    d.t(LP + 12, y + 41, hint, 11, MUTED, MONO, "start")
    for j, (val, sub, tone) in enumerate(cells):
        x = RX[j]
        if tone == "focal":
            d.tone(x, y, ROLE_W, ROW_H, ACC, r=4, op="14", sw=1.4)
        elif tone == OK:
            d.tone(x, y, ROLE_W, ROW_H, OK, r=4, op="10", sw=0.9)
        elif tone == BAD:
            d.tone(x, y, ROLE_W, ROW_H, BAD, r=4, op="10", sw=0.9)
        elif tone == WARN:
            d.tone(x, y, ROLE_W, ROW_H, WARN, r=4, op="10", sw=0.9)
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
        fam = KR if any("가" <= c <= "힣" for c in val) else MONO
        col = ACC if tone == "focal" else (OK if tone == OK else (BAD if tone == BAD else (WARN if tone == WARN else INK)))
        if sub:
            d.t(x + ROLE_W / 2, y + 22, val, 12, col, fam, "middle", 600)
            sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
            d.t(x + ROLE_W / 2, y + 41, sub, 12, MUTED, sfam)
        else:
            d.t(x + ROLE_W / 2, y + 31, val, 12, col, fam, "middle", 600)

LEG_Y = ROW_Y0 + 2 * STRIDE + ROW_H + 24
d.legend(LEG_Y, [("테넌트 식별", ACC), ("응답 가능", OK), ("식별 불가", WARN), ("응답 유실", BAD)])
d.save("11-01.chapter-overview.svg")
