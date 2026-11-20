# -*- coding: utf-8 -*-
# 타입 스펙: type-layers
"""타임아웃 계층 비교와 maxLifetime 설정 기준 도식.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다 (writing-method Diagram Design 계약).
좌표와 간격은 모두 4의 배수로 산출한다.
다크 스킨 토큰과 1곳의 focal 포인트를 적용한다.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 480

d = D(
    W,
    H,
    "TIMEOUT HIERARCHY · RETIREMENT STRATEGY",
    "타임아웃 계층 비교와 maxLifetime 설정 기준",
    "DB 서버, OS 커널, 중간 네트워크 장비, 풀 수명 설정의 상대적 크기와 단축 권장선",
    lead="중간 네트워크 장비의 유휴 한도(350초)보다 maxLifetime을 짧게 두어 연결 단절을 사전에 차단"
)

# 4개 계층 카드/바 배치
CARD_X = 36
CARD_W = 888
CARD_H = 72
CARD_GAP = 16
Y0 = 100

LAYERS = [
    {
        "tier": "TIER 1 · DATABASE SERVER",
        "title": "데이터베이스 서버 유휴 타임아웃",
        "time": "28,800초 (8시간) / PostgreSQL 은 0=끔",
        "details": "MySQL·MariaDB wait_timeout (기본 28,800초) · PostgreSQL idle_session_timeout (14+)",
        "role": "기본값으로는 가장 긴 한도",
        "c": INFO,
        "focal": False,
    },
    {
        "tier": "TIER 2 · OS KERNEL",
        "title": "리눅스 커널 TCP keepalive",
        "time": "7,200초 (2시간)",
        "details": "tcp_keepalive_time=7200 · tcp_keepalive_intvl=75 · tcp_keepalive_probes=9",
        "role": "기본값은 장비 한도보다 길어 예방 못 함 (낮추면 가능)",
        "c": WARN,
        "focal": False,
    },
    {
        "tier": "TIER 3 · NETWORK INFRASTRUCTURE",
        "title": "중간 네트워크 장비 유휴 타임아웃 (인프라 병목 한계)",
        "time": "350초 (AWS NLB TCP 기본, 60~6,000초)",
        "details": "AWS NLB 연결 추적 · 방화벽·NAT 은 제품과 설정마다 다름",
        "role": "알림 없이 추적을 끝내는 실질적 기준선",
        "c": BAD,
        "focal": False,
    },
    {
        "tier": "TIER 4 · CONNECTION POOL (HIKARICP)",
        "title": "HikariCP maxLifetime 및 keepaliveTime 권장 배치",
        "time": "maxLifetime 300초(예) · keepalive 120초",
        "details": "인프라 한도보다 짧은 수명 (지터로 최대 25% 더 짧아짐) · 유휴 연결에 주기적 L7 핑",
        "role": "장비 만료 전 조용한 자체 교체와 conntrack 타이머 지속 갱신 달성",
        "c": ACC,
        "focal": True,  # FOCAL 1곳
    },
]

for i, ly in enumerate(LAYERS):
    cy = Y0 + i * (CARD_H + CARD_GAP)
    if ly["focal"]:
        d.tone(CARD_X, cy, CARD_W, CARD_H, ACC, r=8, op="18", sw=1.6)
    else:
        d.tone(CARD_X, cy, CARD_W, CARD_H, ly["c"], r=8, op="10", sw=1.0)

    # 좌측 티어 뱃지 및 타이틀
    d.t(CARD_X + 16, cy + 22, ly["tier"], 10, ly["c"], MONO, "start", 600)
    d.t(CARD_X + 16, cy + 46, ly["title"], 14, INK, KR, "start", 600)
    d.t(CARD_X + 16, cy + 62, ly["details"], 11, MUTED, KR, "start")

    # 우측 시간 수치 박스
    time_box_w = 340
    time_box_x = CARD_X + CARD_W - time_box_w - 16
    d.box(time_box_x, cy + 12, time_box_w, CARD_H - 24, PAPER, RULE, 0.8, r=6)
    d.t(time_box_x + time_box_w // 2, cy + 32, ly["time"], 12, ly["c"], MONO, "middle", 600)
    d.t(time_box_x + time_box_w // 2, cy + 48, ly["role"], 10, SOFT, KR, "middle")

# 범례
d.legend(452, [
    ("DB 상한 기준선", INFO),
    ("커널 기본 장기 설정", WARN),
    ("인프라 최소 병목 (위험선)", BAD),
    ("풀 안전 권장선 (Focal)", ACC),
])

out_svg = pathlib.Path(__file__).resolve().parent.parent / "01-03.wait_timeout·idle timeout·TCP keepalive.timeout-hierarchy.svg"
d.save(str(out_svg))
print(f"Generated: {out_svg}")
