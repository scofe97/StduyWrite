# 16-01 §2 — 소프트웨어에서는 이야기가 조금 다르다
# 비유만 그리면 "그래서 뭐"로 끝난다. 본문이 "같은 신원과 같은 상태를 줄 수 있다면 대체가
# 성립한다"로 비유를 되받으므로, 그 되받는 줄이 도식 안에 있어야 한다.
# 타입 스펙: type-dp-security-matrix.md — 행은 두 관점(Cattle · Pets), 열은 무엇으로 보나 · 교체하면 · 쿠버네티스에서 · 대체가
#           성립하려면. 마지막 열이 판정이다.
import sys; sys.path.insert(0, ".")
from dd import D, INFO, OK, WARN, MUTED, SOFT, INK, KR
import ddx

d = D(1200, 600, "KUBERNETES IN ACTION · 16-01",
      "교체가 자명한가, 신원을 되돌려야 하는가",
      "소는 구별 없는 개체라 교체가 자명하다. 애완동물은 같은 이름을 줘도 원래처럼 행동하지 않는다. "
      "다만 소프트웨어에서는 신원과 상태를 함께 되돌릴 수 있어 사정이 다르다.",
      "StatefulSet 은 원래 PetSet 이라 불렸다")

ddx.matrix(
    d, x0=24, hdr_y=148, row_h=96, gap=12, focal_col=3,
    cols=[(230, "무엇으로 보나"), (280, "교체하면"), (300, "쿠버네티스에서"), (330, "대체가 성립하려면")],
    rows=[
        ([("Cattle — 소", "구별 없는 개체"), ("알아채지 못한다", "이전과 같지 않아도 된다"),
          ("Deployment 의 파드", "stateless 워크로드"),
          ("아무 조건도 없다", "그래서 교체가 자명하다")], INFO),
        ([("Pets — 애완동물", "이름과 개성이 있다"), ("같지 않다", "같은 이름을 줘도 다르다"),
          ("StatefulSet 의 파드", "stateful 워크로드"),
          ("같은 이름 · 같은 볼륨 · 같은 주소", "셋을 되돌려 줘야 한다")], OK),
    ])

d.t(24, 412, "그래서 StatefulSet 이 하는 일은 애완동물을 소로 바꾸는 것이 아니라, 애완동물의 신원을 "
             "교체 인스턴스에 그대로 넘겨주는 것이다.", 11, MUTED, KR, "start")
d.t(24, 434, "이름은 ordinal 이, 볼륨은 전용 PVC 가, 주소는 headless Service 의 DNS 레코드가 맡는다 — §3~§5 가 그 셋을 차례로 세운다.",
     11, MUTED, KR, "start")
d.legend(464, [("교체가 자명하다", INFO), ("신원을 되돌려야 한다", OK)])
d.save("16-01-pets-vs-cattle.svg")
print("ok")
