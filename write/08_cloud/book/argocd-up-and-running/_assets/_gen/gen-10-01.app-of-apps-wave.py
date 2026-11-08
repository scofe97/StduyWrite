# 10-01 §2 — App-of-Apps 의 부모는 자식 Application 을 wave 순서로 만든다. Application 헬스 체크가 없으면 다음 wave 가 2초 뒤에 시작하고, 있으면 앞 자식이 Healthy 가 된 뒤에 시작한다.
# 본문 근거: 이 노트 ### 2 「App-of-Apps — 부모가 wave 순서로 자식을 만들고 Healthy 를 기다린다」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 database(wave 1, 준비 25초)·backend(wave 2, 준비 15초)·frontend(wave 3, 준비 5초) 자식을 가진 부모를 적용했다.
#            argocd-cm 에 Application 헬스 체크가 없을 때 자식의 생성 시각 간격은 두 번 모두 2초였다(16:14:05 / :07 / :09).
#            resource.customizations.health.argoproj.io_Application 을 더하면 database 에서 backend 까지 27초와 26초, backend 에서 frontend 까지 16초와 17초였다(두 번).
# 공식 근거: argo-cd v3.6.1 docs/user-guide/sync-waves.md(wave 사이 2초 지연), docs/operator-manual/health.md(Application 헬스 Lua), docs/operator-manual/cluster-bootstrapping.md.
# 타입 스펙: type-architecture — 왼쪽 부모에서 오른쪽 자식으로 가는 한 방향 흐름, 줄마다 하나의 설정.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "ARGO CD UP AND RUNNING · 10-01 §2",
      "부모가 자식 Application 을 만드는 간격",
      "위쪽 줄은 argocd-cm 에 Application 헬스 체크가 없을 때다. 부모가 wave 1 database, wave 2 backend, wave 3 frontend 자식을 2초 간격으로 만들고 앞 자식이 Progressing 이어도 기다리지 않는다. "
      "아래쪽 줄은 Application 헬스 체크를 더했을 때다. 앞 자식이 Healthy 가 되어야 다음 자식을 만들어서 database 에서 backend 까지 약 27초, backend 에서 frontend 까지 약 16초가 걸린다.",
      "순서를 정하는 것은 wave 번호와 Application 의 헬스다")

BW, BH = 160, 84
XS = [24, 240, 456, 672]
YS = [124, 262]
rows = [
    ("Application 헬스 체크 없음", BAD, ["2초", "2초", None]),
    ("Application 헬스 체크 있음", OK, ["27초", "16초", None]),
]
boxes = [("parent", "부모 Application", ACC),
         ("database", "wave 1 · 준비 25초", INFO),
         ("backend", "wave 2 · 준비 15초", INFO),
         ("frontend", "wave 3 · 준비 5초", INFO)]

for y, (rl, rc, gaps) in zip(YS, rows):
    d.t(24, y - 12, rl, 12.5, rc, KR, "start", 600)
    cy = y + BH / 2
    for i, (x, (nm, sub, c)) in enumerate(zip(XS, boxes)):
        d.tone(x, y, BW, BH, c, 6, "14", 1.4 if i == 0 else 1.1)
        d.t(x + BW / 2, y + 38, nm, 13, INK, MONO, "middle", 600)
        d.t(x + BW / 2, y + 62, sub, 12, MUTED)
        if i < 3:
            nx = XS[i + 1]
            d.path(f"M {x + BW + 2} {cy} L {nx - 2} {cy}", MUTED, 1.4, m="ar")
            if i >= 1:
                d.chip((x + BW + nx) / 2, cy - 18, gaps[i - 1], rc, size=12)
    if True:
        pass

d.legend(392, [("부모", ACC), ("자식 Application", INFO), ("기다리지 않음", BAD), ("Healthy 대기", OK)])
d.save("10-01.app-of-apps-wave.svg")
