# 10-04.workspace — 워크스페이스는 모듈 사이의 참조를 저장소가 아닌 로컬 소스로 푼다
# 본문 요구(10-04 §4 「워크스페이스로 여러 모듈을 함께 고칩니다」): my_workspace 의 go.work 가 workspace_app 과 workspace_lib 을
#           묶으면, app 의 import 가 GitHub 의 공개 판이 아니라 로컬 lib 으로 풀려 SubNums 까지 쓰인다. GOWORK=off 면 공개 판으로 간다.
# 타입 스펙: type-architecture — 존(my_workspace) 안에 go.work 와 두 모듈, 존 밖에 공개 저장소. 직교 화살표만.
#           focal 은 app → 로컬 lib 으로 풀리는 화살표 하나. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 10장 「Using Workspaces to Modify Modules Simultaneously」, go1.25.1 재현(2026-09-27) —
#           go work init·use 뒤 5 · -1 출력, GOWORK=off 에서 no required module provides package.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 460
d = D(W, H, "ARCHITECTURE · 10-04 §4",
      "워크스페이스가 참조를 로컬 소스로 푸는 모습",
      "my_workspace 의 go.work 는 workspace_app 과 workspace_lib 을 use 로 묶는다. 그러면 app 의 import 는 GitHub 에 올린 v0.1.0 이 아니라 "
      "로컬 workspace_lib 소스로 풀려, 공개 판에 없는 SubNums 까지 쓸 수 있다. GOWORK=off 로 빌드하면 워크스페이스를 끄고 go.mod 의 require 대로 공개 판을 쓴다.",
      lead="점선 안이 로컬 워크스페이스입니다. go.work 는 커밋하지 않습니다.")

d.o.append(f'<rect x="24" y="116" width="600" height="276" rx="10" fill="none" stroke="{OK}" stroke-width="1.2" stroke-dasharray="6 5"/>')
d.t(40, 140, "my_workspace · 로컬", 13, OK, KR, "start", 600)
d.box(48, 164, 552, 44)
d.t(64, 191, "go.work · use ./workspace_app ./workspace_lib", 12, INK, MONO, "start", 600)
d.box(48, 256, 232, 96)
d.t(164, 290, "workspace_app", 14, INK, MONO, "middle", 600)
d.t(164, 314, "AddNums · SubNums 호출", 12, MUTED, KR, "middle")
d.tone(368, 256, 232, 96, OK, 6, "14", 1.0)
d.t(484, 290, "workspace_lib", 14, OK, MONO, "middle", 600)
d.t(484, 314, "로컬 소스 · SubNums 있음", 12, MUTED, KR, "middle")
d.arrow([(280, 304), (366, 304)], ACC, "acc", 1.6)
d.t(324, 296, "import", 11, ACC, MONO, "middle", 600)

d.box(708, 256, 240, 96)
d.t(828, 290, "GitHub workspace_lib", 13, INK, MONO, "middle", 600)
d.t(828, 314, "v0.1.0 · SubNums 없음", 12, MUTED, KR, "middle")
d.path("M 164 352 L 164 376 L 828 376 L 828 354", SOFT, 1.2, m="soft", dash="4 4")
d.t(700, 370, "GOWORK=off 일 때만", 11, MUTED, KR, "middle")

d.legend(412, [("워크스페이스 안 로컬 모듈", OK), ("로컬로 풀리는 import", ACC)])
d.save("10-04.workspace.svg")
print("ok 10-04 workspace")
