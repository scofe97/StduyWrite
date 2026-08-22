# 06-01 §3 — condition 넷은 성격이 갈린다
# 본문: "PodScheduled 와 Initialized 는 ... 곧 충족되고 남은 생애 동안 그대로 유지됩니다.
#        반면 Ready 와 ContainersReady 는 생애 동안 여러 번 바뀔 수 있습니다."
# 타입 스펙: type-gantt.md — 시간축 위의 스팬이라 간트 골격을 빌린다(왼쪽 라벨 열 180px ·
#           행 높이 · 막대는 행 안에서 세로 가운데 · phase grouping 존). 다만 막대가 작업이
#           아니라 True/False 구간이므로 색은 상태색 축을 쓴다. 성격이 갈리는 것이 본문의
#           요점이므로 두 존으로 묶어 그 갈림을 구조로 드러낸다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 556
d = D(W, H, "KUBERNETES IN ACTION · 06-01",
      "condition 넷은 성격이 갈린다 — 한 번 서면 유지 vs 여러 번 바뀜",
      "PodScheduled 와 Initialized 는 한 번 True 가 되면 Pod 의 남은 생애 동안 유지된다. "
      "ContainersReady 와 Ready 는 생애 동안 여러 번 바뀐다.",
      lead="phase 만 보면 '돌고 있네'지만, conditions 를 봐야 '트래픽 받을 준비는 안 됐네'를 안다")

# 전이 시점은 반드시 눈금 위에 둔다. 눈금에 없는 x 에 막대 경계를 두면 그 좌표를
# 설명할 근거가 없어진다 — 계약이 금지하는 눈대중이다. stride 108px.
X0, X1 = 240, 952
TICKS = [240, 348, 456, 564, 672, 780, 888]
TICK_LABELS = ["① 생성", "② 스케줄링", "③ 샌드박스 준비", "④ init 완료",
               "⑤ 컨테이너 준비", "⑥ gate 통과", "⑦ 하나가 실패"]
ROW_H, BAR_H = 44, 26

ddx.band(d, 104, 500, "성격이 갈리므로 진단할 때 보는 자리도 다르다")

for x, lab in zip(TICKS, TICK_LABELS):
    d.t(x, 168, lab, 10, SOFT, KR)
d.line(40, 184, X1, 184, RULE, 0.8)

# 존 둘 — 본문이 말하는 성격의 갈림을 구조로 만든다
ZONES = [(196, 3, "한 번 True 가 되면 그대로 유지된다"),
         (348, 2, "생애 동안 여러 번 바뀔 수 있다")]
for zy, n, lab in ZONES:
    d.o.append(f'<rect x="40" y="{zy}" width="{X1-40}" height="{n*ROW_H}" rx="8" '
               f'fill="{RULE}" fill-opacity="0.03" stroke="{RULE}" stroke-width="1.0"/>')
    ddx.ring_label(d, 40, zy, lab, 11, SOFT, off=16)

# (이름, 행 y 중심, [(x시작, x끝, True인가)], focal 여부)
ROWS = [
    ("PodScheduled", 218, [(X0, 348, False), (348, X1, True)], False),
    ("PodReadyToStartContainers", 262, [(X0, 456, False), (456, X1, True)], False),
    ("Initialized", 306, [(X0, 564, False), (564, X1, True)], False),
    ("ContainersReady", 370, [(X0, 672, False), (672, 888, True), (888, X1, False)], False),
    ("Ready", 414, [(X0, 780, False), (780, 888, True), (888, X1, False)], True),
]
for name, cy, spans, focal in ROWS:
    d.t(224, cy + 4, name, 11, ACC if focal else INK, MONO, "end", 600)
    for a, b, on in spans:
        c = OK if on else BAD
        d.o.append(f'<rect x="{a}" y="{cy-BAR_H//2}" width="{b-a}" height="{BAR_H}" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
        if b - a >= 96:
            d.t((a + b) // 2, cy + 4, "True" if on else "False", 10, c, MONO)
    if focal:
        d.o.append(f'<rect x="40" y="{cy-ROW_H//2}" width="4" height="{ROW_H}" rx="2" fill="{ACC}"/>')

# 눈금 세로 안내선 — 어느 사건에서 무엇이 바뀌는지 눈으로 잇는다
for x in TICKS[1:]:
    d.line(x, 190, x, 436, RULE, 0.8, "4 6")

# 12px 한글 한 줄은 950px 을 넘기지 못한다 — 넘치면 overflow-check 가 잡는다. 두 줄로 나눈다.
d.t(36, 466, "PodReadyToStartContainers 는 1.29 에서 더해진 다섯 번째다 — 책 표에는 없고 "
             "실측(v1.35)에만 보인다.", 12, MUTED, KR, "start")
d.t(36, 486, "쿠버네티스는 새 관측 축이 필요할 때 기존 것을 바꾸지 않고 목록에 더한다.",
     12, MUTED, KR, "start")
d.legend(516, [("True", OK), ("False", BAD), ("본문이 짚는 행", ACC)])
d.save("06-01-pod-conditions-timeline.svg")
print("ok pod-conditions-timeline")
