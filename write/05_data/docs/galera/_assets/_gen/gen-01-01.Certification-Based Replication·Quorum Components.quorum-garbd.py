# -*- coding: utf-8 -*-
# 타입 스펙: type-architecture
"""2노드 클러스터의 쿼럼 붕괴와 Galera Arbitrator(garbd) 비교 도식.

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
    "GALERA CLUSTER · QUORUM & ARBITRATOR",
    "2노드 클러스터의 쿼럼 붕괴와 Galera Arbitrator 중재",
    "동일 가중치 2노드 장애 시 쿼럼 상실과 garbd 중재자 투표를 통한 과반수 유지 비교",
    lead="과반수 쿼럼 판정에서 짝수 노드 배치가 만드는 서비스 중단과 홀수 투표권 확보 원리"
)

# ── 상단 구역: Case 1 - 2노드 단독 (중재자 없음) ─────────────────────
CASE1_Y = 100
CASE1_H = 140
CASE1_W = 888
CASE1_X = 36

d.box(CASE1_X, CASE1_Y, CASE1_W, CASE1_H, PAPER2, RULE, 0.8, r=8)
d.t(CASE1_X + 20, CASE1_Y + 26, "사례 1: 2노드 클러스터 (총 2표 · 쿼럼은 1표 초과 필요)", 13, WARN, KR, "start", 600)

# 노드 1 (생존)
N1_X, N1_W = CASE1_X + 24, 180
d.tone(N1_X, CASE1_Y + 40, N1_W, 80, INFO, r=6, op="12", sw=1.2)
d.t(N1_X + N1_W // 2, CASE1_Y + 66, "노드 1 (DB 노드)", 13, INFO, KR, "middle", 600)
d.t(N1_X + N1_W // 2, CASE1_Y + 88, "투표 가중치: 1표", 12, INK, KR, "middle")
d.t(N1_X + N1_W // 2, CASE1_Y + 106, "정상 가동 중", 12, OK, KR, "middle")

# 노드 2 (장애 발생)
N2_X, N2_W = N1_X + N1_W + 24, 180
d.tone(N2_X, CASE1_Y + 40, N2_W, 80, BAD, r=6, op="12", sw=1.2)
d.t(N2_X + N2_W // 2, CASE1_Y + 66, "노드 2 (장애 노드)", 13, BAD, KR, "middle", 600)
d.t(N2_X + N2_W // 2, CASE1_Y + 88, "투표 가중치: 1표", 12, INK, KR, "middle")
d.t(N2_X + N2_W // 2, CASE1_Y + 106, "네트워크 단절 · 다운", 12, BAD, KR, "middle")

# 화살표 및 결과 판정
d.arrow([(N2_X + N2_W + 12, CASE1_Y + 80), (N2_X + N2_W + 48, CASE1_Y + 80)], MUTED, "ar", 1.2)

RES1_X, RES1_W = N2_X + N2_W + 60, 396
d.tone(RES1_X, CASE1_Y + 40, RES1_W, 80, BAD, r=6, op="12", sw=1.2)
d.t(RES1_X + 20, CASE1_Y + 66, "쿼럼 판정: 1표 / 2표 = 50% (과반수 미달)", 13, BAD, KR, "start", 600)
d.t(RES1_X + 20, CASE1_Y + 88, "남은 노드 1 도 Non-Primary 상태로 전환", 12, INK, KR, "start")
d.t(RES1_X + 20, CASE1_Y + 106, "스플릿 브레인 방지를 위해 클러스터 전체 쿼리 차단", 12, MUTED, KR, "start")


# ── 하단 구역: Case 2 - 2노드 + Galera Arbitrator (garbd) ─────────────
CASE2_Y = 256
CASE2_H = 144
CASE2_W = 888
CASE2_X = 36

d.box(CASE2_X, CASE2_Y, CASE2_W, CASE2_H, PAPER2, RULE, 0.8, r=8)
d.t(CASE2_X + 20, CASE2_Y + 26, "사례 2: 2노드 + Galera Arbitrator (총 3표 · 쿼럼은 1.5표 초과 필요)", 13, OK, KR, "start", 600)

# 노드 1 (생존 DB)
N3_X, N3_W = CASE2_X + 24, 156
d.tone(N3_X, CASE2_Y + 40, N3_W, 84, INFO, r=6, op="12", sw=1.2)
d.t(N3_X + N3_W // 2, CASE2_Y + 66, "노드 1 (DB)", 13, INFO, KR, "middle", 600)
d.t(N3_X + N3_W // 2, CASE2_Y + 88, "투표 가중치: 1표", 12, INK, KR, "middle")
d.t(N3_X + N3_W // 2, CASE2_Y + 108, "정상 가동", 12, OK, KR, "middle")

# 노드 2 (장애 DB)
N4_X, N4_W = N3_X + N3_W + 16, 156
d.tone(N4_X, CASE2_Y + 40, N4_W, 84, BAD, r=6, op="12", sw=1.2)
d.t(N4_X + N4_W // 2, CASE2_Y + 66, "노드 2 (DB)", 13, BAD, KR, "middle", 600)
d.t(N4_X + N4_W // 2, CASE2_Y + 88, "투표 가중치: 1표", 12, INK, KR, "middle")
d.t(N4_X + N4_W // 2, CASE2_Y + 108, "장애 발생", 12, BAD, KR, "middle")

# garbd (중재자) - FOCAL ACCENT!
ARB_X, ARB_W = N4_X + N4_W + 16, 168
d.tone(ARB_X, CASE2_Y + 40, ARB_W, 84, ACC, r=6, op="18", sw=1.6)
d.t(ARB_X + ARB_W // 2, CASE2_Y + 66, "garbd (중재자 데몬)", 13, ACC, KR, "middle", 600)
d.t(ARB_X + ARB_W // 2, CASE2_Y + 88, "투표 가중치: 1표", 12, INK, KR, "middle")
d.t(ARB_X + ARB_W // 2, CASE2_Y + 108, "DB 데이터 없이 투표 참여", 12, MUTED, KR, "middle")

# 화살표 및 결과 판정
d.arrow([(ARB_X + ARB_W + 12, CASE2_Y + 80), (ARB_X + ARB_W + 40, CASE2_Y + 80)], MUTED, "ar", 1.2)

RES2_X, RES2_W = ARB_X + ARB_W + 48, 304
d.tone(RES2_X, CASE2_Y + 40, RES2_W, 84, OK, r=6, op="12", sw=1.2)
d.t(RES2_X + 20, CASE2_Y + 66, "쿼럼 판정: 2표 / 3표 = 66.7%", 13, OK, KR, "start", 600)
d.t(RES2_X + 20, CASE2_Y + 88, "과반수 충족으로 Primary 유지", 12, INK, KR, "start")
d.t(RES2_X + 20, CASE2_Y + 108, "노드 1 단독 읽기·쓰기 서비스 지속", 12, MUTED, KR, "start")


# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 424
d.legend(LEGEND_Y, [("정상 DB 노드", INFO), ("중재자 garbd", ACC), ("쿼럼 유지", OK), ("장애 및 쿼럼 상실", BAD), ("조건부 경고", WARN)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-01.Certification-Based Replication·Quorum Components.quorum-garbd.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
