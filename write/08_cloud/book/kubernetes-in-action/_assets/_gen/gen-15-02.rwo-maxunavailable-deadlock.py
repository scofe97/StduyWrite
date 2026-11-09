# 15-02 §4 — RWO 볼륨과 maxUnavailable 0 의 교착
# 본문이 "서로 맞물려 progressDeadlineSeconds(600초)를 넘긴다"고 서술한다.
# 새 파드는 볼륨을 기다리고, 컨트롤러는 새 파드 Ready를 기다리고, 옛 파드는 볼륨을 쥔 채 유지된다.
# 화살표 셋으로 순환 대기를 닫고, 화살표 3을 끊는 3가지 해소 경로를 함께 보인다.
# 타입 스펙: type-architecture.md — 노드 둘과 볼륨·컨트롤러 배치 및 순환 의존 관계
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 900, 600
d = D(W, H, "KUBERNETES IN ACTION · 15-02",
      "RWO 볼륨과 maxUnavailable 0 의 순환 대기",
      "RWO 볼륨은 단일 노드에만 붙고 maxUnavailable 0 은 새 파드 준비 전까지 옛 파드를 유지한다. "
      "두 조건이 겹치면 노드가 다를 때 볼륨을 서로 기다리는 교착에 빠진다.")

lead = "새 파드는 볼륨을 기다리고 · 컨트롤러는 새 파드를 기다리고 · 옛 파드는 볼륨을 놓지 않음"
d.t(12, 74, lead, 12, MUTED, KR, "start")

# 1. Deployment 컨트롤러 (상단 중앙)
d.box(280, 101, 340, 58, PAPER2, RULE, 1.1, 6)
d.t(450, 124, "Deployment 컨트롤러", 13, INK, KR, "middle", 600)
d.t(450, 144, "maxUnavailable: 0 · 새 파드 Ready 전엔 안 지움", 12, MUTED, KR, "middle")

# 2. 노드 A (기존 노드 - 좌측)
d.box(36, 190, 316, 270, PAPER2, RULE, 0.9, 8)
d.t(52, 214, "노드 A (기존 노드)", 13, INK, KR, "start", 600)
d.t(52, 234, "옛 파드 실행 · 볼륨 연결", 12, MUTED, KR, "start")

# 옛 파드 (v1)
d.box(54, 255, 280, 60, PAPER, OK, 1.2, 6)
d.t(194, 277, "옛 파드 (v1)", 13, OK, KR, "middle", 600)
d.t(194, 299, "Running · 트래픽 수신 중", 12, MUTED, KR, "middle")

# RWO 볼륨 (PVC)
d.box(54, 372, 280, 56, PAPER, WARN, 1.2, 6)
d.t(194, 394, "RWO 블록 볼륨 (PVC)", 13, WARN, KR, "middle", 600)
d.t(194, 414, "단일 노드 제약 · 노드 A 점유", 12, MUTED, KR, "middle")

# 화살표 2: 볼륨 → 옛 파드 (볼륨 점유 유지)
d.path("M 130 372 L 130 323", WARN, 1.4, m="warn")
d.t(142, 348, "2 · 옛 파드가 볼륨 점유 (mount)", 12, WARN, KR, "start")

# 3. 노드 B (새 노드 - 우측)
d.box(548, 190, 316, 270, PAPER2, RULE, 0.9, 8)
d.t(564, 214, "노드 B (새 노드)", 13, INK, KR, "start", 600)
d.t(564, 234, "새 파드 스케줄 · 다른 노드", 12, MUTED, KR, "start")

# 새 파드 (v2)
d.box(566, 255, 280, 60, PAPER, BAD, 1.2, 6)
d.t(706, 277, "새 파드 (v2) · 대기", 13, BAD, KR, "middle", 600)
d.t(706, 299, "STATUS Init:0/1 / ContainerCreating", 12, MUTED, MONO, "middle")

# 볼륨 attach 실패 슬롯
d.box(566, 372, 280, 56, PAPER, BAD, 1.0, 6)
d.t(706, 394, "볼륨 attach 실패", 13, BAD, KR, "middle", 600)
d.t(706, 414, "Multi-Attach error 로 멈춤", 12, MUTED, KR, "middle")

# 새 파드 → 볼륨 attach 시도 (노드 B 내부)
d.path("M 706 315 L 706 364", BAD, 1.2, m="bad", dash="4 4")
d.t(718, 344, "볼륨 마운트 시도", 12, MUTED, KR, "start")

# 4. 중앙 교착 / 기한 초과 콜아웃
d.box(362, 233, 176, 104, PAPER2, BAD, 1.2, 8)
d.t(450, 257, "순환 대기 (Deadlock)", 13, BAD, KR, "middle", 600)
d.t(450, 277, "서로 상대 상태를 기다림", 12, MUTED, KR, "middle")
d.t(450, 303, "600초 경과 시", 12, WARN, KR, "middle", 600)
d.t(450, 323, "ProgressDeadlineExceeded", 11, BAD, MONO, "middle")

# 화살표 1: 새 파드 → 볼륨 (attach 거부, 노드 간 연결)
d.path("M 566 400 L 342 400", BAD, 1.4, m="bad")
d.t(450, 384, "1 · attach 거부", 12, BAD, KR, "middle", 600)
d.t(450, 420, "Multi-Attach error", 12, BAD, MONO, "middle")

# 화살표 3: 컨트롤러 → 옛 파드 (삭제 보류 및 해소 지점)
d.path("M 300 159 L 300 247", OK, 1.4, m="ok")
d.t(290, 172, "3 · 옛 파드 유지", 12, OK, KR, "end", 600)
d.t(290, 188, "Ready 전엔 안 지움", 12, MUTED, KR, "end")

# ✂ 3번 화살표 끊는 자리 칩
d.box(300 - 45, 205 - 12, 90, 24, fill=PAPER, stroke=ACC, sw=1.1, r=4)
d.t(300, 211, "✂ 끊는 자리", 12, ACC, KR, "middle", 600)

# 순환 루프 닫기: 새 파드 → 컨트롤러 (Ready 대기)
d.path("M 700 255 L 700 130 L 628 130", MUTED, 1.4, m="ar")
d.t(690, 172, "Ready 대기", 12, WARN, KR, "end", 600)
d.t(690, 188, "새 파드 준비 전", 12, MUTED, KR, "end")

# 5. 하단 안내문 (교착 없음 및 해소 방법)
d.t(36, 485, "교착 없음: 같은 노드에 스케줄 · NFS 등 attachRequired=false", 12, MUTED, KR, "start")
d.t(36, 507, "3번을 끊는 세 가지 길: Recreate · maxUnavailable ≥ 1 · 수동 삭제", 12, SOFT, KR, "start")

# 6. 범례 (my_legend 패턴)
def my_legend(d, y, items):
    d.line(12, y, d.w - 48, y, RULE, 0.8)
    d.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
    x = 90
    for lab, c in items:
        d.o.append(f'<rect x="{x}" y="{y+10}" width="14" height="14" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        d.t(x + 22, y + 22, lab, 12, MUTED, KR, "start")
        x += 36 + len(lab) * 14

my_legend(d, 532, [
    ("옛 파드 실행", OK),
    ("볼륨 점유", WARN),
    ("연결 거부 · 대기", BAD),
    ("3번 끊는 자리", ACC)
])

d.save("15-02-rwo-maxunavailable-deadlock.svg")
print("ok")
