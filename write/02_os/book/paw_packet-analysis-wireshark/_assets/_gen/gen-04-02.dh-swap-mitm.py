# 04-02 §2 「인증서는 통과시키고 값만 바꾸는 공격」 — 같은 구간을 서명이 없을 때와 있을 때로 두 번 그린다.
# 본문 요구: "중간자는 서버의 인증서를 손대지 않고 그대로 전달합니다. … 그다음 ServerKeyExchange 만 가로채
#            DH 공개값을 자기 값으로 바꿔 보냅니다. 클라이언트는 중간자와 공유 비밀을 맺고, 중간자는 서버와
#            따로 하나를 더 맺습니다." / "값을 바꾸면 서명 검증이 깨지고, 서명을 그대로 두면 값을 바꿀 수 없습니다."
#            주체 셋 사이를 시간순으로 오가는 메시지이고, 논지는 같은 메시지가 서명 유무로 갈리는 자리다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 04-01.server-key-exchange 와 같은 문법으로
#           두 경우를 구분선으로 나눠 쌓는다. 메시지 stride 56, headline(acc)은 서명이 붙은 ServerKeyExchange 하나다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 13, MUTED, KR)

W, H = 960, 764
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02 §2",
          "서명이 없으면 인증서는 통과하고 DH 공개값만 바뀐다",
          "중간자는 서버의 인증서를 그대로 전달해 CA 서명 검증을 통과시킨 뒤 ServerKeyExchange 의 DH 공개값만 "
          "자기 값으로 바꾼다. 서명이 없으면 클라이언트와 서버가 각각 중간자와 공유 비밀을 맺는다. 서명이 붙으면 "
          "바꾼 값과 서명이 맞지 않아 클라이언트의 서명 검증에서 걸린다.",
          "TLS 1.2 ECDHE 기준입니다. A 는 ServerKeyExchange 에 서명이 없다고 가정한 경우입니다")

C, M, S = "클라이언트", "중간자", "서버"
d.lanes([(C, "CLIENT"), (M, "MITM"), (S, "SERVER")], y0=104, lane_w=240)
d.rails(708)

STEP = 56
YA = 236                      # A 의 첫 메시지
YB = YA + STEP * 6            # B 의 첫 메시지 = 572

# 구간 라벨이 클라이언트 레일을 지나는 자리는 레일을 가린다
for top in (YA - 66, YB - 66):
    d.o.append(f'<rect x="{d.LX[C] - 8}" y="{top}" width="16" height="28" fill="{PAPER}"/>')

def between(a, b, y, txt, c):
    x1, x2 = d.LX[a], d.LX[b]
    d.line(x1 + 12, y, x2 - 12, y, c, 1.2)
    d.chip((x1 + x2) / 2, y, txt, c, 13)

# ── A · 서명이 없다면 ─────────────────────────────────────────
d.t(24, YA - 48, "A · 서명이 없다면", 13, SOFT, KR, "start", 600)
d.msg(S, M, "Certificate", YA, INFO, "info", sub="a.test.crt · CA 서명 포함")
d.msg(M, C, "Certificate", YA + STEP, INFO, "info", sub="그대로 전달 · CA 서명 검증 통과")
d.msg(S, M, "ServerKeyExchange", YA + STEP * 2, MUTED, "ar", sub="서버의 DH 공개값")
d.msg(M, C, "ServerKeyExchange", YA + STEP * 3, BAD, "bad", sub="중간자의 DH 공개값으로 교체")
between(C, M, YA + STEP * 4, "공유 비밀 하나", BAD)
between(M, S, YA + STEP * 4, "따로 하나 더", BAD)

d.line(24, YA + STEP * 4 + 36, W - 48, YA + STEP * 4 + 36, RULE, 0.8, "4 6")

# ── B · 서명이 붙으면 ─────────────────────────────────────────
d.t(24, YB - 48, "B · 서명이 붙으면", 13, SOFT, KR, "start", 600)
d.msg(S, M, "ServerKeyExchange", YB, ACC, "acc", sub="DH 공개값 + 서버 서명")
d.msg(M, C, "ServerKeyExchange", YB + STEP, BAD, "bad", sub="값만 교체 · 서명은 서버 것 그대로")
d.chip(d.LX[C], YB + STEP * 2, "서명 검증 실패", BAD, 13)
d.chip(d.LX[M], YB + STEP * 2, "서버 개인키 없음 · 새 서명 불가", MUTED, 13)

d.legend(H - 40, [("인증서 · 그대로 전달", INFO), ("바꿔치기와 그 결과", BAD), ("서명이 붙은 공개값", ACC)])
d.save("04-02.dh-swap-mitm.svg")
