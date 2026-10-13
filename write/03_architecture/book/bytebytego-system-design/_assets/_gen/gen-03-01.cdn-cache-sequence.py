# 타입 스펙: type-sequence — 엣지에서 미스가 지역 캐시와 원본까지 올라갔다 내려와 보관되고 뒤의 요청이 엣지에서 적중하는 왕복(레인 4, 메시지 8).
# 사실 출처: Amazon CloudFront 개발자 안내서 "How CloudFront delivers content"(POP 에서 캐시 확인, 없으면 regional edge cache 를 거쳐 원본, 응답을 캐시에 보관),
#   RFC 9111 §5.1(Age 는 원본이 만들었거나 재검증한 뒤 흐른 시간이고, 필드가 있으면 이번 요청을 위해 원본이 만들거나 검증한 응답이 아니라는 뜻)·§5.2.2.10(s-maxage). /logo.png·max-age=3600·Age: 60 은 문서용 예시 값이다. 미스 경로(처음 요청)의 응답에는 Age 를 두지 않았다. 단계 구성은 추출본 v1.txt 2110~2125행.
# Layout conventions: 레인 4·폭 184·간격 208, 호출 한 건의 stride 64(라벨 y-9, 부라벨 y+17), 첫 메시지 y=196, 상태 칩은 엣지 레인 옆. 모든 좌표 4의 배수.
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

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def chip(s, a, txt, y, c, dx=0):
        x = s.LX[a] + dx
        w = len(txt) * (12 if any("가" <= ch <= "힣" for ch in txt) else 7.8) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 880, 800
d = SeqKR(W, H, "BYTEBYTEGO · 03-01 §7",
          "엣지가 응답을 보관하면 뒤의 요청은 원본까지 가지 않는다",
          "첫 요청은 엣지와 지역 캐시를 지나 원본까지 올라가고 60초 뒤 요청은 엣지에서 끝남 (값은 문서용 예시)",
          "Age 는 원본이 만들거나 검증한 뒤 흐른 초이고 max-age 안이면 신선합니다")
BR, ED, RG, OR = "브라우저", "엣지", "지역 캐시", "원본"
d.lanes([(BR, "사용자 쪽"), (ED, "203.0.113.17"), (RG, "POP 보다 큰 캐시"), (OR, "origin.shop.example")], 100, 184)
d.rails(H - 80)

Y0, S = 196, 64
d.msg(BR, ED, "GET /logo.png", Y0 + 0 * S, MUTED, "ar")
d.msg(ED, RG, "GET /logo.png", Y0 + 1 * S, WARN, "warn", sub="엣지 미스")
d.msg(RG, OR, "GET /logo.png", Y0 + 2 * S, WARN, "warn", sub="지역 캐시 미스")
d.msg(OR, RG, "200 · max-age=3600", Y0 + 3 * S, MUTED, "ar", dash="5 4", sub="Cache-Control")
d.msg(RG, ED, "200", Y0 + 4 * S, MUTED, "ar", dash="5 4")
d.msg(ED, BR, "200", Y0 + 5 * S, MUTED, "ar", dash="5 4")
d.chip(ED, "엣지에 보관", Y0 + 5 * S + 32, WARN, 0)
d.msg(BR, ED, "GET /logo.png", Y0 + 6 * S + 20, MUTED, "ar", sub="60초 뒤")
d.msg(ED, BR, "200 · Age: 60", Y0 + 7 * S + 20, ACC, "acc", dash="5 4", sub="원본 접속 없음")

d.legend(H - 56, [("요청", MUTED), ("미스", WARN), ("적중", ACC)])
d.save("03-01.cdn-cache-sequence.svg")
