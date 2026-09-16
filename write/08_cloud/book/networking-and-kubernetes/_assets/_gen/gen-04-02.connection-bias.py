# 04-02.connection-bias — 롤링 업데이트 뒤 장수 연결이 한쪽으로 쏠리는 과정
# 본문 요구: "1단은 Pod X 와 Y 가 연결을 50 씩 … 2단에서 X 가 내려가고 그 50 이 끊깁니다 … 남은 백엔드 둘로 25 씩 …
#           Y 가 쥐고 있던 50 은 규칙을 다시 지나지 않습니다 … 3단에서 Y 는 75 를 갖고 Z 는 25 … 막대 길이가 그 차이"
# 타입 스펙: type-bar — 가로 막대, 길이 = 연결 수(1 연결 = 6px, 0 기준). 같은 막대를 세 단에 다시 그려
#           어느 몫이 규칙을 지나고 어느 몫이 안 지나는지를 막대 조각으로 보인다(stacked 변형).
#           손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다. 사선 화살표를 없애고 막대로 바꿨다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 552
d = D(W, H, "iptables MODE · WHY LONG-LIVED CONNECTIONS SKEW",
      "확률은 새 연결에만 걸린다",
      "기존 연결은 확률 규칙을 다시 지나지 않으므로 살아남은 Pod 에 그대로 남고, 끊겨서 재수립된 연결만 "
      "규칙을 지나 나뉘기 때문에 롤링 업데이트 뒤 트래픽이 한쪽으로 쏠린다.",
      lead="막대 길이 = 연결 수 · 확률은 반반인데 결과는 3 대 1")

PX0, UNIT, BARH = 256, 6, 24        # 막대 시작 x, 1 연결 폭, 막대 높이
STAGE_X = 32
POD_X = 236                         # Pod 이름 오른쪽 정렬 x


def bar(y, n, c, x0=PX0, dash=None, op="22"):
    w = n * UNIT
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    d.o.append(f'<rect x="{x0}" y="{y}" width="{w}" height="{BARH}" rx="3" fill="{c}{op}" stroke="{c}" stroke-width="1.1"{ds}/>')
    return x0 + w


def stage(y0, title, c):
    d.t(STAGE_X, y0 + 30, title, 13, c, KR, "start", 600)


# 1단 — 업데이트 전
Y1 = 104
stage(Y1, "1 · 업데이트 전", MUTED)
for i, pod in enumerate(["Pod X", "Pod Y"]):
    y = Y1 + 16 + i * 36
    d.t(POD_X, y + 17, pod, 12, MUTED, MONO, "end")
    e = bar(y, 50, INFO)
    d.t(e + 12, y + 17, "50", 12, INFO, MONO, "start", 600)
d.line(32, 196, 968, 196, RULE, 0.8)

# 2단 — 롤링 업데이트
Y2 = 208
stage(Y2, "2 · 롤링 업데이트", MUTED)
yx = Y2 + 16
d.t(POD_X, yx + 17, "Pod X", 12, BAD, MONO, "end")
e = bar(yx, 50, BAD, dash="5 4", op="0A")
d.t(PX0 + 25 * UNIT, yx + 17, "종료 · 50 끊김", 12, BAD, KR, "middle", 600)
yy = Y2 + 52
d.t(POD_X, yy + 17, "Pod Y", 12, MUTED, MONO, "end")
e = bar(yy, 50, INFO)
d.t(e + 12, yy + 17, "50 · 규칙 안 지남", 12, INFO, KR, "start", 600)

# 확률 규칙 — 끊긴 50 만 지난다
RX, RY, RW, RH = 256, 312, 440, 44
d.box(RX, RY, RW, RH, PAPER2, WARN, 1.2, 6)
d.t(RX + 20, RY + 27, "KUBE-SVC 확률 규칙", 13, WARN, KR, "start", 600)
d.t(RX + RW - 20, RY + 27, "재접속 50 → 25 · 25", 12, MUTED, KR, "end")
# 끊긴 막대 오른쪽 끝에서 나와 Pod Y 막대를 비껴 규칙 상자 오른쪽 변으로 들어간다
XJ = 752
d.arrow([(PX0 + 50 * UNIT + 8, yx + BARH // 2), (XJ, yx + BARH // 2), (XJ, RY + RH // 2), (RX + RW + 10, RY + RH // 2)],
        BAD, "bad", 1.3, "5 4")
d.line(32, 376, 968, 376, RULE, 0.8)

# 3단 — 업데이트 후
Y3 = 388
stage(Y3, "3 · 업데이트 후", MUTED)
yy3 = Y3 + 16
d.t(POD_X, yy3 + 17, "Pod Y", 12, ACC, MONO, "end")
e1 = bar(yy3, 50, INFO)
e2 = bar(yy3, 25, WARN, x0=e1)
d.o.append(f'<rect x="{PX0-4}" y="{yy3-4}" width="{e2-PX0+8}" height="{BARH+8}" rx="5" fill="none" stroke="{ACC}" stroke-width="1.4"/>')
d.t(e2 + 16, yy3 + 17, "75 · 기존 50 + 새 25", 12, ACC, KR, "start", 600)
yz = Y3 + 52
d.t(POD_X, yz + 17, "Pod Z", 12, MUTED, MONO, "end")
e = bar(yz, 25, WARN)
d.t(e + 12, yz + 17, "25 · 새 연결", 12, WARN, KR, "start", 600)
d.arrow([(RX + RW // 2, RY + RH + 4), (RX + RW // 2, yy3 - 10)], WARN, "warn", 1.4)

d.legend(484, [("규칙을 안 지나는 기존 연결", INFO), ("규칙을 지나는 새 연결", WARN), ("끊긴 연결", BAD), ("쏠린 결과", ACC)])
d.save("04-02.connection-bias.svg")
print("ok connection-bias")
