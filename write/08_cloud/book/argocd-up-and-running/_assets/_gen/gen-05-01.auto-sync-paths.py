# 05-01 §1 — 자동 동기화가 Git 쪽 변경과 클러스터 쪽 변경을 처리하는 길. 변경이 OutOfSync 로 판정된 뒤 어느 스위치가 결과를 가르는지 세 줄로 보인다.
# 본문 근거: 이 노트 ### 1 「시작 시점」.
# 검증 근거: kind v0.31.0 에 v3.6.1 을 설치하고 automated 를 켠 Application 에서 Git 의 ConfigMap 값을 바꿔 push 하자 sync 명령 없이 반영되었다.
#            prune: true 인 Application 에서 Git 에 없는 ConfigMap 이 자동으로 지워졌고, Prune=false 를 단 ConfigMap 은 남았다.
#            selfHeal 이 꺼진 Application 에서 kubectl patch 로 Git 에 있는 키의 값을 바꾸자 OutOfSync 가 40초 넘게 남았고, selfHeal 을 켜자 몇 초 안에 Git 값으로 돌아왔다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/auto_sync.md("automated sync will not delete resources", "changes that are made to the live cluster will not trigger automated sync"),
#            docs/faq.md("120 seconds + up to 60 seconds of jitter"), docs/operator-manual/argocd-cmd-params-cm.yaml(controller.self.heal.backoff.*).
# 타입 스펙: type-architecture — 왼쪽 원인에서 오른쪽 결과로 가는 한 방향 흐름, 줄마다 하나의 변경.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 458
d = D(W, H, "ARGO CD UP AND RUNNING · 05-01 §1",
      "자동 동기화가 세 변경을 처리하는 길",
      "맨 위 줄은 Git 에 push 한 변경이다. 자동 동기화를 켜면 OutOfSync 로 판정된 뒤 Git 값이 클러스터에 적용된다. "
      "가운데 줄은 Git 에서 지운 리소스이고 prune 이 켜져 있으면 클러스터에서 지워지며 꺼져 있으면 남는다. "
      "맨 아래 줄은 클러스터에서 직접 바꾼 값이고 selfHeal 이 켜져 있으면 Git 값으로 돌아오며 꺼져 있으면 OutOfSync 로 남는다.",
      "스위치마다 갈리는 결과")

# 칸 좌표
C1X, C1W = 24, 178
C2X, C2W = 236, 170
C3X, C3W = 440, 150
C4X, C4W = 624, 232
YS = [120, 218, 316]
RH = 78

for cx, label in ((C1X + C1W / 2, "변경의 원인"), (C2X + C2W / 2, "판정"), (C3X + C3W / 2, "결과를 가르는 스위치"), (C4X + C4W / 2, "결과")):
    d.t(cx, 108, label, 12, MUTED, KR, "middle", 600)

rows = [
    ("Git 에 push 한 변경", "매니페스트 수정", "저장소 조회 뒤", "최대 3분 간격", "automated", "자동 동기화 켜짐",
     [("Git 값을 클러스터에 적용", "sync 명령 없이", OK)]),
    ("Git 에서 지운 리소스", "클러스터에는 남아 있음", "저장소 조회 뒤", "Git 과 클러스터 비교", "prune", "기본은 꺼짐",
     [("켜짐: 클러스터에서 삭제", None, OK), ("꺼짐: 클러스터에 남음", None, WARN)]),
    ("클러스터에서 바꾼 값", "kubectl 로 직접 수정", "변경 감지 뒤", "Git 과 클러스터 비교", "selfHeal", "기본은 꺼짐",
     [("켜짐: Git 값으로 복구", None, OK), ("꺼짐: OutOfSync 로 남음", None, WARN)]),
]

for y, (a1, a2, b1, b2, c1, c2, outs) in zip(YS, rows):
    cy = y + RH / 2
    d.tone(C1X, y, C1W, RH, INFO, 6, "14", 1.1)
    d.t(C1X + C1W / 2, y + 32, a1, 12.5, INK, KR, "middle", 600)
    d.t(C1X + C1W / 2, y + 55, a2, 12, MUTED)
    d.tone(C2X, y, C2W, RH, SOFT, 6, "14", 1.1)
    d.t(C2X + C2W / 2, y + 32, "OutOfSync 판정", 12.5, INK, KR, "middle", 600)
    d.t(C2X + C2W / 2, y + 55, b1, 12, MUTED)
    d.tone(C3X, y, C3W, RH, ACC, 6, "14", 1.4)
    d.t(C3X + C3W / 2, y + 32, c1, 12.5, INK, MONO, "middle", 600)
    d.t(C3X + C3W / 2, y + 55, c2, 12, MUTED)
    d.path(f"M {C1X + C1W + 2} {cy} L {C2X - 2} {cy}", MUTED, 1.4, m="ar")
    d.path(f"M {C2X + C2W + 2} {cy} L {C3X - 2} {cy}", MUTED, 1.4, m="ar")
    if len(outs) == 1:
        t1, t2, c = outs[0]
        d.tone(C4X, y, C4W, RH, c, 6, "14", 1.2)
        d.t(C4X + C4W / 2, y + 32, t1, 12.5, INK, KR, "middle", 600)
        d.t(C4X + C4W / 2, y + 55, t2, 12, MUTED)
        d.path(f"M {C3X + C3W + 2} {cy} L {C4X - 2} {cy}", MUTED, 1.4, m="ar")
    else:
        for i, (t1, _, c) in enumerate(outs):
            oy = y + i * 42
            d.tone(C4X, oy, C4W, 36, c, 6, "14", 1.2)
            d.t(C4X + C4W / 2, oy + 23, t1, 12, INK, KR, "middle", 600)
            ty = oy + 18
            d.path(f"M {C3X + C3W + 2} {cy} L {C3X + C3W + 17} {cy} L {C3X + C3W + 17} {ty} L {C4X - 2} {ty}", MUTED, 1.4, m="ar")

d.legend(414, [("변경 원인", INFO), ("판정", SOFT), ("스위치", ACC), ("반영됨", OK), ("그대로 남음", WARN)])
d.save("05-01.auto-sync-paths.svg")
