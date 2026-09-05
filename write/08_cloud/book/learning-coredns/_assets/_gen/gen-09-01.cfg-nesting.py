# 09-01 §4 — 세 겹의 포함 관계. 순서를 정하는 층은 가운데다.
# 원문 근거: "The plugin.cfg file is a simple configuration file used to control which plug-ins
#            are compiled into CoreDNS during the build." / "regardless of the order that
#            directives are listed in the Corefile, the plug-in chain will be built in the order
#            in plugin.cfg."
# 타입 스펙: type-nested — 바깥이 안을 포함하는 관계가 사실이고, 그 관계는 중첩으로만 보인다.
#           가운데 층 하나가 순서를 정한다는 것이 이 그림의 초점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 566
d = D(W, H, "LEARNING COREDNS · 09-01 §4",
      "세 겹의 포함 관계와 순서를 정하는 층",
      "바깥이 세상의 모든 플러그인이고 안으로 갈수록 실제로 도는 것에 가까워진다. "
      "참여 여부는 가장 안쪽이 고르지만 순서는 가운데가 정한다.",
      "주황이 순서를 정하는 층입니다")

# 중첩 간격 58px — 부제(상단 +48)가 다음 상자 테두리를 걸터앉지 않게 한다.
BOXES = [
    (40, 96, 760, 292, "세상의 모든 플러그인", "인트리 · CoreDNS 조직 · 제3자", False),
    (100, 154, 640, 206, "바이너리에 든 것", "plugin.cfg 의 줄 목록 · 빌드 때", True),
    (160, 212, 520, 120, "이 블록에서 켜진 것", "Corefile 의 지시자 · 실행 때", False),
]

for x, y, w, h, title, sub, focal in BOXES:
    if focal:
        d.tone(x, y, w, h, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER if y == 96 else PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 48, sub, 11, ACC if focal else MUTED, MONO, "start")

d.t(178, 296, "여기서 고르는 것은 참여 여부뿐이다", 11, MUTED, KR, "start")
d.t(178, 318, "순서는 바깥 한 겹이 이미 정해 두었다", 11, ACC, KR, "start")

d.box(20, 404, 840, 84, PAPER, RULE, 0.8)
d.t(36, 428, "그래서 이런 일이 생긴다", 12, INK, KR, "start", 600)
d.t(36, 452, "Corefile 에 적은 순서대로 안 돌고, -plugins 로 본 목록도 체인 순서가 아니다(알파벳 순서다)",
     11, MUTED, KR, "start")
d.t(36, 474, "이미 만들어진 바이너리에서는 그것을 만든 plugin.cfg 가 손에 없다", 11, MUTED, KR, "start")

d.legend(508, [("순서를 정하는 층", ACC)])
d.save("09-01.cfg-nesting.svg")
