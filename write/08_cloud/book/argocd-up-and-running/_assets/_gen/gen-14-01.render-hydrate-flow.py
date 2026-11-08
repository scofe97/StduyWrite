# 14-01 §3 — dry 소스의 커밋을 Source Hydrator 가 렌더해 syncSource 브랜치에 manifest.yaml 로 커밋하고, Argo CD 는 그 브랜치만 동기화한다. 매니페스트가 그대로면 새 커밋 없이 git note 만 옮긴다.
# 본문 근거: 이 노트 「Source Hydrator 설정과 출력」「hydrateTo 와 승격 경계」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1(install-with-hydrator.yaml)을 설치해 확인했다.
#            hydrated 브랜치에 overlays/dev/manifest.yaml·hydrator.metadata·README.md 가 생겼고, 주석만 바꾼 dry 커밋(50d433d)은 새 hydrated 커밋 없이 note 의 dry SHA 만 옮겼다.
#            hydrateTo 를 지정한 web-prod 는 environments/prod-next 에만 push 했다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/source-hydrator.md 「Git Note-based Hydration State Tracking」「Pushing to a "Staging" Branch」.
# 타입 스펙: type-architecture — 왼쪽 dry 원본에서 오른쪽 클러스터로 가는 한 방향 흐름, hydrator 아래로 갈라지는 두 가지 경우.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 488
d = D(W, H, "ARGO CD UP AND RUNNING · 14-01 §3",
      "dry 소스가 hydrated 브랜치를 거쳐 클러스터에 닿는 길",
      "왼쪽의 dry 소스 브랜치에 커밋이 들어오면 가운데 Source Hydrator 가 렌더하고 commit server 가 결과를 push 한다. "
      "결과는 syncSource 브랜치의 manifest.yaml 로 커밋되고 Argo CD 는 그 브랜치만 읽어 클러스터에 동기화한다. "
      "렌더 결과가 이전과 같으면 새 커밋 없이 git note 의 dry SHA 만 옮기고, hydrateTo 가 있으면 대기 브랜치에만 push 한다.",
      "Argo CD 는 렌더한 결과 브랜치만 동기화합니다")

BOX_Y, BOX_H, MID = 164, 142, 235
A_X, A_W = 24, 156
B_X, B_W = 214, 196
C_X, C_W = 444, 212
D_X, D_W = 692, 164

d.tone(A_X, BOX_Y, A_W, BOX_H, INFO, 6, "14", 1.1)
d.t(A_X + A_W / 2, BOX_Y + 38, "dry 소스", 12.5, INK, KR, "middle", 600)
d.t(A_X + A_W / 2, BOX_Y + 68, "main 브랜치", 12, MUTED, MONO)
d.t(A_X + A_W / 2, BOX_Y + 94, "overlays/dev", 11.5, MUTED, MONO)
d.t(A_X + A_W / 2, BOX_Y + 118, "새 커밋", 12, MUTED)

d.box(B_X, BOX_Y, B_W, BOX_H, PAPER2, RULE, 1.0)
d.t(B_X + B_W / 2, BOX_Y + 38, "Source Hydrator", 12.5, INK, KR, "middle", 600)
d.t(B_X + B_W / 2, BOX_Y + 68, "commit server 가 push", 12, MUTED)
d.t(B_X + B_W / 2, BOX_Y + 96, "kustomize build 결과", 11.5, MUTED, MONO)
d.t(B_X + B_W / 2, BOX_Y + 120, "push 용 Secret 사용", 12, MUTED)

d.tone(C_X, BOX_Y, C_W, BOX_H, ACC, 6, "14", 1.4)
d.t(C_X + C_W / 2, BOX_Y + 38, "syncSource 브랜치", 12.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, BOX_Y + 66, "예: environments/dev", 11.5, MUTED, MONO)
d.t(C_X + C_W / 2, BOX_Y + 92, "manifest.yaml", 11.5, MUTED, MONO)
d.t(C_X + C_W / 2, BOX_Y + 114, "hydrator.metadata", 11.5, MUTED, MONO)

d.tone(D_X, BOX_Y, D_W, BOX_H, OK, 6, "14", 1.2)
d.t(D_X + D_W / 2, BOX_Y + 38, "클러스터", 12.5, INK, KR, "middle", 600)
d.t(D_X + D_W / 2, BOX_Y + 68, "Argo CD 가", 12, MUTED)
d.t(D_X + D_W / 2, BOX_Y + 92, "그 브랜치를", 12, MUTED)
d.t(D_X + D_W / 2, BOX_Y + 116, "동기화", 12, MUTED)

for x1, x2 in ((A_X + A_W, B_X), (B_X + B_W, C_X), (C_X + C_W, D_X)):
    d.path(f"M {x1 + 2} {MID} L {x2 - 2} {MID}", MUTED, 1.4, m="ar")

# 렌더 결과가 같을 때
DY, DH = 368, 70
N_W = 150
d.tone(B_X, DY, N_W, DH, WARN, 6, "14", 1.2)
d.t(B_X + N_W / 2, DY + 30, "git note 만 갱신", 11.5, INK, KR, "middle", 600)
d.t(B_X + N_W / 2, DY + 52, "새 커밋 없음", 11.5, MUTED)
d.path(f"M {B_X + N_W / 2} {BOX_Y + BOX_H + 2} L {B_X + N_W / 2} {DY - 2}", MUTED, 1.4, m="ar")
d.chip(B_X + N_W / 2, 326, "렌더 결과 같음", MUTED, 11)

# hydrateTo — 같은 Application 의 대기 브랜치(저장소·경로는 syncSource 에서 물려받음). Hydrator 에서 곧바로 간다.
d.tone(C_X, DY, C_W, DH, SOFT, 6, "22", 1.2)
d.t(C_X + C_W / 2, DY + 26, "대기 브랜치 (hydrateTo)", 11.5, INK, KR, "middle", 600)
d.t(C_X + C_W / 2, DY + 46, "예: environments/dev-next", 11.5, MUTED, MONO)
d.t(C_X + C_W / 2, DY + 63, "누가 옮기기 전엔 동기화 없음", 11, MUTED)
HX = B_X + B_W - 24
d.path(f"M {HX} {BOX_Y + BOX_H + 2} L {HX} {DY + DH / 2} L {C_X - 2} {DY + DH / 2}", MUTED, 1.4, m="ar")
d.chip(HX, 352, "hydrateTo 지정", MUTED, 11)

d.legend(448, [("dry 소스", INFO), ("Hydrator", PAPER2), ("sync 브랜치", ACC), ("동기화", OK), ("노트만", WARN), ("대기", SOFT)])
d.save("14-01.render-hydrate-flow.svg")
