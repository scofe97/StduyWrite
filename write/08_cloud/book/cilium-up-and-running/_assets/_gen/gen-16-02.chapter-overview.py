# 타입 스펙: type-process — 상태 확인에서 sysdump 까지 다섯 점검 단계와 기능별 세 분기. 주체 없는 단계 지도라 chapter-overview 폴더 관례대로 process 의 카드 문법을 쓴다.
# 사실 출처: Cilium Up and Running 16장 cil16.txt 줄 424(cilium status), 458(--test '^(to-fqdns.*)$'), 485-491(3/3 reachable), 503-506(Gateway API CRD 누락 로그), 514-518(--node-list kind-worker2) / docs.cilium.io v1.20 l2-announcements(15s) · bgp-control-plane-configuration(120s) / values.yaml v1.20.2 cilium-envoy
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 448
d = D(W, H, "CILIUM UP AND RUNNING · 16-02", "Day 2 점검 순서와 기능별 분기",
      "범위가 넓은 도구에서 좁은 도구로 내려가고, 그다음 기능마다 의존하는 대상을 본다",
      "단계마다 명령 하나와 그 단계에서 읽는 실제 값")

X0, GAP, CW, CH, Y1 = 12, 24, 160, 140, 104
steps = [
    ("01", "상태", "cilium status", "구성 요소 건강", INFO),
    ("02", "연결 시험", "--test", "'^(to-fqdns.*)$'", INFO),
    ("03", "노드 건강", "cilium-health status", "3/3 reachable", INFO),
    ("04", "로그", "에이전트 · 오퍼레이터", "Gateway API CRD 누락", WARN),
    ("05", "스냅샷", "sysdump --node-list", "kind-worker2", ACC),
]
for i, (num, title, cmd, val, col) in enumerate(steps):
    x = X0 + i * (CW + GAP)
    cx = x + CW // 2
    if col == ACC:
        d.tone(x, Y1, CW, CH, ACC, r=6, op="12", sw=1.4)
    else:
        d.box(x, Y1, CW, CH, PAPER2, RULE, 0.9, 6)
    d.chip(x + 28, Y1 + 20, num, col, size=10)
    d.t(cx, Y1 + 56, title, 13, INK, KR, "middle", 600)
    d.line(x + 12, Y1 + 72, x + CW - 12, Y1 + 72, RULE, 0.6)
    d.t(cx, Y1 + 96, cmd, 12, col, KR if any("가" <= c <= "힣" for c in cmd) else MONO, "middle", 600)
    d.t(cx, Y1 + 120, val, 12, MUTED, KR if any("가" <= c <= "힣" for c in val) else MONO, "middle")
    if i < len(steps) - 1:
        d.arrow([(x + CW + 2, Y1 + 70), (x + CW + GAP - 2, Y1 + 70)], MUTED, "ar", 1.2)

# 05 아래로 내려 버스를 타고 세 분기로 갈라진다 (직각만)
BUS_Y, Y2, BW, BH, BGAP, BX0 = 276, 300, 280, 72, 20, 12
last_cx = X0 + 4 * (CW + GAP) + CW // 2
branches = [
    ("L7 기능", "Envoy · DNS 프록시", "교체 중 공백", INK),
    ("L2 Announcements", "lease 15s · 5s · 2s", "페일오버 10~20초", INK),
    ("BGP", "restartTimeSeconds", "기본 120초", INK),
]
bxs = [BX0 + j * (BW + BGAP) for j in range(3)]
d.line(last_cx, Y1 + CH, last_cx, BUS_Y, ACC, 1.4)
d.line(bxs[0] + BW // 2, BUS_Y, last_cx, BUS_Y, ACC, 1.4)
for j, (name, v1, v2, col) in enumerate(branches):
    x = bxs[j]
    d.arrow([(x + BW // 2, BUS_Y), (x + BW // 2, Y2 - 2)], ACC, "acc", 1.4)
    d.box(x, Y2, BW, BH, PAPER2, RULE, 0.9, 6)
    d.t(x + 16, Y2 + 24, name, 13, col, KR if any("가" <= c <= "힣" for c in name) else MONO, "start", 600)
    d.t(x + 16, Y2 + 44, v1, 12, INK, KR if any("가" <= c <= "힣" for c in v1) else MONO, "start")
    d.t(x + 16, Y2 + 62, v2, 12, MUTED, KR, "start")

d.legend(Y2 + BH + 20, [("범위 좁히기", INFO), ("오류 메시지", WARN), ("전체 수집", ACC)])
d.save("16-02.chapter-overview.svg")
