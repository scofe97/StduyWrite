# 16-01 §3 — ready 와 DNS 가 서로를 기다린다
# 부팅 시점 분산 시스템의 순환이라 사슬이 아니라 고리로 그린다. 고리를 끊는 필드 한 줄이
# focal 이고, 12-02 의 SNI 고리와 같은 형태로 맞춰 읽는 사람이 패턴을 알아보게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1180, 620, "KUBERNETES IN ACTION · 16-01",
      "ready 가 되려면 DNS 가, DNS 가 생기려면 ready 가",
      "기본값에서는 ready 인 파드만 DNS 에 오른다. 그런데 여기서는 그 조건이 스스로를 막는다 — "
      "멤버들이 서로를 찾아야 비로소 각자 준비를 마치기 때문이다.",
      "publishNotReadyAddresses 를 빼면 이 예제는 부팅되지 않는다")

ddx.band(d, 100, 452, "닫힌 고리", x=24, w=680)
CY = [("DNS 레코드가 없다", "ready 인 파드가 없으니", 364, 190),
      ("rs.initiate 실패", "Host not found", 570, 320),
      ("파드가 ready 가 아니다", "MongoDB ping 이 실패한다", 190, 320)]
for t, s, cx, cy in CY:
    ddx.node(d, cx, cy, t, s, 236, 84, BAD)
# 박스: A(246~482 x 148~232) · B(452~688 x 278~362) · C(72~308 x 278~362)
# 고리는 비스듬히 잇지 않고 y=252 통로를 양쪽으로 나눠 쓴다. 두 가로 구간(190~300 · 430~570)은
# 겹치지 않고, 가운데 라벨(x 304~424)도 비켜 간다.
d.path("M 300 232 L 300 252 L 190 252 L 190 274", BAD, 1.5, m="bad")   # A → C
d.path("M 312 320 L 446 320", BAD, 1.5, m="bad")                       # C → B
d.path("M 570 278 L 570 252 L 430 252 L 430 236", BAD, 1.5, m="bad")   # B → A
d.t(364, 268, "화살표는 '막는다'", 10, SOFT, KR)
d.t(364, 414, "아무도 먼저 ready 가 될 수 없다", 11, BAD, KR)

ddx.band(d, 100, 452, "고리를 끊는 한 줄", x=724, w=432)
ddx.node(d, 940, 268, "publishNotReadyAddresses", "true", 380, 88, focal=True)
d.t(940, 200, "기본값은 false 라 빼기 쉽다", 11, MUTED, KR)
d.t(940, 350, "아직 준비되지 않았어도", 11, ACC, KR)
d.t(940, 370, "주소는 공개하라", 11, ACC, KR)
d.t(940, 412, "생성 즉시 DNS 레코드가 생긴다", 11, SOFT, KR)

d.t(24, 500, "부팅 시점의 분산 시스템에서는 이런 순환이 예외가 아니다. 멤버들이 서로를 찾아야 각자 준비를 마치므로, "
             "아무도 먼저 준비될 수 없는 상태가 자연스럽게 만들어진다.", 11, MUTED, KR, "start")
d.t(24, 522, "12-02 의 SNI 닭과 달걀도 같은 모양이었다 — 순서를 앞으로 당기거나, 조건을 한 칸 느슨하게 해야 풀린다.",
     11, MUTED, KR, "start")
d.legend(548, [("닫힌 고리", BAD), ("고리를 끊는 자리", ACC)])
d.save("16-01-not-ready-addresses.svg")
print("ok")
