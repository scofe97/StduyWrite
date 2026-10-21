# 타입 스펙: type-sequence — 참여자 넷(Relay 백홀 · DatagramSession · udpFlowManager · 로컬 서비스), 동일 임대 재연결 시 LeaseDone 유지와 임대 교체 시 이전 LeaseDone 프레임 폐기 시퀀스.
# 사실 출처: docs/maintainer/architecture.md UDP resource ownership,
#   portal/transport/datagram_session.go:43,80,104,116,148,187,
#   sdk/proxy.go:443,489,521, sdk/listener.go:792,1194.
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 18}" width="{_w(label, 11)}" height="15" fill="{PAPER}"/>')
        s.t(mx, y - 7, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="14" fill="{PAPER}"/>')
            s.t(mx, y + 14, sub, 10, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-8} L {x+46} {y-8} L {x+46} {y+8} L {x+13} {y+8}", c, 1.4, m="ar")
        s.t(x + 54, y - 2, label, 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 54, y + 12, sub, 10, MUTED, _kr(sub), "start")

W, H = 960, 680
d = SeqKR(W, H, "PORTAL-TUNNEL · LEASE DONE BOUNDARY SEQUENCE",
          "LeaseDone 토큰 생명주기 — 재연결 보존과 교체 격리",
          "단순 재연결은 LeaseDone 토큰을 유지해 세션을 잇고, 임대 교체 시 토큰을 무효화해 지연 패킷의 혼입을 원천 차단합니다.",
          "임대 교체 경계를 기준으로 이전 패킷과 소켓을 즉시 정리합니다")

PARTICIPANTS = [
    ("Relay 백홀", "QUIC 송수신단"),
    ("DatagramSession", "터널 세션 관리자"),
    ("udpFlowManager", "로컬 소켓 격리"),
    ("로컬 서비스", "대상 UDP 앱")
]
d.LX = {"relay": 110, "session": 370, "flow": 630, "app": 850}
KEYS = ["relay", "session", "flow", "app"]

for k, (nm, sub) in zip(KEYS, PARTICIPANTS):
    x = d.LX[k]
    d.box(x - 84, 100, 168, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, KR)

d.lane_top = 144
d.rails(H - 64)

# ── 1구간: 임대 1 정상 수신 ──
d.msg("relay", "session", "QUIC DATAGRAM (Flow 1)", 180, INFO, "info")
d.selfmsg("session", "frame.LeaseDone = T1 주입", 212, INFO)
d.msg("session", "flow", "Accept() 프레임 인출", 244, INFO, "info")
d.msg("flow", "app", "DialUDP 소켓 전송 (키: Flow1+T1)", 276, OK, "ok")

# ── 2구간: 동일 임대 일시 단절 및 재연결 (T1 보존) ──
d.msg("relay", "session", "일시 단절 후 Bind(newConn)", 326, WARN, "warn", dash="4 3")
d.selfmsg("session", "동일 Lease: T1 토큰 보존", 358, OK)
d.msg("app", "flow", "UDP 응답 수신", 390, OK, "ok")
d.msg("flow", "session", "SendFrame(T1)", 422, OK, "ok", sub="T1 일치 → 전송 성공")

# ── 3구간: 임대 교체 (Lease 2 전환) ──
d.selfmsg("session", "Clear() 호출: close(T1) 및 T2 발급", 474, ACC)
d.selfmsg("flow", "watcher: close(T1) 감지 → 소켓 종료", 508, BAD)
d.msg("flow", "session", "지연된 T1 응답: SendFrame(T1)", 548, BAD, "bad", dash="4 3", sub="frame.LeaseDone != T2")
d.selfmsg("session", "datagram lease ended 에러 (폐기)", 580, BAD)

d.legend(H - 44, [
    ("정상 전달·보존", OK),
    ("임대 1 패킷 수신", INFO),
    ("일시 단절·재연결", WARN),
    ("토큰 교체", ACC),
    ("소켓 종료·패킷 폐기", BAD)
])

out_path = _HERE.parent / "01-07-leasedone.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
