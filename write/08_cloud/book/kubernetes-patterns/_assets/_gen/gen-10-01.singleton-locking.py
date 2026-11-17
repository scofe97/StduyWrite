# 10-01 싱글턴을 만드는 두 층위 — 앱 밖 잠금과 앱 안 잠금을 나란히 놓는다
# 본문: 왼쪽은 앱 바깥 컨트롤러가 replicas 를 1 로 유지해 Pod 가 하나만 뜨는 방식이고, 앱은 자기가
#   싱글턴인지 모른다. 오른쪽은 Pod 셋이 다 떠 있고 분산 락(Lease)을 먼저 잡은 하나만 활성이 된다.
#   아래는 방식마다 주는 보장이다. ReplicaSet 은 at-least-one 이라 가끔 둘, StatefulSet 은
#   at-most-one 이라 가끔 0, 앱 안 락은 Pod 수와 무관하게 활성 하나다.
# 타입 스펙: type-layers — 같은 활성 하나를 두 층위(앱 밖 컨트롤러 / 앱 안 락)가 어떻게 받치는지
#   두 묶음을 나란히 놓고 그 아래에 보장을 한 줄로 붙인다. 옛 SVG 의 구조·라벨 뜻을 그대로 옮기고
#   한글 10px 만 11px 이상으로 올렸다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 900, 432
LX, RX, PW, PY, PH = 24, 466, 410, 104, 220

d = D(W, H, "KUBERNETES PATTERNS · 10-01",
      "싱글턴을 만드는 두 층위",
      "왼쪽 앱 밖 락은 컨트롤러가 replicas 를 1 로 유지해 Pod 가 하나만 뜨고 그 하나가 활성입니다. 오른쪽 앱 안 락은 Pod 셋이 다 떠 있고 분산 락 Lease 를 먼저 잡은 하나만 활성이 됩니다. "
      "아래는 방식마다 주는 보장으로 ReplicaSet 은 가끔 둘, StatefulSet 은 가끔 0, 앱 안 락은 Pod 수와 무관하게 하나입니다.",
      lead="앱 밖 락은 앱이 모르게 하나로 묶고, 앱 안 락은 앱이 직접 하나를 뽑습니다")

def panel(x, c, title, sub):
    d.box(x, PY, PW, PH, PAPER, c, 1.1, 6)
    d.t(x + 20, PY + 26, title, 14, c, MONO, "start", 600)
    d.t(x + 20, PY + 46, sub, 12, MUTED, KR, "start")

# ── 왼쪽: 앱 밖 락 ──────────────────────────────────────
panel(LX, WARN, "out-of-application 락", "앱 모르게 싱글턴")
d.tone(LX + 20, PY + 60, 370, 36, WARN, 5, "30", 1.1)
d.t(LX + 205, PY + 83, "컨트롤러 · replicas: 1", 13, WARN, KR, "middle", 600)
d.path(f"M {LX+205} {PY+100} L {LX+205} {PY+118}", WARN, 1.5, m="warn")
d.tone(LX + 126, PY + 122, 158, 44, OK, 5, "1c", 1.2)
d.t(LX + 205, PY + 142, "Pod", 13, OK, MONO, "middle", 600)
d.t(LX + 205, PY + 159, "활성", 12, OK, KR)
d.t(LX + 20, PY + 190, "Pod 가 하나뿐이라 그것이 활성", 12, MUTED, KR, "start")
d.t(LX + 20, PY + 208, "replica 증가는 못 막음", 12, MUTED, KR, "start")

# ── 오른쪽: 앱 안 락 ────────────────────────────────────
panel(RX, OK, "in-application 락", "앱이 리더 선출")
d.tone(RX + 20, PY + 60, 370, 36, OK, 5, "30", 1.1)
d.t(RX + 205, PY + 83, "분산 락 · Lease", 13, OK, KR, "middle", 600)
PODS = [(RX + 20, "Pod 1", "활성 · 락 보유", True), (RX + 146, "Pod 2", "passive", False), (RX + 272, "Pod 3", "passive", False)]
for x, name, st, active in PODS:
    cx = x + 59
    d.path(f"M {cx} {PY+100} L {cx} {PY+118}", OK if active else MUTED, 1.5,
           m="ok" if active else "ar", dash=None if active else "3 3")
    if active:
        d.tone(x, PY + 122, 118, 44, OK, 5, "1c", 1.2)
        d.t(cx, PY + 142, name, 13, OK, KR, "middle", 600)
        d.t(cx, PY + 159, st, 12, OK, KR)
    else:
        d.o.append(f'<rect x="{x}" y="{PY+122}" width="118" height="44" rx="5" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.0" stroke-dasharray="3 3"/>')
        d.t(cx, PY + 142, name, 13, MUTED, KR, "middle", 600)
        d.t(cx, PY + 159, st, 12, MUTED, MONO)
d.t(RX + 20, PY + 190, "셋 다 건강하지만 활성은 하나", 12, MUTED, KR, "start")
d.t(RX + 20, PY + 208, "일부 컴포넌트만 잠금 가능", 12, MUTED, KR, "start")

# ── 아래: 방식마다 주는 보장 ────────────────────────────
GY = PY + PH + 28
d.t(LX, GY, "각 방식이 주는 보장", 13, SOFT, KR, "start", 600)
GUAR = [(LX, BAD, "at-least-one", "ReplicaSet · 가끔 2개"),
        (LX + 294, INFO, "at-most-one", "StatefulSet · 가끔 0개"),
        (LX + 588, OK, "in-app 락 · 활성 하나", "Pod 수와 무관")]
for x, c, a, b in GUAR:
    d.tone(x, GY + 14, 264, 52, c, 6, "14", 1.1)
    d.t(x + 20, GY + 36, a, 13, c, KR if any('가' <= ch <= '힣' for ch in a) else MONO, "start", 600)
    d.t(x + 20, GY + 56, b, 12, MUTED, KR, "start")

d.save("10-01.singleton-locking.svg")
print("ok singleton-locking")
