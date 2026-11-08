# 04-01.probe-states — 프로브 결과가 컨테이너의 상태를 옮긴다
# 본문 요구: "startup 이 성공하면 readiness 가 Ready 를 켜고, readiness 가 failureThreshold 번 연속 실패하면 Ready=False 로
#           트래픽에서만 빠지고, liveness 나 startup 이 failureThreshold 번 실패하면 컨테이너가 재시작한다.
#           liveness 는 Ready 값과 별개로 계속 돌아 Ready=True·Ready=False 어느 쪽에서든 재시작으로 간다"
# 타입 스펙: type-state.md — 상태와 전이 조건이 요점이라 상태도로 그린다. 컨테이너를 죽이는 재시작 상태에만 focal 을 건다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 536
d = D(W, H, "PROBE STATES · WHAT MOVES A CONTAINER",
      "프로브 결과가 Ready 와 재시작 사이를 옮긴다",
      "startup 이 통과한 뒤 readiness 가 성공하면 Ready=True 가 되고(readiness 프로브가 없으면 startup 통과가 곧 Ready=True), readiness 실패는 Ready=False 로 트래픽에서만 뺀다. startup 이나 liveness 가 실패 횟수를 채우면 Ready 값과 상관없이 컨테이너를 재시작한다.",
      lead="readiness 는 Ready 를 오가게 하고 재시작으로 가는 길은 startup 과 liveness 뿐이다")

SW, SH = 176, 64


def state(cx, cy, title, sub, c, focal=False):
    x, y = cx - SW // 2, cy - SH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, SW, SH, PAPER2, c, 1.2, 8); tc = c
    d.t(cx, cy - 4, title, 13, tc, KR if not title.isascii() else MONO, "middle", 600)
    d.t(cx, cy + 16, sub, 11, MUTED, KR)


S1, S2, S3, S4 = (160, 220), (500, 220), (840, 220), (330, 388)
state(*S1, "기동 중", "startup 검사 · Ready=False", INFO)
state(*S2, "Ready=True", "서비스 대상에 포함", OK)
state(*S3, "Ready=False", "서비스 대상에서 제외", WARN)
state(*S4, "컨테이너 재시작", "재시작 정책 적용", ACC, focal=True)

d.o.append(f'<circle cx="40" cy="220" r="6" fill="{INK}"/>')
d.arrow([(48, 220), (68, 220)], MUTED, "ar", 1.4)

d.arrow([(252, 220), (404, 220)], MUTED, "ar", 1.5)
d.t(328, 204, "startup 성공 뒤 readiness 성공", 11, MUTED, KR, "middle", 600)
d.arrow([(592, 204), (748, 204)], WARN, "warn", 1.5)
d.t(670, 188, "readiness 연속 실패", 11, WARN, KR, "middle", 600)
d.arrow([(748, 236), (592, 236)], OK, "ok", 1.5)
d.t(670, 260, "readiness 성공", 11, OK, KR, "middle", 600)

d.arrow([(160, 252), (160, 388), (234, 388)], ACC, "acc", 1.5)
d.t(170, 330, "startup 실패", 11, ACC, KR, "start", 600)
d.arrow([(500, 252), (500, 388), (426, 388)], ACC, "acc", 1.5)
d.t(510, 330, "liveness 실패", 11, ACC, KR, "start", 600)
d.arrow([(840, 252), (840, 404), (426, 404)], ACC, "acc", 1.5)
d.t(850, 330, "liveness 실패", 11, ACC, KR, "start", 600)
d.arrow([(300, 356), (300, 300), (210, 300), (210, 256)], MUTED, "ar", 1.4)
d.t(312, 330, "컨테이너 재생성", 11, MUTED, KR, "start")

d.t(500, 460, "readiness 프로브가 없으면 기동 직후(startup 프로브가 있으면 통과 직후)부터 Ready=True 로 취급된다", 12, MUTED, KR)
d.legend(476, [("Ready=True", OK), ("트래픽 제외", WARN), ("컨테이너를 죽이는 상태", ACC)])
d.save("04-01.probe-states.svg")
print("ok probe-states")
