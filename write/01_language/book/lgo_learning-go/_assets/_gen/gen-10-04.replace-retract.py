# 10-04.replace-retract — replace·exclude 는 내가 쓰는 의존성에, retract 는 내 모듈을 쓰는 쪽에 작용한다
# 본문 요구(10-04 §3 「의존성 덮어쓰기와 버전 철회」): replace 는 의존성을 포크나 로컬 경로로 바꾸고, exclude 는 다른 모듈의 특정 버전을
#           쓰지 못하게 한다. retract 는 내가 낸 모듈의 go.mod 에 적어, 남들이 그 버전을 쓰지 않게 한다. 원문의 메모대로 retract 는 남들이
#           내 모듈의 버전을, exclude 는 내가 다른 모듈의 버전을 쓰지 못하게 한다.
# 타입 스펙: type-architecture — 가운데 내 모듈 go.mod, 왼쪽 의존 모듈, 오른쪽 내 모듈을 쓰는 모듈. 직교 화살표만.
#           왼쪽으로 가는 화살표 둘(replace · exclude), 오른쪽으로 가는 화살표 하나(retract). focal 은 retract 화살표 하나.
# 사실 출처: Learning Go 2판 10장 「Overriding Dependencies」·「Retracting a Version of Your Module」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 420
NY, NH, NW = 176, 128, 232
XL, XM, XR = 36, 376, 716


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 10-04 §3",
      "replace·exclude 는 내가 쓰는 쪽을, retract 는 남이 쓰는 쪽을 다룹니다",
      "가운데는 내 모듈의 go.mod 다. 왼쪽 의존 모듈에 대해서는 replace 로 포크나 다른 경로로 바꾸거나 exclude 로 특정 버전을 막는다. "
      "오른쪽 내 모듈을 쓰는 모듈에 대해서는 내가 낸 버전을 retract 로 철회해, 그쪽의 go get 과 go mod tidy 가 그 버전으로 올리지 않게 한다.",
      lead="화살표는 지시어가 작용하는 방향입니다.")

d.box(XL, NY, NW, NH, r=8)
d.t(XL + NW // 2, NY + 48, "의존 모듈", 14, INK, KR, "middle", 600)
d.t(XL + NW // 2, NY + 70, "버그 · 관리 중단 · 비호환", 12, MUTED, KR, "middle")

d.tone(XM, NY, NW, NH, INFO, 8, "14", 1.1)
d.t(XM + NW // 2, NY + 48, "내 모듈의 go.mod", 14, INFO, KR, "middle", 600)
d.t(XM + NW // 2, NY + 70, "지시어를 적는 곳", 12, MUTED, KR, "middle")

d.box(XR, NY, NW, NH, r=8)
d.t(XR + NW // 2, NY + 48, "내 모듈을 쓰는 모듈", 14, INK, KR, "middle", 600)
d.t(XR + NW // 2, NY + 70, "go get · go mod tidy", 12, MUTED, MONO, "middle")

y1, y2 = NY + 40, NY + 92
d.arrow([(XM - 2, y1), (XL + NW + 4, y1)], SOFT, "soft", 1.3)
d.t((XL + NW + XM) // 2, y1 - 8, "replace", 12, INK, MONO, "middle", 600)
d.t((XL + NW + XM) // 2, y1 + 18, "포크나 경로로 바꿈", 11, MUTED, KR, "middle")
d.arrow([(XM - 2, y2), (XL + NW + 4, y2)], WARN, "warn", 1.3)
d.t((XL + NW + XM) // 2, y2 - 8, "exclude", 12, WARN, MONO, "middle", 600)
d.t((XL + NW + XM) // 2, y2 + 18, "특정 버전을 막음", 11, MUTED, KR, "middle")

ym = NY + NH // 2
d.arrow([(XM + NW + 2, ym), (XR - 4, ym)], ACC, "acc", 1.5)
d.t((XM + NW + XR) // 2, ym - 10, "retract", 12, ACC, MONO, "middle", 600)
d.t((XM + NW + XR) // 2, ym + 20, "내 버전을 철회", 11, MUTED, KR, "middle")

d.t(XL + NW + (XM - XL - NW) // 2, NY + NH + 36, "내가 쓰는 의존성에 작용", 12, MUTED, KR, "middle", 600)
d.t(XM + NW + (XR - XM - NW) // 2, NY + NH + 36, "내 모듈을 쓰는 쪽에 알림", 12, ACC, KR, "middle", 600)

d.legend(364, [("의존성 바꾸기", SOFT), ("의존성 버전 막기", WARN), ("내 버전 철회", ACC)])
d.save("10-04.replace-retract.svg")
print("ok 10-04 replace-retract")
