# -*- coding: utf-8 -*-
# 타입 스펙: type-data-flow
"""GCache 링 버퍼 구조와 노드 이탈 시간에 따른 상태 전송 분기 도식.

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
    "GALERA CACHE · WRITE-SET RING BUFFER",
    "GCache 링 버퍼 구조와 노드 이탈 시간에 따른 전송 분기",
    "고정 크기 캐시의 순환 덮어쓰기와, Joiner 가 필요한 이력이 밀려났을 때의 SST 전환",
    lead="GCache 에 남은 seqno 범위와 노드 이탈 허용 시간의 관계"
)

X0 = 36
Y0 = 104

# ── 중앙 GCache 링 버퍼 시각화 (가로 선형 순환 슬롯) ──────────────────
BUFFER_ZONE_Y = Y0
BUFFER_ZONE_H = 148
BUFFER_ZONE_W = 888

d.box(X0, BUFFER_ZONE_Y, BUFFER_ZONE_W, BUFFER_ZONE_H, PAPER2, RULE, 0.8, r=8)

# 상단 제목 및 변수 태그
d.t(X0 + 20, BUFFER_ZONE_Y + 28, "Donor 노드의 GCache 링 버퍼 (galera.cache)", 13, INK, KR, "start", 600)
d.tone(X0 + 380, BUFFER_ZONE_Y + 14, 168, 22, INFO, r=4, op="14", sw=0.8)
d.t(X0 + 464, BUFFER_ZONE_Y + 29, "gcache.size = 고정 용량", 11, INFO, MONO, "middle")

# 링 버퍼 슬롯들 (과거 누락 구간 2칸, 유효 보존 구간 4칸, 최신 유입 1칸)
SLOT_Y = BUFFER_ZONE_Y + 52
SLOT_H = 56
SLOT_W = 108
SLOT_GAP = 12
SLOT_START_X = X0 + 24

# 1~2 슬롯: 이미 덮어써져 사라진 seqno 구역 (BAD) - FOCAL 1곳!
d.tone(SLOT_START_X, SLOT_Y, SLOT_W * 2 + SLOT_GAP, SLOT_H, BAD, r=6, op="14", sw=1.4)
d.t(SLOT_START_X + (SLOT_W * 2 + SLOT_GAP) // 2, SLOT_Y + 24, "덮어써진 유실 구간", 11, BAD, KR, "middle", 600)
d.t(SLOT_START_X + (SLOT_W * 2 + SLOT_GAP) // 2, SLOT_Y + 42, "seqno 1000 이하", 11, SOFT, MONO, "middle")

# 3~6 슬롯: 캐시에 보존 중인 유효 seqno 구역 (ACC / INFO)
VALID_X = SLOT_START_X + SLOT_W * 2 + SLOT_GAP + 16
VALID_W = SLOT_W * 4 + SLOT_GAP * 3
d.tone(VALID_X, SLOT_Y, VALID_W, SLOT_H, ACC, r=6, op="16", sw=1.4)
d.t(VALID_X + 24, SLOT_Y + 22, "가장 오래된 seqno: 1001", 11, ACC, MONO, "start", 600)
d.t(VALID_X + VALID_W // 2, SLOT_Y + 36, "현재 GCache 유효 보존 범위 (IST 공급 가능)", 12, INK, KR, "middle", 600)
d.t(VALID_X + VALID_W - 24, SLOT_Y + 22, "최신 seqno: 2500", 11, OK, MONO, "end", 600)

# 경계 라벨
d.t(VALID_X, BUFFER_ZONE_Y + 128, "▲ 캐시 유효 시작점", 11, ACC, KR, "start")
d.t(VALID_X + VALID_W, BUFFER_ZONE_Y + 128, "▲ 최신 트랜잭션", 11, OK, KR, "end")

# 7 슬롯: 새 트랜잭션 유입 방향 (OK)
INFLOW_X = VALID_X + VALID_W + 16
INFLOW_W = 120
d.tone(INFLOW_X, SLOT_Y, INFLOW_W, SLOT_H, OK, r=6, op="10", sw=1.0)
d.t(INFLOW_X + INFLOW_W // 2, SLOT_Y + 24, "신규 트랜잭션", 11, OK, KR, "middle", 600)
d.t(INFLOW_X + INFLOW_W // 2, SLOT_Y + 42, "순환 덮어쓰기 유입", 11, SOFT, KR, "middle")


# ── 하단 구역: 두 Joiner 노드의 대조 판정 ────────────────────────────
BOT_Y = 272
BOT_H = 136
BOT_W = 888

d.box(X0, BOT_Y, BOT_W, BOT_H, PAPER2, RULE, 0.8, r=8)

# 케이스 A: 단기 이탈 노드 (IST 성공)
CASE_A_W = 416
CASE_A_X = X0 + 16
d.tone(CASE_A_X, BOT_Y + 14, CASE_A_W, 108, OK, r=6, op="12", sw=1.2)
d.t(CASE_A_X + 20, BOT_Y + 38, "케이스 A: 단기 이탈 노드 (Joiner A)", 13, OK, KR, "start", 600)
d.t(CASE_A_X + 20, BOT_Y + 60, "마지막 seqno: 1200 (다음 1201 이 캐시에 있음)", 11, MONO, INK, "start")
d.t(CASE_A_X + 20, BOT_Y + 80, "판정: GCache 범위 내 존재 → IST (증분 전송) 수행", 12, OK, KR, "start", 600)
d.t(CASE_A_X + 20, BOT_Y + 98, "결과: Donor 잠금 없이 빠진 쓰기 집합만 받아 동기화", 11, MUTED, KR, "start")

# 케이스 B: 장기 이탈 또는 쓰기 과부하 노드 (SST 강제)
CASE_B_W = 416
CASE_B_X = CASE_A_X + CASE_A_W + 24
d.tone(CASE_B_X, BOT_Y + 14, CASE_B_W, 108, BAD, r=6, op="12", sw=1.2)
d.t(CASE_B_X + 20, BOT_Y + 38, "케이스 B: 장기 이탈 노드 (Joiner B)", 13, BAD, KR, "start", 600)
d.t(CASE_B_X + 20, BOT_Y + 60, "마지막 seqno: 850 (다음 851 이 이미 밀려남)", 11, MONO, INK, "start")
d.t(CASE_B_X + 20, BOT_Y + 80, "판정: 필요 write-set 유실 → SST (스냅샷 전송) 강제", 12, BAD, KR, "start", 600)
d.t(CASE_B_X + 20, BOT_Y + 98, "결과: 전체 데이터 복사 발생 및 Donor 리소스 부하", 11, MUTED, KR, "start")


# ── 범례 ─────────────────────────────────────────────────────────────
LEGEND_Y = 428
d.legend(LEGEND_Y, [("유효 캐시 범위 (IST)", ACC), ("정상 판정 및 유입", OK), ("이력 유실 및 SST 전환", BAD), ("시스템 설정", INFO)])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-02.State Transfers·Restarting the Cluster.gcache-ringbuffer.svg"
d.save(str(out_svg))
print(f"생성 완료: {out_svg}")
