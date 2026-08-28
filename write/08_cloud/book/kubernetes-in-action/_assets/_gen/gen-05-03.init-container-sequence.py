# 05-03 §init — 순차와 병렬이 한 줄에 붙어 있다
# 본문: "일반 init 컨테이너는 정의된 순서대로 완료되어야 다음 단계로 넘어갑니다."
#       마지막 init 이 끝난 뒤에야 주 컨테이너들이 (순서 보장 없이) 시작한다.
# 타입 스펙: type-gantt.md — 시간축 위의 두 구간이라 스팬. 앞 구간은 하나씩 이어지고 뒤 구간은 겹친다 —
#           그 대비가 요점이므로 겹침 자체를 막대의 겹침으로 그린다. 상자를 나란히 놓고
#           화살표로 잇는 옛 방식으로는 '병렬' 이 그림에 나타나지 않는다.
#           하나의 시간축 위에 다섯 구간 막대가 놓이고, 앞 셋은 겹치지 않고 뒤 둘은 완전히 겹친다 —
#           겹침 여부가 곧 순차와 병렬이라 시간 겹침을 보이는 gantt 계약 그대로다.
#           마지막 init 완료 지점의 세로 점선이 정본의 마일스톤 표시에 해당한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 584
d = D(W, H, "KUBERNETES IN ACTION · 05-03",
      "init 은 하나씩 이어지고, 주 컨테이너는 한꺼번에 뜬다",
      "init 컨테이너는 정의된 순서대로 하나가 끝나야 다음이 시작한다. 마지막 init 이 완료된 "
      "뒤에야 주 컨테이너들이 시작하고, 그들 사이에는 순서 보장이 없다.",
      lead="앞 구간은 겹치지 않고 뒤 구간은 겹친다 — 막대가 겹치는지가 곧 병렬 여부다")

X0, XEND = 240, 940
GATE = 660
ROW_H, BAR_H = 52, 30

ddx.band(d, 104, 528, "마지막 init 이 성공해야 이 문이 열린다 — 실패하면 주 컨테이너는 시작조차 못 한다")

d.t(X0, 190, "시간 →", 10, SOFT, KR, "start")
d.line(60, 204, XEND, 204, RULE, 0.8)

ROWS = [("1st init", 240, 380, INFO, "끝나야 다음이 시작한다"),
        ("2nd init", 380, 520, INFO, "앞이 성공해야 시작한다"),
        ("last init", 520, GATE, INFO, "여기까지 순차다"),
        ("Container A", GATE, XEND, OK, "동시에 시작한다"),
        ("Container B", GATE, XEND, OK, "순서 보장은 없다")]
for i, (name, a, b, c, note) in enumerate(ROWS):
    cy = 244 + i * ROW_H
    d.t(224, cy + 4, name, 11, c, MONO, "end", 600)
    d.o.append(f'<rect x="{a}" y="{cy-BAR_H//2}" width="{b-a}" height="{BAR_H}" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
    d.t((a + b) // 2, cy + 4, ddx.fit(note, 10, b - a - 16, name), 10, c, KR)

d.path(f"M {GATE} 212 L {GATE} 480", ACC, 1.4, dash="6 5")
d.chip(GATE, 220, "마지막 init 완료 — 여기서 문이 열린다", ACC, 11)

# 대괄호는 실제 막대 범위를 감싼다(행 cy 244·296·348 / 400·452, 막대 높이 30).
# x 는 52 로 — 108 에 두면 라벨이 행 이름("Container B")과 겹친다.
ddx.bracket(d, 52, 229, 363, "순차", INFO)
ddx.bracket(d, 52, 385, 467, "병렬", OK)

# 마지막 행 막대가 437~467 을 쓴다 — 산문은 그 아래로
d.t(36, 496, "init 이 도는 동안 주 컨테이너의 state 는 waiting/PodInitializing 이다 — "
             "아직 시작 전이라는 뜻이다", 12, MUTED, KR, "start")
d.legend(544, [("순차로 도는 init", INFO), ("한꺼번에 뜨는 주 컨테이너", OK), ("문이 열리는 시점", ACC)])
d.save("05-03-init-container-sequence.svg")
print("ok init-container-sequence")
