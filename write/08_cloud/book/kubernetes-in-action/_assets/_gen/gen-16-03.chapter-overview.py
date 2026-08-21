# 16-03 전체 지도 — 교체의 주도권을 누가 쥐는가
# 본문이 "색이 붙은 곳은 두 군데뿐"이라 서술하고 앰버는 maxSurge 부재, 붉은은 OnDelete 의
# ready 판단 책임이라고 적는다. 세 절이 주도권을 사용자 쪽으로 한 칸씩 옮기는 축이다.
import sys; sys.path.insert(0, ".")
from dd import D, WARN, BAD, MUTED, KR
import ddx

d = D(1180, 560, "KUBERNETES IN ACTION · 16-03",
      "교체의 주도권을 누가 쥐는가",
      "세 방식은 나란한 선택지가 아니라 한 축의 눈금이다. 순서와 시점을 컨트롤러가 다 쥔 쪽에서 "
      "시작해, 어디까지 · 언제까지를 한 칸씩 사용자에게 넘긴다.",
      "§1 RollingUpdate · §2 partition · §3 OnDelete")

ddx.chapter_map(d, 108, x=24, w=1132, rows=[
    ("§1  RollingUpdate", "컨트롤러가 순서와 시점을 전부 정한다",
     "maxSurge 가 없다 — Deployment 와 달리 초과 생성으로 앞당길 수 없다", WARN),
    ("§2  partition", "어디까지 교체할지를 사용자가 정한다", None, None),
    ("§3  OnDelete", "언제 교체할지까지 사용자가 가져온다",
     "파드가 ready 인지 판단할 책임도 컨트롤러가 아니라 사용자에게 넘어온다", BAD),
])

d.t(24, 432, "주도권을 가져올수록 컨트롤러가 대신 봐 주던 것도 함께 사라진다. OnDelete 는 시점을 얻는 대신 "
             "'이 파드가 받을 수 있는가'를 스스로 판단해야 한다.", 11, MUTED, KR, "start")
d.legend(456, [("컨트롤러가 못 해 주는 것", WARN), ("사용자가 떠안는 책임", BAD)])
d.save("16-03.chapter-overview.svg")
print("ok")
