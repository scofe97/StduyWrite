# 11-01 §2 — selector 가 뒤에 설 파드를 고른다
# '어느 조합이 되고 안 되는가'라 행렬이다(계약 §타입을 본문이 정한다). 행은 후보 파드,
# 열은 판단 축, 판정 열을 focal 로 둔다. 네임스페이스 탈락이 함정이라 마지막 행에 담았다.
# 타입 스펙: type-dp-security-matrix.md — 행은 후보 파드 넷, 열은 라벨·네임스페이스·판정. 어느 조합이 포함되고 빠지는지가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, KR, MONO
import ddx

d = D(1014, 628, "KUBERNETES IN ACTION · 11-01",
      "selector 가 뒤에 설 파드를 고른다",
      "Service 의 selector 와 파드 라벨을 맞춰 본다. 값이 맞으면 다른 라벨이 더 붙어 있어도 들어오고, "
      "값이 다르면 빠진다. 라벨이 같아도 네임스페이스가 다르면 selector 는 보지 못한다.",
      "quote Service · selector 는 app=quote 하나뿐")

ddx.matrix(
    d, x0=24, hdr_y=140, row_h=84, gap=12, focal_col=3,
    cols=[(200, "후보 파드"), (270, "파드 라벨"), (160, "네임스페이스"), (300, "selector app=quote")],
    rows=[
        ([("quote-001", "stable"), ("app=quote, rel=stable", ""), ("kiada",),
          ("포함", "app 값이 맞는다")], OK),
        ([("quote-canary", "canary"), ("app=quote, rel=canary", ""), ("kiada",),
          ("포함", "rel 은 매칭에 끼지 않는다")], OK),
        ([("quiz", "다른 서비스"), ("app=quiz", ""), ("kiada",),
          ("제외", "app 값이 다르다")], BAD),
        ([("quote-001", "다른 ns 의 같은 이름"), ("app=quote", ""), ("other-ns",),
          ("제외", "selector 는 ns 안에서만 본다")], BAD),
    ])

d.legend(560, [("들어온다", OK), ("빠진다", BAD)])
d.save("11-01-service-label-selector.svg")
print("ok")
