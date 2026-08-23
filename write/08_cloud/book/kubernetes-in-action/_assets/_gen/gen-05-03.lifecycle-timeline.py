# 05-03 §생명주기 — 세 종류가 사는 구간이 다르다
# 본문 실측: 시작은 sidecar(:17) → init-work(:18) → main·helper(:25~26),
#           종료는 main SIGTERM 이 먼저이고 sidecar SIGTERM 이 3초 뒤.
#           (두 실측은 lifecycle-demo / shutdown-order-demo 로 서로 다른 실행이다.)
# 타입 스펙: 각자가 *얼마나 사는가* 가 요점이므로 사건 점이 아니라 구간 막대로 그린다
#           (type-gantt 의 스팬 골격). 같은 편의 다른 장들이 순서를 다루므로, 이 장은
#           수명의 길이 차이만 진다 — 사이드카 막대가 가장 길고 init 막대가 가장 짧다.
#           두 실측을 이어 붙였으므로 눈금 간격은 순서만 나타낸다고 축에 적어 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 596
d = D(W, H, "KUBERNETES IN ACTION · 05-03",
      "사이드카 막대가 가장 길고 init 막대가 가장 짧다",
      "네이티브 사이드카는 주 컨테이너보다 먼저 뜨고 맨 나중에 죽으므로 Pod 수명을 거의 다 "
      "덮는다. init 은 제 일을 끝내면 사라지고, 주 컨테이너는 그 사이에서만 산다.",
      lead="누가 먼저인가가 아니라 누가 얼마나 사는가를 본다 — 길이가 곧 보장의 범위다")

MARKS = [(200, "사이드카 시작", ":17"), (320, "init 시작", ":18"), (440, "init 완료", ""),
         (560, "주 컨테이너 시작", ":25~26"), (760, "주 컨테이너 SIGTERM", ""),
         (880, "사이드카 SIGTERM", "+3초")]
ROW_H, BAR_H = 68, 36

ddx.band(d, 104, 540, "사이드카가 아직 필요할 때 먼저 멈추지 않는다 — 그 보장이 막대 길이로 보인다")

for x, lab, stamp in MARKS:
    d.t(x, 190, lab, 10, SOFT, KR)
    if stamp:
        d.t(x, 204, stamp, 9, SOFT, MONO)
    d.line(x, 214, x, 452, RULE, 0.8, "4 6")
d.line(60, 224, 940, 224, RULE, 0.8)

ROWS = [("네이티브 사이드카", 268, 200, 880, ACC, "Pod 수명을 거의 다 덮는다"),
        # 막대가 120px 뿐이라 라벨은 그 안에 드는 길이로 — fit 가드가 잡아 준다
        ("init 컨테이너", 336, 320, 440, INFO, "끝나면 사라진다"),
        ("주 컨테이너 main·helper", 404, 560, 760, OK, "이 사이에서만 산다")]
for name, cy, a, b, c, note in ROWS:
    d.t(184, cy + 4, name, 11, c, KR, "end", 600)
    d.o.append(f'<rect x="{a}" y="{cy-BAR_H//2}" width="{b-a}" height="{BAR_H}" rx="5" '
               f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t((a + b) // 2, cy + 5, ddx.fit(note, 11, b - a - 16, name), 11, c, KR)

d.t(60, 480, "시간 → (lifecycle-demo 의 시작과 shutdown-order-demo 의 종료를 이어 붙였다 — "
             "눈금 간격은 순서만 나타낸다)", 10, SOFT, KR, "start")
d.t(36, 512, "먼저 뜨는 것과 맨 나중에 죽는 것이 한 막대에 같이 들어 있다 — 그래서 로그 수집기나 "
             "프록시가 빈 구간 없이 곁을 지킨다.", 12, MUTED, KR, "start")
d.legend(556, [("네이티브 사이드카", ACC), ("init 컨테이너", INFO), ("주 컨테이너", OK)])
d.save("05-03-lifecycle-timeline.svg")
print("ok lifecycle-timeline")
