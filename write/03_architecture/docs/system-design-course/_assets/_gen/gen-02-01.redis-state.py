# 타입 스펙: type-state — Redis 의 정상 모드에서 장애 감지(DB 폴백), 복구 중(미전달 N건 재동기화)을 거쳐 정상으로 복귀하는 유한 상태 머신. focal 은 재동기화 상태.
# 사실 출처: 요약 §4.4·§4.18, 조사 보고서 행 4·5·12, Redis Persistence·Sentinel 문서, 본문 2절 H3(Redis 정상 캐시 우선 읽기 → 마스터 크래시 및 타임아웃 감지 시 DB 수신함 폴백 → Redis 재가동 후 백그라운드 워커가 delivered IS NULL 미전달 N건 재동기화 → 완료 후 정상 복귀).
# Layout conventions: 3개 상태 박스 수평 배치(x=64·376·688, w=216, h=156), 직각 전이선(하단 ㄷ자 복귀선 y=404), W=960, H=540. 모든 좌표 4의 배수.
import pathlib
import sys

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import D, ACC, BAD, INFO, INK, KR, MONO, MUTED, OK, RULE, SOFT, WARN

W, H = 960, 540
d = D(
    W,
    H,
    "SYSTEM DESIGN COURSE · 02-01 §2",
    "Redis 정상·장애·복구 중의 상태 전이",
    "마스터 크래시 감지 후 DB 폴백, 재가동 후 미전달 데이터 재동기화 완료 뒤 정상 복귀하는 상태 머신.",
    "[정상] Redis 우선 읽기 → [장애] DB 폴백 → [복구 중] DB→Redis 미전달 N건 동기화 → [정상 복귀]",
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


# -------------------------------------------------------------
# 1. 상태 박스 렌더 함수
# -------------------------------------------------------------
def state_node(x, y, w, h, state_code, name, sub, lines, c, focal=False):
    d.tone(x, y, w, h, c, 8, "16" if focal else "08", 1.4 if focal else 1.0)
    d.chip(x + w // 2, y + 24, state_code, c, 11, 8)
    d.t(x + w // 2, y + 54, name, 15, INK, KR, "middle", 600)
    d.t(x + w // 2, y + 74, sub, 12, c if focal else MUTED, fam(sub), "middle")
    d.line(x + 16, y + 88, x + w - 16, y + 88, c if focal else RULE, 0.8)

    for i, line in enumerate(lines):
        d.t(x + 20, y + 108 + i * 20, line, 12, MUTED, fam(line), "start")


# -------------------------------------------------------------
# 2. 상태 노드 배치
# -------------------------------------------------------------
# 시작 점 (Start Dot)
d.o.append(f'<circle cx="20" cy="230" r="6" fill="{INK}"/>')
d.arrow([(28, 230), (60, 230)], INK, "ar", 1.4)

# State 1: 정상 모드
state_node(
    64,
    148,
    216,
    164,
    "NORMAL",
    "정상 모드",
    "Redis 캐시 우선 읽기",
    ["Redis 마스터 활성", "캐시 적중", "정본 DB 선영속 유지"],
    OK,
)

# State 2: 장애 폴백 모드
state_node(
    376,
    148,
    216,
    164,
    "FAILED",
    "장애 모드",
    "DB 수신함 폴백 읽기",
    ["마스터 노드 크래시", "Sentinel 페일오버 진행", "DB 수신함 폴백"],
    BAD,
)

# State 3: 복구 및 재동기화 모드 (Focal: ACC)
state_node(
    688,
    148,
    216,
    164,
    "RESYNCING",
    "재동기화 모드",
    "백그라운드 캐시 복원",
    ["신규 인스턴스 재가동", "미전달 데이터 조회", "미전달 N건 캐시 재동기화"],
    ACC,
    focal=True,
)


# -------------------------------------------------------------
# 3. 전이 화살표 (Transitions)
# -------------------------------------------------------------
# Transition 1: NORMAL -> FAILED
d.arrow([(280, 230), (372, 230)], BAD, "bad", 1.4)
d.t(328, 196, "마스터 크래시", 12, BAD, KR, "middle", 600)
d.t(328, 214, "[연결 타임아웃]", 11, MUTED, MONO, "middle")
d.t(328, 252, "/ DB 폴백 전환", 11, BAD, KR, "middle")

# Transition 2: FAILED -> RESYNCING
d.arrow([(592, 230), (684, 230)], WARN, "warn", 1.4)
d.t(640, 194, "Redis 재가동", 12, WARN, KR, "middle", 600)
d.t(640, 210, "[AOF 복원]", 11, MUTED, KR, "middle")
d.t(640, 224, "[최대 1초 누락]", 11, MUTED, KR, "middle")
d.t(640, 246, "/ 미전달 N건", 11, ACC, KR, "middle")
d.t(640, 260, "동기화", 11, ACC, KR, "middle")

# Transition 3: RESYNCING -> NORMAL (하단 ㄷ자 직각 루프백)
c3_x = 688 + 108  # 796
c1_x = 64 + 108  # 172
loop_y = 404

d.arrow(
    [(c3_x, 312), (c3_x, loop_y), (c1_x, loop_y), (c1_x, 316)],
    OK,
    "ok",
    1.4,
)
d.t(484, loop_y - 12, "재동기화 완료 [delivered IS NULL 0건]", 12, OK, KR, "middle", 600)
d.t(484, loop_y + 18, "/ Redis 우선 읽기 경로로 복귀", 12, MUTED, KR, "middle")


# -------------------------------------------------------------
# 4. 범례 (Legend)
# -------------------------------------------------------------
d.legend(
    H - 44,
    [
        ("정상 상태", OK),
        ("장애 감지", BAD),
        ("장애 복구", WARN),
        ("재동기화 (초점)", ACC),
    ],
)

out_path = str(ASSETS_DIR / "02-01.redis-state.svg")
d.save(out_path)
print(f"saved: {out_path}")
