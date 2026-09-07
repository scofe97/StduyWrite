# 03-02 §5 — 순서 번호가 한 바퀴 돌면 옛 사본과 새 세그먼트가 같은 번호를 단다.
# 본문 근거: "이전에 보낸 번호 x 의 패킷이 더 이상 망에 없다고 확신할 때까지 그 번호를 다시 쓰지 않습니다",
#   그리고 채널을 "패킷을 버퍼링해 두었다가 미래의 아무 시점에 제멋대로 뱉어 내는 것"으로 보라는 대목.
# 수치: 2^32 바이트 × 8 ÷ 1 Gbps = 34.36초. 최대 세그먼트 수명 2분(RFC 7323)보다 짧다.
# 논점은 "조용히 진다"는 것 — 체크섬도 통과하고 재전송도 안 일어나 아무 신호가 남지 않는다.
# 타입 스펙: type-timeline — 하나의 시간축 위에서 두 사건이 같은 좌표(번호)로 겹치는 것이 전부다.
#            축약: 화살표는 직교 엘보만 쓴다. 지연을 기울기로 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 660
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-02 §5",
      "같은 번호를 단 소포가 둘입니다",
      "1 Gbps 로 4 GiB 를 나르면 32비트 순서 공간이 34.36초에 한 바퀴 돈다. 세그먼트 최대 수명 2분보다 "
      "짧으므로 옛 사본이 아직 떠 있는 동안 같은 번호가 재사용된다.",
      "받는 쪽은 번호만 보므로 먼저 온 쪽이 이깁니다")

AXY = 306
d.line(60, AXY, 940, AXY, RULE, 1.2)

TOP = [
    (170, 80, 180, "세그먼트 A", "seq 1000", "보냈는데 큐에 붙들립니다", WARN),
    (470, 330, 280, "그 사이 4 GiB 를 나릅니다", "2³² 바이트", "번호가 0 으로 돌아옵니다", MUTED),
    (750, 640, 220, "세그먼트 B", "seq 1000", "한 바퀴 돌아 같은 번호", ACC),
]
for cx, bx, bw, head, code, note, c in TOP:
    d.tone(bx, 140, bw, 96, c, 6, "12", 1.3)
    d.t(cx, 168, head, 12, c, KR, "middle", 600)
    d.t(cx, 192, code, 11, INK, MONO)
    d.t(cx, 216, note, 11, MUTED, KR)
    d.arrow([(cx, 240), (cx, AXY - 10)], c, "ar", 1.3)

for cx, lab in ((170, "t = 0"), (470, "t = 34.36 s"), (750, "t = 34.4 s")):
    d.t(cx + 14, AXY - 10, lab, 11, SOFT, MONO, "start")
    d.line(cx, AXY - 5, cx, AXY + 5, RULE, 1.2)

d.path(f"M 170 {AXY} L 170 330 L 545 330 L 545 346", WARN, 1.4, m="warn", dash="5 5")
d.t(330, 324, "망이 붙들고 있다가 뒤늦게 뱉어 냅니다", 11, WARN, KR)
d.arrow([(750, AXY), (750, 346)], ACC, "acc", 1.4)

BOT = [
    (430, 230, "A 가 먼저 도착합니다", "그 자리에 옛 내용을 넣습니다", "옛 내용이 들어갑니다", BAD),
    (700, 230, "B 가 나중 도착합니다", "이미 1000 을 받았다고 봅니다", "진짜 새것이 버려집니다", BAD),
]
for bx, bw, head, mid, tail, c in BOT:
    d.tone(bx, 352, bw, 100, c, 6, "12", 1.3)
    d.t(bx + bw / 2, 380, head, 12, c, KR, "middle", 600)
    d.t(bx + bw / 2, 404, mid, 11, MUTED, KR)
    d.t(bx + bw / 2, 428, tail, 11, INK, KR)

d.box(24, 486, W - 48, 94, PAPER2, RULE, 0.9, 6)
d.t(44, 512, "아무도 오류를 못 느낍니다", 12, INK, KR, "start", 600)
d.t(44, 534, "체크섬은 A 자신에 대해 계산된 것이라 통과하고 ACK 도 정상으로 나가니 재전송이 일어나지 않습니다. 종단 간 검사도 이것은 못 잡습니다.",
    11, MUTED, KR, "start")
d.t(44, 556, "비트가 뒤집힌 것이 아니라 멀쩡한 세그먼트가 엉뚱한 자리에 들어앉은 것이기 때문입니다. 그래서 번호 밖의 축인 타임스탬프가 필요합니다.",
    11, OK, KR, "start")

d.legend(H - 44, [("옛 사본", WARN), ("새 세그먼트", ACC), ("조용히 지는 자리", BAD), ("PAWS 가 메우는 곳", OK)])
d.save("03-02.sequence-wrap.svg")
print("ok sequence-wrap")
