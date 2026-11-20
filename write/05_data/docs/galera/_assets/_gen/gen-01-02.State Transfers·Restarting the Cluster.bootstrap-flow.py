# -*- coding: utf-8 -*-
# 타입 스펙: type-process
"""전체 정지 뒤 안전한 첫 노드 선정 및 부트스트랩 순서 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
좌표와 간격은 모두 4의 배수로 산출한다.
다크 스킨 토큰과 1곳의 focal 포인트를 적용한다.
"""
import pathlib
import sys

# 상위 폴더의 dd.py 임포트
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 480

d = D(
    W,
    H,
    "CLUSTER CRASH RECOVERY · BOOTSTRAP WORKFLOW",
    "전체 정지 뒤 안전한 첫 노드 선정과 부트스트랩 절차",
    "grastate.dat 상태 확인부터 wsrep-recover seqno 복구 및 단일 노드 부트스트랩 순서",
    lead="최신 seqno 기반의 단일 노드 부트스트랩과 스플릿 브레인 방지 복구 흐름"
)

# ── 단계 카드 4단계 배치 ──────────────────────────────────────────────
CARD_Y = 104
CARD_H = 168
CARD_W = 196
CARD_GAP = 28
X0 = 36

STEPS = [
    {
        "num": "STEP 1",
        "title": "전체 정지 확인",
        "sub": "Primary 부재",
        "items": ["모든 노드 정지 확인", "합류할 Primary 없음", "수동 부트스트랩 필요"],
        "tone": BAD,
        "focal": False,
    },
    {
        "num": "STEP 2",
        "title": "상태 파일 점검",
        "sub": "grastate.dat 판정",
        "items": ["safe_to_bootstrap 확인", "비정상 시 wsrep-recover", "최고 seqno 노드 확정"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 3",
        "title": "단일 부트스트랩",
        "sub": "galera_new_cluster",
        "items": ["최신 노드 1대만 지정", "새 Primary 생성", "복수 실행 엄격 금지"],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳: 단일 노드 부트스트랩
    },
    {
        "num": "STEP 4",
        "title": "나머지 노드 합류",
        "sub": "일반 시작 명령",
        "items": ["systemctl start 호출", "새 Primary 에 연결", "IST 또는 SST 동기화"],
        "tone": OK,
        "focal": False,
    },
]

for i, st in enumerate(STEPS):
    cx = X0 + i * (CARD_W + CARD_GAP)
    if st["focal"]:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, st["tone"], r=8, op="10", sw=1.0)
    
    d.t(cx + CARD_W // 2, CARD_Y + 24, st["num"], 10, st["tone"], MONO, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 48, st["title"], 13, INK, KR, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 68, st["sub"], 11, SOFT, KR, "middle")

    d.line(cx + 12, CARD_Y + 80, cx + CARD_W - 12, CARD_Y + 80, RULE, 0.8)

    for j, it in enumerate(st["items"]):
        iy = CARD_Y + 104 + j * 20
        d.t(cx + CARD_W // 2, iy, it, 11, MUTED, KR, "middle")

    if i < len(STEPS) - 1:
        ax1 = cx + CARD_W + 4
        ax2 = cx + CARD_W + CARD_GAP - 4
        ay = CARD_Y + CARD_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)


# ── 하단 분기 상세 및 주의사항 구역 ──────────────────────────────────
ZONE_Y = 292
ZONE_H = 112
ZONE_W = 888

d.box(X0, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, 0.8, r=8)

# 좌측: safe_to_bootstrap 분기 상세
BRANCH_W = 416
BRANCH_X = X0 + 16
d.tone(BRANCH_X, ZONE_Y + 14, BRANCH_W, 84, INFO, r=6, op="12", sw=1.0)
d.t(BRANCH_X + 20, ZONE_Y + 36, "시작점 판정 기준 (grastate.dat)", 13, INFO, KR, "start", 600)
d.t(BRANCH_X + 20, ZONE_Y + 56, "정상 순차 종료: 마지막 종료 노드 safe_to_bootstrap=1", 11, INK, KR, "start")
d.t(BRANCH_X + 20, ZONE_Y + 74, "비정상 종료: 최대 seqno (-1 이면 wsrep-recover)", 11, MUTED, KR, "start")

# 우측: 다중 부트스트랩 금지 경고 (BAD)
WARN_W = 416
WARN_X = BRANCH_X + BRANCH_W + 24
d.tone(WARN_X, ZONE_Y + 14, WARN_W, 84, BAD, r=6, op="12", sw=1.2)
d.t(WARN_X + 20, ZONE_Y + 36, "금지: 복수 노드 동시 부트스트랩", 13, BAD, KR, "start", 600)
d.t(WARN_X + 20, ZONE_Y + 56, "두 노드에서 동시 실행 시 독립된 Primary Component 생성", 11, INK, KR, "start")
d.t(WARN_X + 20, ZONE_Y + 74, "데이터가 갈라진 두 클러스터(스플릿 브레인)", 11, BAD, KR, "start", 600)


# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 428
d.legend(LEGEND_Y, [("정상 단계 진행", OK), ("단일 부트스트랩 실행", ACC), ("판정 및 상태 점검", INFO), ("중단 및 위험 금지", BAD)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-02.State Transfers·Restarting the Cluster.bootstrap-flow.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
