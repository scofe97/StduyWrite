# 01-01 §4 — 층을 내려갈 때마다 헤더가 하나씩 붙는다. 페이로드는 대개 위 층에서 온 패킷이다.
# 타입 스펙: type-nested — 바깥 상자가 안쪽 상자를 통째로 페이로드로 삼는 포함 관계.
#           안쪽으로 갈수록 원래 데이터에 가깝고, 각 테두리 왼쪽의 세로 띠가 그 층이 덧붙인 헤더다.
#           축약: 안쪽 여백을 사방 균일하게 두지 않고 왼쪽만 헤더 폭만큼 더 준다 —
#           헤더가 페이로드 *앞*에 붙는다는 사실이 그림에서 읽혀야 하기 때문이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 512
HDR_W, STEP_X, STEP_Y, INSET_R = 56, 92, 40, 28

LAYERS = [
    ("링크 층이 붙입니다", "프레임 · frame", "H l", INK),
    ("네트워크 층이 붙입니다", "데이터그램 · datagram", "H n", INFO),
    ("트랜스포트 층이 붙입니다", "세그먼트 · segment", "H t", OK),
]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-01 §4",
      "층마다 봉투를 하나씩 씌웁니다",
      "보내는 호스트에서 애플리케이션 메시지가 아래로 내려가며 층마다 헤더를 하나씩 얻는다. 어느 층에서 보든 패킷은 헤더와 페이로드 둘로 갈리고, 그 페이로드는 대개 위 층에서 온 패킷이다.",
      "받는 쪽은 바깥부터 하나씩 뜯습니다 — 그것이 역캡슐화입니다")

x, y = 24, 132
w, h = W - 48, 268
for name, pdu, hdr, c in LAYERS:
    d.tone(x, y, w, h, c, 8, op="0A", sw=1.2)
    d.t(x + 16, y + 24, name, 11, c, KR, "start", 600)
    d.t(x + w - 16, y + 24, pdu, 11, MUTED, MONO, "end")
    d.box(x + 16, y + 36, HDR_W, h - 52, PAPER2, c, 1.1, 4)
    d.t(x + 16 + HDR_W / 2, y + 36 + (h - 52) / 2 + 4, hdr, 11, c, MONO)
    x += STEP_X; y += STEP_Y; w -= STEP_X + INSET_R; h -= STEP_Y + 20

d.tone(x, y, w, h, ACC, 8)
d.t(x + w / 2, y + h / 2 - 4, "메시지 · message", 12, ACC, MONO, "middle", 600)
d.t(x + w / 2, y + h / 2 + 18, "애플리케이션이 만든 원본", 11, MUTED, KR)

d.t(24, 428, "호스트는 다섯 층을 다 구현하고 라우터는 3층까지, 링크 계층 스위치는 2층까지만 벗깁니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("원본 데이터", ACC), ("각 층이 덧붙인 헤더", INFO)])
d.save("01-01.encapsulation.svg")
