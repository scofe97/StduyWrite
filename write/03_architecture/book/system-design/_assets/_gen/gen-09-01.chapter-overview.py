# 타입 스펙: type-process — 절 일곱을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §4.
# 사실 출처: 추출본 v2.txt 2341~2377행(요구·추정)·2387~2466행(구성 요소·흐름)·2476~2490행(BFS)·2491~2549행(프론티어)·2550~2589행(다운로더)·2590~2601행(견고성)·2613~2631행(문제 콘텐츠),
#   계산: 1,000,000,000 ÷ (30 × 86,400) = 385.8 ≈ 400 · 500 TB × 12 × 5 = 30 PB.
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 09-01",
      "웹 크롤러를 일곱 절로 읽는다",
      "규모를 추정한 뒤 부품과 한 URL 의 여정을 보고, BFS 의 두 결함을 프론티어가 푸는 과정에서 다운로더·견고성·함정으로 이어 간다.",
      "규모 → 부품 → BFS → 프론티어 → 다운로더 → 견고성 → 걸러 내기")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "규모와 요구", "400 QPS · 30 PB", INFO),
    ("§2", "부품과 여정", "11 개 부품 · 한 바퀴", INFO),
    ("§3", "BFS 의 결함", "FIFO · 호스트 몰림", INFO),
    ("§4", "URL 프론티어", "전면 f · 후면 b", ACC),
    ("§5", "다운로더", "robots.txt · DNS 캐시", INFO),
    ("§6", "견고성", "안정 해시 · 상태 저장", INFO),
    ("§7", "걸러 내기", "해시 · 길이 상한", INFO),
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
    d.t(x + 14, y + 100, val, 13 if fam(val) == KR else 12, MUTED, fam(val), "start")

for i in range(6):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("09-01.chapter-overview.svg")
