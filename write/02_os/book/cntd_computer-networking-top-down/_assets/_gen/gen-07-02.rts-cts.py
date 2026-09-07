# 타입 스펙: type-sequence — 주체 여럿 사이의 시간순 메시지. 짧은 예약 프레임이 긴 프레임의 자리를 잡아 준다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.1 Figure 7.21 —
#   RTS · CTS · DATA · ACK 순서와 CTS 의 두 가지 역할은 원문 그대로
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

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * (11.0 if any("가" <= ch <= "힣" for ch in txt) else 7.0) + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, kr(txt))


W, H = 940, 588
d = SeqKR(W, H, "SECTION 7.3.1 · RTS AND CTS",
          "짧은 두 프레임으로 긴 프레임의 자리를 미리 잡습니다",
          "숨은 단말이 있어도 CTS 를 들은 기기는 지정된 시간 동안 조용히 있는다. 충돌하더라도 짧은 프레임만 낭비된다.",
          "메시지 순서와 CTS 의 두 역할은 원문 Figure 7.21 의 것입니다")

d.lanes([("보내려는 기기", "sender"), ("AP", "access point"), ("AP 반대편 기기들", "hidden from sender")],
        y0=106, lane_w=252)
d.rails(388)

d.msg("보내려는 기기", "AP", "RTS", 168, INFO, "info",
      sub="보낼 DATA 와 ACK 에 필요한 시간을 담습니다")
d.msg("AP", "AP 반대편 기기들", "CTS", 220, ACC, "acc",
      sub="들리는 범위의 모두에게 나갑니다")
d.msg("AP", "보내려는 기기", "CTS", 262, ACC, "acc", sub="보내도 좋다는 허락")
d.state("AP 반대편 기기들", "지정된 시간 동안 송신 보류", 306, WARN)
d.msg("보내려는 기기", "AP", "DATA", 344, OK, "ok")
d.msg("AP", "보내려는 기기", "ACK", 376, OK, "ok")

PY = 412
d.box(24, PY, 430, 100, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "얻는 것 둘", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "숨은 단말이 CTS 를 듣고 물러납니다.",
    "충돌이 나도 짧은 RTS·CTS 만 날립니다.",
]):
    d.t(44, PY + 52 + i * 22, "·  " + ln, 11, MUTED, KR, "start")

d.box(474, PY, 430, 100, PAPER2, RULE, 1.0)
d.t(494, PY + 26, "그래서 항상 쓰지는 않습니다", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "RTS·CTS 자체가 지연과 채널을 씁니다.",
    "긴 DATA 프레임을 예약할 때만 씁니다.",
]):
    d.t(494, PY + 52 + i * 22, "·  " + ln, 11, MUTED, KR, "start")

d.legend(534, [("예약 요청", INFO), ("예약 허락", ACC), ("보류 중", WARN), ("실제 데이터", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-02.rts-cts.svg"
d.save(out)
print("→", out)
