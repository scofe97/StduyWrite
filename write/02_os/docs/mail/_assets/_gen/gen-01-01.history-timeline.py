# 사실 출처: RFC 561, RFC 733, RFC 821, RFC 822, RFC 973, RFC 974, RFC 1425, RFC 1869, RFC 2045, RFC 2821, RFC 2822, RFC 5321, RFC 5322, Internet Hall of Fame
# 타입 스펙: type-timeline
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 560
d = D(
    W, H,
    "MAIL SYSTEM THEORY · 01 HISTORY TIMELINE",
    "인터넷 메일 40년 표준의 진화 (1971~2008)",
    "전달 규약(SMTP)과 메시지 형식(IMF), DNS 라우팅이 세 갈래로 맞물려 발전한 연표",
    "1971년 @ 기호 도입에서 1982년 규약 분리, 1986년 MX 도입, 2008년 현행 RFC 5321·5322 정립까지"
)

# 세 갈래 트랙 기준선 (Y 좌표)
Y_SMTP = 164  # 전달 규약 (SMTP)
Y_IMF  = 300  # 메시지 형식 (IMF)
Y_DNS  = 436  # DNS 및 라우팅

# 트랙 헤더 (좌측 뱃지)
def draw_track_header(y, title, code, color):
    d.box(16, y - 24, 112, 48, PAPER2, color, 1.2, 6)
    d.t(72, y - 6, title, 13, INK, KR, "middle", 600)
    d.t(72, y + 14, code, 11, color, MONO, "middle", 600)

draw_track_header(Y_SMTP, "전달 규약", "SMTP", OK)
draw_track_header(Y_IMF,  "메시지 형식", "IMF", INFO)
draw_track_header(Y_DNS,  "DNS · 경로", "ROUTING", WARN)

# 트랙 수평 기준선
d.line(140, Y_SMTP, 940, Y_SMTP, RULE, 1.0)
d.line(140, Y_IMF,  940, Y_IMF,  RULE, 1.0)
d.line(140, Y_DNS,  940, Y_DNS,  RULE, 1.0)

# 세로 동기화 가이드선 (1982, 2001, 2008)
for sync_x, year_lbl in ((444, "1982"), (780, "2001"), (888, "2008")):
    d.line(sync_x, Y_SMTP - 58, sync_x, Y_DNS + 58, RULE, 0.8, dash="3 3")
    d.t(sync_x, Y_SMTP - 64, f"{year_lbl}년 동시 정립", 11, SOFT, KR, "middle")

# 사건 데이터: (x, y, 연도, RFC/이름, 설명, 색상, focal 여부, 텍스트 상단/하단)
events = [
    # 1. 전달 규약 (Y_SMTP = 164)
    (212, Y_SMTP, "1971", "SNDMSG", "CPYNET 결합 전송", OK, False, True),
    (444, Y_SMTP, "1982", "RFC 821", "SMTP 표준 제정", OK, False, True),
    (644, Y_SMTP, "1995", "RFC 1869", "ESMTP 확장 개정", OK, False, False),
    (780, Y_SMTP, "2001", "RFC 2821", "SMTP 통합 갱신", OK, False, True),
    (888, Y_SMTP, "2008", "RFC 5321", "현행 SMTP 핵심 규격", ACC, True, False),

    # 2. 메시지 형식 (Y_IMF = 300)
    (260, Y_IMF, "1973", "RFC 561", "헤더 문법 표준화", INFO, False, True),
    (348, Y_IMF, "1977", "RFC 733", "텍스트 메시지 규격", INFO, False, False),
    (444, Y_IMF, "1982", "RFC 822", "IMF 표준 형식 제정", INFO, False, True),
    (684, Y_IMF, "1996", "RFC 2045", "MIME 멀티미디어", INFO, False, False),
    (780, Y_IMF, "2001", "RFC 2822", "IMF 통합 갱신", INFO, False, True),
    (888, Y_IMF, "2008", "RFC 5322", "현행 IMF 핵심 규격", INFO, False, False),

    # 3. DNS · 라우팅 (Y_DNS = 436)
    (212, Y_DNS, "1971", "@ 기호", "user@host 주소", WARN, False, True),
    (444, Y_DNS, "1982", "소스 라우트", "RFC 821 경로 규정", WARN, False, False),
    (524, Y_DNS, "1986", "RFC 974", "MX 라우팅 규칙", WARN, False, True),
]

for x, y, year, title, sub, color, focal, is_top in events:
    r = 6 if focal else 4
    fill_col = color if focal else PAPER
    d.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill_col}" stroke="{color}" stroke-width="1.4"/>')

    # 카드 너비/높이
    bw = 136 if focal else 128
    bh = 44

    if is_top:
        by = y - bh - 14
        d.line(x, y - r, x, by + bh, color if focal else RULE, 0.8)
    else:
        by = y + 14
        d.line(x, y + r, x, by, color if focal else RULE, 0.8)

    bx = x - bw // 2
    if focal:
        d.tone(bx, by, bw, bh, color, r=4, op="20", sw=1.4)
        d.t(x, by + 16, f"{year} · {title}", 11, color, MONO, "middle", 600)
        d.t(x, by + 34, sub, 13, INK, KR, "middle", 600)
    else:
        d.box(bx, by, bw, bh, PAPER2, RULE, 0.9, 4)
        d.t(x, by + 16, f"{year} · {title}", 11, color, MONO, "middle", 600)
        d.t(x, by + 34, sub, 13, INK, KR, "middle")

# 범례
d.legend(H - 44, [
    ("전달 규약 (SMTP 계열)", OK),
    ("메시지 형식 (IMF 계열)", INFO),
    ("DNS 및 라우팅 규격", WARN),
    ("현행 표준 전환점", ACC),
])

out = Path(__file__).parent.parent / "01-01.history-timeline.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
