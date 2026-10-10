# 타입 스펙: type-sequence — 클라이언트·진입 노드·백엔드 노드 사이 기본 SNAT 왕복과 DSR 직접 응답의 시퀀스 비교.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 693-708(SNAT 지연·관측성 상실), 줄 782-807(클라이언트 172.18.0.5, 진입 노드 172.18.0.4:30080, SNAT IP 10.244.0.232), 줄 859-876(DSR 직접 응답과 출발지 IP 보존) / docs.cilium.io v1.20 kubeproxy-free(DSR 동작)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, xs, y0=96, lane_w=200):
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
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 7.4 + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12, c, _kr(txt))


W, H = 920, 600
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 08-02 §1", "기본 SNAT 과 DSR 의 응답 경로 비교",
          "진입 노드를 되돌아가는 SNAT 대 백엔드가 클라이언트로 곧장 쏘는 DSR",
          "DSR 은 역방향 경유 홉을 없애고 클라이언트 원본 IP 를 백엔드에 보존합니다")

A, B, C = "클라이언트", "진입 노드", "백엔드 노드"
d.lanes([(A, "172.18.0.5"), (B, "172.18.0.4:30080"), (C, "kind-worker 등")],
        [150, 460, 770], y0=96, lane_w=190)
d.rails(540)

# 기본 SNAT 구역
d.chip(90, 168, "기본 모드 (SNAT)", OK, 12)

d.msg(A, B, "요청 패킷", 196, MUTED, "ar", sub="출발 172.18.0.5 → 목적 172.18.0.4:30080")
d.state(B, "출발지 SNAT 변환 (10.244.0.232)", 236, INFO)
d.msg(B, C, "포워딩", 270, MUTED, "ar", sub="출발 10.244.0.232 → 목적 백엔드 Pod")

d.msg(C, B, "응답 패킷 (경유)", 316, MUTED, "ar", dash="5 4", sub="목적지 10.244.0.232 (진입 노드)")
d.state(B, "역방향 SNAT 복원", 356, INFO)
d.msg(B, A, "클라이언트 응답", 390, MUTED, "ar", dash="5 4", sub="출발 172.18.0.4:30080 → 목적 172.18.0.5")

# 구분선
d.line(30, 422, W - 30, 422, RULE, 0.8, "4 4")

# DSR 구역
d.chip(90, 444, "DSR 활성화", ACC, 12)

d.msg(A, B, "요청 패킷", 472, MUTED, "ar", sub="출발 172.18.0.5 → 목적 172.18.0.4:30080")
d.state(B, "DSR 디스패치 (IP 옵션 / Geneve)", 506, ACC)
d.msg(B, C, "포워딩 (원출발지 보존)", 536, MUTED, "ar", sub="출발 172.18.0.5 유지")

d.msg(C, A, "직접 응답 (DSR)", 572, ACC, "acc", dash="5 4", sub="진입 노드 경유 생략 · 출발 172.18.0.4:30080")

d.save("08-02.dsr-flow.svg")
