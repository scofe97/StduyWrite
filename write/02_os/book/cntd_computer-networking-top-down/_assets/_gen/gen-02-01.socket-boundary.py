# 02-01 §2 — 소켓이 어디에 놓이는지, 그 위아래로 통제가 어떻게 갈리는지.
# 본문이 문의 위치를 한 문장으로 못 박는다: "소켓은 한 호스트 안에서 애플리케이션 층과
# 트랜스포트 층 사이의 인터페이스입니다." 그래서 소켓을 층 사이의 한 칸으로 그렸다.
# 아래 띠의 주소 두 조각도 본문 그대로다 — 호스트는 IP, 받는 소켓은 포트 번호.
# 타입 스펙: type-layers — 위에서 아래로 쌓인 추상 수준. accent 는 한 층에만 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 648
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §2",
      "소켓은 집의 문이고 통제의 경계선입니다",
      "프로세스는 집, 소켓은 그 집의 문. 문 위쪽은 개발자가 전부 통제하고 아래쪽은 거의 통제하지 못한다.",
      "층 하나가 아니라 층과 층 사이에 놓인 것이 소켓입니다")

LX, LW = 64, 840
LAYERS = [
    (112, 64, "애플리케이션 층", "프로세스 = 집. 메시지를 만들고 읽는 코드가 전부 여기 있습니다", INK, "전부 통제합니다"),
    (256, 64, "트랜스포트 층", "TCP · UDP. 고를 수 있는 것은 프로토콜 하나와 파라미터 몇 개입니다", INK, "거의 통제하지 못합니다"),
    (332, 56, "네트워크 층", "데이터그램을 목적지 호스트까지 나릅니다", MUTED, "통제 없습니다"),
    (400, 56, "링크 · 물리 층", "한 칸씩 실어 나릅니다", MUTED, "통제 없습니다"),
]
for y, h, name, sub, col, ctrl in LAYERS:
    d.box(LX, y, LW, h, PAPER2, RULE, 0.9)
    d.t(LX + 20, y + 26, name, 13, col, KR, "start", 600)
    d.t(LX + 20, y + 46, sub, 11, MUTED, KR, "start")
    d.t(LX + LW - 20, y + 36, ctrl, 11, SOFT, KR, "end")

# 층과 층 사이의 문 (이 그림의 강조점)
d.tone(LX, 184, LW, 64, ACC, 6, "12", 1.4)
d.t(LX + 20, 212, "소켓", 14, ACC, KR, "start", 600)
d.t(LX + 72, 212, "집의 문 — 애플리케이션과 네트워크 사이의 API 입니다", 12, INK, KR, "start")
d.t(LX + 20, 234, "밀어낸 쪽은 문 반대편에 메시지를 날라 줄 운송 기반 시설이 있다고 가정합니다", 11, MUTED, KR, "start")

# 주소 두 조각
d.line(24, 484, 976, 484, RULE, 0.8)
d.t(24, 510, "그 문을 지목하는 주소는 두 조각입니다", 13, INK, KR, "start", 600)
for i, (head, body) in enumerate([("호스트", "IP 주소로 지목합니다"),
                                  ("받는 소켓", "목적지 포트 번호로 지목합니다")]):
    x = 24 + i * 300
    d.tone(x, 524, 284, 52, INFO, 6, "12", 1.2)
    d.t(x + 16, 548, head, 12, INFO, KR, "start", 600)
    d.t(x + 16, 566, body, 11, MUTED, KR, "start")
d.t(632, 548, "웹 서버 80 · 메일 서버 25", 11, MUTED, MONO, "start")
d.t(632, 566, "전체 목록은 IANA 가 관리합니다", 11, MUTED, KR, "start")

d.legend(H - 44, [("통제의 경계선", ACC), ("주소의 두 조각", INFO), ("주어진 대로 쓰는 층", MUTED)])
d.save("02-01.socket-boundary.svg")
print("ok socket-boundary")
