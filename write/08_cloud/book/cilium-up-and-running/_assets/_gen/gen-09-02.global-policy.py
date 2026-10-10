# 타입 스펙: type-sequence — red 클러스터 클라이언트의 frontend 라벨 보유 여부에 따른 Egress 및 blue 클러스터 Ingress(io.cilium.k8s.policy.cluster) 판정 시퀀스.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 1063-1080(nginx-policy), 1097-1130(frontend-policy), 1144-1156(curl 200 성공), 1164-1169(curl 타임아웃)
import sys
sys.path.insert(0, ".")
from dd import Seq, ACC, OK, INFO, SOFT, MUTED, INK, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
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
        w = len(txt) * 7.5 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, _kr(txt))

W, H = 920, 650
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 09-02 §3", "전역 네트워크 정책의 클러스터 라벨 판정",
          "io.cilium.k8s.policy.cluster 라벨 기반 Egress 허용과 Ingress 상호 검증 흐름",
          "io.cilium.k8s.policy.cluster 라벨 기반 Egress 허용과 Ingress 상호 검증 흐름")

A, B, C, D_SVC = "red 클라이언트", "red Cilium 에이전트", "blue Cilium 에이전트", "blue nginx Pod"
d.lanes([
    (A, "kind-red Pod"),
    (B, "Egress Policy"),
    (C, "Ingress Policy"),
    (D_SVC, "kind-blue 백엔드")
], [110, 340, 580, 810])
d.rails(618)

# 1구간: 라벨 보유 정상 흐름
d.t(460, 168, "── 정상 인가: app=frontend 라벨 보유 (Egress & Ingress 일치) ──", 12, OK, KR, "middle", 600)

d.msg(A, B, "curl nginx", 198, INK, "ar", sub="DNS 조회 통과 후 TCP 연결")
d.state(B, "Egress: cluster In [green,blue]", 232, OK)
d.msg(B, C, "패킷 전송 (신원: frontend, cluster: red)", 262, OK, "ar", sub="출발지 신원(frontend, cluster=red)")
d.state(C, "Ingress: cluster==red 확인", 294, OK)
d.msg(C, D_SVC, "요청 전달", 324, OK, "ar")
d.msg(D_SVC, A, "응답", 354, OK, "ar", dash="5 4", sub="Hello from blue-worker2")

# 2구간: 미인가 흐름
d.t(460, 404, "── 미인가 차단: app=frontend 라벨 없음 (Ingress 불일치) ──", 12, SOFT, KR, "middle", 600)

d.msg(A, B, "curl nginx -m2", 434, INK, "ar", sub="라벨 미부여 테스트 Pod")
d.state(B, "Egress 정책 대상 아님 → 통과", 474, MUTED)
d.msg(B, C, "패킷 전송 (frontend 라벨 없음)", 512, MUTED, "ar")
d.state(C, "Ingress 불일치 → 드롭", 544, SOFT)
d.msg(C, A, "연결 타임아웃 (2002ms)", 584, SOFT, "ar", dash="5 4", sub="curl: (28) Connection timed out")

d.save("09-02.global-policy.svg")
