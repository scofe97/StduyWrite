# 03-04.three-addresses — 세 주소가 각각 어디까지 가서 어떻게 끝나는가
# 본문 요구: §5 의 요점은 결과가 아니라 "어디까지 갔느냐"다. 거부는 목적지까지 갔다는 증거이고
#           타임아웃은 도중에 사라졌다는 뜻이라, 두 실패의 종착지가 서로 달라야 한다.
#           그래서 결과 표가 아니라 여정을 그린다.
# 타입 스펙: type-sequence.md — 세로가 시간, 가로가 주체. 응답이 돌아오는 화살표가 있는 것과
#           없는 것이 갈리는 게 논지라, 마지막 왕복만 응답 화살표가 없다.
# 좌표: Layout conventions 타입이라 공식이 없다. 메시지 stride 56 하나로 고정.
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """계약 §프리미티브가 한글을 mono 로 내보내는 자리 — lanes·msg·state 의 한글만 한글 스택으로."""
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = sum(11 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, _kr(txt))

W, H = 1000, 572
Y0, STRIDE, RAIL_BOT = 180, 56, 480           # 첫 메시지 라벨이 레인 머리 바닥(148)에 닿지 않게 12px 내림

d = SeqKR(W, H, "THREE ADDRESSES · HOW FAR DID IT GET",
        "다른 호스트에서 세 주소 — 둘은 답을 받고 하나는 사라진다",
        "ubuntu2 에서 같은 컨테이너를 세 가지 주소로 부른 여정. 앞의 둘은 목적지 호스트까지 도달해 "
        "각각 응답과 거부를 받고, 컨테이너 IP 로 간 것만 게이트웨이 너머에서 응답 없이 사라진다.",
        lead="거부는 도달했다는 증거입니다 · 응답 화살표가 없는 마지막 한 줄만 성격이 다릅니다")

LANES = d.lanes([("ubuntu2", "192.168.139.238"),
                 ("게이트웨이", "192.168.139.1"),
                 ("ubuntu1 · go-web", "192.168.139.208 · 172.17.0.4")])
A, G, B = "ubuntu2", "게이트웨이", "ubuntu1 · go-web"
d.rails(RAIL_BOT)

y = Y0
d.msg(A, B, "192.168.139.208:80", y, OK, sub="같은 랜 · 게이트웨이 경유 없음")
y += STRIDE
d.msg(B, A, "200 OK", y, OK, dash="4 4", sub="DNAT 으로 컨테이너 8080 에 전달")

y += STRIDE + 12
d.msg(A, B, "192.168.139.208:8080", y, WARN, sub="호스트 포트 8080 점유자 없음")
y += STRIDE
d.msg(B, A, "TCP RST", y, WARN, dash="4 4", sub="exit 7 · 거절도 응답")

y += STRIDE + 12
d.msg(A, G, "172.17.0.4:80", y, BAD, sub="경로 없음 · 기본 경로로 전달")
y += STRIDE
d.state(G, "172.17.0.0/16 모름 · 폐기", y, BAD)

# 응답 화살표 유무의 뜻과 손댈 곳(목적지 포트 vs 출발지 경로)은 본문 §5 가 맡는다
# 마지막 상태 칩(≈482)과 범례 구분선 사이 여유를 둔다
d.legend(RAIL_BOT + 36, [("성공", OK), ("거부 — 도달했다는 증거", WARN), ("타임아웃 — 도중에 사라짐", BAD)])
d.save("03-04.three-addresses.svg")
print("ok three-addresses")
