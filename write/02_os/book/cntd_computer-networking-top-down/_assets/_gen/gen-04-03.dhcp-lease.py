# 타입 스펙: type-state — DHCP 클라이언트의 임대 상태 전이.
# 출처: RFC 2131 §4.4 상태 기계 + 이 기계의 실측 임대값 (lease 3,599 / T1 1,799 / T2 3,149)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, KR, MONO

W, H = 1000, 560
d = D(W, H, "DHCP LEASE STATE · RFC 2131",
      "빌린 주소에는 기한이 있습니다",
      "DHCP 클라이언트가 주소를 처음 얻는 네 단계와, 임대를 이어 가는 T1·T2 갱신 전이. 초 단위 값은 이 기계가 실제로 받은 임대에서 가져왔다.",
      "아래 초 단위 값은 임대 3,599초짜리 실측 응답에서 계산한 것입니다")

BW, BH = 200, 64
XS = [24, 278, 532, 786]
GAPS = [251, 505, 759]


def row(y, header, states, trans, hot=()):
    d.t(24, y - 38, header, 11, SOFT, KR, "start", 600)
    for x, (nm, sub) in zip(XS, states):
        d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 7)
        d.t(x + BW / 2, y + 27, nm, 13, INK, MONO, "middle", 600)
        d.t(x + BW / 2, y + 47, sub, 11, MUTED, KR, "middle")
    for i, (top, bot) in enumerate(trans):
        c = ACC if i in hot else MUTED
        d.arrow([(XS[i] + BW + 4, y + BH / 2), (XS[i + 1] - 6, y + BH / 2)],
                c, "acc" if i in hot else "ar", 1.5)
        d.t(GAPS[i], y - 24, top, 11, c, KR, "middle", 600)
        d.t(GAPS[i], y - 8, bot, 10, MUTED, MONO, "middle")


row(150, "처음 붙을 때 — 네 단계",
    [("INIT", "주소가 없습니다"), ("SELECTING", "제안을 기다립니다"),
     ("REQUESTING", "확정을 기다립니다"), ("BOUND", "임대를 씁니다")],
    [("DISCOVER", "dst 255.255.255.255 · src 0.0.0.0"),
     ("OFFER 뒤 REQUEST", "yiaddr · mask · lease"),
     ("ACK", "xid 0x82035391 · lease 3,599s")])

row(340, "임대를 이어 갈 때 — 타이머 둘",
    [("BOUND", "임대를 씁니다"), ("RENEWING", "임대해 준 서버에 재요청"),
     ("REBINDING", "아무 서버에나 재요청"), ("INIT", "주소를 놓고 처음부터")],
    [("T1 에 도달", "0.5 x lease = 1,799s"),
     ("T2 에 도달", "0.875 x lease = 3,149s"),
     ("임대 만료", "lease = 3,599s")],
    hot=(0, 1))

# 갱신에 성공하면 BOUND 로 돌아온다
d.path("M 632 404 L 632 448 L 124 448 L 124 410", OK, 1.4, m="ok", dash="6 5")
d.path("M 430 404 L 430 448", OK, 1.4, dash="6 5")
d.chip(250, 448, "ACK 를 받으면 BOUND 로", OK, 11)

d.t(24, 484, "위아래 두 줄의 BOUND 는 같은 상태입니다. 처음 얻는 길과 이어 가는 길이 여기서 만납니다.",
     11, MUTED, KR, "start")

d.legend(504, [("타이머가 미는 전이", ACC), ("갱신 성공", OK), ("그 밖의 전이", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "04-03.dhcp-lease.svg"
d.save(out)
print("T1", 3599 * 0.5, "T2", 3599 * 0.875, "→", out)
