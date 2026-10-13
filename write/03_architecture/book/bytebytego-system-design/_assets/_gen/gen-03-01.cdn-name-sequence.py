# 타입 스펙: type-sequence — 사이트 권한 서버의 CNAME 이 CDN 권한 서버로 이어지고 CDN 이 리졸버 주소 기준으로 엣지 주소를 고르는 이름 풀이(레인 4, 메시지 6).
# 사실 출처: RFC 1034 §3.6.2(CNAME 은 별칭, 정규 이름은 RDATA), RFC 7871 §1(권한 서버는 질의한 리졸버의 주소로 위치를 판단, EDNS Client Subnet 이 클라이언트 네트워크를 알림, Informational),
#   RFC 2606(.example 은 문서·예시용 최상위 이름), RFC 5737(203.0.113.0/24 TEST-NET-3 은 문서용 주소). 이름·주소는 모두 예시 값이며 측정값이 아니다. 단계 구성은 추출본 v1.txt 2070~2110행.
# Layout conventions: 레인 4·폭 184·간격 208, 호출 한 건의 stride 64(라벨 y-9, 부라벨 y+17), 첫 메시지 y=196. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))


W, H = 880, 640
d = SeqKR(W, H, "BYTEBYTEGO · 03-01 §6",
          "사이트의 이름이 CDN 의 이름으로 바뀌고 엣지 주소가 나온다",
          "CNAME 한 단계 뒤 CDN 권한 서버가 질의한 리졸버를 기준으로 엣지를 고름 (이름·주소는 문서용 예시)",
          "CDN 권한 서버가 보는 것은 사용자가 아니라 리졸버의 주소입니다")
BR, RS, ST, CD = "브라우저", "재귀 리졸버", "사이트 권한 서버", "CDN 권한 서버"
d.lanes([(BR, "스텁"), (RS, "캐시 보유"), (ST, "www.shop.example"), (CD, "cdn.example")], 100, 184)
d.rails(H - 80)

Y0, S = 196, 64
d.msg(BR, RS, "www.shop.example A ?", Y0 + 0 * S, MUTED, "ar")
d.msg(RS, ST, "www.shop.example A ?", Y0 + 1 * S, MUTED, "ar")
d.msg(ST, RS, "CNAME shop.cdn.example", Y0 + 2 * S, INFO, "info", dash="5 4", sub="별칭 응답")
d.msg(RS, CD, "shop.cdn.example A ?", Y0 + 3 * S, MUTED, "ar", sub="질의 출처는 리졸버 주소", dx=100)
d.msg(CD, RS, "A 203.0.113.17", Y0 + 4 * S, ACC, "acc", dash="5 4", sub="리졸버에서 가까운 엣지", dx=100)
d.msg(RS, BR, "A 203.0.113.17", Y0 + 5 * S, OK, "ok", dash="5 4", sub="CNAME 사슬의 끝")

d.legend(H - 56, [("질의", MUTED), ("별칭 응답", INFO), ("엣지 선택", ACC), ("최종 주소", OK)])
d.save("03-01.cdn-name-sequence.svg")
