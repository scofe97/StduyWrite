# 10-03 §1 — 어느 지점에서 무엇이 갱신되는가
# 짝 도식(filesystem-resize-layers)이 '누가 무엇을' 을 맡으므로, 이쪽은 시간축만 본다.
# 사용자가 보는 값이 언제 바뀌는지가 축이어야 "미뤄진다"는 말이 눈에 잡힌다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 10-03",
      "숫자가 바뀌는 시점이 서로 다르다",
      "apply 는 즉시 받아들여지지만 그것은 요구가 적힌 것뿐이다. 실제 확장은 두 층에서 차례로 일어나고, "
      "사용자가 보는 값도 그 순서대로 갱신된다.",
      "PVC 1Gi → 3Gi")

X = lambda i: 160 + i * 240
EV = [("kubectl apply", "spec.resources 가 3Gi 로", INFO),
      ("블록 디바이스 확장", "CSI 컨트롤러가 볼륨을 키운다", OK),
      ("FileSystemResizePending", "파드를 기다린다", WARN),
      ("파일시스템 확장", "그 노드에서 resize2fs", ACC),
      ("CAPACITY 3Gi", "status 가 따라온다", ACC)]
for i, (t, s, c) in enumerate(EV):
    cx = X(i)
    d.line(cx, 300, cx, 340, RULE, 1.0)
    if c is ACC:
        d.o.append(f'<rect x="{cx-110}" y="196" width="220" height="88" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(cx - 110, 196, 220, 88, "#161B22", c, 1.1, 6)
    d.t(cx, 228, ddx.fit(t, 12, 200, t), 12, c, KR if any('가' <= ch <= '힣' for ch in t) else MONO,
        "middle", 600)
    d.t(cx, 254, ddx.fit(s, 10, 196, s), 10, MUTED, KR)
d.line(X(0) - 40, 340, X(4) + 40, 340, RULE, 1.0)
for i in range(4):
    d.path(f"M {X(i)+16} 340 L {X(i+1)-20} 340", MUTED, 1.3, m="ar")

d.t(X(2), 392, "여기서 멈춰 있을 수 있다 — 파드가 없으면 2 층이 시작되지 않는다", 11, WARN, KR)
d.t(X(3) + 120, 440, "df 로 본 크기가 이때 늘어난다", 11, ACC, KR, "middle")

d.t(24, 512, "그래서 CAPACITY 가 3Gi 인데 컨테이너 안 df 는 1Gi 로 보이는 구간이 생긴다. "
             "둘이 어긋난 것이 아니라 서로 다른 층을 말하고 있다.", 11, MUTED, KR, "start")
d.t(24, 534, "줄이는 방향은 지원하지 않는다 — 늘리는 것만 된다.", 11, MUTED, KR, "start")
d.legend(560, [("요구", INFO), ("1 층", OK), ("기다리는 구간", WARN), ("2 층과 그 결과", ACC)])
d.save("10-03-resize-flow.svg")
print("ok")
