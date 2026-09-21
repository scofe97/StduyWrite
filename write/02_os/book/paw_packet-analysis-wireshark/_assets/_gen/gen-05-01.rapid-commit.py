# 05-01 §3 — rapid commit 이 네 걸음을 두 걸음으로 줄인다.
# 본문 요구: "SOLICIT 다음에 ADVERTISE 없이 바로 REPLY 가 오면 rapid commit 이 쓰인 것입니다.
#            두 메시지만 보이는 것이 실패가 아니라 정상일 수 있다는 뜻이라, 메시지 수만 세고
#            판단하면 안 됩니다."
#            같은 두 주체 사이에서 경로가 갈리므로 두 컷을 위아래로 쌓아 대비시킨다.
#            위 컷은 SARR 네 걸음, 아래 컷은 두 걸음이고, 건너뛰어지는 것은 ADVERTISE 하나다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. headline(accent)은 ADVERTISE 없이
#           바로 오는 REPLY 하나. 프리미티브의 Seq.msg 가 한글을 MONO 로 하드코딩하므로
#           gen-05-01.sarr.py 와 같은 SeqKR 계약으로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 16, sub, 11, MUTED, KR)

W, H = 940, 688
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §3",
          "rapid commit — SARR 네 걸음을 두 걸음으로",
          "같은 두 주체 사이에서 경로가 갈린다. 위는 SARR 네 메시지, 아래는 rapid commit 옵션이 붙어 "
          "두 메시지로 끝나는 경우다. 건너뛰어지는 것은 ADVERTISE 하나이고, REQUEST 도 함께 사라진다. "
          "캡처에 메시지가 둘만 보이는 것이 실패가 아니라 정상일 수 있다.",
          "메시지 수만 세면 rapid commit 을 실패로 오독합니다")

d.lanes([("클라이언트", "UDP 546"), ("서버", "UDP 547")], y0=104, lane_w=300)
d.rails(560)

# 위 컷 — SARR 네 걸음 (대비용이라 흐리게)
d.t(24, 176, "SARR 기본 · 네 메시지", 11, SOFT, KR, "start", 600)
d.msg("클라이언트", "서버", "SOLICIT", 204, MUTED, "ar", sub="msgtype==1 · 서버 탐색")
d.msg("서버", "클라이언트", "ADVERTISE", 256, MUTED, "ar", sub="msgtype==2 · 가용성 통지")
d.msg("클라이언트", "서버", "REQUEST", 308, MUTED, "ar", sub="msgtype==3 · 서버 하나 선택")
d.msg("서버", "클라이언트", "REPLY", 360, MUTED, "ar", sub="msgtype==7 · 주소 확정")

d.line(24, 400, W - 48, 400, RULE, 0.8, "4 6")

# 아래 컷 — rapid commit 두 걸음
d.t(24, 436, "SARR + rapid commit · 두 메시지", 11, ACC, KR, "start", 600)
d.msg("클라이언트", "서버", "SOLICIT", 464, INFO, "info",
      sub="msgtype==1 · rapid commit 옵션 동봉")
d.msg("서버", "클라이언트", "REPLY", 524, ACC, "acc",
      sub="msgtype==7 · ADVERTISE 없이 바로 확정")

d.state("클라이언트", "IPv6 주소 확보", 560, OK)

d.t(24, 596, "건너뛰는 것 — ADVERTISE 와 REQUEST 두 메시지 · 왕복 한 번", 12, SOFT, KR, "start")
d.t(24, 618, "서버가 옵션 미지원 — 위 컷의 네 메시지 교환으로 되돌아감", 11, MUTED, KR, "start")

d.legend(H - 44, [("ADVERTISE 없이 오는 확정", ACC), ("옵션이 실리는 자리", INFO), ("주소 확보", OK)])
d.save("05-01.rapid-commit.svg")
