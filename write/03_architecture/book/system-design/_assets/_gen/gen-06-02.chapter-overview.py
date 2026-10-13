# 타입 스펙: type-process — 절 여덟을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §1.
# 사실 출처: 추출본 v2.txt 1692~1913행(버저닝·벡터 시계 1692 · 장애 처리 1757 · 구조도 1846 · 쓰기 경로 1862 · 읽기 경로 1876 · 요약 1896),
#   PDF 98~108쪽 그림의 값(D5([Sx,3],[Sy,1],[Sz,1]) · s2 9908 / 11:58:02 · 루트 5357 vs 9213 · 키 7~9),
#   Dynamo 논문 §4.4~4.8(https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf).
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, INK, SOFT, PAPER2, RULE, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-02",
      "충돌과 장애를 다루는 다섯 기법과 노드 안의 읽기·쓰기",
      "동시 쓰기를 벡터 시계로 가르고, 장애를 가십으로 알아내 임시 위탁과 머클 트리로 메운 뒤, 한 노드의 쓰기와 읽기를 따라간다.",
      "값 하나가 충돌하고 복제본 하나가 사라진 뒤 디스크에 닿기까지")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "벡터 시계", "D5([Sx,3],[Sy,1],[Sz,1])", ACC),
    ("§2", "가십 프로토콜", "s2 · 9908 · 11:58:02", INFO),
    ("§3", "임시 위탁", "s2 다운 → s3 가 대신 받음", INFO),
    ("§4", "머클 트리", "5357 ≠ 9213 → 키 7~9", INFO),
    ("§5", "데이터 센터 장애", "여러 센터에 복제", INFO),
    ("§6", "쓰기 경로", "로그 → 메모리 → SSTable", OK),
    ("§7", "읽기 경로", "메모리 → 블룸 → SSTable", OK),
    ("§8", "목표와 기법", "열 줄 대응표", INFO),
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

for i in range(7):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
# 첫 줄 끝 카드에서 둘째 줄 첫 카드로 내려가는 읽기 순서
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("충돌·장애 처리", INFO), ("가장 먼저 만나는 절", ACC), ("노드 안 경로", OK)])
d.save("06-02.chapter-overview.svg")
