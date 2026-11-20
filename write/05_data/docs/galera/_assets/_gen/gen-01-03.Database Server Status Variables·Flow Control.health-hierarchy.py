# -*- coding: utf-8 -*-
# 타입 스펙: type-layers
"""상태 변수로 확인하는 클러스터 건강 진단 계층 도식.

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
    "GALERA MONITORING · DIAGNOSTIC HIERARCHY",
    "상태 변수로 확인하는 클러스터 건강 진단 계층",
    "쿼럼과 멤버십 확인부터 노드 상태 전이 및 복제 큐·흐름 제어 정체까지 4단계 점검 순서",
    lead="wsrep 상태 변수의 계층적 조회 순서와 진단 기준값"
)

# ── 레이어 4단 배치 (세로 누적 스택) ─────────────────────────────────
X0 = 64
W_LAYER = 848
LAYER_H = 68
LAYER_GAP = 12
Y0 = 104

LAYERS = [
    {
        "tag": "LEVEL 1",
        "name": "쿼럼 성립 여부",
        "var1": "wsrep_cluster_status",
        "var2": "",
        "norm": "Primary",
        "desc": "Primary Component 소속 검증 · 쿼럼 상실 시 트랜잭션 처리 중단",
        "tone": OK,
        "focal": False,
    },
    {
        "tag": "LEVEL 2",
        "name": "클러스터 구성원 수",
        "var1": "wsrep_cluster_size",
        "var2": "",
        "norm": "기대 노드 수 일치",
        "desc": "정상 동작 노드 대수 일치 확인 · 노드 이탈 및 분리 감지",
        "tone": INFO,
        "focal": False,
    },
    {
        "tag": "LEVEL 3",
        "name": "노드 동기화·준비",
        "var1": "wsrep_local_state_comment",
        "var2": "wsrep_ready",
        "norm": "Synced / ON",
        "desc": "동기화 완료 여부 · OFF 면 거의 모든 쿼리 거부",
        "tone": INFO,
        "focal": False,
    },
    {
        "tag": "LEVEL 4",
        "name": "복제 지연 및 흐름 제어",
        "var1": "wsrep_local_recv_queue_avg",
        "var2": "wsrep_flow_control_paused",
        "norm": "0.0 / 0.0",
        "desc": "수신 큐 적재 여부 및 쓰기 정지 비율 · 단일 저속 노드 병목 추적",
        "tone": ACC,
        "focal": True,  # FOCAL 1곳
    },
]

for i, ly in enumerate(LAYERS):
    ly_y = Y0 + i * (LAYER_H + LAYER_GAP)
    
    # 외곽 상자
    if ly["focal"]:
        d.tone(X0, ly_y, W_LAYER, LAYER_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.box(X0, ly_y, W_LAYER, LAYER_H, PAPER2, RULE, 0.8, r=8)
    
    # 1. 인덱스 태그 뱃지 (좌측)
    tag_color = ACC if ly["focal"] else ly["tone"]
    d.tone(X0 + 16, ly_y + 16, 72, 36, tag_color, r=4, op="18", sw=1.0)
    d.t(X0 + 52, ly_y + 38, ly["tag"], 11, tag_color, MONO, "middle", 600)
    
    # 2. 레이어 진단 명칭 및 대상 변수 (중앙 좌측)
    d.t(X0 + 104, ly_y + 26, ly["name"], 14, INK, KR, "start", 600)
    if ly["var2"]:
        d.t(X0 + 104, ly_y + 44, ly["var1"], 11, SOFT, MONO, "start")
        d.t(X0 + 104, ly_y + 58, ly["var2"], 11, SOFT, MONO, "start")
    else:
        d.t(X0 + 104, ly_y + 48, ly["var1"], 11, SOFT, MONO, "start")
    
    # 구분 점선
    d.line(X0 + 440, ly_y + 12, X0 + 440, ly_y + LAYER_H - 12, RULE, 0.8, dash="2,2")
    
    # 3. 정상 기준값 및 진단 목적 (우측)
    d.t(X0 + 460, ly_y + 28, f"기준: {ly['norm']}", 12, tag_color, KR, "start", 600)
    d.t(X0 + 460, ly_y + 48, ly["desc"], 11, MUTED, KR, "start")

# 좌측 검사 방향 화살표 및 안내 라벨 (x=36)
d.line(36, Y0 + 16, 36, Y0 + 3 * (LAYER_H + LAYER_GAP) + LAYER_H - 16, RULE, 1.2)
d.arrow([(36, Y0 + 16), (36, Y0 + 3 * (LAYER_H + LAYER_GAP) + LAYER_H - 8)], MUTED, "ar", 1.2)
d.t(36, Y0 - 12, "진단 순서", 11, SOFT, KR, "middle")

# 하단 범례 (Y=428, H=480, 여유 52px)
d.legend(428, [
    ("정상 기준 충족", OK),
    ("상태 확인 변수", INFO),
    ("병목 관측 지점 (FOCAL)", ACC)
])

# 파일 저장
out_path = pathlib.Path(__file__).resolve().parent.parent / "01-03.Database Server Status Variables·Flow Control.health-hierarchy.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
