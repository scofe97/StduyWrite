# 타입 스펙: type-sequence — BGP Graceful Restart 활성화 시 계획된 업그레이드(경로 유지·세션 복구)와 비자발적 장애(블랙홀·페일오버 지연) 두 갈래 시퀀스.
# 값 근거: 본문 §5 및 ch16.txt 줄 733-757(BGP 스피커 에이전트 내장, 업그레이드 중 데이터패스 유지·세션 단절, Graceful Restart 경로 유지, 비자발적 장애 시 타이머 만료까지 트래픽 전송으로 페일오버 지연) / docs.cilium.io v1.20 bgp-control-plane-configuration(CiliumBGPPeerConfig, gracefulRestart.enabled, restartTimeSeconds 120s) · bgp-control-plane-operation(hold time + restart time, PodCIDR drain, Service ECMP 재해시)
import sys

sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, RULE, KR, MONO


class KrSeq(Seq):
    """한글 라벨은 KR 스택과 13px 이상으로, 영문·식별자는 MONO 로 그린다."""

    def _fam(s, txt):
        return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

    def lanes(s, names, y0=104, lane_w=232):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 36 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, "#161B22", RULE, 1.0)
            s.t(x, y0 + 20, nm, 14, INK, s._fam(nm), "middle", 600)
            s.t(x, y0 + 39, sub, 12, MUTED, s._fam(sub), "middle")
        s.lane_top = y0 + 48
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        fam = s._fam(label)
        sz = 13 if fam == KR else 12
        s.t(mx, y - 9, label, sz, c, fam, "middle", 600)
        if sub:
            sfam = s._fam(sub)
            s.t(mx, y + 17, sub, 13 if sfam == KR else 11, MUTED, sfam, "middle")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        fam = s._fam(txt)
        sz = 13 if fam == KR else 11
        char_w = 12.5 if fam == KR else 7.2
        w = max(124, len(txt) * char_w + 20)
        s.o.append(
            f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>'
        )
        s.t(x, y + 5, txt, sz, c, fam, "middle", 600)


W, H = 960, 608
d = KrSeq(
    W,
    H,
    "CILIUM UP AND RUNNING · 16-02 §5",
    "Graceful Restart 와 업그레이드 · 장애의 갈래",
    "Graceful Restart 를 켜면 계획된 업그레이드 중 피어가 경로를 붙잡아 eBPF 데이터패스로 연결을 잇지만, 비자발적 장애에서는 타이머 만료까지 죽은 노드로 트래픽이 가 페일오버가 늦어집니다.",
    lead="CiliumBGPPeerConfig gracefulRestart.enabled=true · restartTimeSeconds 120s 기준",
)

d.lanes(
    [
        ("상류 BGP 피어", "BGP Router"),
        ("Cilium 에이전트", "내장 BGP 스피커"),
        ("커널 데이터패스", "eBPF Datapath"),
    ],
    y0=100,
    lane_w=236,
)
d.rails(540)

# Combined fragment frame (ALT) spanning all 3 lifelines
FX, FY, FW, FH = 44, 168, 872, 360
d.o.append(
    f'<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="4" fill="rgba(245,245,243,0.04)" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>'
)
d.o.append(
    f'<rect x="{FX}" y="{FY}" width="44" height="18" rx="2" fill="{PAPER}" stroke="rgba(245,245,243,0.22)" stroke-width="1"/>'
)
d.t(FX + 22, FY + 13, "ALT", 9, MUTED, MONO, "middle", 600)

# Region 1: Planned upgrade (guard positioned clear of lifeline x=154)
d.t(168, FY + 16, "[계획된 업그레이드 · preflight 준비]", 13, OK, KR, "start", 600)
d.state("Cilium 에이전트", "에이전트 재시작", 216, INFO)
d.msg("Cilium 에이전트", "상류 BGP 피어", "BGP 세션 끊김 (재시작)", 256, INFO, "info", "4 3", "피어가 경로 즉시 철회 보류")
d.msg("상류 BGP 피어", "커널 데이터패스", "기존·신규 트래픽 계속 전달", 304, ACC, "acc", None, "eBPF 살아 있어 연결 유지")
d.msg("Cilium 에이전트", "상류 BGP 피어", "120초 내 복귀 · 세션 재개", 344, OK, "ok", "4 3")

# Divider between ALT regions
DIV_Y = 368
d.line(FX + 8, DIV_Y, FX + FW - 8, DIV_Y, "rgba(245,245,243,0.20)", 1.0, "4 3")

# Region 2: Involuntary outage (guard positioned clear of lifeline x=154)
d.t(168, DIV_Y + 22, "[비자발적 장애 · 링크 단절·정전]", 13, BAD, KR, "start", 600)
d.state("Cilium 에이전트", "노드·링크 중단", 420, BAD)
_x1, _x3 = d.LX["상류 BGP 피어"], d.LX["커널 데이터패스"]
_xe = (_x1 + _x3) / 2 + 40
d.path(f"M {_x1 + 10} 464 L {_xe} 464", WARN, 1.5, m="warn")
d.t((_x1 + _xe) / 2, 455, "hold time + 120s 동안 계속 송신", 13, WARN, KR, "middle", 600)
d.t((_x1 + _xe) / 2, 481, "죽은 노드로 전송 · 페일오버 지연", 13, MUTED, KR, "middle")
d.t(_xe + 8, 469, "✕ 유실", 13, WARN, KR, "start", 600)
d.state("상류 BGP 피어", "만료 뒤 경로 철회", 506, WARN)

d.legend(
    H - 44,
    [
        ("세션 중단 · 복귀", INFO),
        ("트래픽 유지 (이득)", ACC),
        ("세션 재개", OK),
        ("페일오버 지연 (대가)", WARN),
        ("노드 정지", BAD),
    ],
)
d.save("16-02.bgp-graceful-restart.svg")
print("ok 16-02 bgp gr")
