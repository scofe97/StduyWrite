# 02-02.probability-fanout — 위에서부터 평가되는 규칙과 그 결과 몫
# 본문: "KUBE-SVC 체인을 위에서부터 — 마킹 규칙이 먼저이고 확률은 그 다음이다"
# 타입 스펙: type-nested.md 경계 둘 + 부채꼴 전개. 확률이 세 번 다른데 몫이 같은 것이
#           요점이므로 왼쪽은 평가 순서, 오른쪽은 최종 몫을 나란히 둔다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 680
d = D(W, H, "KUBE-SVC · PROBABILITY FANOUT",
      "KUBE-SVC 체인을 위에서부터 — 마킹 규칙이 먼저이고 확률은 그 다음이다",
      "확률은 0.333 · 0.5 · 무조건으로 다르지만 최종 몫은 셋 다 1/3 이다. 앞 규칙이 빗나간 만큼만 남기 때문이다.",
      lead="확률은 셋 다 다른데 최종 몫은 같다 — 앞이 빗나간 만큼만 남기 때문이다")

LW, LH, RW, RH = 400, 72, 380, 72
LX, RX = 244, 748
LEFT = (40, 196, 408, 380)
RIGHT = (530, 254, 430, 322)
LCY = [246, 334, 422, 510]
# 규칙 1·2·3 과 KUBE-SEP 은 1:1 대응이므로 행을 맞춘다. 행이 어긋나 있던 탓에
# 잇는 선이 비스듬했다 — 오른쪽 행 높이를 왼쪽과 같이 두면 선이 곧아진다.
RCY = LCY[1:]

def bx(cx, cy, w, h, t, s, tag, c=None, focal=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(x + 16, cy - 8, ddx.fit(t, 12, w // 2, t), 12, tc, KR, "start", 600)
    d.t(x + 16, cy + 14, ddx.fit(s, 10, w // 2 + 20, s), 10, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·!' for ch in s) else KR, "start")
    d.t(x + w - 16, cy + 4, ddx.fit(tag, 10, w // 2 - 20, tag), 10, SOFT,
        MONO if all(ord(ch) < 128 or ch in '·-' for ch in tag) else KR, "end")

ddx.band(d, 104, 616, "확률이 다른 이유는 앞 규칙이 걸러 간 뒤의 남은 몫을 나누기 때문이다")
for (rx, ry, rw, rh), lab, c in [(LEFT, "KUBE-SVC-LOLE4ISW44XBNF3G — 위에서부터 평가", INFO),
                                 (RIGHT, "KUBE-SEP 체인 — 여기서 목적지가 바뀐다", ACC)]:
    d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, rx, ry, lab, 11, c, off=16)

bx(LX, LCY[0], LW, LH, "첫 규칙은 마킹", "! -s 10.244.0.0/16", "-j KUBE-MARK-MASQ", focal=True)
for cy, (t, s, tag) in zip(LCY[1:], [("규칙 1", "--probability 0.33333333349", "-j KUBE-SEP-2MJG…"),
                                     ("규칙 2", "--probability 0.50000000000", "-j KUBE-SEP-R4KM…"),
                                     ("규칙 3", "확률 조건 없음", "-j KUBE-SEP-MIOV…")]):
    bx(LX, cy, LW, LH, t, s, tag)
for a, b in zip(LCY, LCY[1:]):
    d.path(f"M {LX} {a+LH//2+4} L {LX} {b-LH//2-8}", MUTED, 1.4, m="ar")

for cy, (t, s, tag) in zip(RCY, [("KUBE-SEP-2MJG…", "DNAT 10.244.1.66:8080", "최종 몫 1/3"),
                                 ("KUBE-SEP-R4KM…", "DNAT 10.244.1.67:8080", "최종 몫 1/3"),
                                 ("KUBE-SEP-MIOV…", "DNAT 10.244.1.8:8080", "최종 몫 1/3")]):
    bx(RX, cy, RW, RH, t, s, tag, ACC)
for lcy, rcy, lab in zip(LCY[1:], RCY, ["1/3 적중", "남은 절반", "마지막 하나"]):
    d.path(f"M {LX+LW//2+6} {lcy} L {RX-RW//2-8} {rcy}", MUTED, 1.4, m="ar")
    # 라벨은 두 점선 경계(448 · 530) 한가운데에 둔다 — 선 중점(500)에 두면
    # '마지막 하나' 처럼 긴 라벨이 오른쪽 경계에 2px 까지 붙는다.
    d.t((LEFT[0] + LEFT[2] + RIGHT[0]) // 2, lcy - 14, lab, 10, MUTED, KR)

d.t(36, 592, "1/3 이 빗나가면 2/3 이 남고, 그 절반이 다시 1/3 이다 — 마지막은 조건 없이 나머지 전부를 받는다",
     12, MUTED, KR, "start")
d.legend(632, [("평가 순서", INFO), ("목적지가 바뀌는 자리", ACC)])
d.save("02-02.probability-fanout.svg")
print("ok probability-fanout")
