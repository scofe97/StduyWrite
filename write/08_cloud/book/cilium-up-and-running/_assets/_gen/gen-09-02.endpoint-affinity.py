# 타입 스펙: type-sequence — local affinity 설정 하에서 로컬 백엔드 정상 시 로컬 선택과 중단(replicas=0) 시 원격 백엔드 자동 폴백 시퀀스.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 883-887(affinity=local), 896-903(green-worker 3회 응답), 911-915(scale --replicas=0), 935-943(blue-worker2·red-worker2 폴백)
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

W, H = 920, 560
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 09-02 §2", "Endpoint Affinity 와 투명한 원격 전환",
          "affinity=local 설정 시 로컬 우선 응답과 로컬 중단 시 원격 클러스터 자동 폴백",
          "affinity=local 설정 시 로컬 우선 응답과 로컬 중단 시 원격 클러스터 자동 폴백")

A, B, C, D_EP = "test Pod", "eBPF 데이터패스", "green-worker", "blue / red-worker2"
d.lanes([
    (A, "kind-green netshoot"),
    (B, "affinity=local"),
    (C, "로컬 백엔드 (green)"),
    (D_EP, "원격 백엔드 (blue·red)")
], [110, 340, 580, 810])
d.rails(528)

# 1구간 구분 라벨
d.t(460, 168, "── 정상 상태: 로컬 백엔드 우선 선택 (replicas=1) ──", 12, OK, KR, "middle", 600)

d.msg(A, B, "curl nginx", 198, INK, "ar", sub="Service IP 목적지")
d.state(B, "affinity=local 확인", 232, OK)
d.msg(B, C, "요청 포워딩", 262, OK, "ar", sub="로컬 green-worker 선택")
d.msg(C, A, "응답", 298, OK, "ar", dash="5 4", sub="Hello from green-worker")

# 2구간 구분 라벨
d.t(460, 350, "── 장애 조치: 로컬 Pod 중단 (replicas=0 스케일다운) ──", 12, ACC, KR, "middle", 600)

d.state(C, "replicas=0 중단", 380, SOFT)
d.msg(A, B, "curl nginx", 412, INK, "ar", sub="Service IP 재호출")
d.state(B, "로컬 부재 → 원격 폴백", 446, ACC)
d.msg(B, D_EP, "크로스 클러스터 포워딩", 476, ACC, "ar", sub="원격 풀 무작위 선택")
d.msg(D_EP, A, "응답", 512, ACC, "ar", dash="5 4", sub="Hello from blue/red-worker2")

d.save("09-02.endpoint-affinity.svg")
