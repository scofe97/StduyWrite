# 15-02 §1 — 가용 파드 수가 바닥에 닿느냐
# 두 전략의 차이는 절차가 아니라 그 절차가 가용 수를 어디까지 떨어뜨리느냐다. 그러니
# 단계 나열이 아니라 가용 수를 세로 축으로 둔 두 줄이어야 한다.
# 타입 스펙: type-data-flow.md — 같은 네 단계를 두 전략으로 지나는 두 벌의 흐름. 단계마다 옛/새 파드 수가 바뀌고,
#           가용 수가 0 에 닿느냐가 갈림길이라 그 값을 칸마다 적었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 660, "KUBERNETES IN ACTION · 15-02",
      "가용 수가 0 에 닿느냐가 갈림길이다",
      "두 전략 모두 옛 파드를 새 파드로 바꾼다. 다른 것은 그 과정에서 요청을 받을 수 있는 파드가 "
      "몇 개 남느냐다.",
      "replicas 3 · 0.5 → 0.6")

def strip(y0, label, steps, c, focal, verdict, vc):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1152)
    BW = 168
    for i, (t, old, new, avail) in enumerate(steps):
        cx = 130 + i * 196
        d.t(cx, y0 + 52, t, 10, SOFT, KR)
        d.box(cx - BW // 2, y0 + 66, BW, 76, PAPER2, RULE, 1.0, 6)
        d.t(cx, y0 + 92, f"0.5 × {old}", 11, MUTED, MONO)
        d.t(cx, y0 + 114, f"0.6 × {new}", 11, MUTED, MONO)
        col = OK if avail > 0 else (ACC if focal else WARN)
        ddx.tag(d, cx, y0 + 166, f"가용 {avail}", col, 118)
        if i < len(steps) - 1:
            d.path(f"M {cx+BW//2+6} {y0+104} L {cx+196-BW//2-10} {y0+104}", MUTED, 1.3, m="ar")
    d.t(1090, y0 + 108, verdict, 11, vc, KR)

strip(100, "Recreate — 전부 한꺼번에", [
    ("시작", 3, 0, 3), ("전부 종료", 0, 0, 0), ("전부 생성", 0, 3, 0), ("준비 완료", 0, 3, 3),
], WARN, True, "가용 0 구간이 생긴다", ACC)

strip(340, "RollingUpdate — 하나씩", [
    ("시작", 3, 0, 3), ("하나 교체", 2, 1, 3), ("둘 교체", 1, 2, 3), ("완료", 0, 3, 3),
], OK, False, "가용 수가 유지된다", OK)

d.t(24, 596, "Recreate 는 옛 파드의 컨테이너가 다 끝난 뒤에야 새 파드를 만든다. 그 사이 서비스가 멈추므로, "
             "옛·새 버전이 동시에 돌면 안 되고 다운타임이 문제없을 때만 고른다.", 11, MUTED, KR, "start")
d.legend(618, [("요청을 받을 수 있다", OK), ("받을 수 없는 구간", ACC)])
d.save("15-02-recreate-vs-rollingupdate.svg")
print("ok")
