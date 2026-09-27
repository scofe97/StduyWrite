# 03-03 §5 — 손실을 알아채는 길이 둘이고, 그중 빠른 쪽은 조건이 붙는다는 것.
# 본문 근거: "타임아웃 기반 재전송의 문제는 기다리는 시간이 길다" · "같은 데이터에 대해 중복 ACK 를
#   셋 받으면 ... 타이머 만료 전에 다시 보냄."
# 1차 자료: RFC 5681 §3.2 "A TCP receiver SHOULD send an immediate duplicate ACK when an
#   out-of-order segment arrives." — 방아쇠가 '뒤 세그먼트의 도착'이므로 뒤가 없으면 이 길이 없다.
# 논점: 빠른 재전송은 타임아웃을 대체하지 않는다. 흔한 경우를 앞당길 뿐이고,
#   잃어버린 것 뒤에 세그먼트가 셋 이상 도착하지 않으면 중복 ACK 가 셋 모이지 않아 시계만 남는다.
#   (RFC 5681 §3.2 "arrival of 3 duplicate ACKs". RFC 8985 RACK-TLP 는 이 꼬리 손실을 탐침으로 따로 다루지만 이 도식은 고전 규칙만 그린다.)
#   '최소 1초'는 RFC 6298 (2.4) 의 SHOULD 하한이다.
# 타입 스펙: type-flowchart — 하나의 물음이 두 갈래를 가르고, 갈래마다 걸리는 시간이 다르다.
#   축약: 중복 ACK 를 셋까지 세는 이유(망의 재정렬)는 여기서 다루지 않는다. 03-02 의 몫이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 700
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §5",
      "빠른 길에는 조건이 붙습니다",
      "손실을 알아채는 길이 둘이다. 중복 ACK 는 잃어버린 것 뒤에 세그먼트가 셋 이상 더 도착해야 셋이 모이고, "
      "그러지 못하면 남는 것은 시계 하나뿐이다.",
      "그래서 타임아웃은 느려도 없앨 수 없습니다")

d.tone(380, 132, 240, 56, MUTED, 6, "10", 1.2)
d.t(500, 156, "세그먼트 하나가 사라졌음", 11.5, INK, KR, "middle", 600)
d.t(500, 176, "보내는 쪽은 아직 모름", 11, MUTED, KR)

d.arrow([(500, 190), (500, 218)], MUTED, "ar", 1.3)
d.tone(330, 220, 340, 62, ACC, 6, "12", 1.4)
d.t(500, 246, "그 뒤에 세그먼트가 셋 이상 도착합니까", 12, ACC, KR, "middle", 600)
d.t(500, 268, "도착 하나가 중복 ACK 하나를 만듦", 11, MUTED, KR)

d.path("M 500 284 L 500 308 L 246 308 L 246 326", ACC, 1.4, m="acc")
d.path("M 500 284 L 500 308 L 754 308 L 754 326", BAD, 1.4, m="bad")
d.t(373, 302, "셋 이상", 11, ACC, KR, "middle")
d.t(631, 302, "둘 이하 — 끝 무렵에 사라짐", 11, BAD, KR, "middle")

LEFT = [("뒤 세그먼트가 셋 이상 도착", "도착마다 구멍을 다시 봄", OK),
        ("중복 ACK 를 즉시 보냄", "도착이 방아쇠", OK),
        ("셋이 모이면 재전송", "타이머 만료를 안 기다림", ACC)]
RIGHT = [("뒤에 도착하는 것이 둘 이하", "중복 ACK 도 둘 이하", SOFT),
         ("문턱 셋에 못 미침", "빠른 재전송이 발동하지 않음", BAD),
         ("시계가 다 흐를 때까지", "타임아웃 뒤에 재전송", WARN)]
for col, items, cx in ((LEFT, LEFT, 246), (RIGHT, RIGHT, 754)):
    for i, (head, sub, c) in enumerate(items):
        y = 332 + i * 74
        d.tone(cx - 190, y, 380, 60, c, 6, "10", 1.2)
        d.t(cx, y + 26, head, 11.5, c, KR, "middle", 600)
        d.t(cx, y + 46, sub, 11, MUTED, KR)
        if i < 2:
            d.arrow([(cx, y + 60), (cx, y + 70)], c, "ok" if c is OK else ("soft" if c is SOFT else "bad"), 1.2)

d.t(246, 574, "빠른 재전송 — 왕복 한 번 남짓", 11, ACC, KR, "middle", 600)
d.t(754, 574, "타임아웃 — RFC 권고 하한 1초", 11, WARN, KR, "middle", 600)

d.box(24, 596, W - 48, 60, PAPER2, RULE, 0.9, 6)
d.t(44, 620, "왼쪽 길은 조건부이고 오른쪽 길은 항상 있음", 12, INK, KR, "start", 600)
d.t(44, 642, "빠른 재전송은 타임아웃을 대체하는 것이 아니라 흔한 경우를 앞당기는 것 · 뒤에 셋이 못 오면 왼쪽 길이 없음",
    11, MUTED, KR, "start")

d.legend(H - 44, [("뒤에 셋 이상 올 때", OK), ("앞당기는 길", ACC), ("셋이 못 올 때", BAD), ("남는 길", WARN)])
d.save("03-03.loss-detection.svg")
print("ok loss-detection")
