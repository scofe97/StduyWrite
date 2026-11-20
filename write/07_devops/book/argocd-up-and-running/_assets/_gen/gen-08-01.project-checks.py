# 08-01 §2 — AppProject 는 Application 을 만들거나 갱신할 때와 컨트롤러가 refresh 할 때마다 소스 저장소와 배포 대상을 대조하고, 동기화할 때 리소스 종류를 대조한다. 어긋나면 앞 단계는 InvalidSpecError, 뒤 단계는 sync Failed 로 끝난다.
# 본문 근거: 이 노트 ### 2 「AppProject 가 막는 것」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 sourceRepos 와 destinations 를 좁힌 프로젝트에서 확인했다.
#            허용 목록에 없는 저장소나 네임스페이스를 가진 Application 은 API 호출이 InvalidSpecError 로 거부되었고, YAML 로 선언적으로 적용하면 Application 의 condition 에 같은 오류가 남았다.
#            컨트롤러도 refresh 할 때마다 같은 검사를 다시 한다(v3.6.1 controller/appcontroller.go refreshAppConditions 의 argo.ValidatePermissions). 프로젝트를 나중에 좁히면 이미 있던 Application 에도 InvalidSpecError 가 붙는다.
#            clusterResourceWhitelist 에 없는 종류나 namespaceResourceBlacklist 에 있는 종류를 Git 에 넣고 sync 하면 `resource <group>:<Kind> is not permitted in project <name>` 으로 sync 가 Failed 였다.
#            허용 목록과 거부 목록은 적힌 순서와 상관없이 "허용 하나 일치 그리고 거부 일치 없음" 이면 통과했다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/projects.md("Source repositories", "Destination clusters", "Cluster resource whitelist"),
#            docs/operator-manual/project.yaml(sourceRepos, destinations, clusterResourceWhitelist, namespaceResourceBlacklist).
# 타입 스펙: type-architecture — 왼쪽 시점에서 오른쪽 결과로 가는 한 방향 흐름, 줄마다 하나의 시점.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "ARGO CD UP AND RUNNING · 08-01 §2",
      "AppProject 가 거르는 때와 항목",
      "위쪽 줄은 Application 을 만들거나 갱신하는 때와 컨트롤러가 refresh 하는 때다. 프로젝트의 sourceRepos 와 destinations 를 대조해 허용된 값이면 다음으로 가고 어긋나면 InvalidSpecError 로 거부한다. "
      "아래쪽 줄은 동기화하는 시점이다. 프로젝트가 허용한 리소스 종류만 클러스터에 적용되고 허용하지 않은 종류가 있으면 not permitted in project 오류와 함께 동기화가 Failed 로 끝난다.",
      "같은 프로젝트가 때에 따라 다른 항목을 본다")

C1X, C1W = 24, 210
C2X, C2W = 272, 270
C3X, C3W = 580, 276
YS = [124, 262]
RH = 108

for cx, label in ((C1X + C1W / 2, "시점"), (C2X + C2W / 2, "프로젝트가 대조하는 항목"), (C3X + C3W / 2, "결과")):
    d.t(cx, 108, label, 12, MUTED, KR, "middle", 600)

rows = [
    ("만들기·갱신 · refresh", "API 호출 · 컨트롤러 refresh",
     "sourceRepos · destinations", "저장소와 클러스터·네임스페이스",
     [("허용 목록에 있음: 다음 단계", OK), ("InvalidSpecError", BAD)]),
    ("동기화", "매니페스트를 렌더링한 뒤",
     "리소스 종류 목록", "화이트리스트와 블랙리스트",
     [("허용된 종류: 클러스터에 적용", OK), ("not permitted in project: Failed", BAD)]),
]

for y, (a1, a2, b1, b2, outs) in zip(YS, rows):
    cy = y + RH / 2
    d.tone(C1X, y, C1W, RH, INFO, 6, "14", 1.1)
    d.t(C1X + C1W / 2, y + 46, a1, 12.5, INK, KR, "middle", 600)
    d.t(C1X + C1W / 2, y + 72, a2, 12, MUTED)
    d.tone(C2X, y, C2W, RH, ACC, 6, "14", 1.4)
    d.t(C2X + C2W / 2, y + 46, b1, 12.5, INK, KR if "종류" in b1 else MONO, "middle", 600)
    d.t(C2X + C2W / 2, y + 72, b2, 12, MUTED)
    d.path(f"M {C1X + C1W + 2} {cy} L {C2X - 2} {cy}", MUTED, 1.4, m="ar")
    for i, (t1, c) in enumerate(outs):
        oy = y + 4 + i * 52
        d.tone(C3X, oy, C3W, 46, c, 6, "14", 1.2)
        d.t(C3X + C3W / 2, oy + 28, t1, 12, INK, KR, "middle", 600)
        ty = oy + 23
        d.path(f"M {C2X + C2W + 2} {cy} L {C2X + C2W + 18} {cy} L {C2X + C2W + 18} {ty} L {C3X - 2} {ty}", MUTED, 1.4, m="ar")

d.legend(392, [("시점", INFO), ("프로젝트 대조", ACC), ("통과", OK), ("거부", BAD)])
d.save("08-01.project-checks.svg")
