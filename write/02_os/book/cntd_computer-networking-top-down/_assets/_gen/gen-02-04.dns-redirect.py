# 02-04 §4 — 원문 Figure 2.20 의 여섯 단계. 이름 해석 도중에 요청이 CDN 으로 넘어간다.
# 넘겨주기가 일어나는 3단계에 색을 달리 줬다 — IP 주소가 아니라 다른 도메인의 이름을 돌려주는 자리다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 응답은 점선, 마지막 성공만 강조색.
#
# dd.py 의 Seq.msg 를 두 군데 고쳐 쓴다 — 한글 라벨은 KR 로, 라벨 x 는 옮길 수 있게.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, lx=0):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + lx
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 1000, 724
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-04 §4",
          "이름 해석 도중에 넘어갑니다",
          "원문 Figure 2.20. NetCinema 의 권한 서버가 IP 주소 대신 KingCDN 도메인의 이름을 돌려주면서 요청이 CDN 으로 넘어간다.",
          "3단계가 넘겨주기입니다 — 주소가 아니라 다른 이름을 돌려줍니다")

d.lanes([("사용자 호스트", "브라우저"), ("LDNS", "로컬 DNS"),
         ("netcinema", "권한 DNS"), ("kingcdn DNS", "CDN 의 사설 DNS"), ("a1105", "콘텐츠 서버")],
        y0=104, lane_w=168)
d.rails(568)

d.msg("사용자 호스트", "LDNS", "video.netcinema.com ?", 186, sub="2단계 — 링크를 누르면")
d.msg("LDNS", "netcinema", "query", 240, lx=-60)
d.msg("netcinema", "LDNS", "a1105.kingcdn.com", 284, INFO, dash="5 4", lx=-60,
      sub="3단계 — 주소가 아니라 이름")
d.msg("LDNS", "kingcdn DNS", "a1105.kingcdn.com ?", 350, lx=-118)
d.msg("kingcdn DNS", "LDNS", "콘텐츠 서버 IP", 394, MUTED, dash="5 4", lx=-118,
      sub="4단계 — 어느 서버인지 여기서 정해집니다")
d.msg("LDNS", "사용자 호스트", "IP 주소", 452, MUTED, dash="5 4", sub="5단계")
d.msg("사용자 호스트", "a1105", "GET /6Y7B23V", 512, ACC, mk="acc", lx=-176,
      sub="6단계 — 직접 TCP 연결")

d.t(20, 600, "DASH 를 쓰면 서버가 먼저 매니페스트를 보내고, 클라이언트가 그 목록에서 청크를 골라 가져갑니다.",
     11, MUTED, KR, "start")
d.t(20, 622, "CDN 이 이 조회로 알게 되는 것은 클라이언트의 주소가 아니라 LDNS 의 주소입니다 — 이 설계의 근본 약점입니다.",
     11, MUTED, KR, "start")

d.legend(H - 60, [("최종 요청", ACC), ("넘겨주기", INFO), ("나머지", MUTED)])
d.save("02-04.dns-redirect.svg")
