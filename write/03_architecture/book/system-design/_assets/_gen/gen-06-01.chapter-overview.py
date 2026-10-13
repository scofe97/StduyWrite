# 타입 스펙: type-process — 절 여섯을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §5.
# 사실 출처: 추출본 v2.txt 1492~1691행(범위 1513 · 단일 서버 1525 · CAP 1538 · 파티션 1605 · 복제 1626 · 일관성 1642 · 일관성 모델 1676), PDF 93·94쪽 그림(key0 → s1, N=3 복제 s1·s2·s3),
#   Dynamo 논문 §6(흔한 (N,R,W) = (3,2,2)).
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-01",
      "키-값 저장소를 여섯 절로 읽는다",
      "요구사항에서 출발해 분할 중의 선택을 정하고, 키를 나누고 복제한 뒤, 정족수와 일관성 강도로 닫는다.",
      "n3 가 끊겼을 때의 선택에서 W + R > N 까지")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "요구사항", "10 KB 미만 · 단일 서버", INFO),
    ("§2", "CAP 선택", "n3 단절 · CP · AP", INFO),
    ("§3", "안정 해시", "key0 → s1", INFO),
    ("§4", "복제와 센터", "N = 3 · s1 s2 s3", INFO),
    ("§5", "정족수", "W + R > N", ACC),
    ("§6", "일관성 강도", "강한 · 약한 · 최종", INFO),
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
    d.t(x + 14, y + 100, val, 12, MUTED, fam(val), "start")

for i in range(5):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("06-01.chapter-overview.svg")
