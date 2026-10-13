# 타입 스펙: type-process — 조회 흐름의 네 저장소·응답 단계를 카드로 늘어놓고, 같은 게시물 칩을 단계마다 반복해 ID 한 줄이 객체 두 겹을 얻어 자라는 것을 칩 높이로 보인다.
# 사실 출처: 추출본 v2.txt 3095~3112행(피드 캐시에서 ID 목록 → 게시물 캐시·사용자 캐시에서 객체 → JSON)·3101행(미디어는 CDN)·PDF 174~175쪽 그림. user 12 · 게시물 9003 · 9001 · 글쓴이 41 · 7 은 설명용 예시 값.
# Layout conventions: 카드 폭 200·높이 72, x stride 232(x=24 부터), 카드 y=100, 캡션 y=196, 칩 폭 144(카드 안 x+28), 줄 y=212·304 stride 92, 칩 높이 28·52·76. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, SOFT, KR, MONO

W, H = 960, 500
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 11-01 §5",
      "피드 캐시의 ID 한 줄은 두 저장소를 거쳐 완성된 항목이 된다",
      "user 12 의 피드 캐시에는 게시물 ID 9003 · 9001 만 있고, 게시물 캐시에서 본문과 글쓴이 ID 를, 사용자 캐시에서 글쓴이 이름과 사진을 받아 JSON 두 건으로 돌려준다.",
      "user 12 가 GET /v1/me/feed 를 부른 뒤")

CW, CH, XS0, STRIDE = 200, 72, 24, 232
CY, CAPY = 100, 196
CHX, CHW = 28, 144
LANES = (212, 304)

CARDS = (
    ("뉴스 피드 캐시", "user 12 의 목록", "ID 2 개"),
    ("게시물 캐시", "객체 읽기", "객체 2 개"),
    ("사용자 캐시", "글쓴이 읽기", "글쓴이 2 명"),
    ("응답", "JSON 으로 반환", "항목 2 건"),
)
POSTS = ((9003, 41), (9001, 7))
# 단계마다 (줄 수, 색, focal)
STAGES = ((1, ACC, True), (2, WARN, False), (3, WARN, False), (3, OK, False))
LINE_H = 24


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


for i, (title, sub, cap) in enumerate(CARDS):
    x = XS0 + STRIDE * i
    d.tone(x, CY, CW, CH, INFO, 6, "12", 1.0)
    d.t(x + 14, CY + 32, title, 15, INK, KR, "start", 600)
    d.t(x + 14, CY + 56, sub, 13, MUTED, fam(sub), "start")
    d.t(x + CW / 2, CAPY, cap, 13, SOFT, KR, "middle", 600)
    if i < 3:
        d.arrow([(x + CW + 2, CY + 36), (x + STRIDE - 6, CY + 36)], MUTED, "ar", 1.5)

for i, (lines, c, focal) in enumerate(STAGES):
    x = XS0 + STRIDE * i + CHX
    h = 4 + LINE_H * lines
    for (pid, author), y in zip(POSTS, LANES):
        if focal:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CHW}" height="{h}" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CHW}" height="{h}" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        d.t(x + CHW / 2, y + 20, str(pid), 13, c, MONO, "middle", 600)
        if lines >= 2:
            d.t(x + CHW / 2, y + 20 + LINE_H, f"글쓴이 {author}", 13, c, KR, "middle")
        if lines >= 3:
            d.t(x + CHW / 2, y + 20 + 2 * LINE_H, "이름 · 사진", 13, c, KR, "middle")

d.chip(XS0 + STRIDE * 3 + CW / 2, 408, "이미지 · 동영상은 CDN", MUTED, 13)

d.legend(H - 56, [("저장소 단계", INFO), ("ID 만", ACC), ("객체를 채우는 중", WARN), ("완성된 항목", OK)])
d.save("11-01.hydration-flow.svg")
