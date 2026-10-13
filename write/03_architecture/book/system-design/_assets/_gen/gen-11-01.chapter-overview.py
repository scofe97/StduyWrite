# 타입 스펙: type-process — 절 일곱을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §3.
# 사실 출처: 추출본 v2.txt 2973~2986행(요구사항: 친구 5,000 · 1,000만 DAU)·2999~3009행(두 API)·3034~3094행(팬아웃 서비스와 모델)·3095~3112행(조회)·3113~3125행(캐시 다섯 층)·3134~3147행(확장).
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 11-01",
      "뉴스 피드를 일곱 절로 읽는다",
      "범위와 두 API 에서 출발해 게시 흐름을 보고, 쓸 때 밀기와 읽을 때 당기기를 섞는 팬아웃을 고른 뒤, 팬아웃 서비스·조회 흐름·캐시 다섯 층·확장 주제로 이어진다.",
      "범위 → 게시 → 팬아웃 혼합 → 조회 → 캐시 층")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "범위와 두 API", "POST · GET /v1/me/feed", INFO),
    ("§2", "게시 흐름", "인증 · 저장 · 팬아웃", INFO),
    ("§3", "팬아웃 혼합", "일반 밀기 · 유명인 당기기", ACC),
    ("§4", "팬아웃 서비스", "그래프 DB → 큐 → 캐시", INFO),
    ("§5", "조회 흐름", "ID 목록 → JSON", INFO),
    ("§6", "캐시 다섯 층", "피드부터 카운터까지", INFO),
    ("§7", "확장 주제", "DB · 웹 · 큐 · 지표", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = (0, i) if i < 4 else (1, i - 4)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 13, MUTED, fam(val), "start")

for i in range(6):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("11-01.chapter-overview.svg")
