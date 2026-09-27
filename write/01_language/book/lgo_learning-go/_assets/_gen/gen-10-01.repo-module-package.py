# 10-01.repo-module-package — 저장소 안에 모듈, 모듈 안에 패키지
# 본문 요구(10-01 §1 「저장소·모듈·패키지」): 저장소는 소스가 놓이는 버전 관리 장소, 모듈은 go.mod 로 한 단위가 되어
#           함께 배포·버전되는 묶음, 패키지는 모듈 안의 디렉터리다. 원문 package_example 의 루트·math·do-format 을 예로 쓴다.
# 타입 스펙: type-nested — 바깥에서 안쪽으로 저장소 ⊃ 모듈 ⊃ 패키지 셋. 한 겹당 안쪽 여백 32, 패키지 칸 폭 248·간격 24.
#           focal 은 모듈 겹(go.mod 가 있는 곳) 하나. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 10장 「Repositories, Modules, and Packages」·「Creating and Accessing a Package」.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 984, 480
RX, RY, RW, RH = 24, 112, 924, 304
MX, MY, MW, MH = 56, 172, 860, 212
PY, PW, PH = 260, 248, 96
PXS = [88, 360, 632]

d = D(W, H, "NESTED · 10-01 §1",
      "저장소 안에 모듈, 모듈 안에 패키지",
      "저장소는 소스 코드가 놓이는 버전 관리 장소다. 그 안에서 go.mod 가 있는 디렉터리 트리가 모듈이 되며, 모듈은 한 단위로 배포되고 버전이 매겨진다. "
      "모듈 안의 각 디렉터리가 패키지다. 원문 package_example 에서는 루트의 main, math, do-format 디렉터리의 format 패키지가 한 모듈에 들어 있다.",
      lead="가장 바깥이 저장소, 가운데가 모듈, 안쪽 칸이 패키지입니다. 원문은 한 저장소에 모듈 하나를 권합니다.")

d.box(RX, RY, RW, RH, r=10)
d.t(RX + 20, RY + 28, "저장소 · github.com/learning-go-book-2e/package_example", 13, MUTED, KR, "start", 600)
d.tone(MX, MY, MW, MH, ACC, 8, "0C", 1.4)
d.t(MX + 20, MY + 28, "모듈 · go.mod", 14, ACC, KR, "start", 600)
d.t(MX + 20, MY + 50, "module github.com/learning-go-book-2e/package_example", 12, MUTED, MONO, "start")
pk = [("package main", "루트 · main.go"), ("package math", "math/ · math.go"), ("package format", "do-format/ · formatter.go")]
for x, (name, sub) in zip(PXS, pk):
    d.tone(x, PY, PW, PH, INFO, 6, "14", 1.0)
    d.t(x + PW // 2, PY + 40, name, 14, INFO, MONO, "middle", 600)
    d.t(x + PW // 2, PY + 64, sub, 12, MUTED, MONO, "middle")

d.legend(432, [("모듈 · 배포와 버전의 단위", ACC), ("패키지 · 디렉터리", INFO)])
d.save("10-01.repo-module-package.svg")
print("ok 10-01 repo-module-package")
