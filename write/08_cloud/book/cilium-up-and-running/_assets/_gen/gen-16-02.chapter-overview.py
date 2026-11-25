# 타입 스펙: type-flowchart — Day 2 장애 증상에서 4단계 범위 좁히기(§1)를 거쳐 기능별 점검(§2~§5)으로 갈리는 깔때기 흐름도.
# 값 근거: 본문 §1~§5 및 ch16.txt 줄 424(cilium status), 458(--test '^(to-fqdns.*)$', 123 tests), 485-491(cilium-health status, 3/3 reachable), 503-518(Gateway API CRD 누락, cilium sysdump --node-list kind-worker2), 593-608(cilium-envoy·DNS 프록시), 634-654(lease 15s·5s·2s, 10~20초), 701-727(PodCIDR·Service /32·/128), 733-755(CiliumBGPPeerConfig·restartTimeSeconds 120s)
import sys

sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 720
d = D(
    W,
    H,
    "CILIUM UP AND RUNNING · 16-02 OVERVIEW",
    "Day 2 장애 점검 순서와 기능별 분기",
    "증상에서 시작해 cilium status, connectivity test, cilium-health, 로그와 sysdump 순으로 범위를 좁히고, 특정된 기능에 따라 L7, L2, BGP 층으로 내려갑니다.",
    lead="왼쪽 깔때기에서 명령 결과에 따라 단계를 넘기고, 특정된 기능은 오른쪽 카드로 내려갑니다.",
)


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def diamond(cx, cy, hw, hh, line1, line2=None):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(
        f'<polygon points="{pts}" fill="{PAPER2}" stroke="{SOFT}" stroke-width="1.1"/>'
    )
    if line2:
        d.t(cx, cy - 4, line1, 13, INK, kr(line1), "middle", 600)
        d.t(cx, cy + 16, line2, 11, MUTED, kr(line2), "middle")
    else:
        d.t(cx, cy + 5, line1, 13, INK, kr(line1), "middle", 600)


# Zone titles
d.t(24, 108, "1단계 · 범위 좁히기 (§1)", 13, MUTED, KR, "start", 600)
d.line(24, 116, 476, 116, RULE, 0.8)
d.t(528, 108, "기능별 가지 (§2·§3·§5) · 설계 비교 (§4)", 13, MUTED, KR, "start", 600)
d.line(528, 116, 936, 116, RULE, 0.8)

CX = 160

# Start oval
d.box(40, 128, 240, 44, PAPER2, SOFT, 1.1, r=20)
d.t(CX, 148, "Day 2 장애 증상", 14, INK, KR, "middle", 600)
d.t(CX, 165, "연결 실패 · 지연", 13, MUTED, KR, "middle")
d.arrow([(CX, 172), (CX, 196)], INFO, "info", 1.4)

# Gate 1: cilium status
diamond(CX, 236, 128, 38, "cilium status", "에이전트 정상?")
d.chip(276, 208, "§1", INFO, 11)
d.arrow([(288, 236), (332, 236)], WARN, "warn", 1.3)
d.t(310, 224, "이상", 13, WARN, KR, "middle", 600)
d.tone(336, 212, 140, 48, WARN, r=6, op="12", sw=1.0)
d.t(406, 234, "해당 데몬 복구", 13, WARN, KR, "middle", 600)
d.t(406, 252, "Pod 상태 점검", 13, MUTED, KR, "middle")

d.arrow([(CX, 274), (CX, 304)], OK, "ok", 1.4)
d.t(172, 294, "정상", 13, OK, KR, "start", 600)

# Gate 2: connectivity test
diamond(CX, 344, 136, 38, "connectivity test", "항목별 보고서")
d.chip(280, 316, "§1", INFO, 11)
d.arrow([(296, 344), (332, 344)], WARN, "warn", 1.3)
d.t(314, 332, "실패", 13, WARN, KR, "middle", 600)
d.tone(336, 320, 140, 48, WARN, r=6, op="12", sw=1.0)
d.t(406, 342, "실패 시험 확인", 13, WARN, KR, "middle", 600)
d.t(406, 360, "보고서에서 확인", 13, MUTED, KR, "middle")

d.arrow([(CX, 382), (CX, 412)], INFO, "info", 1.4)
d.t(172, 402, "실패 · 증상 남음", 13, INFO, KR, "start", 600)

# Gate 3: cilium-health status
diamond(CX, 452, 132, 38, "cilium-health status", "3/3 reachable?")
d.chip(280, 424, "§1", INFO, 11)
d.arrow([(292, 452), (332, 452)], WARN, "warn", 1.3)
d.t(312, 440, "불통", 13, WARN, KR, "middle", 600)
d.tone(336, 428, 140, 48, WARN, r=6, op="12", sw=1.0)
d.t(406, 450, "하부 망 점검", 13, WARN, KR, "middle", 600)
d.t(406, 468, "unreachable 경로", 13, MUTED, KR, "middle")

d.arrow([(CX, 490), (CX, 524)], OK, "ok", 1.4)
d.t(172, 512, "3/3 reachable", 12, OK, MONO, "start", 600)

# Step 4: Logs + sysdump (Focal ACC)
d.tone(24, 528, 272, 92, ACC, r=6, op="16", sw=1.4)
d.chip(276, 544, "§1", ACC, 11)
d.t(40, 554, "에이전트·오퍼레이터 로그", 14, ACC, KR, "start", 700)
d.t(40, 578, "예: Gateway API CRD 누락", 13, INK, KR, "start")
d.t(40, 602, "sysdump --node-list kind-worker2", 12, MUTED, MONO, "start")

# Bus from Step 4 to Right Functional Cards (§2~§5)
BUS_X = 500
d.line(296, 566, BUS_X, 566, ACC, 1.4)
d.line(BUS_X, 310, BUS_X, 566, ACC, 1.4)

cards = [
    ("§4", "BGP 광고 비교 · 흐름 밖", "PodCIDR vs Service", "/32 · /128 고정 VIP", OK, 128),
    ("§2", "L7 프록시 공백", "cilium-envoy · DNS 프록시", "Pod 교체 중 연결 드롭", INFO, 256),
    ("§3", "L2 Announcements", "Lease 15s · 5s · 2s", "ARP 캐시 · gARP 복구", INFO, 384),
    ("§5", "BGP Graceful Restart", "restartTimeSeconds 120s", "유지 vs 장애 지연", WARN, 512),
]

for sec, title, val1, val2, col, cy in cards:
    mid_y = cy + 54
    if sec != "§4":
        d.arrow([(BUS_X, mid_y), (524, mid_y)], ACC, "acc", 1.4)
    d.tone(528, cy, 408, 108, col, r=6, op="12", sw=1.1)
    d.chip(912, cy + 20, sec, col, 11)
    d.t(544, cy + 32, title, 14, col, KR, "start", 700)
    d.t(544, cy + 60, val1, 13, INK, kr(val1), "start")
    d.t(544, cy + 86, val2, 13, MUTED, kr(val2), "start")

d.legend(
    H - 44,
    [
        ("상태 점검 · 범위 좁히기", INFO),
        ("진단 수집 · 분기점", ACC),
        ("정상 경로 · VIP 절약", OK),
        ("이상 · 공백 · 지연", WARN),
    ],
)
d.save("16-02.chapter-overview.svg")
print("ok 16-02 overview")
