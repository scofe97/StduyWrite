# 타입 스펙: type-process — 팬아웃 서비스의 다섯 단계를 카드로 늘어놓고, 아래 칸에 같은 슬롯 네 줄을 반복해 친구 ID 가 넷에서 셋으로 줄고 게시물 ID 와 짝지어 피드 줄이 되는 값 이동을 보인다.
# 사실 출처: 단계 구조는 추출본 v2.txt 3076~3094행(그래프 DB → 사용자 캐시 설정 거르기 → 큐 → 작업자 → 피드 캐시에 <post_id, user_id>)·PDF 173쪽 그림. 글쓴이 7 · 게시물 9001 · 친구 12 · 31 · 55 · 88 · 55 의 음소거는 설명용 예시 값.
# Layout conventions: 카드 폭 160·높이 72, x stride 184(x=24 부터), 카드 y=100, 캡션 y=212, 값 칩 폭 112·높이 28, 줄 y=228 부터 stride 36. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, SOFT, KR, MONO

W, H = 960, 452
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 11-01 §4",
      "게시물 9001 은 친구 4 명 중 3 명의 피드에 한 줄씩 쌓인다",
      "글쓴이 7 의 친구 ID 12 · 31 · 55 · 88 을 그래프 DB 에서 받고, 사용자 설정이 55 를 걸러 3 명이 남으며, 큐와 작업자를 거쳐 피드 캐시에 (9001, 12) · (9001, 31) · (9001, 88) 세 줄이 쌓인다.",
      "글쓴이 7 · 게시물 9001 · 친구 4 명")

CW, CH, XS0, STRIDE = 160, 72, 24, 184
CY, CAPY, VY0, VS = 100, 212, 228, 36
CHW, CHH = 112, 28

CARDS = (
    ("1", "그래프 DB", "친구 ID 조회", "친구 4 명"),
    ("2", "사용자 캐시", "설정으로 거르기", "3 명 남음"),
    ("3", "메시지 큐", "게시물 ID 와 함께", "게시물 1 + 친구 3"),
    ("4", "팬아웃 작업자", "큐에서 꺼내기", "친구 3 명"),
    ("5", "피드 캐시", "친구마다 한 줄", "피드 3 줄"),
)
# 열마다 (줄 번호, 글자, 색, focal)
VALUES = (
    ((0, "12", INFO, False), (1, "31", INFO, False), (2, "55", INFO, False), (3, "88", INFO, False)),
    ((0, "12", OK, False), (1, "31", OK, False), (2, "55 제외", ACC, True), (3, "88", OK, False)),
    ((0, "post 9001", WARN, False), (1, "12", OK, False), (2, "31", OK, False), (3, "88", OK, False)),
    ((1, "12", OK, False), (2, "31", OK, False), (3, "88", OK, False)),
    ((1, "9001 · 12", WARN, False), (2, "9001 · 31", WARN, False), (3, "9001 · 88", WARN, False)),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


for i, (tag, title, sub, cap) in enumerate(CARDS):
    x = XS0 + STRIDE * i
    d.tone(x, CY, CW, CH, INFO, 6, "12", 1.0)
    d.t(x + 14, CY + 24, tag, 12, INFO, MONO, "start", 600)
    d.t(x + 14, CY + 46, title, 15, INK, KR, "start", 600)
    d.t(x + 14, CY + 64, sub, 13, MUTED, KR, "start")
    d.t(x + CW / 2, CAPY, cap, 13, SOFT, KR, "middle", 600)
    if i < 4:
        d.arrow([(x + CW + 2, CY + 36), (x + STRIDE - 6, CY + 36)], MUTED, "ar", 1.5)

for i, col in enumerate(VALUES):
    x = XS0 + STRIDE * i + (CW - CHW) // 2
    for row, txt, c, focal in col:
        y = VY0 + VS * row
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CHW}" height="{CHH}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + CHW / 2, y + 19, txt, 13, ACC, fam(txt), "middle", 600)
        else:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CHW}" height="{CHH}" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            d.t(x + CHW / 2, y + 19, txt, 13, c, fam(txt), "middle")

# 피드 캐시 열의 머리: 줄 하나가 post_id 와 user_id 한 쌍임을 칩 위에 적는다.
d.t(XS0 + STRIDE * 4 + CW / 2, VY0 + 18, "post_id · user_id", 11, SOFT, MONO, "middle")

d.legend(H - 56, [("친구 ID", INFO), ("남은 친구", OK), ("게시물", WARN), ("걸러진 친구", ACC)])
d.save("11-01.fanout-values.svg")
