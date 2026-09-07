# 타입 스펙: type-sequence — 두 참여자가 시간 축을 따라 주고받고 각자 상태를 남긴다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.6.1 Figure 8.24 (책 592~593쪽) —
#   hello · 인증서 · EMS 의 순서와 MS 에서 네 열쇠를 유도하는 것은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO


def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, kr(sub))


W, H = 940, 632
d = SeqKR(W, H, "SECTION 8.6.1 · THE ALMOST-TLS HANDSHAKE",
          "핸드셰이크가 남기는 것은 마스터 비밀 하나입니다",
          "이 국면이 끝나면 둘만 MS 를 안다. 나머지 열쇠는 전부 거기서 유도된다.",
          "메시지 순서와 네 열쇠는 원문 Figure 8.24 의 것입니다")
d.lanes([("밥 (클라이언트)", "client"), ("앨리스 (서버)", "server")], y0=120, lane_w=280)
d.rails(440)

d.msg("밥 (클라이언트)", "앨리스 (서버)", "TCP 연결", 196, SOFT, sub="먼저 세웁니다")
d.msg("밥 (클라이언트)", "앨리스 (서버)", "hello", 252, INFO)
d.msg("앨리스 (서버)", "밥 (클라이언트)", "인증서", 300, OK, sub="CA 가 서명한 공개키")
d.state("밥 (클라이언트)", "MS 를 만듭니다", 348, ACC)
d.msg("밥 (클라이언트)", "앨리스 (서버)", "EMS = K_A+(MS)", 396, ACC)
d.state("앨리스 (서버)", "개인키로 MS 복호", 430, ACC)

PY = 468
d.box(24, PY, 892, 100, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "MS 하나에서 열쇠 넷을 유도합니다 — 방향마다, 그리고 암호화와 무결성마다 따로", 12, INK, KR, "start", 600)
d.line(44, PY + 40, 896, PY + 40, RULE, 0.8)
KEYS = [(44, "E_B", "밥 → 앨리스 암호화"), (268, "M_B", "밥 → 앨리스 HMAC"),
        (492, "E_A", "앨리스 → 밥 암호화"), (716, "M_A", "앨리스 → 밥 HMAC")]
for x, k, desc in KEYS:
    d.t(x, PY + 66, k, 12, OK, MONO, "start", 600)
    d.t(x, PY + 86, desc, 11, MUTED, KR, "start")

d.legend(576, [("클라이언트가 여는 것", INFO), ("서버가 내놓는 것", OK), ("마스터 비밀", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-03.almost-tls-handshake.svg"
d.save(out); print("→", out.name)
