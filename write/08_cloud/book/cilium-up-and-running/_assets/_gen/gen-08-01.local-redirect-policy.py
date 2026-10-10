# 타입 스펙: type-sequence — 클라이언트 Pod 에서 서비스 ClusterIP 로 보낸 요청을 eBPF LRP 가 같은 노드의 백엔드로 가로채 로컬에서 처리하는 시퀀스.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 403-406(netshoot-client 10.0.2.226 및 로컬 Pod 10.0.2.27, 원격 Pod 10.0.0.209), 줄 434-436(LRP 전 ID 6: 두 노드 백엔드 등록), 줄 482-484(LRP 후 ID 7: LocalRedirect 10.0.2.27:8080 한정), 줄 492-504(20회 요청 모두 로컬 Pod 응답)
import sys
sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=96, lane_w=190):
        s.LX = {}
        for (nm, sub), x in zip(names, xs):
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 19, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 36, sub, 11, MUTED, MONO)
        s.lane_top = y0 + 44

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 920, 560
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 08-01 §3", "LRP eBPF 로컬 리다이렉트 시퀀스",
          "클라이언트 요청이 서비스 IP 에서 동일 노드 백엔드로 변환되는 과정",
          "eBPF 가 서비스 요청을 가로채 동일 노드 Pod 로 DNAT 하여 원격 홉을 없앱니다")

A, B, C, E = "클라이언트 Pod", "노드 eBPF (LRP)", "로컬 백엔드 Pod", "원격 백엔드 Pod"
d.lanes([(A, "netshoot (10.0.2.226)"),
         (B, "kind-worker2 (KPR)"),
         (C, "pvkgf (10.0.2.27)"),
         (E, "phmpq (10.0.0.209)")],
        [125, 365, 605, 810], y0=96, lane_w=170)
d.rails(510)

# 시퀀스 단계
d.msg(A, B, "서비스 요청 (TCP 8080)", 164, MUTED, "ar", sub="목적 10.96.219.113:8080")
d.state(B, "LRP 정책 조회 (ID 7)", 206, ACC)
d.state(B, "로컬 DNAT (10.0.2.27:8080)", 248, OK)

# 원격 전송 우회 표시 (점선 x 표시)
d.path(f"M {365 + 10} 290 L {810 - 12} 290", WARN, 1.4, m="warn", dash="4 4")
d.t((365 + 810) / 2, 282, "원격 워커 전송 차단 (홉 제거)", 11, WARN, KR, "middle", 600)

d.msg(B, C, "로컬 패킷 전달", 336, OK, "ok", sub="목적 10.0.2.27:8080")
d.msg(C, B, "HTTP 응답 반환", 388, MUTED, "ar", dash="5 4", sub="Request served by pvkgf")
d.msg(B, A, "클라이언트 응답 수신", 474, OK, "ok", dash="5 4", sub="노드 내부 왕복 완결")

d.save("08-01.local-redirect-policy.svg")
