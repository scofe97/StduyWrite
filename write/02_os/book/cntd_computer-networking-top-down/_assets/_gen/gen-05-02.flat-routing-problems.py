# 타입 스펙: type-architecture — 경계 없는 한 덩어리(점선 영역) 안의 라우터와 링크, 그 아래 무너지는 두 자리.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.3 도입 (규모·관리 자율성 두 문제)
# 짝: gen-05-02.as-nesting.py 가 같은 라우터 배치에 AS 경계를 그은 해결 그림이다.
#     라우터 좌표·카드 위치·줄 순서를 두 생성기가 똑같이 쓴다 — 한쪽을 옮기면 다른 쪽도 옮긴다.
# 주의: 라우터 이름 1a~3d 는 원문 Figure 5.8 의 배치를 빌렸을 뿐, 이 그림 자체는 원문에 없다(경계 이전 상태는 노트의 읽기).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, ACC, BAD, KR, MONO

W, H = 1000, 640
d = D(W, H, "SECTION 5.3 · BEFORE AUTONOMOUS SYSTEMS",
      "경계가 없으면 가정이 두 곳에서 무너집니다",
      "앞 편의 가정을 인터넷 크기로 늘린 모습. AS 경계 없이 모든 라우터가 같은 알고리즘을 돌리고 서로를 알아야 해서, 규모와 관리 자율성 두 곳에서 문제가 생긴다.",
      "앞 편의 가정을 인터넷 크기로 늘린 모습입니다. 라우터 배치는 아래 해결 그림과 같고, AS 경계만 아직 없습니다.")

# 경계 없는 한 덩어리 — 점선은 '경계'가 아니라 '인터넷 전체'를 둘러싼다
d.o.append(f'<rect x="20" y="116" width="960" height="300" rx="12" fill="{INK}04" '
           f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="6 4"/>')
d.tone(36, 128, 84, 24, ACC, r=4, op="12", sw=1.4)          # focal — 아래 해결 그림에서 그어질 자리
d.t(78, 144, "경계 없음", 12, ACC, KR, "middle", 600)
d.t(136, 144, "인터넷 전체가 하나의 알고리즘 · 모든 라우터가 서로를 앎", 12, INK, KR, "start", 600)

for cx, owner in ((188, "ISP 1 의 라우터"), (500, "ISP 2 의 라우터"), (812, "ISP 3 의 라우터")):
    d.t(cx, 196, owner, 12, SOFT, KR)


def router(x, y, name):
    d.box(x, y, 76, 44, PAPER2, MUTED, 1.0, 6)
    d.t(x + 38, y + 19, name, 12, INK, MONO, "middle", 600)
    d.t(x + 38, y + 36, "전부를 앎", 12, MUTED, KR)


for x, y, name in ((72, 248, "1a"), (168, 248, "1b"), (72, 316, "1d"), (240, 316, "1c"),
                   (384, 248, "2b"), (480, 248, "2d"), (384, 316, "2a"), (552, 316, "2c"),
                   (696, 248, "3b"), (792, 248, "3c"), (696, 316, "3a"), (864, 316, "3d")):
    router(x, y, name)

# 링크 — 경계가 없으니 주인이 다른 라우터 사이의 링크도 여느 링크와 똑같이 그린다.
# 해결 그림의 eBGP 두 줄만 남기면 경계가 없는데도 그 두 링크가 특별해 보인다(2026-09-13 사용자 지적).
LINKS = [
    (148, 270, 168, 270), (244, 270, 384, 270), (460, 270, 480, 270), (556, 270, 696, 270), (772, 270, 792, 270),
    (148, 338, 240, 338), (316, 338, 384, 338), (460, 338, 552, 338), (628, 338, 696, 338), (772, 338, 864, 338),
    (110, 292, 110, 316), (422, 292, 422, 316), (734, 292, 734, 316),
]
for x1, y1, x2, y2 in LINKS:
    d.line(x1, y1, x2, y2, MUTED, 1.2)

d.t(500, 392, "그림은 12개 · 실제 인터넷은 라우터 수억 개", 12, MUTED, KR)

# 무너지는 두 자리 — 해결 그림의 두 칸과 줄 단위로 짝이 맞는다
CARDS = [
    (20, "규모", "라우터 수억 개를 감당 못 함",
     ["모든 목적지 저장 → 막대한 메모리",
      "변화마다 전부에게 브로드캐스트",
      "거리 벡터는 이 규모에서 수렴 못 함"]),
    (516, "관리 자율성", "주인마다 사정이 다름",
     ["자기 망을 자기 뜻대로 운영",
      "라우팅 알고리즘을 스스로 선택",
      "내부 구조를 밖에 감춤"]),
]
for x, head, sub, lines in CARDS:
    d.tone(x, 440, 464, 128, BAD, r=8, op="10", sw=1.2)
    d.t(x + 20, 468, head, 14, BAD, KR, "start", 600)
    d.t(x + 20 + (28 if len(head) == 2 else 80) + 16, 468, sub, 12, MUTED, KR, "start")
    for i, ln in enumerate(lines):
        y = 496 + 24 * i
        d.box(x + 20, y - 8, 4, 4, BAD, BAD, 0, 1)
        d.t(x + 32, y, ln, 13, INK, KR, "start")

d.legend(592, [("무너지는 자리", BAD), ("라우터", MUTED)])
d.t(960, 614, "KUROSE-ROSS 9E §5.3", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.flat-routing-problems.svg"
d.save(out)
print("→", out)
