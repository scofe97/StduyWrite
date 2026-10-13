# 타입 스펙: type-process — 절 여덟을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §4.
# 사실 출처: 추출본 v2.txt 3585~3606행(추정)·3622~3634행(빈도 표·LIKE 질의)·3655~3696행(트라이·접두사 길이)·3699~3708행(노드별 상위 k)·3730~3760행(수집 경로)·3762~3790행(질의 최적화)·3797~3815행(갱신·삭제)·3817~3836행(샤딩).
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01",
      "검색어 자동완성을 여덟 절로 읽는다",
      "요구사항과 추정에서 출발해 빈도 표와 트라이로 질의를 풀고, 노드별 상위 k 캐시와 주 단위 수집 경로, 질의 최적화, 갱신, 샤딩으로 이어진다.",
      "추정 → 빈도 표 → 트라이 → 노드별 캐시 → 수집 경로 → 질의 → 갱신 → 샤딩")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "요구사항과 추정", "23,000 QPS · 0.4 GB/일", INFO),
    ("§2", "빈도 표 개략 설계", "LIKE 'tw%' · LIMIT 5", INFO),
    ("§3", "트라이", "tr → true 35 · try 29", INFO),
    ("§4", "노드별 상위 k 캐시", "be → best 35 · bet 29", ACC),
    ("§5", "수집 경로", "로그 → 집계 → 주간 재구축", INFO),
    ("§6", "질의 서비스 최적화", "max-age 3600 · 샘플링", INFO),
    ("§7", "갱신과 필터", "beer 10 → 30", INFO),
    ("§8", "샤딩", "a–m · n–z", INFO),
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

for i in range(7):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("13-01.chapter-overview.svg")
