# 타입 스펙: type-process — 작은 세그먼트 제어 메커니즘의 단계별 흐름.
# 사실 출처: ch15.txt 1~445행 — 1B 입력, 4개 세그먼트(88B·40B·88B·40B), 지연 ACK 편승(3개), Nagle 묶음(19개→11개), 교착 지연(200ms).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO, OK, WARN, BAD, INFO

W, H = 920, 432
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-01",
      "대화형 통신에서 지연 ACK 와 Nagle 이 결합하는 과정",
      "사용자의 1바이트 키 입력이 네 세그먼트를 만들고, 지연 ACK 가 에코에 편승해 셋으로 줄이며, Nagle 이 RTT 동안 패킷을 묶는다. "
      "그러나 두 알고리즘이 함께 작동하면 ACK 지연 타이머가 끝날 때까지 데이터 전송이 멈추는 상호 교착이 발생한다.",
      "오버헤드를 줄이려는 두 최적화가 만나면 타이머 만료까지 멈춥니다")

CW, CH, GAP = 164, 210, 16
X0 = 26
Y = 140

STEPS = [
    ("1단계", "키 1회 입력", "1바이트 데이터", "사용자 1타", "터미널 문자 'd'", INFO),
    ("2단계", "세그먼트 넷", "4개 · 총 256B", "키·에코 각 88B", "순수 ACK 각 40B", WARN),
    ("3단계", "지연 ACK 편승", "3개 · 총 216B", "ACK 편승 에코", "순수 ACK 1개 절감", OK),
    ("4단계", "Nagle 알고리즘", "11개 세그먼트", "19개에서 8개 감소", "190ms RTT 주기", ACC),
    ("5단계", "상호 교착 정지", "최대 200ms 지연", "Nagle 송신 보류", "ACK 지연 타이머 대기", BAD),
]

for i, (step, title, metric, detail1, detail2, color) in enumerate(STEPS):
    x = X0 + i * (CW + GAP)
    if i < len(STEPS) - 1:
        d.arrow([(x + CW, Y + CH / 2), (x + CW + GAP - 4, Y + CH / 2)], MUTED, "ar", 1.4)
    
    d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.tone(x, Y, CW, 34, color, 8, "18", 1.2)
    d.t(x + CW / 2, Y + 22, step, 12, color, MONO, "middle", 600)
    
    d.t(x + CW / 2, Y + 60, title, 14, INK, KR, "middle", 600)
    d.t(x + CW / 2, Y + 92, metric, 13, color, MONO, "middle", 600)
    
    d.line(x + 12, Y + 114, x + CW - 12, Y + 114, RULE, 0.8)
    
    d.t(x + CW / 2, Y + 144, detail1, 11, MUTED, KR, "middle")
    d.t(x + CW / 2, Y + 172, detail2, 11, SOFT, KR, "middle")

d.save("15-01.chapter-overview.svg")
