# 02-02.ebpf-verifier-gate — eBPF 가 커널 안으로 들어가는 경로와 그 관문
# 본문 요구: "eBPF는 샌드박스된 특수 프로그램을 커널 안에서 실행하는 시스템입니다.
#            Netfilter·iptables처럼 커널과 유저스페이스를 오가지 않는다는 점이 구조적 차이입니다."
#            + §5 "프로그램을 로드하면 커널의 verifier 가 그것을 통째로 정적 검사합니다."
#            + §5 "verifier 가 푸는 것은 신뢰 문제입니다."
#            + §5 attach point 다섯(kprobes·uprobes·tracepoints·perf_events·XDP)
# 타입 스펙: type-swimlane.md — 레인 = 주체(유저스페이스 · 커널). 이 편의 논지가 바로 그 경계라
#           레인을 넘는 화살표가 가장 중요한 간선이 된다. 경계를 넘는 곳이 딱 둘이라는 것이 요점 —
#           제어는 로드 때 한 번만 넘어가고, 그 뒤로는 데이터(맵)만 올라온다.
#           focal 은 handoff 가 아니라 verifier 에 건다. 본문이 그 도식에서 짚는 단 하나가 관문이다.
# 좌표: Layout conventions 타입이라 공식이 없다 — 단계 stride 208·레인 h 120 으로 고정, 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, PAPER, PAPER2, INFO, BAD, KR, MONO

W, H = 1000, 792
BW, BH = 160, 72
CX = [272 + i * 208 for i in range(4)]              # 272 480 688 896
LANE_X, LANE_W, LANE_H = 24, 952, 120
U_Y, K_Y = 156, 316                                  # 유저스페이스 · 커널 레인

d = D(W, H, "EBPF · THE VERIFIER IS THE GATE",
      "eBPF 가 커널 안으로 들어가는 길 — verifier 를 통과해야 붙는다",
      "위 레인이 유저스페이스이고 아래가 커널이다. 경계를 넘는 곳은 둘뿐 — 로드할 때 제어가 한 번 내려가고, "
      "그 뒤로는 맵을 통해 데이터만 올라온다. 붙은 프로그램은 이벤트마다 커널 안에서만 돈다.",
      lead="Netfilter·iptables 는 패킷마다 경계를 오간다 · eBPF 는 로드할 때 한 번만 넘는다")


def lane(y, name, sub):
    d.box(LANE_X, y, LANE_W, LANE_H, PAPER2, RULE, 1.0, 8)
    d.t(40, y + 32, name, 13, INK, KR, "start", 600)
    d.t(40, y + 52, ddx.fit(sub, 12, 168, sub), 12, MUTED, KR, "start")


def cell(cx, cy, title, sub, kind="has"):
    x, y = cx - BW // 2, cy - BH // 2
    if kind == "focal":
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = sc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, INFO, 1.1, 6); tc, sc = INFO, MUTED
    d.t(cx, cy - 6, ddx.fit(title, 13, BW - 14, title), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(sub, 12, BW - 12, sub), 12, sc, KR)


lane(U_Y, "유저스페이스", "여기서 만들고 읽는다")
lane(K_Y, "커널", "검사·컴파일·실행이 여기서")

# 유저스페이스 — 만드는 쪽과 읽는 쪽
cell(CX[0], U_Y + 60, "1 작성·컴파일", "C → eBPF 바이트코드")
cell(CX[3], U_Y + 60, "맵 읽기", "결과 데이터만 올라온다")

# 커널 — 관문·번역·실행
cell(CX[1], K_Y + 60, "2 verifier", "로드 시점 정적 검사", "focal")
cell(CX[2], K_Y + 60, "3 JIT", "네이티브 코드로 번역")
cell(CX[3], K_Y + 60, "4 attach·실행", "이벤트마다 커널 안에서")

# 경계를 넘는 곳 (1) — 로드. 제어가 내려간다
d.path(f"M {CX[0]} {U_Y + 96} L {CX[0]} 292 L {CX[1] - BW // 2 - 12} 292 "
       f"L {CX[1] - BW // 2 - 12} {K_Y + 60} L {CX[1] - BW // 2 - 8} {K_Y + 60}", ACC, 1.6, m="acc")
d.chip((CX[0] + CX[1]) // 2, 292, "bpf() 시스템콜", ACC, 12)

# 경계를 넘는 곳 (2) — 맵. 데이터만 올라온다
d.path(f"M {CX[3] + 40} {K_Y + 24} L {CX[3] + 40} {U_Y + 96}", INFO, 1.4, m="info", dash="5 5")
d.t(CX[3] + 48, 300, "맵", 12, INFO, KR, "start")

# 레인 안 진행
for a, b in ((CX[1], CX[2]), (CX[2], CX[3])):
    d.path(f"M {a + BW // 2 + 8} {K_Y + 60} L {b - BW // 2 - 10} {K_Y + 60}", MUTED, 1.4, m="ar")

# 통과 못 하면 붙지 못한다
d.chip(CX[1], K_Y + 108, "거부 → 로드 실패", BAD, 12)

# verifier 가 보는 넷
d.box(LANE_X, 476, LANE_W, 80, PAPER, RULE, 1.0, 8)
d.t(40, 500, "verifier 가 로드 시점에 확인하는 넷", 12, SOFT, KR, "start", 600)
for cx, txt in zip([148 + i * 232 for i in range(4)],
                   ["끝나는 것이 보장되는가", "메모리 접근이 범위 안인가",
                    "쓰지 않은 자리를 읽지 않는가", "허용된 helper 만 부르는가"]):
    d.t(cx, 536, ddx.fit(txt, 13, 216, txt), 13, MUTED, KR)

# 붙을 수 있는 자리
d.box(LANE_X, 580, LANE_W, 88, PAPER, RULE, 1.0, 8)
d.t(40, 604, "4 단계에서 붙을 수 있는 자리", 12, SOFT, KR, "start", 600)
for cx, (nm, sub) in zip([116 + i * 184 for i in range(5)],
                         [("kprobes", "커널 동적 추적"), ("uprobes", "유저스페이스 추적"),
                          ("tracepoints", "정적 · 버전 안정"), ("perf_events", "시간 샘플링"),
                          ("XDP", "드라이버 수준 패킷")]):
    d.t(cx, 632, nm, 13, INFO, MONO, "middle", 600)
    d.t(cx, 652, ddx.fit(sub, 12, 168, sub), 12, MUTED, KR)

d.t(24, 700, "verifier 는 성능을 주지 않습니다. 성능은 경계를 안 넘는 것과 해시 조회에서 나옵니다.",
    13, MUTED, KR, "start")
d.t(24, 722, "verifier 가 푸는 것은 신뢰입니다 — 커널을 못 죽인다는 보장이 로드 시점에 서므로 재부팅 없이 기능을 넣습니다.",
    13, MUTED, KR, "start")
d.legend(744, [("관문 — 통과해야 붙는다", ACC), ("경계를 넘는 데이터", INFO), ("통과 못 한 경우", BAD)])
d.save("02-02.ebpf-verifier-gate.svg")
print("ok ebpf-verifier-gate")
