# 06-02 §4 — 빌드 시점의 CoW 층 누적과 런타임의 유니온 마운트(N:1)·바인드 마운트(1:1) 구분.
# 타입 스펙: type-swimlane — 위 레인은 빌드 시점(docker build), 아래 레인은 런타임(docker run).
#           유니온 마운트는 N:1 겹쳐 쌓기, 바인드 마운트는 1:1 직접 연결을 나란히 보인다.
#           accent 는 빌드에서 완성된 읽기 전용 층이 런타임으로 넘어가는 handoff 와 런타임 쓰기 층.
#           형제 도식 06-02.image-layers.svg 는 Dockerfile 각 줄의 Step ID 와 72.8MB 공유를 다루고,
#           이 도식은 빌드·런타임 시점 경계와 유니온(N:1)·바인드(1:1) 경로 매핑을 다룬다.
# 축약: OverlayFS 세부 디렉터리 이름(lowerdir·upperdir·whiteout)은 docs container/03-02 로 넘겨 생략했다.
#       경로 예(/srv/data, /app/data)는 1:1 연결을 보이기 위한 설명용 예시다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 584
d = D(W, H, "LEARNING MODERN LINUX · 06-02 §4",
      "빌드는 층을 겹치고 런타임은 쓰기 층과 바인드를 더한다",
      "빌드 시점(docker build)에는 베이스 층 위에 COPY 와 RUN 마다 읽기 전용 이미지 층이 CoW 변경분으로 쌓인다. "
      "런타임(docker run)에는 유니온 마운트가 그 읽기 전용 층 N개와 컨테이너 전용 쓰기 층 1개를 하나의 루트(/)로 합치고(N:1), "
      "바인드 마운트(-v)는 호스트 폴더를 컨테이너 경로에 1:1로 직접 잇는다.",
      "유니온 마운트는 여러 층을 하나로 합치고(N:1), 바인드 마운트는 두 경로를 직접 잇습니다(1:1)")

LABX, LABW = 24, 136
R1Y, R1H = 104, 136
DIV_Y = 284
R2Y, R2H = 300, 212

# ── 레인 1: 빌드 시점 (docker build) ──────────────────────
d.box(LABX, R1Y, LABW, R1H, PAPER2, INFO, 1.2, 8)
d.t(LABX + LABW / 2, R1Y + 58, "빌드 시점", 14, INK, KR, "middle", 600)
d.t(LABX + LABW / 2, R1Y + 82, "docker build", 12, INFO, MONO, "middle", 600)

# 빌드 단계 3칸
d.box(180, 120, 176, 104, PAPER2, INFO, 1.1, 6)
d.t(268, 150, "FROM ubuntu:20.04", 12, INFO, MONO, "middle", 600)
d.t(268, 174, "베이스 층 (RO)", 12, INK, KR)
d.t(268, 198, "디스크에 한 벌 공유", 12, MUTED, KR)

d.arrow([(356, 172), (398, 172)], MUTED, "ar", 1.4)

d.box(400, 120, 200, 104, PAPER2, OK, 1.1, 6)
d.t(500, 150, "COPY · RUN", 12, OK, MONO, "middle", 600)
d.t(500, 174, "새 층 누적 (RO)", 12, INK, KR)
d.t(500, 198, "CoW 변경분만 저장", 12, MUTED, KR)

d.arrow([(600, 172), (642, 172)], MUTED, "ar", 1.4)

d.box(644, 120, 212, 104, PAPER2, INFO, 1.1, 6)
d.t(750, 150, "이미지 완성", 13, INK, KR, "middle", 600)
d.t(750, 174, "읽기 전용 층 N개", 12, INFO, KR)
d.t(750, 198, "greeter:1 (불변)", 12, MUTED, MONO)

# ── 레인 경계 ─────────────────────────────────────────────
d.line(24, DIV_Y, W - 24, DIV_Y, RULE, 1.0)

# ── 레인 2: 런타임 (docker run) ─────────────────────────
d.box(LABX, R2Y, LABW, R2H, PAPER2, ACC, 1.2, 8)
d.t(LABX + LABW / 2, R2Y + 94, "런타임", 14, INK, KR, "middle", 600)
d.t(LABX + LABW / 2, R2Y + 118, "docker run", 12, ACC, MONO, "middle", 600)

# 서브 패널 틀 (fill=none 으로 두어 handoff 화살표가 가려지지 않게 한다)
d.box(180, 308, 376, 196, "none", RULE, 0.9, 8)
d.t(396, 330, "유니온 마운트 (N:1)", 13, INK, KR, "middle", 600)

d.box(576, 308, 280, 196, "none", RULE, 0.9, 8)
d.t(716, 330, "바인드 마운트 (1:1)", 13, INK, KR, "middle", 600)

# ── 레인 1 → 레인 2 handoff 화살표 ───────────────────────
d.arrow([(750, 224), (750, 260), (268, 260), (268, 344)], ACC, "acc", 1.6)
d.t(512, 248, "읽기 전용 층 전달", 12, ACC, KR, "middle", 600)

# ── 왼쪽: 유니온 마운트 (N:1) ─────────────────────────────
d.box(192, 348, 152, 56, PAPER2, INFO, 1.1, 6)
d.t(268, 372, "이미지 층 N개", 12, INFO, KR, "middle", 600)
d.t(268, 392, "읽기 전용 (RO)", 12, MUTED, KR)

d.tone(192, 424, 152, 56, ACC, 6, "14", 1.3)
d.t(268, 448, "쓰기 층 1개", 12, ACC, KR, "middle", 600)
d.t(268, 468, "컨테이너 (RW)", 12, MUTED, KR)

d.path("M 344 376 L 376 376 L 376 412", INFO, 1.4)
d.path("M 344 452 L 376 452 L 376 412", ACC, 1.4)
d.arrow([(376, 412), (402, 412)], OK, "ok", 1.5)

d.box(404, 380, 136, 64, PAPER2, OK, 1.2, 6)
d.t(472, 408, "통합 / (merged)", 12, OK, KR, "middle", 600)
d.t(472, 428, "N개 층을 하나로", 12, MUTED, KR)

# ── 오른쪽: 바인드 마운트 (1:1) ───────────────────────────
d.box(608, 348, 216, 56, PAPER2, WARN, 1.1, 6)
d.t(716, 372, "호스트 폴더", 12, WARN, KR, "middle", 600)
d.t(716, 392, "/srv/data", 12, MUTED, MONO)

d.arrow([(716, 404), (716, 438)], WARN, "warn", 1.5)
d.t(732, 426, "-v 직접 연결", 12, WARN, KR, "start", 600)

d.box(608, 440, 216, 56, PAPER2, WARN, 1.1, 6)
d.t(716, 464, "컨테이너 경로", 12, INK, KR, "middle", 600)
d.t(716, 484, "/app/data", 12, MUTED, MONO)

# ── 범례 ─────────────────────────────────────────────────
d.legend(536, [
    ("읽기 전용 이미지 층", INFO),
    ("빌드 누적 · 통합 뷰", OK),
    ("층 전달 · 런타임 쓰기 층", ACC),
    ("호스트 1:1 연결", WARN),
])

d.save("06-02.bind-vs-union.svg")
print("ok 06-02.bind-vs-union")
