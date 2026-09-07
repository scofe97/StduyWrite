# 01-04 §4 — 처리량을 정하는 것은 경로 위 가장 느린 링크이고, 그 링크는 다른 흐름과 나눠 쓸 때 더 느려진다.
# 값 출처: 원문 1.4.4 의 세 예 — 2링크(min{Rs,Rc}), 접속망 제약, 코어 공유 링크(5 Mbps ÷ 10 = 500 kbps).
# 타입 스펙: type-flowchart — 판정을 물어 가며 좁히는 결정 흐름. 마름모가 물음이고
#           끝 상자가 답이다. 초점은 실무에서 가장 자주 걸리는 답 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 680

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-04 §4",
      "처리량은 무엇이 정하나",
      "원문이 드는 세 예를 물음의 순서로 세운 것. 다른 흐름이 없으면 경로 위 가장 느린 링크가 답이고, 다른 흐름이 그 링크를 함께 쓰면 나눈 몫이 답이다.",
      "오늘날 인터넷에서 걸리는 자리는 대개 코어가 아니라 접속망입니다")

def box(x, y, w, h, t1, t2, c=None, r=8):
    if c: d.tone(x, y, w, h, c, r)
    else: d.box(x, y, w, h, PAPER2, RULE, 1.0, r)
    d.t(x + w / 2, y + (26 if t2 else 34), t1, 12, c if c else INK, KR, "middle", 600)
    if t2: d.t(x + w / 2, y + 48, t2, 11, MUTED, KR)
    return x, y, w, h

def dia(cx, cy, w, h, t):
    d.o.append(f'<path d="M {cx} {cy - h/2} L {cx + w/2} {cy} L {cx} {cy + h/2} L {cx - w/2} {cy} Z" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
    d.t(cx, cy + 4, t, 12, INK, KR, "middle", 600)
    return cx, cy, w, h

START = box(340, 108, 280, 60, "파일 하나를 받는 처리량", "무엇이 상한을 정하나")
Q1 = dia(480, 232, 400, 88, "경로 위 링크 중 최소는 무엇인가")
A1 = box(60, 344, 300, 76, "min { R1, R2, … , RN }", "병목 링크의 전송률입니다", INFO)
Q2 = dia(660, 356, 380, 88, "그 링크를 다른 흐름도 쓰는가")
A2 = box(600, 480, 300, 76, "나눠 가진 몫", "코어 5 Mbps 를 열이 나누면 500 kbps", BAD)
A3 = box(252, 480, 300, 76, "접속망이 병목", "오늘날 가장 흔한 답입니다", ACC)

d.arrow([(480, 168), (480, 188)], MUTED, "ar", 1.3)
d.arrow([(280, 232), (210, 232), (210, 340)], MUTED, "ar", 1.3)
d.t(226, 224, "코어는 대개 과잉 공급", 11, MUTED, KR, "start")
d.arrow([(680, 232), (760, 232), (760, 312)], MUTED, "ar", 1.3)
d.arrow([(660, 400), (660, 476)], BAD, "bad", 1.3)
d.t(672, 436, "예 — 공유 링크가 병목", 11, BAD, KR, "start")
d.arrow([(470, 400), (402, 400), (402, 476)], ACC, "acc", 1.3)
d.t(392, 436, "아니오", 11, ACC, KR, "end")
d.arrow([(210, 420), (210, 452), (300, 452), (300, 476)], INFO, "info", 1.2)

d.t(24, 586, "F 비트 파일을 옮기는 시간은 대략 F ÷ min{Rs, Rc} 입니다 — 32 Mbit 파일을 2 Mbps 서버에서 1 Mbps 접속으로 받으면 32초",
     11, MUTED, KR, "start")

d.legend(H - 60, [("가장 흔한 병목", ACC), ("코어를 나눠 쓸 때", BAD), ("일반 규칙", INFO)])
d.save("01-04.throughput-bottleneck.svg")
