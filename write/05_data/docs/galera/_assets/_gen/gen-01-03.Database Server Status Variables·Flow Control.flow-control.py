# -*- coding: utf-8 -*-
# 타입 스펙: type-process
"""수신 큐 임계값과 흐름 제어 일시 정지 및 재개 순환 도식.

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
    "GALERA FLOW CONTROL · FEEDBACK CYCLE",
    "수신 큐 임계값과 흐름 제어 일시 정지 및 재개 순환",
    "저속 노드의 수신 큐 초과로 인한 클러스터 쓰기 중단과 앱플라이어 소화 후 정상화 순서",
    lead="gcs.fc_limit 상한 도달 시 PAUSE 전파와 fc_factor 하한 도달 시 RESUME 재개 메커니즘"
)

# ── 단계 카드 5단계 배치 (가로 방향 프로세스) ─────────────────────────
CARD_Y = 104
CARD_H = 168
CARD_W = 160
CARD_GAP = 28
X0 = 36

STEPS = [
    {
        "num": "STEP 1",
        "title": "트랜잭션 복제",
        "sub": "수신 큐 적재",
        "items": ["쓰기 집합 수신", "로컬 큐 버퍼링", "정상 순차 처리"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 2",
        "title": "임계값 초과",
        "sub": "상한선 도달",
        "items": ["수신 큐 누적 증가", "gcs.fc_limit 초과", "저속 노드 정체"],
        "tone": WARN,
        "focal": False,
    },
    {
        "num": "STEP 3",
        "title": "일시 정지 전파",
        "sub": "FC_PAUSE 신호",
        "items": ["전 노드 브로드캐스트", "신규 쓰기 일시 중단", "fc_sent 카운트 증가"],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳: 흐름 제어 발동
    },
    {
        "num": "STEP 4",
        "title": "백로그 소화",
        "sub": "앱플라이어 반영",
        "items": ["큐 대기 쓰기 반영", "스레드 병렬 적용", "수신 큐 크기 감소"],
        "tone": INFO,
        "focal": False,
    },
    {
        "num": "STEP 5",
        "title": "복제 정상 재개",
        "sub": "FC_RESUME 전파",
        "items": ["하한 비율 도달", "재개 신호 전송", "전체 쓰기 정상화"],
        "tone": OK,
        "focal": False,
    },
]

for i, st in enumerate(STEPS):
    cx = X0 + i * (CARD_W + CARD_GAP)
    
    # 카드 외곽
    if st["focal"]:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.tone(cx, CARD_Y, CARD_W, CARD_H, st["tone"], r=8, op="10", sw=1.0)
    
    # 상단 단계 뱃지
    d.t(cx + CARD_W // 2, CARD_Y + 24, st["num"], 10, st["tone"], MONO, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 48, st["title"], 13, INK, KR, "middle", 600)
    d.t(cx + CARD_W // 2, CARD_Y + 68, st["sub"], 11, SOFT, KR, "middle")

    # 구분선
    d.line(cx + 12, CARD_Y + 80, cx + CARD_W - 12, CARD_Y + 80, RULE, 0.8)

    # 항목 불릿
    for j, it in enumerate(st["items"]):
        iy = CARD_Y + 104 + j * 20
        d.t(cx + CARD_W // 2, iy, it, 11, MUTED, KR, "middle")

    # 단계 간 연결 화살표 (수평 직선)
    if i < len(STEPS) - 1:
        ax1 = cx + CARD_W + 4
        ax2 = ax1 + CARD_GAP - 8
        ay = CARD_Y + 84
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.4)

# ── 하단 피드백 루프 (Step 5 → Step 1 정상 주기 복귀) ───────────────
LOOP_Y = 332
X_START = X0 + 4 * (CARD_W + CARD_GAP) + CARD_W // 2  # 788 + 80 = 868
X_END = X0 + CARD_W // 2                             # 36 + 80 = 116
CHIP_X1 = 372
CHIP_X2 = 588

# ㄷ자 직각 연결 경로 (텍스트 칩 구간을 비워 글자-선 겹침 방지)
d.line(X_START, CARD_Y + CARD_H + 8, X_START, LOOP_Y, OK, 1.4)
d.line(X_START, LOOP_Y, CHIP_X2, LOOP_Y, OK, 1.4)
d.arrow([(CHIP_X1, LOOP_Y), (X_END, LOOP_Y), (X_END, CARD_Y + CARD_H + 16)], OK, "ok", 1.4)

# 피드백 안내 칩
d.chip(W // 2, LOOP_Y, "대기열 정상화 후 복제 파이프라인 재개", OK, 11)

# 하단 범례 (Y=424, H=480)
d.legend(424, [
    ("정상 복제 단계", INFO),
    ("임계 초과 감지", WARN),
    ("흐름 제어 일시 정지 (FOCAL)", ACC),
    ("해제 및 재개", OK)
])

# 파일 저장
out_path = pathlib.Path(__file__).resolve().parent.parent / "01-03.Database Server Status Variables·Flow Control.flow-control.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
