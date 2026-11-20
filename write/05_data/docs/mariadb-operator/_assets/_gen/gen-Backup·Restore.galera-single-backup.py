# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""Galera 단일 노드 백업 원칙과 비복제 테이블 예외 처리 도식.

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
    "GALERA CLUSTER · SINGLE NODE BACKUP ARCHITECTURE",
    "Galera 단일 노드 백업 원칙과 비복제 테이블 예외 처리",
    "동기 복제 데이터 동일성에 기반한 단일 백업과 MyISAM 및 wsrep 시스템 테이블 예외 제어",
    lead="노드 하나의 백업이 클러스터 스냅샷이 되는 이유와 Galera 덤프에서 빼는 세 가지"
)

# ── 상단 3개 노드 클러스터 카드 배치 ──────────────────────────────────
NODE_Y = 104
NODE_H = 168
NODE_W = 280
NODE_GAP = 28
X0 = 28

NODES = [
    {
        "role": "BACKUP TARGET NODE",
        "name": "galera-0 (단일 백업 대상)",
        "sub": "MariaDB 수동 절차 기준",
        "items": [
            "wsrep_desync=ON 복제 적용 멈춤",
            "mariadb-backup 실행",
            "OFF 로 되돌린 뒤 IST 로 따라잡기",
        ],
        "tone": ACC,
        "focal": True,  # FOCAL 1곳 (백업 대상 노드)
    },
    {
        "role": "NORMAL TRAFFIC NODE",
        "name": "galera-1 (서비스 노드)",
        "sub": "클러스터 쿼럼 유지",
        "items": [
            "백업 작업을 맡지 않음",
            "정상 애플리케이션 쿼리 처리",
            "동기식 인증 복제 유지",
        ],
        "tone": INFO,
        "focal": False,
    },
    {
        "role": "NORMAL TRAFFIC NODE",
        "name": "galera-2 (서비스 노드)",
        "sub": "클러스터 쿼럼 유지",
        "items": [
            "백업 작업을 맡지 않음",
            "정상 애플리케이션 쿼리 처리",
            "Primary Component 과반 유지",
        ],
        "tone": INFO,
        "focal": False,
    },
]

for i, nd in enumerate(NODES):
    cx = X0 + i * (NODE_W + NODE_GAP)
    if nd["focal"]:
        d.tone(cx, NODE_Y, NODE_W, NODE_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.tone(cx, NODE_Y, NODE_W, NODE_H, nd["tone"], r=8, op="10", sw=1.0)

    # 상단 뱃지
    d.t(cx + NODE_W // 2, NODE_Y + 24, nd["role"], 10, nd["tone"], MONO, "middle", 600)
    d.t(cx + NODE_W // 2, NODE_Y + 48, nd["name"], 13, INK, KR, "middle", 600)
    d.t(cx + NODE_W // 2, NODE_Y + 68, nd["sub"], 11, SOFT, KR, "middle")

    # 구분선
    d.line(cx + 12, NODE_Y + 80, cx + NODE_W - 12, NODE_Y + 80, RULE, 0.8)

    # 항목 목록
    for j, it in enumerate(nd["items"]):
        iy = NODE_Y + 104 + j * 20
        d.t(cx + NODE_W // 2, iy, it, 11, MUTED, KR, "middle")

# 노드 간 복제 동기화 연결선
y_rep = NODE_Y + NODE_H // 2
d.arrow([(X0 + NODE_W + 4, y_rep), (X0 + NODE_W + NODE_GAP - 4, y_rep)], SOFT, "ar", 1.2)
d.arrow([(X0 + 2 * NODE_W + NODE_GAP + 4, y_rep), (X0 + 2 * NODE_W + 2 * NODE_GAP - 4, y_rep)], SOFT, "ar", 1.2)


# ── 하단 세 가지 핵심 예외 처리 구역 ────────────────────────────────────
ZONE_Y = 296
ZONE_H = 104
ZONE_W = 904
ZONE_X = 28

d.box(ZONE_X, ZONE_Y, ZONE_W, ZONE_H, PAPER2, RULE, 0.8, r=8)

# 1) mysql.global_priv (MyISAM 비복제)
B1_W = 276
B1_X = ZONE_X + 16
d.tone(B1_X, ZONE_Y + 14, B1_W, 76, BAD, r=6, op="12", sw=1.2)
d.t(B1_X + 16, ZONE_Y + 36, "mysql.global_priv 예외", 13, BAD, KR, "start", 600)
d.t(B1_X + 16, ZONE_Y + 54, "MyISAM 비복제 테이블 유실 방지", 11, INK, KR, "start")
d.t(B1_X + 16, ZONE_Y + 72, "ignoreGlobalPriv 로 덤프 제외", 11, MUTED, KR, "start")

# 2) mysql.wsrep_* (런타임 복제 테이블)
B2_W = 276
B2_X = B1_X + B1_W + 20
d.tone(B2_X, ZONE_Y + 14, B2_W, 76, WARN, r=6, op="12", sw=1.2)
d.t(B2_X + 16, ZONE_Y + 36, "mysql.wsrep_* 예외", 13, WARN, KR, "start", 600)
d.t(B2_X + 16, ZONE_Y + 54, "복원 때 DROP 거부(ERROR 1142) 회피", 11, INK, KR, "start")
d.t(B2_X + 16, ZONE_Y + 72, "--ignore-table 로 덤프에서 자동 제외", 11, MUTED, KR, "start")

# 3) LOCK TABLES 차단
B3_W = 276
B3_X = B2_X + B2_W + 20
d.tone(B3_X, ZONE_Y + 14, B3_W, 76, OK, r=6, op="12", sw=1.2)
d.t(B3_X + 16, ZONE_Y + 36, "LOCK TABLES 호환성", 13, OK, KR, "start", 600)
d.t(B3_X + 16, ZONE_Y + 54, "Galera 와 호환되지 않는 구문", 11, INK, KR, "start")
d.t(B3_X + 16, ZONE_Y + 72, "dump 시 --skip-add-locks 주입", 11, MUTED, KR, "start")

# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 424
d.legend(LEGEND_Y, [("단일 백업 대상 노드", ACC), ("정상 서비스 노드", INFO), ("인증 테이블 위험 예방", BAD), ("클러스터 테이블 보호", WARN), ("호환성 옵션", OK)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "Backup·Restore.galera-single-backup.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
