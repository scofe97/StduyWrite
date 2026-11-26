# 사실 출처: Spring Security 7.1.1 ConcurrentSessionFilter·LogoutFilter·HttpSecurity.addFilterAfter()
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 768
d = D(
    W, H,
    "FLOWCHART · PAIRED TRACES · FILTER ORDER",
    "같은 로그아웃 요청이 두 순서에서 갈리는 지점",
    "만료 표시된 세션의 POST /api/my/logout 이 LogoutFilter 에서 끝나 204, 순서를 뒤집으면 ConcurrentSessionFilter 에서 끝나 401",
    "SecurityConfig 의 addFilterAfter(ConcurrentSessionFilter, LogoutFilter) 기준"
)

LX, RX = 260, 620
DW, DH = 132, 36
COL_W = 240


def diamond(cx, cy, name, cond, c):
    pts = f"{cx},{cy-DH} {cx+DW},{cy} {cx},{cy+DH} {cx-DW},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="{1.4 if c == ACC else 1.2}"/>')
    d.t(cx, cy - 3, name, 12, INK, MONO, "middle", 600)
    d.t(cx, cy + 14, cond, 12, MUTED, KR)


def step(cx, cy, title, sub, c=RULE):
    d.box(cx - COL_W / 2, cy - 26, COL_W, 52, PAPER2, c, 1.1)
    d.t(cx, cy - 4, title, 12, INK, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR)


def result(cx, cy, code, sub, c):
    d.tone(cx - COL_W / 2, cy - 26, COL_W, 52, c)
    d.t(cx, cy - 4, code, 12, c, MONO, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, KR)


def skipped(cx, cy, title):
    d.o.append(f'<rect x="{cx-COL_W/2}" y="{cy-26}" width="{COL_W}" height="52" rx="6" fill="none" stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    d.t(cx, cy - 4, title, 12, MUTED, MONO, "middle", 600)
    d.t(cx, cy + 14, "도달 안 함", 12, SOFT, KR)


def next_filter(cx, cy):
    d.box(cx - 48, cy - 26, 96, 52, PAPER2, RULE, 1.0)
    d.t(cx, cy + 4, "다음 필터로", 12, INK, KR, "middle", 600)


# 공통 요청
d.box(300, 100, 280, 56, PAPER2, RULE, 1.0)
d.t(440, 123, "POST /api/my/logout", 12, INK, MONO, "middle", 600)
d.t(440, 142, "쿠키 sid-B · 만료 표시됨", 12, MUTED, KR)
for cx in (LX, RX):
    d.arrow([(440, 156), (440, 176), (cx, 176), (cx, 198)], MUTED, "ar", 1.4)

# 열 머리
for cx, ttl, flow in ((LX, "실제 순서", "LogoutFilter → ConcurrentSessionFilter"),
                      (RX, "뒤집은 순서", "ConcurrentSessionFilter → LogoutFilter")):
    d.box(cx - 160, 198, 320, 48, PAPER2, RULE, 1.0)
    d.t(cx, 218, ttl, 13, INK, KR, "middle", 600)
    d.t(cx, 236, flow, 11, MUTED, MONO)
d.line(440, 184, 440, 672, RULE, 0.8, dash="4 4")

R1, R2, R3, R4 = 332, 448, 544, 640

# 왼쪽: 실제 순서
d.arrow([(LX, 246), (LX, R1 - DH - 2)], MUTED, "ar", 1.4)
diamond(LX, R1, "LogoutFilter", "로그아웃 URL 일치?", ACC)
d.arrow([(LX, R1 + DH), (LX, R2 - 28)], OK, "ok", 1.4)
d.t(LX + 10, (R1 + DH + R2 - 28) / 2 + 4, "일치", 12, OK, KR, "start")
step(LX, R2, "LogoutHandler", "세션 무효화 · 쿠키 삭제", OK)
d.arrow([(LX, R2 + 26), (LX, R3 - 28)], OK, "ok", 1.4)
result(LX, R3, "204 No Content", "여기서 응답 종료", OK)
d.arrow([(LX, R3 + 26), (LX, R4 - 28)], SOFT, "soft", 1.2, dash="4 4")
skipped(LX, R4, "ConcurrentSessionFilter")

# 왼쪽: 다른 URL 우회 분기
d.path(f"M {LX-DW} {R1} L 72 {R1} L 72 {R4-28}", SOFT, 1.2, m="soft", dash="4 4")
d.t(100, R1 - 8, "다른 URL", 12, SOFT, KR, "middle")
next_filter(72, R4)

# 오른쪽: 뒤집은 순서
d.arrow([(RX, 246), (RX, R1 - DH - 2)], MUTED, "ar", 1.4)
diamond(RX, R1, "ConcurrentSessionFilter", "만료 표시됨?", WARN)
d.arrow([(RX, R1 + DH), (RX, R2 - 28)], BAD, "bad", 1.4)
d.t(RX + 10, (R1 + DH + R2 - 28) / 2 + 4, "표시됨", 12, BAD, KR, "start")
step(RX, R2, "LogoutHandler", "세션 무효화", BAD)
d.arrow([(RX, R2 + 26), (RX, R3 - 28)], BAD, "bad", 1.4)
result(RX, R3, "401 Unauthorized", "여기서 응답 종료", BAD)
d.arrow([(RX, R3 + 26), (RX, R4 - 28)], SOFT, "soft", 1.2, dash="4 4")
skipped(RX, R4, "LogoutFilter")

# 오른쪽: 만료 표시 없음 우회 분기
d.path(f"M {RX+DW} {R1} L 808 {R1} L 808 {R4-28}", SOFT, 1.2, m="soft", dash="4 4")
d.t(780, R1 - 8, "표시 없음", 12, SOFT, KR, "middle")
next_filter(808, R4)

d.legend(H - 56, [
    ("갈린 지점 (핵심)", ACC),
    ("204 응답", OK),
    ("401 응답", BAD),
    ("조건 검사", WARN),
    ("도달 안 함", SOFT),
])

out_path = Path(__file__).parent.parent / "02-02.logout-order.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
