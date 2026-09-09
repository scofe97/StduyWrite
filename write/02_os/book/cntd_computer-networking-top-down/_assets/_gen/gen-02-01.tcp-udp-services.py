# 02-01 §3 — TCP 가 주는 넷과 UDP 에 없는 넷을 같은 행에 놓고 견준다.
# 오른쪽 열의 문장은 본문이 UDP 항목마다 적어 둔 결과를 그대로 옮긴 것이다.
# 처리량·타이밍은 둘 다 안 주므로 행에 넣지 않고 아래 주석으로 갈라 두었다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 항목, 열은 프로토콜.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 552
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §3",
      "UDP 는 없는 것을 세는 편이 빠릅니다",
      "핸드셰이킹·도착 보장·순서 보장·혼잡 제어 넷을 TCP 와 UDP 로 견주고, 없을 때 무슨 일이 되는지를 적었다.",
      "혼잡 제어가 빠진 자리가 UDP 를 고르는 이유입니다")

C0, C0W = 24, 196          # 항목
C1, C1W = 232, 180         # TCP
C2, C2W = 424, 180         # UDP
C3, C3W = 616, 360         # UDP 에서는 이렇게 됩니다
HY, RH, RS = 108, 40, 48
ROWS = [("핸드셰이킹", "곧장 말을 시작합니다"),
        ("도착 보장", "닿는다는 보장이 없습니다"),
        ("순서 보장", "보낸 순서와 다를 수 있습니다"),
        ("혼잡 제어", "원하는 속도로 밀어 넣습니다")]

for x, w, lab in ((C0, C0W, ""), (C1, C1W, "TCP"), (C2, C2W, "UDP"), (C3, C3W, "UDP 에서는 이렇게 됩니다")):
    d.box(x, HY, w, RH, PAPER2, RULE, 0.9)
    if lab:
        d.t(x + w / 2, HY + 26, lab, 12, INK, KR, "middle", 600)

for i, (item, effect) in enumerate(ROWS):
    y = HY + RH + 8 + i * RS
    focal = (item == "혼잡 제어")
    if focal:
        d.tone(C0, y, C0W, RH, ACC, 6, "12", 1.4)
        d.t(C0 + C0W / 2, y + 26, item, 12, ACC, KR, "middle", 600)
    else:
        d.box(C0, y, C0W, RH, PAPER2, RULE, 0.9)
        d.t(C0 + C0W / 2, y + 26, item, 12, INK, KR)
    d.tone(C1, y, C1W, RH, OK, 6, "14", 1.1)
    d.t(C1 + C1W / 2, y + 26, "있습니다", 12, OK, KR)
    d.tone(C2, y, C2W, RH, BAD, 6, "14", 1.1)
    d.t(C2 + C2W / 2, y + 26, "없습니다", 12, BAD, KR)
    d.box(C3, y, C3W, RH, PAPER2, RULE, 0.9)
    d.t(C3 + 16, y + 26, effect, 11, MUTED, KR, "start")

BY = HY + RH + 8 + 4 * RS + 16
d.line(24, BY, 976, BY, RULE, 0.8)
d.t(24, BY + 26, "혼잡 제어는 통신하는 프로세스가 아니라 인터넷 전체의 복리를 위한 서비스입니다. "
                 "그래서 그것을 피하려고 UDP 를 고르는 앱이 생깁니다.", 11, ACC, KR, "start")
d.t(24, BY + 48, "네 축 가운데 보안은 TCP 도 UDP 도 주지 않아 TLS 를 애플리케이션 층에 얹습니다.", 11, MUTED, KR, "start")
d.t(24, BY + 70, "처리량 보장과 타이밍 보장은 둘 다 못 주므로 이 표에 행으로 두지 않았습니다.", 11, MUTED, KR, "start")
d.t(24, BY + 92, "다만 밀어 넣는 속도가 곧 종단 처리량은 아닙니다. 중간 링크의 용량과 혼잡이 그보다 낮출 수 있습니다.",
    11, INFO, KR, "start")

d.legend(H - 44, [("TCP 가 주는 것", OK), ("UDP 에 없는 것", BAD), ("이 절의 논점", ACC), ("단서", INFO)])
d.save("02-01.tcp-udp-services.svg")
print("ok tcp-udp-services")
