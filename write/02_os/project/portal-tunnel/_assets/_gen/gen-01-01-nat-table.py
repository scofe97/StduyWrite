# 타입 스펙: type-sequence
# 사실 출처: RFC 3022(Traditional NAT/NAPT), RFC 4787(NAT Behavioral Requirements), netfilter conntrack 커널 동작
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqNAT(Seq):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, lead)
        s.o.insert(19, f'<marker id="ok_left" viewBox="0 0 8 8" refX="1" refY="4" markerWidth="6.5" markerHeight="6.5" orient="auto"><path d="M8 0 L0 4 L8 8 z" fill="{OK}"/></marker>')

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 11)/2}" y="{y - 20}" width="{_w(label, 11)}" height="16" fill="{PAPER}"/>')
        s.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 10)/2}" y="{y + 4}" width="{_w(sub, 10)}" height="15" fill="{PAPER}"/>')
            s.t(mx, y + 15, sub, 10, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-8} L {x+46} {y-8} L {x+46} {y+8} L {x+13} {y+8}", c, 1.4, m="ar")
        s.t(x + 54, y - 2, label, 11, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 54, y + 12, sub, 10, MUTED, _kr(sub), "start")

W, H = 960, 640
d = SeqNAT(
    W, H,
    "NETFILTER · NAT & CONNTRACK STATE SEQUENCE",
    "아웃바운드 SYN 표 등록과 외부 인바운드 차단 흐름",
    "내부에서 나간 SYN 패킷은 NAT 표에 변환 쌍을 생성하여 돌아오는 응답을 맞이하지만, 외부에서 시작된 임의 SYN 패킷은 표에 없어 버려집니다.",
    "NAT 상태 표 한 줄의 생성과 역방향 조회 및 미등록 인바운드 폐기 과정"
)

NAMES = (
    ("노트북 (사설망)", "192.168.0.10:51000"),
    ("공유기 (NAT/conntrack)", "공인 203.0.113.7"),
    ("원격 서버 (공인망)", "93.184.216.34:443")
)
d.LX = {"laptop": 150, "router": 500, "server": 850}
KEYS = ["laptop", "router", "server"]

for k, (nm, sub) in zip(KEYS, NAMES):
    x = d.LX[k]
    d.box(x - 90, 100, 180, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 136, sub, 10, MUTED, MONO)

d.lane_top = 144
d.rails(H - 70)

# 단계 1: 내부 발신 SYN (아웃바운드)
d.msg("laptop", "router", "TCP SYN", 184, INFO, "info", sub="192.168.0.10:51000 → 93.184.216.34:443")

# NAT 표 1단계: 엔트리 생성
d.box(370, 212, 260, 36, fill=PAPER2, stroke=INFO, sw=1.1, r=4)
d.t(500, 226, "NAT 엔트리 생성 (SYN_SENT)", 10, INFO, KR, "middle", 600)
d.t(500, 240, "192.168.0.10:51000 ↔ 203.0.113.7:40001", 9, MUTED, MONO, "middle")

# 공유기 -> 원격 서버: 변환된 SYN
d.msg("router", "server", "TCP SYN (SNAT)", 274, INFO, "info", sub="203.0.113.7:40001 → 93.184.216.34:443")

# 단계 2: 원격 응답 SYN-ACK 인입
d.msg("server", "router", "TCP SYN-ACK", 330, OK, "ok", sub="93.184.216.34:443 → 203.0.113.7:40001")

# NAT 표 2단계: 역방향 조회 일치 및 상태 전이
d.box(370, 358, 260, 36, fill=PAPER2, stroke=OK, sw=1.1, r=4)
d.t(500, 372, "NAT 역방향 일치 (SYN_RECV)", 10, OK, KR, "middle", 600)
d.t(500, 386, "목적지 복원 → 192.168.0.10:51000", 9, MUTED, KR, "middle")

# 공유기 -> 노트북: 복원된 SYN-ACK
d.msg("router", "laptop", "TCP SYN-ACK (de-SNAT)", 420, OK, "ok", sub="93.184.216.34:443 → 192.168.0.10:51000")

# 단계 3: 외부 임의 인바운드 SYN (표 없음)
d.msg("server", "router", "임의 TCP SYN 인입", 486, BAD, "bad", dash="4 3", sub="원격:55555 → 공유기:8080 (비요청)")

# 공유기 매칭 실패 및 폐기
d.box(370, 514, 260, 36, fill=PAPER2, stroke=BAD, sw=1.1, r=4)
d.t(500, 528, "NAT 표 조회 실패 (엔트리 부재)", 10, BAD, KR, "middle", 600)
d.t(500, 542, "패킷 즉시 폐기 (DROP / RST)", 9, BAD, KR, "middle")

# 범례
d.legend(592, [
    ("아웃바운드 발신 (SNAT)", INFO),
    ("대응 응답 복원 (de-SNAT)", OK),
    ("미등록 인바운드 차단", BAD)
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-01-nat-table.svg"))
d.save(out)
print(f"saved: {out}")
