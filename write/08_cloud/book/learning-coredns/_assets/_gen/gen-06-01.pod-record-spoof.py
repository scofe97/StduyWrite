# 06-01 §8 — 파드 A 레코드는 이름에 적힌 IP 를 확인 없이 돌려주므로, 다른 네임스페이스의 파드를 이 네임스페이스 것처럼 보이게 한다.
# 본문 근거: 이 노트 §8(그 IP 의 파드가 지정된 네임스페이스에 있는지 확인하지 않는다 · 네임스페이스 밖의 파드를 안의 것처럼).
# 소스 근거: CoreDNS kubernetes README — insecure "Always return an A record with IP from request (without checking k8s)",
#            verified "Return an A record if there exists a pod in same namespace with matching IP".
# 값: 네임스페이스 이름 prod·dev 와 주소 10.5.88.7 은 설명용(주소는 이 노트 allow 목록의 원서 예제 주소).
# 타입 스펙: type-sequence — 질의·응답·접속의 시간순 왕복에서 확인 단계가 빠진 자리가 논지다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, OK, INK, PAPER, PAPER2, RULE, KR, MONO


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
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 38, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))


def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(12.0 if "가" <= ch <= "힣" else 7.2 for ch in txt) + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{PAPER}" stroke="none"/>')
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 5, txt, 12, c, KR)


W, H = 880, 560
d = SeqKR(W, H, "LEARNING COREDNS · 06-01 §8",
          "이름에 적힌 IP 를 확인 없이 돌려준다",
          "prod 네임스페이스의 클라이언트가 10-5-88-7.prod.pod 를 묻는다. 확인하지 않는 모드는 이름에서 IP 를 꺼내 그대로 답하고, "
          "클라이언트는 실제로 dev 에 있는 파드를 prod 의 파드로 믿고 접속한다.",
          "주황 칸이 빠진 확인 단계입니다")

d.lanes([("prod 의 클라이언트", "와일드카드 인증서를 믿음"),
         ("CoreDNS", "pods insecure"),
         ("10.5.88.7 의 파드", "실제로는 dev 네임스페이스")], y0=104, lane_w=240)
d.rails(440)

d.msg("prod 의 클라이언트", "CoreDNS", "A 질의", 200, MUTED, sub="10-5-88-7.prod.pod.cluster.local")
cx = d.LX["CoreDNS"]
d.box(cx - 120, 236, 240, 44, PAPER, "none", 0, 6)   # 레인 점선이 글자를 가르지 않게 불투명 바탕
d.tone(cx - 120, 236, 240, 44, ACC, 6, "12", 1.4)
d.t(cx, 256, "그 IP 의 파드가 prod 에 있나", 12, ACC, KR, "middle", 600)
d.t(cx, 273, "확인하지 않음", 12, ACC, KR)
d.msg("CoreDNS", "prod 의 클라이언트", "A 10.5.88.7", 320, BAD, mk="bad", sub="이름에서 꺼낸 주소 그대로")
d.msg("prod 의 클라이언트", "10.5.88.7 의 파드", "prod 의 파드라고 믿고 접속", 392, BAD, mk="bad")
chip("10.5.88.7 의 파드", "네임스페이스 밖의 파드", 424, BAD)

d.t(20, 478, "verified · 같은 네임스페이스에 그 IP 의 파드가 있을 때만 답한다", 13, MUTED, KR, "start")
d.legend(496, [("빠진 확인 단계", ACC), ("잘못 믿고 쓰는 경로", BAD)])
d.save("06-01.pod-record-spoof.svg")
