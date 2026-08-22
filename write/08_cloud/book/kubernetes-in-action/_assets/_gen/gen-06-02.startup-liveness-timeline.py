# 06-02 §8 실측 — 같은 명령을 걸어도 실패 기록은 한쪽에만 남는다
# 본문: "같은 명령인데 startup 은 7번 실패 기록이 남고, liveness 는 단 한 번도 실패하지
#        않았습니다 — liveness 가 그 20초 동안 아예 실행되지 않았기 때문입니다."
#       "startup 이 7번 실패하는 사이에도 RESTARTS 는 0 이었습니다."
# 타입 스펙: 두 주체가 같은 시간축을 나눠 쓰므로 type-swimlane 의 레인 + 시간축. 레인마다
#           활성 구간이 갈리는 것이 요점이라 구간을 띠로 칠하고 인계 시점에 세로선을 세운다.
#           실패 7건의 정확한 초는 본문에 없으므로 개별 눈금으로 찍지 않는다 — 구간과 건수만 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 596
d = D(W, H, "KUBERNETES IN ACTION · 06-02",
      "같은 cat /tmp/ready 인데 실패 기록은 한쪽에만 남는다",
      "기동 20초 동안 파일이 없어 두 probe 다 실패할 명령인데, 이벤트에는 startup 실패 7건만 "
      "남고 liveness 실패는 0건이었다. liveness 가 그 구간에 아예 실행되지 않았기 때문이다.",
      lead="기동 실패는 startup 이 흡수하고, 뜬 뒤의 빠른 감지는 liveness 가 맡는 분업")

X0, PITCH = 240, 176            # 10초 = 176px
HANDOFF = X0 + 2 * PITCH        # 20s
XEND = X0 + 4 * PITCH           # 40s
TOP_CY, BOT_CY = 292, 404
BAND_H = 56

ddx.band(d, 104, 540, "활성 구간이 갈리므로 같은 명령이라도 한쪽에만 기록이 남는다")

for i in range(5):
    x = X0 + i * PITCH
    d.t(x, 196, f"{i*10}s", 10, SOFT, MONO)
d.line(40, 212, XEND, 212, RULE, 0.8)

def lane(cy, name, sub, spans):
    d.t(224, cy - 6, name, 12, INK, MONO, "end", 600)
    d.t(224, cy + 12, sub, 10, SOFT, MONO, "end")
    for a, b, c, label, dash in spans:
        d.o.append(f'<rect x="{a}" y="{cy-BAND_H//2}" width="{b-a}" height="{BAND_H}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.1"'
                   f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
        for j, line in enumerate(label):
            d.t((a + b) // 2, cy - 4 + j * 18, ddx.fit(line, 11, b - a - 20, name), 11,
                c if j == 0 else SOFT, KR)

lane(TOP_CY, "startup", "period=3s", [
    (X0, HANDOFF, BAD, ["실패 7회 — 파일이 없다", "예산 10 안이라 RESTARTS 는 0"], False),
    (HANDOFF, XEND, MUTED, ["성공 후 손을 뗀다"], True)])
lane(BOT_CY, "liveness", "period=5s", [
    (X0, HANDOFF, MUTED, ["비활성 — 실행되지 않는다", "실패 이벤트 0건"], True),
    (HANDOFF, XEND, OK, ["5초마다 감시"], False)])

# 인계 시점 — 두 레인을 관통하는 세로선 하나
d.path(f"M {HANDOFF} 220 L {HANDOFF} 448", ACC, 1.4, dash="6 5")
d.chip(HANDOFF, 236, "/tmp/ready 생성 · startup 성공", ACC, 11)
d.t(HANDOFF + 12, 466, "여기서 liveness 로 인계되고 READY 가 1/1 이 된다", 11, ACC, KR, "start")

d.t(36, 508, "startup 의 실패 7건은 예산(failureThreshold 10) 안이라 '아직 뜨는 중'으로 취급돼 "
             "컨테이너를 죽이지 않았다", 12, MUTED, KR, "start")
d.legend(556, [("실패가 기록된 구간", BAD), ("감시 중", OK), ("인계 시점", ACC)])
d.save("06-02-startup-liveness-timeline.svg")
print("ok startup-liveness-timeline")
