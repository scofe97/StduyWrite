# 타입 스펙: type-sequence — 클라이언트 → eBPF(L3/L4 판정) → L7 규칙 리다이렉트 → Envoy(메서드·경로 검사) → 허용 시 백엔드 프록시 및 거부 시 403 반환 시퀀스.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 90-106(test pod, curl), 115-123(toPorts http rules), 131-163(403 Forbidden, server: envoy), 190-212(Envoy datapath), 243-265(test IP 10.0.0.212, CiliumInternalIP 10.0.0.196) / docs.cilium.io v1.20 security/policy/layer7/ · helm 템플릿 v1.20.2 cilium-envoy/daemonset.yaml
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, INFO, OK, WARN, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    """한글 라벨과 서브 라벨을 명확히 렌더하는 Seq 확장."""
    def lanes(s, names, xs, y0=104, lane_w=190):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, MONO)
        s.lane_top = y0 + 44

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, _kr(txt))


W, H = 920, 720
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 13-01", "L7 정책이 HTTP 요청을 검사하고 전달하는 흐름",
          "eBPF 가 L7 규칙을 확인해 Envoy 로 넘기고, Envoy 가 정규식을 검사해 200 전달 또는 403 거부를 결정한다",
          "eBPF 가 L7 규칙을 확인해 Envoy 로 넘기고, Envoy 가 정규식을 검사해 200 전달 또는 403 거부를 결정한다")

A = "클라이언트 Pod"
B = "eBPF 데이터패스"
C = "노드 Envoy"
E = "백엔드 Pod"

d.lanes([(A, "10.0.0.212 · test"), (B, "노드 커널 · 정책 맵"), (C, "10.0.0.196 · cilium-envoy"), (E, "webserver:8080")],
        [115, 345, 575, 805], y0=104, lane_w=190)
d.rails(690)

d.msg(A, B, "TCP 연결 시도", 176, INK, "ar", sub="dst webserver:8080")
d.state(B, "L3/L4 통과 · L7 리다이렉트", 222, ACC)
d.msg(B, C, "L7 포트만 리다이렉트", 268, ACC, "ar", sub="그 외 포트는 eBPF 가 처리")
d.msg(A, C, "GET /api 요청", 322, OK, "ar", sub="HTTP/1.1 · method GET")
d.state(C, "정규식 일치 (200 OK 판정)", 366, OK)
d.msg(C, E, "백엔드 프록시 요청", 414, OK, "ar", sub="src 10.0.0.196 (CiliumInternalIP)")
d.msg(E, C, "200 응답 반환", 478, MUTED, "ar", dash="5 4", sub='본문 "API"')
d.msg(C, A, "200 응답 전달", 540, OK, "ar", dash="5 4", sub='본문 "API"')
d.msg(A, C, "GET /admin 요청", 604, WARN, "ar", sub="미허용 경로 호출")
d.state(C, "정규식 불일치 (403 거부)", 636, BAD)
d.msg(C, A, "403 Forbidden 응답", 672, BAD, "ar", dash="5 4", sub='본문 "Access denied" · server envoy')

d.save("13-01.chapter-overview.svg")
