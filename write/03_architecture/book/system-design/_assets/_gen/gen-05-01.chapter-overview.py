# 타입 스펙: type-process — 절 여섯을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §3.
# 사실 출처: 추출본 v2.txt 1325~1491행(재해시 1329 · 해시 링 1363 · 서버 조회 1389 · 추가 1398 · 제거 1406 · 두 문제 1410 · 가상 노드 1430 · 영향 범위 1453 · 사용처 1471),
#   값은 이 편 본문의 예시(0~99 공간 s0=15·s1=40·s2=65·s3=90, s4=10)와 계산값(§4 편차 35%→4%)을 그대로 옮겼다.
# Layout conventions: 카드 폭 288·높이 124, x stride 312(24·336·648), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 05-01",
      "안정 해시를 여섯 절로 읽는다",
      "서버 번호로 나누는 방식이 무너지는 값에서 출발해 링 조회·이동 범위·가상 노드를 거쳐 쓰이는 곳까지 간다.",
      "키 8개는 나머지 연산에서, 키 4개는 링 위에서 어디로 가는지")

CW, CH = 288, 124
XS = (24, 336, 648)
YS = (104, 276)
CARDS = (
    ("§1", "나머지 연산", "% 4 → % 3 · 8 중 5 이동", INFO),
    ("§2", "해시 링", "0 ~ 2^160 − 1 · 시계 방향", INFO),
    ("§3", "추가와 제거", "k0 → s4 · k1 → s2", ACC),
    ("§4", "가상 노드", "구간 25·50·25 → 33·35·32", INFO),
    ("§5", "영향 범위", "(90, 10] · 20", INFO),
    ("§6", "쓰이는 곳", "Dynamo · Cassandra · Maglev", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = divmod(i, 3)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 13, MUTED, fam(val), "start")

for i in (0, 1, 3, 4):
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
# 첫 줄 끝 카드에서 둘째 줄 첫 카드로 내려가는 읽기 순서
d.arrow([(pos[2][0] + CW // 2, YS[0] + CH + 4), (pos[2][0] + CW // 2, 252), (pos[3][0] + CW // 2, 252), (pos[3][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 44, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("05-01.chapter-overview.svg")
