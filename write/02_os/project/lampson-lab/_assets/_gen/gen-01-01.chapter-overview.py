# 01-01 학습 목표 뒤 전체 지도 — 절 넷이 고정 키에서 한 바퀴까지 간다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 국면 · 그 절이 주는 것)이
#           반복되고 화살표가 읽는 순서를 나른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "LAMPSON LAB · 01-01",
      "고정 키를 버리고 5분짜리 인증서를 쓴다 — 읽는 순서",
      "절 넷. 고정 키의 문제에서 시작해 인증서로 바꾸고, 남는 요청자 문제를 거쳐 접속 경로 한 바퀴로 닫힌다.",
      "세 번째 절이 이 편의 핵심이다 — 인증서를 짧게 만들면 문제가 CA 앞으로 옮겨 간다")

CW, CH, GAP, X0 = 404, 108, 24, 24
Y1, Y2 = 120, 252
cards = [
    ("§1", "문제 · 고정 키", "만료 없음 · 호스트마다 등록 · 누가인지 흐림"),
    ("§2", "해법 · SSH 인증서", "CA 서명 · 유효 기간 · principal"),
    ("§3", "남는 문제 · 누가 요청하는가", "토큰을 두면 또 하나의 고정 키가 된다"),
    ("§4", "한 바퀴 · uid 에서 세션까지", "SVID · X5C 토큰 · 인증서 · sshd"),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), (Y1 if i < 2 else Y2)

for i in range(3):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 4, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cy = Y1 + CH + 16
        d.path(f"M {x1 + CW / 2} {y1 + CH} V {cy} H {X0 + CW / 2} V {y2 - 4}", MUTED, 1.4, m="ar")

for i, (n, title, mark) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, y + 30, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 20, y + 58, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 84, mark, 12, MUTED, KR, "start")

d.t(24, 392, "다음 두 편이 이 질문의 답을 판다 — 신원은 프로세스에서, principal 은 CA 에서", 12, SOFT, KR, "start")
d.save("01-01.chapter-overview.svg")
