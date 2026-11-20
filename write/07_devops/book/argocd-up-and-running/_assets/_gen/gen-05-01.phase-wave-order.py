# 05-01 §3 — sync 한 번이 세 단계로 나뉘고, 단계 안에서는 wave 숫자가 작은 리소스부터, 앞 wave 가 Healthy 가 된 뒤에 다음 wave 가 적용되는 순서.
#            아래 줄은 PreSync Job 이 실패했을 때의 경로다.
# 본문 근거: 이 노트 ### 3 「순서」.
# 검증 근거: kind v0.31.0 에서 PreSync Job(wave 3), Deployment db(wave 1), Service db(wave 2), Deployment app(wave 3), Service app(wave 4), PostSync Job(wave 0 과 wave 1) 을
#            가진 Application 을 sync 했다. 객체 시각이 create-tables 완료 05:50:52 → db 생성 05:50:58 → Service db 생성 05:51:23(readiness 통과 뒤) → app 05:51:26 → Service app 05:51:28
#            → 스키마 Job 05:51:31 → wave 1 Job 05:51:44(스키마 Job 완료 05:51:39 뒤) 순서였다.
#            readiness 가 통과하지 않는 db 를 둔 Application 은 db 가 Ready 0/1 로 남고 wave 2 이후가 만들어지지 않았다.
#            종료 코드 1 의 PreSync Job precheck 은 Failed 가 되었고 Deployment 는 만들어지지 않았으며 SyncFail Job on-fail 이 Succeeded 가 되고 동작은 Failed 로 끝났다.
# 공식 근거: argo-cd v3.6.1 docs/user-guide/sync-waves.md("Order all resources according to their wave", "The phase / The wave they are in (lower values first) / By kind / By name",
#            "This is the first number where any resource is out-of-sync or unhealthy", "The current delay between each sync wave is 2 seconds").
# 타입 스펙: type-architecture — 왼쪽 단계에서 오른쪽 단계로 가는 흐름, 단계 안은 위에서 아래 wave 순서, 아래 줄은 실패 경로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 510
d = D(W, H, "ARGO CD UP AND RUNNING · 05-01 §3",
      "sync 한 번의 적용 순서",
      "왼쪽에서 오른쪽으로 PreSync, Sync, PostSync 세 단계가 차례로 실행된다. "
      "각 단계 안에서는 wave 숫자가 작은 리소스부터 적용되고 앞 wave 가 Healthy 가 된 뒤에 다음 wave 가 시작된다. "
      "아래 줄은 PreSync Job 이 실패한 경로로, SyncFail Job 이 실행되고 Sync 단계는 실행되지 않은 채 동작이 Failed 로 끝난다.",
      "wave 범위 예와 스키마 사용 사례를 겹쳐 그림")

BH, GAP = 40, 18          # wave 칸 높이, 칸 사이 간격
TOP = 96                  # 단계 칸 위쪽
CH = 36 + 4 * BH + 3 * GAP + 12   # 가장 긴 Sync 단계 기준 높이

phases = [
    ("PreSync", 24, 210, INFO, [("create-tables", "wave 3 · Job", INFO)]),
    ("Sync", 264, 270, ACC, [("db", "wave 1 · PVC·Deployment", ACC), ("db", "wave 2 · Service", ACC),
                              ("app", "wave 3 · Deployment", ACC), ("app", "wave 4 · Service", ACC)]),
    ("PostSync", 564, 292, INFO, [("스키마 적재", "wave 0 · Job", INFO), ("test-deployment", "wave 1 · Job", INFO)]),
]

for name, x, w, c, waves in phases:
    d.box(x, TOP, w, CH, c + "0A", c, 0.9, 8)
    d.t(x + 14, TOP + 24, name, 12.5, INK, MONO, "start", 600)
    for i, (rn, sub, bc) in enumerate(waves):
        by = TOP + 36 + i * (BH + GAP)
        d.tone(x + 14, by, w - 28, BH, bc, 6, "14", 1.2 if bc == ACC else 1.1)
        d.t(x + w / 2, by + 17, rn, 12, INK, KR, "middle", 600)
        d.t(x + w / 2, by + 33, sub, 12, MUTED)
        if i < len(waves) - 1:
            ax = x + w / 2
            d.path(f"M {ax} {by + BH + 1} L {ax} {by + BH + GAP - 2}", MUTED, 1.3, m="ar")
            d.t(ax + 10, by + BH + 13, "Healthy 후", 12, MUTED, KR, "start")

# 단계 사이 화살표
mid = TOP + 36 + BH / 2
d.path(f"M {24 + 210 + 2} {mid} L {264 - 2} {mid}", MUTED, 1.4, m="ar")
d.path(f"M {264 + 270 + 2} {mid} L {564 - 2} {mid}", MUTED, 1.4, m="ar")

# 실패 경로
FY = TOP + CH + 18
d.box(24, FY, 832, 74, BAD + "0A", BAD, 0.9, 8)
d.t(38, FY + 24, "PreSync 실패 경로", 12.5, INK, KR, "start", 600)
fb = [(210, 200, "precheck", "PreSync Job 실패", BAD),
      (450, 190, "on-fail", "SyncFail Job 실행", WARN),
      (656, 184, "동작 결과 Failed", "Sync 단계는 실행 안 됨", BAD)]
for x, w, t1, t2, c in fb:
    d.tone(x, FY + 14, w, 48, c, 6, "14", 1.2)
    d.t(x + w / 2, FY + 34, t1, 12, INK, KR, "middle", 600)
    d.t(x + w / 2, FY + 52, t2, 12, MUTED)
cy = FY + 38
d.path(f"M {210 + 200 + 2} {cy} L {450 - 2} {cy}", MUTED, 1.4, m="ar")
d.path(f"M {450 + 190 + 2} {cy} L {656 - 2} {cy}", MUTED, 1.4, m="ar")

LY = FY + 74 + 18
d.legend(LY, [("Hook Job", INFO), ("Sync 단계 리소스", ACC), ("실패 경로", BAD), ("SyncFail Job", WARN)])
assert H >= LY + 40, (H, LY + 40)
d.save("05-01.phase-wave-order.svg")
