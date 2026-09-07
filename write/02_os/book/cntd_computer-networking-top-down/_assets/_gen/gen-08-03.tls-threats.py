# 타입 스펙: type-dp-security-matrix — 무엇이 빠지면 어떤 사고가 나는가를 격자로.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.6 도입 (책 592쪽) —
#   향수 주문 시나리오와 세 가지 결과는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 568
d = D(W, H, "SECTION 8.6 · WHY TLS",
      "빠진 것마다 다른 사고가 납니다",
      "밥이 향수를 주문한다. 셋 중 무엇이 없느냐가 무엇을 잃느냐를 정한다.",
      "세 시나리오는 원문 §8.6 도입의 것입니다")

ROWS = [("기밀성", "encryption", "침입자가 주문을 가로채 결제 카드 정보를 얻습니다", "그 정보로 밥의 돈을 씁니다"),
        ("데이터 무결성", "integrity", "침입자가 주문을 고칩니다", "밥이 원한 것의 열 배를 사게 됩니다"),
        ("서버 인증", "authentication", "트루디의 사이트가 앨리스의 로고를 겁니다", "돈을 갖고 사라지거나 신원을 도용합니다")]
LX, LW = 24, 216
CX1, CW1 = 264, 400
CX2, CW2 = 688, 288
Y0, RH, STRIDE = 172, 72, 84
d.t(LX, 148, "없으면", 11, SOFT, KR, "start", 600)
d.t(CX1 + CW1 / 2, 148, "벌어지는 일", 11, SOFT, KR, "middle", 600)
d.t(CX2 + CW2 / 2, 148, "밥이 잃는 것", 11, SOFT, KR, "middle", 600)
for i, (name, en, what, lose) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    d.tone(LX, y, LW, RH, BAD, 6, "16", 1.2)
    d.t(LX + LW / 2, y + 32, name, 12, BAD, KR, "middle", 600)
    d.t(LX + LW / 2, y + 52, en, 10, SOFT, MONO)
    d.box(CX1, y, CW1, RH, PAPER2, RULE, 0.9)
    d.t(CX1 + CW1 / 2, y + 42, what, 11, INK, KR)
    d.box(CX2, y, CW2, RH, PAPER2, RULE, 0.9)
    d.t(CX2 + CW2 / 2, y + 42, lose, 11, MUTED, KR)

PY = Y0 + 3 * STRIDE + 8
d.tone(24, PY, 952, 60, ACC, 8, "16", 1.4)
d.t(44, PY + 26, "TLS 가 이 셋에 클라이언트 인증까지 더해 위에서 도는 응용에 줍니다", 12, ACC, KR, "start", 600)
d.t(44, PY + 48, "엄밀히는 응용 계층 프로토콜이며, 역사적으로 TCP 위에 얹혔고 지금은 QUIC 안에서 UDP 위에서도 돕니다.",
    11, MUTED, KR, "start")

d.legend(508, [("빠진 성질", BAD), ("TLS 가 주는 것", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-03.tls-threats.svg"
d.save(out); print("→", out.name)
