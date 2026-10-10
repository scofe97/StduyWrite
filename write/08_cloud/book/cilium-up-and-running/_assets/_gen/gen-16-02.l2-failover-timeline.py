# 타입 스펙: type-timeline — 리더 노드 정지부터 리스 만료, 새 리더, gARP, 클라이언트 캐시 갱신까지의 L2 페일오버 타임라인과 기본값·조정값 두 구간.
# 사실 출처: Cilium Up and Running 16장 cil16.txt 줄 634-654(리스 이름·leaseDuration 15s·leaseRetryPeriod 2s·leaseRenewDeadline 5s), 665-679(ARP 캐시·gARP) / docs.cilium.io v1.20 network/l2-announcements Leases 절(기본 10~20초, 3s·1s·200ms 예시 2~4초)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 460
d = D(W, H, "CILIUM UP AND RUNNING · 16-02 §3", "리더 장애에서 클라이언트 복구까지",
      "리스 만료까지는 Cilium 타이머가, 그 뒤 복구는 클라이언트 ARP 캐시가 정합니다",
      "기본값 15s · 5s · 2s 기준 10~20초")

Y_BASE = 200
d.line(40, Y_BASE, 880, Y_BASE, RULE, sw=1.2)

events = [
    (100, "0초", True, "리더 정지", "리스 갱신 중단", BAD, False),
    (280, "10~20초", False, "리스 만료", "leaseDuration 15s", INFO, False),
    (460, "만료 직후", True, "새 리더", "리스 획득", ACC, True),
    (640, "선출 직후", False, "gARP", "새 MAC 브로드캐스트", OK, False),
    (820, "수용 시 즉시", True, "ARP 캐시 갱신", "무시하면 캐시 만료까지", WARN, False),
]
for x, tm, above, title, sub, col, focal in events:
    r = 6 if focal else 4
    d.o.append(f'<circle cx="{x}" cy="{Y_BASE}" r="{r}" fill="{col if focal else PAPER}" stroke="{col}" stroke-width="1.4"/>')
    d.t(x, Y_BASE - 14 if above else Y_BASE + 24, tm, 12, col if focal else MUTED, MONO if tm[0].isdigit() else KR, "middle", 600)
    if above:
        ty = Y_BASE - 60
        d.line(x, Y_BASE - 22, x, ty + 22, RULE, sw=0.8, dash="2 2")
    else:
        ty = Y_BASE + 64
        d.line(x, Y_BASE + 32, x, ty - 16, RULE, sw=0.8, dash="2 2")
    if focal:
        d.tone(x - 80, ty - 16, 160, 44, col, r=4, op="18", sw=1.2)
        d.t(x, ty + 2, title, 12, col, KR if any("가" <= c <= "힣" for c in title) else MONO, "middle", 600)
        d.t(x, ty + 20, sub, 12, INK, KR, "middle")
    else:
        d.t(x, ty, title, 12, col, KR if any("가" <= c <= "힣" for c in title) else MONO, "middle", 600)
        d.t(x, ty + 18, sub, 12, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "middle")

# 아래 구간: 값에 따른 페일오버 폭
Y_B = 320
d.t(540, Y_B, "leaseDuration · leaseRenewDeadline · leaseRetryPeriod", 11, MUTED, MONO, "start")
rows = [
    ("기본값", "15s · 5s · 2s", "페일오버 10~20초", INFO),
    ("조정값", "3s · 1s · 200ms", "페일오버 2~4초", OK),
]
for k, (nm, vals, rng, col) in enumerate(rows):
    y = Y_B + 28 + k * 32
    d.t(40, y, nm, 12, col, KR, "start", 600)
    d.t(120, y, rng, 12, col, KR, "start", 600)
    d.t(540, y, vals, 11, INK, MONO, "start")

d.legend(404, [("장애", BAD), ("리스 만료", INFO), ("새 리더", ACC), ("ARP 공지", OK), ("캐시 지연", WARN)])
d.save("16-02.l2-failover-timeline.svg")
