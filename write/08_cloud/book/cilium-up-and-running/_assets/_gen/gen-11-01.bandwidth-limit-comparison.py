# 타입 스펙: type-dp-security-matrix — 행 = Bandwidth Manager 적용 전(기본 상태)과 Pod 주석 적용 후(대역폭 제한), 열 = Pod 주석 설정 · 커널 스케줄러 메커니즘 · netperf 측정 처리량 · 대역폭 제어 영향 비교 행렬. 배정된 comparison 타입이 설치 목록에 없어 비교 행렬 문법을 가진 이 타입으로 선언했다. 셀 1개만 focal.
# 사실 출처: Cilium Up and Running 11장 cil11.txt 줄 874(EDT with BPF [CUBIC] [eth0]), 950-958(기본 처리량 8827.69 Mbps), 984(kubernetes.io/egress-bandwidth="10M"), 993-997(제한 후 처리량 9.54 Mbps)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 360
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 176, 12, 172, 8
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 52, 60
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(4)]

d = D(W, H, "CILIUM UP AND RUNNING · 11-01 §5", "Bandwidth Manager 적용 전·후 처리량 비교",
      "Pod egress 주석 유무에 따른 eBPF EDT 동작과 netperf 측정 처리량 차이",
      "Pod egress 주석 유무에 따른 eBPF EDT 동작과 netperf 측정 처리량 차이")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "측정 조건", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "condition", 11, MUTED, MONO)

cols = [
    ("Pod 주석 설정", "annotation"),
    ("커널 스케줄러", "mechanism"),
    ("측정 처리량", "netperf"),
    ("대역폭 통제 영향", "impact")
]
for j, (nm, code) in enumerate(cols):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, code, 11, MUTED, MONO)

rows = [
    ("제한 전 (기준선)", "baseline", [
        ("미설정", "기본 Pod", None),
        ("Linux 기본 큐잉", "qdisc fq", None),
        ("8827.69 Mbps", "10^6bits/sec", WARN),
        ("대역폭 독점 위험", "noisy neighbor", WARN)]),
    ("제한 후 (10M 상한)", "rate-limited", [
        ("egress-bandwidth", "10M 지정", OK),
        ("EDT with BPF", "FQ Pacing", OK),
        ("9.54 Mbps", "10 Mbps 이하", "focal"),
        ("송신 인터페이스 억제", "공정 점유 보장", OK)]),
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
        elif tone == WARN:
            d.tone(x, y, ROLE_W, ROW_H, WARN, r=4, op="10", sw=0.9)
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
        fam = KR if any("가" <= c <= "힣" for c in val) else MONO
        col = ACC if tone == "focal" else (OK if tone == OK else (WARN if tone == WARN else INK))
        if sub:
            d.t(x + ROLE_W / 2, y + 22, val, 12, col, fam, "middle", 600)
            sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
            d.t(x + ROLE_W / 2, y + 41, sub, 12, MUTED, sfam)
        else:
            d.t(x + ROLE_W / 2, y + 31, val, 12, col, fam, "middle", 600)

LEG_Y = ROW_Y0 + 1 * STRIDE + ROW_H + 24
d.legend(LEG_Y, [("대역폭 제한 적용", ACC), ("정상 제어", OK), ("대역폭 독점", WARN)])
d.save("11-01.bandwidth-limit-comparison.svg")
