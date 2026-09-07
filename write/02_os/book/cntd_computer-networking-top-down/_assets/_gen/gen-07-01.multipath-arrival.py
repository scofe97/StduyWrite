# 타입 스펙: type-sequence — 주체 여럿 사이의 시간순 전달. 한 번 보낸 신호가 세 번에 걸쳐 도착한다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.1 Figure 7.7 · Figure 7.8 —
#   직진파와 반사파의 시차, 그리고 coherence time 의 정의는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO


def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """Seq 프리미티브가 라벨 font 를 MONO 로 고정하므로 한글만 KR 로 돌려 씁니다."""

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dx = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dx} {y} L {x2 - 12 * dx} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, KR)


W, H = 940, 588
d = SeqKR(W, H, "SECTION 7.2.1 · MULTIPATH AND COHERENCE TIME",
          "한 번 보냈는데 세 번 도착합니다",
          "직진파와 반사파가 서로 다른 거리를 지나 시차를 두고 도착한다. 그 시차가 송신 간격의 하한을 정한다.",
          "경로 구성과 용어는 원문 Figure 7.7 · Figure 7.8 의 것입니다")

LANES = [("송신기", "sender"), ("가까운 건물", "reflector 1"),
         ("먼 건물", "reflector 2"), ("수신기", "receiver")]
d.lanes(LANES, y0=106, lane_w=196)
d.rails(322)

d.msg("송신기", "수신기", "line of sight", 176, OK, "ok",
      sub="가장 짧은 거리라 가장 먼저 닿습니다")
d.msg("송신기", "가까운 건물", "reflect", 222, WARN, "warn")
d.msg("가까운 건물", "수신기", "delayed copy 1", 252, WARN, "warn")
d.msg("송신기", "먼 건물", "reflect", 282, INFO, "info")
d.msg("먼 건물", "수신기", "delayed copy 2", 312, INFO, "info")

AY = 360
d.t(24, AY - 12, "수신기가 보는 것 — 한 번의 송신이 시간 위로 퍼집니다", 12, INK, KR, "start", 600)
X0, X1 = 176, 852
d.line(X0, AY + 76, X1, AY + 76, RULE, 1.0)
d.t(X1 + 16, AY + 80, "시각", 10, SOFT, KR, "start")
PULSES = [(0.06, OK, "직진파"), (0.22, WARN, "반사파 1"), (0.40, INFO, "반사파 2")]
for frac, c, lab in PULSES:
    x = X0 + (X1 - X0) * frac
    d.line(x, AY + 76, x, AY + 24, c, 2.4)
    d.t(x, AY + 14, lab, 11, c, KR)

XA = X0 + (X1 - X0) * 0.06
XB = X0 + (X1 - X0) * 0.40
d.line(XA, AY + 96, XB, AY + 96, ACC, 1.6)
d.line(XA, AY + 88, XA, AY + 104, ACC, 1.6)
d.line(XB, AY + 88, XB, AY + 104, ACC, 1.6)
d.t((XA + XB) / 2, AY + 124, "coherence time — 다음 펄스는 이 폭이 지난 뒤에야 보낼 수 있습니다",
    11, ACC, KR, "middle", 600)

d.t(24, AY + 156,
    "더 촘촘히 보내면 앞 펄스의 반사가 뒤 펄스와 섞여 수신기가 둘을 갈라내지 못합니다.", 11, MUTED, KR, "start")

d.legend(AY + 176, [("직진파", OK), ("반사파", WARN), ("더 늦은 반사파", INFO), ("송신 간격의 하한", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-01.multipath-arrival.svg"
d.save(out)
print("→", out)
