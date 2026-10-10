# 타입 스펙: type-sequence — test Pod 의 cilium.io. A 질의가 데이터패스·DNS 프록시·CoreDNS 를 거쳐 응답 IP 를 FQDN identity 로 등록하고, 이어진 TCP 443 연결이 허용되는 순서. 레인은 구성 요소, 메시지는 질의·응답·등록 한 번.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 683-747(FQDN Identity 여덟 단계: UDP 질의·CoreDNS 서비스 IP 변환·rules.dns 로 에이전트에 넘김·응답 IP 를 FQDN 캐시와 IP 캐시에 등록한 뒤 응답·TCP 연결 허용), 줄 573(nameserver 10.96.0.10), 줄 597-640(toFQDNs matchName cilium.io · 80/443) / docs.cilium.io v1.20 security/policy/layer7·layer3
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


def _w(txt, kr=12, la=7.4):
    return sum(kr if "가" <= c <= "힣" else la for c in str(txt))


class SeqKR(Seq):
    """한글 라벨을 한글 스택으로, 글자는 12px 로 내보내는 Seq."""
    def lanes(s, names, xs, y0=104, lane_w=196):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = _w(txt) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 920, 708
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 13-02 OVERVIEW", "FQDN 정책이 응답 IP 를 연결 허용으로 바꾸는 순서",
          "질의가 DNS 프록시를 거치며 응답 IP 가 FQDN identity 로 등록되고, 이어진 연결이 그 identity 로 허용됩니다",
          "질의가 DNS 프록시를 거치며 응답 IP 가 FQDN identity 로 등록되고, 이어진 연결이 그 identity 로 허용됩니다")
P, DP, PX, CD = "test Pod", "eBPF 데이터패스", "DNS 프록시", "CoreDNS"
d.lanes([(P, "app.kubernetes.io/name=test"), (DP, "ipcache · 정책 맵"), (PX, "cilium-agent 안"), (CD, "서비스 10.96.0.10")],
        [120, 340, 560, 780])
d.rails(676)

d.msg(P, DP, "A cilium.io.", 196, MUTED, "ar", sub="UDP 53")
d.msg(DP, PX, "리다이렉트", 252, MUTED, "ar", sub="rules.dns 규칙")
d.msg(PX, CD, "질의 중계", 308, MUTED, "ar")
d.msg(CD, PX, "응답 IP", 364, MUTED, "ar", dash="5 4")
d.msg(PX, DP, "ipcache 등록", 420, ACC, "acc", sub="IP → cilium.io identity")
d.msg(PX, DP, "응답 반환", 476, MUTED, "ar", dash="5 4")
d.msg(DP, P, "응답 전달", 532, MUTED, "ar", dash="5 4")
d.msg(P, DP, "TCP 443", 588, MUTED, "ar", sub="목적지 IP 조회")
d.state(DP, "toFQDNs cilium.io 허용", 640, OK)
d.save("13-02.chapter-overview.svg")
