# 타입 스펙: type-sequence — 백엔드가 하나뿐인 서비스에서 클라이언트 노드의 에이전트가 재시작되는 동안 백엔드 Pod 가 바뀌면 서비스 맵이 낡아 요청이 여러 번 실패하고 에이전트가 돌아오면 맵이 맞춰지는 순서
# 사실 출처: 추출본 cil16.txt 줄 226-254(Traffic Stability During Upgrade) / docs.cilium.io v1.20 operations/upgrade(Upgrade Impact·Version Specific Notes)
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12 if _kr(sub) == KR else 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12 if _kr(label) == KR else 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 12 if _kr(sub) == KR else 11, MUTED, _kr(sub))
    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = sum(12.5 if "가" <= ch <= "힣" else 7.0 for ch in txt) + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 12 if _kr(txt) == KR else 11, c, _kr(txt))

W, H = 920, 724
d = SeqKR(W, H, "CILIUM UP AND RUNNING · 16-01 §3", "에이전트 교체 중 서비스 맵이 낡는 순서",
          "기존 연결은 이어지고 에이전트가 돌아올 때까지 바뀐 백엔드로 가는 요청만 실패합니다",
          "백엔드가 하나뿐인 서비스에서 클라이언트 노드의 에이전트가 재시작되는 동안")
L = d.lanes([("client Pod", "클라이언트 노드"), ("서비스 맵", "eBPF"),
             ("cilium 에이전트", "DaemonSet"), ("backend Pod", "서비스 하나뿐")], y0=100, lane_w=180)
d.rails(656)

d.state("cilium 에이전트", "재시작 중", 196, WARN)
d.msg("client Pod", "서비스 맵", "서비스 IP 로 요청", 252, OK, "ok", sub="backend-1 로 전달")
d.state("backend Pod", "backend-1 → backend-2", 312, INFO)
d.state("서비스 맵", "backend-1 남음", 312, WARN)

# focal: 낡은 항목으로 간 요청 여러 번
d.tone(24, 346, W - 72, 72, ACC, r=6, op="0A", sw=1.2)
d.msg("client Pod", "서비스 맵", "서비스 IP 로 요청", 380, BAD, "bad", sub="backend-1 · 도달 불가")
d.state("client Pod", "재시도 · 백오프", 452, INFO)

d.state("cilium 에이전트", "기동 완료", 508, OK)
d.msg("cilium 에이전트", "서비스 맵", "맵 갱신", 564, OK, "ok", sub="backend-2")
d.msg("client Pod", "서비스 맵", "서비스 IP 로 요청", 624, OK, "ok", sub="backend-2 로 전달")

d.legend(668, [("정상 전달", OK), ("에이전트 없음", WARN), ("낡은 항목 요청", BAD), ("Pod 교체·재시도", INFO), ("초점 구간", ACC)])
d.save("16-01.agent-upgrade-sequence.svg")
