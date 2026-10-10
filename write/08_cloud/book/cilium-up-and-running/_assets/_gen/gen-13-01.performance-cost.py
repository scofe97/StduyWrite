# 타입 스펙: type-dp-security-matrix — 행 = L3/L4 정책만 대 L7 HTTP 정책 적용 두 경로, 열 = 처리 경로 · Siege 총 시간 · 개별 응답 시간 · 초당 처리량의 비교 행렬. 배정된 comparison 타입이 스펙 목록에 없어 비교 행렬 스펙의 이 타입으로 선언했다. 셀 1개만 focal.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 366-387(L3 Siege: 2500 hits, 10.21s, 0.03s, 244.86 trans/sec), 397-422(L7 Siege: 2500 hits, 20.35s, 0.02s, 122.85 trans/sec)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 360
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 176, 12, 172, 8
HDR_Y, HDR_H = 96, 52
ROW_Y0, ROW_H, STRIDE = 168, 52, 60
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(4)]

d = D(W, H, "CILIUM UP AND RUNNING · 13-01 §3", "L3/L4 정책과 L7 정책의 처리 성능 비교",
      "Siege 2,500회 요청 기준 커널 eBPF 직결 경로와 Envoy 프록시 경유 경로의 소요 시간 및 처리량 차이",
      "Siege 2,500회 요청 기준 커널 eBPF 직결 경로와 Envoy 프록시 경유 경로의 소요 시간 및 처리량 차이")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 24, "적용 정책", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HDR_Y + 42, "policy mode", 11, MUTED, MONO)

cols = [
    ("패킷 처리 경로", "datapath"),
    ("Siege 총 소요 시간", "elapsed time"),
    ("개별 응답 시간", "response time"),
    ("초당 처리량", "transaction rate")
]
for j, (nm, code) in enumerate(cols):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 24, nm, 13, INK, KR, "middle", 600)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 42, code, 11, MUTED, MONO)

rows = [
    ("L3/L4 정책만", "L3/L4 only", [
        ("커널 eBPF 직결", "사용자 공간 미경유", OK),
        ("10.21초", "2500 hits 완료", None),
        ("0.03초", "약 30ms 소요", None),
        ("244.86 trans/sec", "동시성 6.25", OK)]),
    ("L7 HTTP 정책", "L7 via Envoy", [
        ("Envoy 프록시 경유", "별도 TCP 연결", WARN),
        ("20.35초", "소요 시간 약 2배", WARN),
        ("0.02초", "약 20ms 소요", None),
        ("122.85 trans/sec", "처리량 약 50% 급감", "focal")]),
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
d.legend(LEG_Y, [("프록시 오버헤드 (처리량 반감)", ACC), ("커널 고속 처리", OK), ("총 소요 시간 증가", WARN)])
d.save("13-01.performance-cost.svg")
