# 타입 스펙: type-process
# 30-01 장 지도 — Image Builder 전체 구성 지도
# 본문: 클러스터 내부 빌드는 스케줄러 활용과 자동 재배포 CD 이점을 제공하지만,
#   rootless 비특권 빌드가 핵심 전제다. 도구는 오케스트레이터와 빌더로 나뉘며,
#   Build Pod와 OpenShift 파이프라인으로 빌드-배포를 연결한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 280

d = D(W, H, "KUBERNETES PATTERNS · 30-01",
      "Image Builder — 클러스터 안에서 이미지를 빌드하기",
      "클러스터 내부 이미지 빌드의 단계별 구성 지도: 보안 전제, 계층 분리, 순차 파이프라인, 도구 선택",
      lead="클러스터 스케줄러 활용 · rootless 보안 전제 · 순차 파이프라인과 도구 선택")

# ── 4단계 절 지도 (## 1. ~ ## 4.) ──────────────────────────────────────────
TOP_Y = 100
CARD_H = 114
CARD_W = 210
GAP = 24
START_X = 24

cards = [
    {
        "sec": "§1. 보안 위험과 전제",
        "kw1": "Docker 데몬 root 위험",
        "kw2": "rootless 비특권 빌드",
        "color": BAD,
    },
    {
        "sec": "§2. 계층 분리",
        "kw1": "컨테이너 이미지 빌더",
        "kw2": "파이프라인 오케스트레이터",
        "color": INFO,
    },
    {
        "sec": "§3. 파이프라인 연계",
        "kw1": "Build Pod 순차 실행",
        "kw2": "ImageStream 자동 트리거",
        "color": ACC,
    },
    {
        "sec": "§4. 도구 선택",
        "kw1": "명세 · 방식별 빌더 선택",
        "kw2": "빌드 전용 네임스페이스",
        "color": OK,
    },
]

for i, c in enumerate(cards):
    x = START_X + i * (CARD_W + GAP)
    color = c["color"]
    # focal: §3
    if color == ACC:
        d.tone(x, TOP_Y, CARD_W, CARD_H, ACC, 6, "16", 1.4)
    else:
        d.tone(x, TOP_Y, CARD_W, CARD_H, color, 6, "0E", 1.0)
    
    # 절 헤더
    d.t(x + CARD_W // 2, TOP_Y + 28, c["sec"], 14, color, KR, "middle", 600)
    d.line(x + 16, TOP_Y + 42, x + CARD_W - 16, TOP_Y + 42, RULE, 0.8)
    
    # 핵심어 1, 2
    d.t(x + CARD_W // 2, TOP_Y + 68, c["kw1"], 13, INK, KR, "middle", 500)
    d.t(x + CARD_W // 2, TOP_Y + 92, c["kw2"], 13, MUTED, KR, "middle")

    # 연결 화살표 (다음 칸으로)
    if i < len(cards) - 1:
        arr_x1 = x + CARD_W + 3
        arr_x2 = arr_x1 + GAP - 6
        mid_y = TOP_Y + CARD_H // 2
        d.arrow([(arr_x1, mid_y), (arr_x2, mid_y)], MUTED, "ar", 1.3)

# ── 범례 ─────────────────────────────────────────────────────────────────
LEG_Y = TOP_Y + CARD_H + 22
d.legend(LEG_Y, [
    ("보안 전제", BAD),
    ("계층 추상화", INFO),
    ("실행 메커니즘", ACC),
    ("선택 기준", OK),
])

d.save("30-01.image-builder.svg")
print("ok gen-30-01.image-builder")
