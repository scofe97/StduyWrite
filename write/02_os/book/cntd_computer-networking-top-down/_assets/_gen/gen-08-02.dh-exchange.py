# 타입 스펙: type-sequence — 두 참여자가 시간 축을 따라 한 번씩 주고받고, 각자 따로 계산한다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.2.2 Diffie-Hellman (책 573쪽) —
#   p·g 공개, SA·SB 비밀, 2,048 비트 권장, 그리고 g^(SA·SB) 로 만나는 유도는 원문 그대로.
#   원문이 K_B+ 를 g^SA 로 적은 것은 오기이며 본문에 정오로 병기했다. 여기서는 g^SB 로 그린다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO


def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """Seq.msg 는 라벨 font 를 MONO 로 못 박아 한글 자간이 벌어진다. 그 인자만 바꾼다."""
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, kr(sub))


W, H = 940, 596
d = SeqKR(W, H, "SECTION 8.2.2 · DIFFIE-HELLMAN",
          "공유 비밀을 주고받지 않고 만들어 냅니다",
          "오간 것은 공개키 둘뿐이다. 그런데 양쪽이 같은 값에 도달한다.",
          "p·g 공개와 SA·SB 비밀, 2,048 비트 권장은 원문 §8.2.2 의 것입니다")
d.lanes([("앨리스", "secret SA"), ("밥", "secret SB")], y0=120, lane_w=280)
d.rails(468)

d.t(470, 200, "p 와 g 를 골라 공개합니다 — 공격자도 압니다", 11, SOFT, KR)
d.state("앨리스", "K_A+ = g^SA mod p", 240, INFO)
d.state("밥", "K_B+ = g^SB mod p", 240, OK)
d.msg("앨리스", "밥", "K_A+", 292, INFO)
d.msg("밥", "앨리스", "K_B+", 336, OK)
d.state("앨리스", "(K_B+)^SA mod p", 392, ACC)
d.state("밥", "(K_A+)^SB mod p", 392, ACC)
d.t(470, 440, "둘 다 g^(SA·SB) mod p 에 도달합니다", 12, ACC, KR, "middle", 600)

PY = 484
d.box(24, PY, 892, 60, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "안전이 기대는 곳", 12, INK, KR, "start", 600)
d.t(44, PY + 48, "K_A+ 와 g 와 p 를 알아도 SA 를 알아내기가 극도로 어렵습니다. RSA 에서 n 을 인수분해하는 것만큼 어렵습니다.",
    11, MUTED, KR, "start")

d.legend(556, [("앨리스가 만든 것", INFO), ("밥이 만든 것", OK), ("둘이 만나는 자리", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-02.dh-exchange.svg"
d.save(out); print("→", out.name)
