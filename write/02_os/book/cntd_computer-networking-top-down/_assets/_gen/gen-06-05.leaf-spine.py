# 타입 스펙: type-architecture — 구성 요소와 그 사이 관계. zone 으로 두 세대의 토폴로지를 묶어 대비한다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.6.1 Figure 6.32 · Figure 6.33 —
#   경로 4 개 400 Gbps, 페이스북의 16 x 16, 잎-등뼈에서 정확히 두 홉이라는 서술 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 1000, 582
d = D(W, H, "SECTION 6.6.1 · MORE LINKS, FEWER HOPS",
      "티어 사이 연결을 늘리고 층을 줄입니다",
      "TOR 하나를 티어 2 스위치 여럿에 붙이면 랙 사이에 서로 겹치지 않는 경로가 여럿 생긴다. 그 끝이 잎과 등뼈 두 층짜리 구조다.",
      "경로 수와 홉 수는 원문 §6.6.1 의 서술 그대로입니다")

# 왼쪽 — 연결을 늘린 3층
d.t(24, 116, "티어 사이 연결을 늘린 3 층", 12, INK, KR, "start", 600)
d.tone(24, 132, 452, 216, INFO, 7, "0A", 1.0)
T1 = [(72, 156), (208, 156), (344, 156)]
T2 = [(72, 232), (208, 232), (344, 232)]
TOR = [(72, 300), (208, 300), (344, 300)]
for pts, label, c in [(T1, "티어 1", MUTED), (T2, "티어 2", INFO), (TOR, "TOR", OK)]:
    for x, y in pts:
        d.tone(x, y, 88, 40, c, 5, "14", 1.1)
        d.t(x + 44, y + 25, label, 11, c, KR, "middle", 600)
for x1, _ in T2:
    for x2, _ in T1:
        d.line(x1 + 44, 232, x2 + 44, 196, f"{INFO}55", 0.9)
for x1, _ in TOR:
    for x2, _ in T2:
        d.line(x1 + 44, 300, x2 + 44, 272, f"{OK}55", 0.9)
d.t(250, 366, "TOR 하나가 티어 2 여럿에 붙습니다", 11, MUTED, KR)

# 오른쪽 — 잎과 등뼈
d.t(524, 116, "잎과 등뼈 2 층", 12, INK, KR, "start", 600)
d.tone(524, 132, 452, 216, ACC, 7, "0A", 1.0)
SPINE = [(568, 168), (712, 168), (856, 168)]
LEAF = [(568, 280), (712, 280), (856, 280)]
for x, y in SPINE:
    d.tone(x, y, 88, 40, ACC, 5, "14", 1.2)
    d.t(x + 44, y + 25, "등뼈", 11, ACC, KR, "middle", 600)
for x, y in LEAF:
    d.tone(x, y, 88, 40, OK, 5, "14", 1.2)
    d.t(x + 44, y + 25, "잎", 11, OK, KR, "middle", 600)
for x1, _ in LEAF:
    for x2, _ in SPINE:
        d.line(x1 + 44, 280, x2 + 44, 208, f"{ACC}55", 0.9)
d.t(750, 366, "잎 하나가 모든 등뼈에 붙습니다", 11, MUTED, KR)

BOX = [
    (24, 392, 452, "연결을 늘리면 무엇을 얻나", [
        "티어 2 둘 사이에 겹치지 않는 경로가 넷, 합쳐서 400 Gbps 입니다",
        "용량만이 아니라 경로 다양성 덕분에 신뢰성도 함께 오릅니다",
        "페이스북은 TOR 하나를 티어 2 열여섯 개에 붙입니다",
    ], INFO),
    (524, 392, 452, "층을 줄이면 무엇을 얻나", [
        "접근 스위치 너머 통신이 정확히 스위치 두 홉으로 고정됩니다",
        "용량은 링크 속도를 올리거나 등뼈를 옆으로 더 놓아 늘립니다",
        "서버끼리 오가는 동서 트래픽이 늘어난 것이 이 변화의 배경입니다",
    ], ACC),
]
for x, y, w, title, lines, c in BOX:
    d.box(x, y, w, 92, PAPER2, f"{c}44", 1.2, 7)
    d.t(x + 16, y + 22, title, 11, c, KR, "start", 600)
    d.line(x + 16, y + 32, x + w - 16, y + 32, RULE, 0.8)
    for i, s in enumerate(lines):
        d.t(x + 16, y + 52 + i * 18, "·  " + s, 10, MUTED, KR, "start")

d.line(24, 504, W - 48, 504, RULE, 0.8)
d.t(24, 524, "여러 층으로 쌓은 이런 상호 연결망을 Clos 망이라 부릅니다. 전화 교환을 연구한 Charles Clos 의 이름에서 왔습니다.",
     11, MUTED, KR, "start")

d.legend(542, [("잎-등뼈 구조", ACC), ("3 층 구조", INFO), ("랙에 닿는 층", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-05.leaf-spine.svg"
d.save(out)
print("→", out)
