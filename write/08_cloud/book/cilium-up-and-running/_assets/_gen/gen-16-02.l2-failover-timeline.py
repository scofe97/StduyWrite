# 타입 스펙: type-timeline — 리더 노드 정지부터 리스 만료, 새 리더 선출, gARP, 클라이언트 ARP 캐시 갱신까지의 L2 페일오버 타임라인과 기본값·조정값 비교.
# 값 근거: 본문 §3 및 ch16.txt 줄 634-680(리스 cilium-l2announce-<ns>-<svc>, leaseDuration 15s, leaseRenewDeadline 5s, leaseRetryPeriod 2s, ARP 캐시, gARP) / docs.cilium.io v1.20 network/l2-announcements(기본 10~20초, 3s·1s·200ms 예시 2~4초)
import sys

sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 480
d = D(
    W,
    H,
    "CILIUM UP AND RUNNING · 16-02 §3",
    "리더 장애에서 클라이언트 복구까지",
    "리스 만료까지는 Cilium 의 세 타이머가 결정하고, 그 뒤 실제 트래픽 전환 시점은 클라이언트의 ARP 캐시와 gARP 수용 여부가 정합니다.",
    lead="기본값 15s · 5s · 2s 기준 페일오버 폭 10~20초",
)

Y_BASE = 204
d.line(40, Y_BASE, 920, Y_BASE, RULE, sw=1.2)

events = [
    (104, "0초", True, "리더 정지", "리스 갱신 중단", BAD, False),
    (292, "10~20초", False, "리스 만료", "15s ± 5s (Duration±Deadline)", INFO, False),
    (480, "만료 직후", True, "새 리더 선출", "cilium-l2announce-* 획득", ACC, True),
    (668, "선출 직후", False, "gARP 송출", "새 MAC 브로드캐스트", OK, False),
    (856, "수용 시 즉시", True, "ARP 캐시 갱신", "무시 시 캐시 만료까지", WARN, False),
]

for x, tm, above, title, sub, col, focal in events:
    r = 6 if focal else 4
    d.o.append(
        f'<circle cx="{x}" cy="{Y_BASE}" r="{r}" fill="{col if focal else PAPER}" stroke="{col}" stroke-width="1.4"/>'
    )
    d.t(
        x,
        Y_BASE - 14 if above else Y_BASE + 24,
        tm,
        13,
        col if focal else MUTED,
        MONO if tm[0].isdigit() else KR,
        "middle",
        600,
    )
    if above:
        ty = Y_BASE - 68
        d.line(x, Y_BASE - 24, x, ty + 24, RULE, sw=0.8, dash="2 2")
    else:
        ty = Y_BASE + 68
        d.line(x, Y_BASE + 32, x, ty - 16, RULE, sw=0.8, dash="2 2")
    if focal:
        d.tone(x - 104, ty - 20, 208, 48, col, r=4, op="16", sw=1.3)
        d.t(x, ty, title, 14, col, KR, "middle", 700)
        d.t(x, ty + 20, sub, 12, INK, KR, "middle")
    else:
        d.t(x, ty, title, 14, col, KR, "middle", 600)
        d.t(x, ty + 20, sub, 13, MUTED, KR, "middle")

# Bottom section: Lease parameter comparison
Y_B = 328
d.line(40, Y_B - 12, 920, Y_B - 12, RULE, sw=0.8)
d.t(40, Y_B + 8, "구분", 13, MUTED, KR, "start", 600)
d.t(160, Y_B + 8, "예상 페일오버 폭", 13, MUTED, KR, "start", 600)
d.t(440, Y_B + 8, "leaseDuration · leaseRenewDeadline · leaseRetryPeriod", 11, MUTED, MONO, "start")

rows = [
    ("기본값", "페일오버 10~20초", "15s · 5s · 2s", INFO),
    ("조정값", "페일오버 2~4초 (API 부하 증가)", "3s · 1s · 200ms", OK),
]
for k, (nm, rng, vals, col) in enumerate(rows):
    y = Y_B + 36 + k * 32
    d.t(40, y, nm, 13, col, KR, "start", 600)
    d.t(160, y, rng, 13, col, KR, "start", 600)
    d.t(440, y, vals, 12, INK, MONO, "start")

d.legend(
    H - 44,
    [
        ("장애", BAD),
        ("리스 만료", INFO),
        ("새 리더", ACC),
        ("ARP 공지 · 단축", OK),
        ("캐시 지연", WARN),
    ],
)
d.save("16-02.l2-failover-timeline.svg")
print("ok 16-02 l2 timeline")
