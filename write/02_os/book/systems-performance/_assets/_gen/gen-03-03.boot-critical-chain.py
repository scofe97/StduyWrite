# 03-03 §4 — 원서 3.4.2 의 systemd-analyze critical-chain 출력: 서비스마다 @활성화 시각 위에 +시작 시간 막대.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간(서비스 시작에 걸린 시간)이다.
#           축약: 행은 '+' 값이 있는 서비스 일곱, 시각순. target 은 막대 없이 graphical.target 세로선만 둔다.
#           1초 = 64px, 행 40, 막대 24(스펙). focal 은 가장 긴 systemd-networkd-wait-online(1.860s).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 524
X0, PX, Y0, RH, BH = 312, 64, 136, 40, 24
def X(s): return X0 + s * PX

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-03 §4",
       "부팅 임계 경로 — 서비스마다 활성화 시각과 시작에 걸린 시간",
       "원서 3.4.2 의 critical-chain 출력에서 + 값이 있는 서비스 일곱을 활성화 시각(@)에 놓고 시작에 걸린 시간(+)을 막대로 그렸다. graphical.target 은 9.663초에 닿았다.",
       "가장 긴 막대가 부팅을 가장 오래 붙잡은 서비스입니다")

ROWS = [("systemd-remount-fs.service", 0.391, 0.081), ("cloud-init-local.service", 2.107, 1.141),
        ("systemd-networkd.service", 3.254, 0.235), ("systemd-networkd-wait-online.service", 3.498, 1.860),
        ("cloud-init.service", 5.361, 0.905), ("snapd.socket", 6.316, 0.016), ("snapd.seeded.service", 9.062, 0.062)]
for s in range(0, 11):
    d.line(X(s), Y0 - 8, X(s), Y0 + len(ROWS) * RH, RULE, 0.8)
    d.t(X(s), Y0 - 16, f"{s}s", 12, SOFT, MONO)
for i, (name, at, dur) in enumerate(ROWS):
    y = Y0 + i * RH + 8
    focal = dur == 1.860
    c = ACC if focal else INFO
    w = max(dur * PX, 3)
    d.tone(X(at), y, w, BH, c, 3, "33" if focal else "22", 1.2 if focal else 1.0)
    d.t(X0 - 16, y + 17, name, 12, ACC if focal else INK, MONO, "end", 600 if focal else 400)
    lab = f"+{int(dur * 1000)}ms" if dur < 1 else f"+{dur:.3f}s"
    if at > 9: d.t(X(at) - 8, y + 17, lab, 12, c, MONO, "end", 600)   # graphical.target 선을 피해 왼쪽에
    else: d.t(X(at) + w + 8, y + 17, lab, 12, c, MONO, "start", 600)
gx = X(9.663)
d.line(gx, Y0 - 8, gx, Y0 + len(ROWS) * RH + 8, INK, 1.2, "4 4")
d.t(gx, Y0 + len(ROWS) * RH + 26, "graphical.target @9.663s", 12, INK, MONO, "end")

d.legend(Y0 + len(ROWS) * RH + 48, [("가장 느린 서비스", ACC), ("임계 경로의 서비스", INFO)])
d.save("03-03.boot-critical-chain.svg")
