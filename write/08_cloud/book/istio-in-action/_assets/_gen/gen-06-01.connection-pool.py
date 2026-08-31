# 06-01 §7 요청이 커넥션 풀 한계를 만나는 순서.
# 본문: "커넥션 오버플로 자체로는 오류가 올라오지 않는다 — 커넥션이 넘치면 기존 커넥션에 압력이 더해지고,
# 그 결과로 대기 큐가 자라며, 결국 서킷 브레이커가 발동한다. 빠른 실패는 대기 요청이나 병렬 요청이 임계를 넘을 때 나온다."
# 원문은 두 임계를 "pending or parallel"로 나란히 놓는다. 순서를 매기지 않으므로 도식도 한 판단 안에 병렬로 둔다.
# 타입 스펙: type-flowchart — 판단 논리. 타원(시작·끝) · 마름모(판단, ≤3 출구) · 사각형(행동). 예는 오른쪽, 아니오는 아래.
#           초점은 빠른 실패 하나. 교차하는 화살표가 없도록 판단을 세로로 세운다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 620
d = D(W, H, "ISTIO IN ACTION · 06-01 §7",
      "요청이 커넥션 풀 한계를 만나는 순서",
      "커넥션이 maxConnections 를 넘으면 통계에만 기록되고 오류는 나지 않는다. 그 압력이 대기 큐를 키우고, "
      "대기 요청이나 병렬 요청이 임계를 넘을 때 비로소 빠른 실패가 난다.",
      "실패 수와 맞는 통계는 upstream_cx_overflow 가 아니라 upstream_rq_pending_overflow 입니다")

CX = 300
def oval(y, txt, w=260):
    d.o.append(f'<rect x="{CX - w/2}" y="{y}" width="{w}" height="40" rx="20" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(CX, y + 25, txt, 12, INK, KR, "middle", 600)
def diamond(cy, l1, l2, hw=190, hh=58):
    d.o.append(f'<polygon points="{CX},{cy - hh} {CX + hw},{cy} {CX},{cy + hh} {CX - hw},{cy}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(CX, l2 and cy - 6 or cy + 4, l1, 12, INK, MONO, "middle", 600)
    if l2: d.t(CX, cy + 14, l2, 12, INK, KR)
def side(y, txt, subs, c, focal=False, w=320, h=56):
    x = 620
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(x + w / 2, y + 24, txt, 12, ACC if focal else c, KR, "middle", 600)
    for i, sub in enumerate(subs):
        d.t(x + w / 2, y + 44 + i * 16, sub, 11, ACC if focal else MUTED, MONO)

oval(104, "simple-web 에서 나가는 요청")
d.path(f"M {CX} 144 L {CX} 178", MUTED, 1.4, m="ar")
diamond(240, "maxConnections", "를 넘는가")
d.path(f"M {CX + 190} 240 L 618 240", WARN, 1.4, m="warn")
d.t(460, 230, "넘는다", 11, WARN, KR)
side(208, "통계에만 기록 — 오류 아님", ["upstream_cx_overflow"], WARN)
d.t(780, 296, "기존 커넥션에 압력이 더해진다", 11, WARN, KR)
d.path("M 780 304 L 780 330 L 500 330", WARN, 1.2, m="warn", dash="4 3")

d.path(f"M {CX} 298 L {CX} 348", MUTED, 1.4, m="ar")
d.t(CX + 12, 332, "안 넘는다", 11, MUTED, KR, "start")
diamond(420, "대기 요청 또는 병렬 요청이", "임계를 넘는가", hh=64)
d.t(CX, 452, "http1MaxPendingRequests · http2MaxRequests", 11, SOFT, MONO)
d.path(f"M {CX + 190} 420 L 618 420", ACC, 1.6, m="acc")
d.t(460, 410, "넘는다", 11, ACC, KR)
side(376, "빠른 실패 — HTTP 500", ["x-envoy-overloaded 헤더", "upstream_rq_pending_overflow"], ACC, focal=True, h=76)
d.path(f"M {CX - 190} 420 L 120 420 L 120 316", OK, 1.4, m="ok")
d.t(112, 336, "안 넘는다 → 상위로 전송", 11, OK, KR, "start")

d.legend(520, [("오류를 내지 않는 오버플로", WARN), ("빠른 실패 — 이 절의 논점", ACC), ("통과", OK)])
d.save("06-01.connection-pool.svg")
