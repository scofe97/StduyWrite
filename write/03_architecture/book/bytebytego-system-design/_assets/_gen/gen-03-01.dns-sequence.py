# 타입 스펙: type-sequence — 재귀 리졸버가 example.com A 를 풀려고 루트·.com TLD·권한 서버에 반복 질의하고 위임 두 번과 최종 답을 받는 왕복(레인 5, 메시지 8).
# 사실 출처: 직접 측정 dig 9.10.6, 2026-10-12T16:28Z — `dig +norecurse @a.root-servers.net|@a.gtld-servers.net|@hera.ns.cloudflare.com example.com A`.
#   루트 응답 AUTHORITY com. NS 13개·TTL 172800·ADDITIONAL a.gtld-servers.net A 192.5.6.30, .com 응답 example.com. NS hera/elliott.ns.cloudflare.com·glue 108.162.192.162, 권한 응답 flags qr aa·A 104.20.23.154·172.66.147.243·TTL 300.
#   a.root-servers.net=198.41.0.4 (dig a.root-servers.net A +short). 용어 RFC 9499 §6 (recursive/iterative/referral).
# Layout conventions: 레인 5·폭 128·간격 200, 호출 한 건의 stride 72(라벨 y-9, 부라벨 y+17·y+33), 첫 메시지 y=204. 모든 좌표 4의 배수.
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
            s.t(x, y0 + 20, nm, 14, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sub2=None, sw=1.5, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))
        if sub2:
            s.t(mx, y + 33, sub2, 12, MUTED, _kr(sub2))


W, H = 1000, 856
d = SeqKR(W, H, "BYTEBYTEGO · 03-01 §2",
          "루트와 TLD 는 위임만 하고 권한 서버가 답을 가진다",
          "재귀 리졸버가 example.com A 를 묻는 질의 세 번과 응답 세 개, 측정 2026-10-12T16:28Z · dig 9.10.6",
          "위임 응답은 ANSWER 가 비고 aa 플래그가 없으며 최종 답에만 aa 가 붙습니다")
BR, RS, RT, TL, AU = "브라우저", "재귀 리졸버", "루트", ".com TLD", "권한 서버"
d.lanes([(BR, "스텁"), (RS, "캐시 보유"), (RT, "198.41.0.4"), (TL, "192.5.6.30"), (AU, "108.162.192.162")], 100, 128)
d.rails(H - 80)

Y0, S = 204, 72
q = "example.com A ?"
d.msg(BR, RS, q, Y0 + 0 * S, MUTED, "ar", sub="재귀 요청")
d.msg(RS, RT, q, Y0 + 1 * S, MUTED, "ar", sub="재귀 요구 없음 · RD 0")
d.msg(RT, RS, "NS a.gtld-servers.net", Y0 + 2 * S, ACC, "acc", dash="5 4", sub="glue 192.5.6.30", sub2="TTL 172800 · aa 없음")
d.msg(RS, TL, q, Y0 + 3 * S, MUTED, "ar", sub="a.gtld-servers.net", dx=100)
d.msg(TL, RS, "NS hera.ns.cloudflare.com", Y0 + 4 * S, WARN, "warn", dash="5 4", sub="glue 108.162.192.162", sub2="TTL 172800 · aa 없음", dx=100)
d.msg(RS, AU, q, Y0 + 5 * S, MUTED, "ar", sub="hera.ns.cloudflare.com")
d.msg(AU, RS, "A 104.20.23.154", Y0 + 6 * S, OK, "ok", dash="5 4", sub="A 172.66.147.243", sub2="TTL 300 · aa")
d.msg(RS, BR, "A 104.20.23.154", Y0 + 7 * S, OK, "ok", dash="5 4", sub="A 172.66.147.243", sub2="TTL 300 동안 캐시")

d.legend(H - 56, [("질의", MUTED), ("루트의 위임", ACC), (".com 의 위임", WARN), ("최종 답", OK)])
d.save("03-01.dns-sequence.svg")
