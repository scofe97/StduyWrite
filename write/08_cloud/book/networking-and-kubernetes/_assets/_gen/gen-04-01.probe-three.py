# 04-01.probe-three — 세 프로브는 실패했을 때 무엇을 하느냐로 갈린다
# 본문 요구: 표 "프로브 | 실패 시 | 용도" 세 행 그대로. 절 요약이 "실패했을 때 무엇을
#           하느냐로 갈립니다" 이므로 실패 시 동작을 가운데 축으로 둔다.
# 타입 스펙: type-dp-security-matrix.md — 행이 프로브 셋, 열이 실패 시·용도 — 본문 표 세 행 그대로
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 528   # 행 3개가 424 에서 끝나므로 주석·범례는 그 아래
d = D(W, H, "PROBES · WHAT HAPPENS ON FAILURE",
      "세 프로브는 실패했을 때 무엇을 하느냐로 갈린다",
      "readiness 는 트래픽만 끊고 liveness 는 컨테이너를 죽이며 startup 은 나머지를 유예시킨다.",
      lead="컨테이너를 죽이는 것은 liveness 하나뿐이다 — 외부 의존을 여기에 걸면 남의 장애가 내 재시작이 된다")

LX, LW, C1, C2, CW1, CW2 = 32, 208, 256, 604, 332, 364
ROWS = [
    ("readinessProbe", "죽이지 않고 실패 기록 → Endpoints 에서 제외", "지금 트래픽 받아도 되는가", INFO),
    ("livenessProbe", "Kubelet 이 컨테이너를 종료 (재시작 정책)", "재시작해야 하는 상태인가", ACC),
    ("startupProbe", "성공 전까지 다른 프로브 비활성 · 실패하면 종료", "느린 기동에 유예를 줄까", INFO),
]
d.t(LX + LW // 2, 148, "프로브", 12, SOFT, KR, "middle", 600)
d.t(C1 + CW1 // 2, 148, "실패하면", 12, SOFT, KR, "middle", 600)
d.t(C2 + CW2 // 2, 148, "묻는 질문", 12, SOFT, KR, "middle", 600)

RY, RH = 172, 76
for i, (nm, fail, ask, c) in enumerate(ROWS):
    y = RY + i * (RH + 12)
    if c is ACC:
        d.tone(LX, y, LW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(LX, y, LW, RH, PAPER2, c, 1.1, 6)
    d.t(LX + LW // 2, y + 44, nm, 13, c, MONO, "middle", 600)
    for x, w, txt in ((C1, CW1, fail), (C2, CW2, ask)):
        d.box(x, y, w, RH, PAPER2, RULE, 0.9, 6)
        d.t(x + w // 2, y + 44, ddx.fit(txt, 12, w - 24, txt), 12,
            ACC if c is ACC else MUTED, KR)

d.t(36, 456, "메인 페이지를 liveness 로 걸면 DB 장애가 컨테이너 재시작이 되고, CrashLoopBackoff 가 겹쳐 전면 다운으로 커진다",
    12, MUTED, KR, "start")
d.legend(468, [("트래픽만 끊는다", INFO), ("컨테이너를 죽인다", ACC)])
d.save("04-01.probe-three.svg")
print("ok probe-three")
