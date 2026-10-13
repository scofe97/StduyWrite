# 타입 스펙: type-process — 절 여섯을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §3.
# 사실 출처: 추출본 v2.txt 3921~3946행(요구·추정)·3947~3973행(구성)·3974~4023행(업로드)·4024~4046행(스트리밍)·4051~4073행(트랜스코딩)·4074~4093행(DAG),
#   계산: 5,000,000 × 10% × 300 MB = 150 TB · 5,000,000 × 5 × 0.3 GB × $0.02 = $150,000.
# Layout conventions: 카드 폭 288·높이 124, x stride 312(24·336·648), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-01",
      "YouTube 업로드를 여섯 절로 읽는다",
      "규모와 비용을 어림하고 클라우드로 쓸 부품을 정한 뒤, 업로드의 두 갈래와 스트리밍을 보고, 변환이 왜 필요하며 DAG 로 어떻게 쪼개는지로 이어 간다.",
      "규모 → 구조 → 업로드 → 스트리밍 → 변환 → DAG")

CW, CH = 288, 124
XS = (24, 336, 648)
YS = (104, 276)
CARDS = (
    ("§1", "규모와 비용", "150 TB/일 · $150,000/일", INFO),
    ("§2", "클라우드로 쓸 부품", "BLOB 저장소 · CDN", INFO),
    ("§3", "업로드 두 갈래", "영상 갈래 · 메타데이터 갈래", ACC),
    ("§4", "스트리밍", "조각 파일 · 화질 전환", INFO),
    ("§5", "트랜스코딩", "코덱 · 컨테이너 · 비트레이트", INFO),
    ("§6", "DAG", "세 갈래 · 조립", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = (0, i) if i < 3 else (1, i - 3)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 13 if fam(val) == KR else 12, MUTED, fam(val), "start")

for i in range(5):
    if i == 2:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
# 윗줄 끝(§3)에서 아랫줄 처음(§4)으로 읽는 순서를 잇는다.
d.arrow([(pos[2][0] + CW // 2, YS[0] + CH + 4), (pos[2][0] + CW // 2, 252), (pos[3][0] + CW // 2, 252), (pos[3][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("14-01.chapter-overview.svg")
