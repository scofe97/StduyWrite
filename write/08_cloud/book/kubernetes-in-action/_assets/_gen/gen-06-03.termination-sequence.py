# 06-03 §7 — 종료는 컨테이너마다 독립으로 진행되고, 셋 다 끝나야 Pod 가 지워진다
# 본문: "각 컨테이너 안에서는 PreStop hook → SIGTERM → 유예 시간 만료 시 SIGKILL 순서가
#        독립적으로 진행되고, 모든 컨테이너가 멈추면 Pod 오브젝트가 삭제됩니다."
#       "A 는 PreStop 실행 중 종료돼 SIGTERM 을 보내지 않은 경우, B 는 hook 이 없어 SIGTERM 을
#        바로 보낸 경우, C 는 유예 시간 안에 멈추지 않아 SIGKILL 로 종료된 경우"
# 타입 스펙: type-swimlane — 세 컨테이너가 같은 시간축을 나눠 쓰고, 레인마다 결말이 다르다.
#           유예 만료가 셋 모두에 걸리는 하나의 마감이므로 세 레인을 관통하는 세로선으로 세운다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 640
d = D(W, H, "KUBERNETES IN ACTION · 06-03",
      "종료는 컨테이너마다 따로 간다 — 셋 다 멈춰야 Pod 가 지워진다",
      "삭제 요청이 오면 일반 컨테이너들의 종료 절차가 함께 시작되지만, PreStop → SIGTERM → "
      "SIGKILL 은 컨테이너 안에서 독립적으로 진행된다. 결말은 셋 다 다를 수 있다.",
      lead="유예 시간은 컨테이너마다 세는 것이 아니라 Pod 하나에 걸리는 마감이다")

X0, XEND = 300, 900
DEADLINE = 780
LANES = [(268, "Container A", "preStop 만으로 끝났다"),
         (368, "Container B", "hook 이 없다"),
         (468, "Container C", "유예 안에 안 멈췄다")]
BAND_H = 52

ddx.band(d, 104, 584, "PreStop 은 SIGTERM 보다 먼저 실행되고 그만큼 SIGTERM 을 미룬다")

d.chip(160, 212, "kubectl delete pod", ACC, 11)
d.path(f"M 160 224 L 160 244 L {X0-40} 244", ACC, 1.4)
d.path(f"M {X0-40} 244 L {X0-40} {LANES[-1][0]}", ACC, 1.4)
for cy, _, _ in LANES:
    d.path(f"M {X0-40} {cy} L {X0-8} {cy}", ACC, 1.4, m="acc")

def seg(a, b, cy, c, label, dash=False, label_cx=None):
    """label_cx 로 라벨을 띠 안에서 옮긴다 — 유예 만료 세로선(780)이 지나는 자리를 피한다."""
    d.o.append(f'<rect x="{a}" y="{cy-BAND_H//2}" width="{b-a}" height="{BAND_H}" rx="6" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.1"'
               f'{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
    d.t(label_cx or (a + b) // 2, cy + 4, ddx.fit(label, 11, b - a - 16, label), 11, c, KR)

# 진입 화살표가 x=260~292 를 쓴다 — 레인 이름은 250 에서 끝내 비켜 준다
for cy, name, tail in LANES:
    d.t(250, cy - 6, name, 12, INK, MONO, "end", 600)
    d.t(250, cy + 12, tail, 10, SOFT, KR, "end")

seg(X0, 560, LANES[0][0], INFO, "preStop 실행 중 프로세스 종료")
seg(560, XEND, LANES[0][0], MUTED, "SIGTERM 을 보내지 않았다", dash=True, label_cx=670)
seg(X0, 460, LANES[1][0], BAD, "SIGTERM 즉시")
seg(460, XEND, LANES[1][0], MUTED, "곱게 내려갔다", dash=True, label_cx=620)
seg(X0, 420, LANES[2][0], INFO, "preStop")
seg(420, DEADLINE, LANES[2][0], BAD, "SIGTERM — 반응하지 않는다")
seg(DEADLINE, XEND, LANES[2][0], WARN, "SIGKILL")

d.path(f"M {DEADLINE} 232 L {DEADLINE} 512", WARN, 1.4, dash="6 5")
d.chip(DEADLINE, 224, "deletionGracePeriodSeconds 만료", WARN, 11)

d.path(f"M {XEND} 512 L {XEND} 540 L 500 540", MUTED, 1.4, m="ar")
d.chip(430, 540, "셋 다 멈추면 Pod 오브젝트 삭제", MUTED, 11)

d.t(36, 560, "유예를 0 으로 주면 PreStop 과 정리 절차를 건너뛴다 — 느린 종료의 해법은 유예 단축이 "
             "아니라 앱에 SIGTERM 핸들러를 넣는 것이다", 12, MUTED, KR, "start")
d.legend(600, [("삭제 요청", ACC), ("정상 종료 경로", INFO), ("시그널을 받은 구간", BAD),
               ("강제 종료", WARN)])
d.save("06-03-termination-sequence.svg")
print("ok termination-sequence")
