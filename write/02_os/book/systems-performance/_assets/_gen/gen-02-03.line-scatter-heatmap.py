# 02-03 §7 — 세 시각화가 각각 보여 주는 것과 못 보여 주는 것.
# 타입 스펙: type-dp-security-matrix — 시각화(행) × 읽어야 할 것(열)의 가능 여부 격자.
#           옛 손 SVG(세 패널 서술)를 타입 전환해 재생성. 칸의 말은 원서 2.10.1~2.10.3(p.67–69) 문장을 줄인 것이다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 928, 448
LX, CX, CW = 24, 168, 184
Y0, RH, RG = 120, 64, 10
COLS = ["시간 추이", "개별 이상치", "몸통의 패턴", "데이터 규모"]
ROWS = [
    ("라인 차트", [("x 축 = 시간", OK), ("평균에 묻힘", WARN), ("요약값만", WARN), ("원서 언급 없음", None)]),
    ("산점도", [("x 축 = 완료 시각", OK), ("전부 보임", OK), ("서브ms 점 겹침", BAD), ("페인트 벽", BAD)]),
    ("히트맵", [("x 버킷", OK), ("위쪽 옅은 블록", OK), ("패턴이 드러남", OK), ("수천 시스템도 같게", OK)]),
]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-03 §7",
       "같은 디스크 I/O, 세 장의 그림",
       "MySQL 서버의 디스크 I/O 지연을 그린 세 시각화가 시간 추이·개별 이상치·몸통 패턴·데이터 규모를 각각 어떻게 다루는지 칸으로 나눴다.",
       "원서 2.10.1~2.10.3 · 같은 트레이스")

for j, c in enumerate(COLS):
    x = CX + j * CW
    d.box(x + 4, Y0, CW - 8, 32, PAPER2, RULE, 1.0, 4)
    d.t(x + CW / 2, Y0 + 21, c, 13, INK, KR, "middle", 600)

for i, (name, cells) in enumerate(ROWS):
    y = Y0 + 44 + i * (RH + RG)
    focal = name == "히트맵"
    d.t(LX, y + 37, name, 14, ACC if focal else INK, KR, "start", 600)
    for j, (txt, c) in enumerate(cells):
        x = CX + j * CW
        if c: d.tone(x + 4, y, CW - 8, RH, c, 6)
        else: d.box(x + 4, y, CW - 8, RH, PAPER2, RULE, 1.0, 6)
        d.t(x + CW / 2, y + 37, txt, 13, INK if c else SOFT, KR, "middle")
    if focal: d.tone(LX - 8, y - 4, CX - LX, RH + 8, ACC, 6)

yl = Y0 + 44 + 3 * (RH + RG) + 8
d.legend(yl, [("보임", OK), ("가려짐", WARN), ("한계", BAD)])
d.save("02-03.line-scatter-heatmap.svg")
