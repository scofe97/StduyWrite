# 사실 출처: Spring Security 7.1.1 CsrfFilter·LogoutFilter·ConcurrentSessionFilter·AuthorizationFilter
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 800
d = D(
    W, H,
    "FLOWCHART · SESSION FILTER CHAIN",
    "요청 하나가 필터를 지나며 갈리는 판단",
    "LogoutFilter와 ConcurrentSessionFilter가 요청을 검사해 204, 401, 통과로 분기하는 흐름",
    "Spring Security 필터 체인 순서와 세션 만료 검사 기준"
)

CX = 340          # 본선 중심 x
RX = 680          # 오른쪽 분기 결과 x
BW, BH = 250, 48  # 일반 단계 상자 너비·높이
DW, DH = 84, 32   # 마름모 반폭·반높이
ROWS = [116, 184, 256, 332, 408, 484, 560, 636, 712]


def oval(cx, cy, w, label, c):
    d.o.append(f'<rect x="{cx-w/2}" y="{cy-18}" width="{w}" height="36" rx="18" fill="{c}14" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, label, 12, INK, KR, "middle", 600)


def step(cx, cy, title, sub, c=RULE, w=BW):
    d.box(cx - w / 2, cy - BH / 2, w, BH, PAPER2, c, 1.1)
    d.t(cx, cy - 4, title, 12, INK, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR)


def diamond(cx, cy, label, c=MUTED):
    pts = f"{cx},{cy-DH} {cx+DW},{cy} {cx},{cy+DH} {cx-DW},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, label, 12, INK, KR, "middle", 600)


def result(cx, cy, code, sub, c, w=210):
    d.tone(cx - w / 2, cy - BH / 2, w, BH, c)
    d.t(cx, cy - 4, code, 12, c, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR)


def down(y1, y2, c=MUTED, label=None):
    d.arrow([(CX, y1), (CX, y2 - 2)], c, "ar", 1.4)
    if label:
        d.t(CX + 10, (y1 + y2) / 2 + 4, label, 12, MUTED, KR, "start")


# 0. 요청 도착
oval(CX, ROWS[0], 150, "요청 도착", INFO)
down(ROWS[0] + 18, ROWS[1] - BH / 2)

# 1. CsrfFilter
step(CX, ROWS[1], "CsrfFilter", "읽기 메서드 제외")
down(ROWS[1] + BH / 2, ROWS[2] - DH)

# 2. LogoutFilter 분기
diamond(CX, ROWS[2], "POST /api/my/logout?", INFO)
d.arrow([(CX + DW, ROWS[2]), (RX - 105 - 2, ROWS[2])], OK, "ok", 1.4)
d.t((CX + DW + RX - 105) / 2, ROWS[2] - 8, "일치", 12, OK, KR)
result(RX, ROWS[2], "204 No Content", "세션 무효화 · 쿠키 삭제", OK)
down(ROWS[2] + DH, ROWS[3] - DH, MUTED, "다른 URL")

# 3. ConcurrentSessionFilter: 세션 존재 여부
diamond(CX, ROWS[3], "세션 객체 존재?", WARN)
# 세션 없음 -> 우회 선 (LX 쪽으로)
LX = 90
d.path(f"M {CX-DW} {ROWS[3]} L {LX} {ROWS[3]} L {LX} {ROWS[7]} L {CX-BW/2-2} {ROWS[7]}", MUTED, 1.4, m="ar")
d.t((CX - DW + LX) / 2, ROWS[3] - 8, "없음", 12, MUTED, KR)
down(ROWS[3] + DH, ROWS[4] - DH, MUTED, "있음")

# 4. ConcurrentSessionFilter: SessionRegistry 등록 여부
diamond(CX, ROWS[4], "표에 등록됨?", WARN)
# 표에 없음 -> 우회 선 (LX + 28 쪽으로)
d.path(f"M {CX-DW} {ROWS[4]} L {LX+28} {ROWS[4]} L {LX+28} {ROWS[7]-20} L {CX-BW/2-2} {ROWS[7]-20}", MUTED, 1.4, m="ar")
d.t((CX - DW + LX + 28) / 2, ROWS[4] - 8, "미등록", 12, MUTED, KR)
down(ROWS[4] + DH, ROWS[5] - DH, MUTED, "등록됨")

# 5. ConcurrentSessionFilter: 만료 표시 여부 (focal 포인트: ACC)
diamond(CX, ROWS[5], "만료 표시됨?", ACC)
d.arrow([(CX + DW, ROWS[5]), (RX - 105 - 2, ROWS[5])], BAD, "bad", 1.4)
d.t((CX + DW + RX - 105) / 2, ROWS[5] - 8, "isExpired", 12, BAD, MONO)
result(RX, ROWS[5], "401 Unauthorized", "세션 무효화 · 필터 종료", BAD)
down(ROWS[5] + DH, ROWS[6] - BH / 2, OK, "정상")

# 6. 시각 갱신
step(CX, ROWS[6], "refreshLastRequest()", "마지막 요청 시각 갱신", OK)
down(ROWS[6] + BH / 2, ROWS[7] - BH / 2)

# 7. 인가 및 컨트롤러 전달
step(CX, ROWS[7], "AuthorizationFilter", "URL 인가(/api/admin/** 역할 등)")
down(ROWS[7] + BH / 2, ROWS[8] - 18)

# 8. 컨트롤러 도착
oval(CX, ROWS[8], 160, "컨트롤러 도착", OK)

d.legend(H - 44, [
    ("만료 판정 (핵심)", ACC),
    ("정상 통과 · 204", OK),
    ("조건 분기", WARN),
    ("차단 · 401", BAD),
    ("요청 · 시작", INFO),
])

out_path = Path(__file__).parent.parent / "02-02.filter-chain.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
