# 2026-09-07 A 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "같은 구성 세 대 중 한 대만 아프다"이지 패킷이 어디서 사라지는가가 아니다.
# 층별 폐기 자리는 원인 분석 절의 drop-layers 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 랙 경계로 동일 구성 셋을 나란히 둔다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 804, 400
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-07 A",
      "같은 랙의 같은 구성 세 대",
      "동일하게 구성한 사내 API 서버 세 대가 같은 랙에 있다. 그중 한 대에서만 "
      "응답 실패율이 0.3% 안팎으로 꾸준히 나온다.",
      lead="구성이 같으므로 차이는 구성 밖에 있습니다")

RX, RY, RW, RH = 40, 122, 724, 164
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0, 8)
d.t(RX + 14, RY + 22, "같은 랙 · 동일 구성", 12, SOFT, KR, "start", 600)

SPECS = [("서버 1", "정상", OK), ("서버 2", "실패율 0.3%", BAD), ("서버 3", "정상", OK)]
for i, (name, state, c) in enumerate(SPECS):
    x = RX + 28 + i * 228
    if c is BAD:
        d.tone(x, RY + 42, 212, 104, BAD, 6)
    else:
        d.box(x, RY + 42, 212, 104, PAPER2, RULE, 0.9, 6)
    d.t(x + 106, RY + 70, name, 14, c, KR, "middle", 600)
    d.t(x + 106, RY + 94, state, 12, c, KR, "middle")
    d.t(x + 106, RY + 118, "91일째 재시작 없음", 11, SOFT, KR, "middle")

d.t(W // 2, 326, "CPU 도 메모리도 여유가 있고 애플리케이션 로그에 예외가 하나도 없습니다",
    13, MUTED, KR, "middle")
d.t(W // 2, 352, "자원의 총량은 확인했지만 요청이 지나는 길은 아직 보지 않았습니다",
    12, WARN, KR, "middle")
d.t(W // 2, 378, "클라이언트가 보는 것은 타임아웃뿐입니다", 12, SOFT, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-07.rack-topology.svg"))
print("ok")
