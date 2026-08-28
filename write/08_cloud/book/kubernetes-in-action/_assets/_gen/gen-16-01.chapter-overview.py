# 16-01 전체 지도 — 파드에 신원을 주는 일
# 본문이 "색이 붙은 곳은 두 군데뿐이고 둘 다 경고"라 서술하고 두 띠의 뜻을 적는다.
# 앰버는 §3 의 headless Service 순서, 붉은은 §5 의 rs.initiate 미실행이다.
# 타입 스펙: type-process.md — 절마다 같은 의미 슬롯이 세로로 반복된다.
import sys; sys.path.insert(0, ".")
from dd import D, WARN, BAD, MUTED, KR
import ddx

d = D(1180, 664, "KUBERNETES IN ACTION · 16-01",
      "파드에 신원을 주는 일",
      "Deployment 의 파드는 서로 교체 가능한 소이고, StatefulSet 의 파드는 이름과 볼륨과 주소를 가진 "
      "애완동물이다. 그 신원이 어디서 생기고 어떻게 불리는지를 따라간다.",
      "§1 막다른 길 · §2 관점 전환 · §3 생성 · §4 확인 · §5 완성")

ddx.chapter_map(d, 108, x=24, w=1132, rows=[
    ("§1  막다른 길", "Deployment 로는 replica 마다 볼륨과 주소를 줄 수 없다", None, None),
    ("§2  관점 전환", "파드를 소가 아니라 애완동물로 본다", None, None),
    ("§3  생성", "headless Service 를 먼저 만들고 StatefulSet 을 만든다",
     "순서를 바꾸면 rs.initiate 가 Host not found 로 실패한다", WARN),
    ("§4  확인", "ordinal 이름과 전용 PVC 가 번호로 짝지어졌는지 본다", None, None),
    ("§5  완성", "DNS 가 그 신원을 네트워크에서 부를 수 있게 만든다",
     "리플리카 셋을 초기화하지 않으면 파드가 영영 ready 가 되지 않는다", BAD),
])

d.t(24, 584, "OrderedReady 는 앞 파드가 ready 가 될 때까지 다음을 만들지 않는다. "
             "그래서 초기화 전에는 quiz-0 이 영영 not ready 로 남고 quiz-1 은 생성조차 되지 않는다.",
     11, MUTED, KR, "start")
d.legend(608, [("순서를 어기면", WARN), ("초기화를 빠뜨리면", BAD)])
d.save("16-01.chapter-overview.svg")
print("ok")
