# 12-01 §work queue 랩 — "적재부터 큐 소진까지"
# 단계 나열로 그리면 본문이 "이 랩의 핵심" 이라고 못 박은 것이 묻힌다. completions 를 비우면
# worker-pool 모드가 되고, 그래서 "일이 다 끝나기 전에는 어떤 워커도 먼저 나가면 안 된다".
# 그 규칙은 워커 다섯이 *같은 x 에서 함께 끝나는* 것으로만 눈에 보이므로 레인을 다섯 줄 깐다.
# 윗단은 본문이 따로 적는 비대칭 — 넣는 길은 클러스터 밖 port-forward, 꺼내는 길은 안의 DNS.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 712
d = D(W, H, "KUBERNETES UP AND RUNNING · 12-01",
      "큐가 빌 때까지 아무도 먼저 나가지 않는다",
      "kuard 에 내장된 메모리 큐를 조율자로 세우고, 일감 100 건을 넣고, 워커 다섯이 병렬로 비운다. "
      "넣는 길과 꺼내는 길이 서로 다르다.",
      "completions 를 비우면 Job 은 worker-pool 모드로 들어간다")

CY = 228
ddx.node(d, 140, CY, "내 노트북의 curl", "일감 100 건을 넣는다", w=220, h=68)
d.box(456, 158, 328, 132, PAPER, RULE, 1.0, 8)
d.t(620, 178, "ReplicaSet · replicas 1", 10, SOFT, KR)
ddx.node(d, 620, CY, "queue 파드", "kuard 내장 메모리 큐", w=280, h=76)
d.t(620, 308, "머신 장애가 나도 새 파드가 만들어진다", 10, SOFT, KR)
ddx.node(d, 910, CY, "Service queue", "DNS 이름으로 찾는다", w=140, h=68)
ddx.node(d, 1134, CY, "consumers Job", "parallelism 5", w=188, h=68)

d.path(f"M 250 {CY} L 448 {CY}", MUTED, 1.5, m="ar", dash="5 4")
d.t(349, 208, "port-forward 8080", 10, SOFT, MONO)
d.t(349, 254, "클러스터 밖에서 여는 임시 통로", 10, SOFT, KR)
d.path(f"M 1040 {CY} L 988 {CY}", INFO, 1.5, m="info")
d.path(f"M 840 {CY} L 792 {CY}", INFO, 1.5, m="info")
d.t(916, 190, "클러스터 안의 정규 경로", 10, INFO, KR)
d.t(916, 274, "http://queue:8080/memq/server", 9, SOFT, MONO)

# ── 아랫단: 큐 깊이와 종료 조건
d.line(12, 340, W - 24, 340, RULE, 0.8)
d.t(12, 364, "큐 깊이 — 적재부터 소진까지", 13, INK, KR, "start", 600)

X0, A, B, C, XE = 140, 440, 580, 1010, 1150
TOP, BASE = 400, 480
d.line(X0 - 16, BASE, XE + 10, BASE, RULE, 1.0)
d.t(X0 - 26, TOP + 4, "100", 9, SOFT, MONO, "end")
d.t(X0 - 26, BASE + 4, "0", 9, SOFT, MONO, "end")
d.t(X0 - 26, 380, "depth", 8, SOFT, MONO, "end")
d.path(f"M {X0} {BASE} L {A} {TOP} L {B} {TOP} L {C} {BASE} L {XE} {BASE}", INK, 1.6)
for x, lab in ((A, "depth 100"), (B, "job-consumers 적용"), (C, "큐가 비었다")):
    d.line(x, 392, x, 560, RULE, 1.0, "4 5")
    d.t(x, 384, lab, 10, SOFT, KR)
d.t((X0 + A) / 2, 466, "curl 로 100 건 적재", 10, SOFT, KR)
d.t((B + C) / 2, 420, "워커 다섯이 병렬로 꺼낸다", 10, SOFT, KR)

for i in range(5):
    y = 500 + i * 13
    d.line(B, y, C - 6, y, SOFT, 1.0)
    d.o.append(f'<rect x="{C-6}" y="{y-3}" width="6" height="6" fill="{ACC}"/>')
d.t(B - 16, 530, "워커 5 개", 10, SOFT, KR, "end")
d.line(C, 392, C, 566, ACC, 1.4)

BT, BB = 578, 638
d.o.append(f'<rect x="12" y="{BT}" width="{W-36}" height="{BB-BT}" rx="8" '
           f'fill="{ACC}0E" stroke="{ACC}" stroke-width="1.2"/>')
d.t(W / 2, BT + 24,
    "completions 를 비워 두면 worker-pool 모드다. 첫 파드가 종료 코드 0 으로 나가는 순간 Job 은 정리에 들어가 새 파드를 만들지 않는다.",
    11, ACC, KR)
d.t(W / 2, BT + 46,
    "그래서 다섯은 큐가 빈 것을 각자 확인하고 함께 끝난다 — 하나라도 먼저 나가면 남은 일감을 처리할 워커가 줄어든다.",
    11, ACC, KR)

d.legend(BB + 24, [("함께 끝나는 지점", ACC), ("클러스터 안의 경로", INFO)])
d.save("12-01.workqueue-lab.svg")
print("h 필요:", BB + 24 + 48, " 실제:", H)
