# 01-01.osi-tcpip-mapping — OSI 7계층이 TCP/IP 4계층으로 접히는 자리
# 본문 요구(01-01 §4): "TCP/IP 는 OSI 의 상위 세 계층을 Application 하나로 합쳐 4계층으로
#           줄였습니다"가 절 요약이고, 본문이 계층별로 "OSI 의 Application·Presentation·Session
#           세 계층이 여기에 합쳐집니다" · "RFC 1122 해석에 따라 Link 에 포함시키기도 하지만
#           책은 완결성을 위해 따로 둡니다"로 접히는 자리를 지목한다. 그래서 오른쪽 칸의 높이가
#           곧 몇 개를 흡수했는지이고, 3→1 · 1:1 · 1:1 · 2→1 네 칩이 그 비율을 다시 적는다.
#           왼쪽을 7칸으로 두고 오른쪽만 합치는 배치라야 "접힌다"가 눈에 보인다 — 양쪽을 각각
#           7칸·4칸으로 나란히 두면 대응이 아니라 두 목록이 된다.
#           TCP/IP 쪽에 번호가 없는 것도 본문 사실이다("TCP/IP 계층에는 번호가 없습니다").
#           그래서 왼쪽 이름에만 7~1 을 붙였다.
# 타입 스펙: type-layers.md — 위아래로 쌓인 추상 수준 두 벌. 두 벌 사이의 대응이 논지라
#           같은 높이에 마주 세우고 연결선으로 묶는다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 810, 638
LX, RX, COLW = 12, 462, 300
Y0, ROW_H, STRIDE = 118, 58, 66
BUS = 364                          # 여러 줄을 한 칸으로 모으는 세로 줄기
OUT, INN = LX + COLW + 18, RX - 14  # 왼쪽에서 나가는 자리 · 오른쪽으로 들어가는 자리

d = D(W, H, "LAYER MAPPING · 01-01 OSI",
      "OSI 7계층이 TCP/IP 4계층으로 접히는 자리",
      "OSI 7계층과 TCP/IP 4계층의 대응. 상위 3계층(Application·Presentation·Session)이 "
      "TCP/IP의 Application 하나로, 하위 2계층(Data Link·Physical)이 Link 하나로 접힌다. "
      "Transport와 Network는 1:1로 대응한다.",
      lead="위 3개와 아래 2개가 각각 하나로 접힙니다 — 가운데 둘만 1:1로 남습니다.")

d.t(LX + COLW / 2, 100, "OSI 7계층 — 참조 모델", 11, SOFT, MONO)
d.t(RX + COLW / 2, 100, "TCP/IP 4계층 — 실제 구현", 11, SOFT, MONO)

LEFT = [("7 Application",  "Data",             "HTTP·DNS·SSH",      INFO),
        ("6 Presentation", "Data",             "인코딩·압축·암호화", INFO),
        ("5 Session",      "Data",             "duplex·체크포인트",  INFO),
        ("4 Transport",    "Segment·Datagram", "흐름 제어·오류 제어", OK),
        ("3 Network",      "Packet",           "주소 지정·라우팅",   WARN),
        ("2 Data Link",    "Frame",            "같은 네트워크 안",   ACC),
        ("1 Physical",     "Bit",              "전기·빛·전파",      BAD)]

_MK = {INFO: "info", OK: "ok", WARN: "warn", ACC: "acc", BAD: "bad"}


def row_cy(i):
    return Y0 + STRIDE * i + ROW_H / 2

for i, (name, pdu, sub, c) in enumerate(LEFT):
    y = Y0 + STRIDE * i
    d.tone(LX, y, COLW, ROW_H, c, 6, "12", 1.1)
    d.t(LX + 16, y + 24, name, 13, c, MONO, "start", 600)
    d.t(LX + COLW - 14, y + 24, pdu, 10, MUTED, MONO, "end")
    d.t(LX + 16, y + 43, sub, 11, MUTED, KR, "start")

# (첫 행, 흡수한 줄 수, 이름, 한 줄, 덧줄, 색, 비율 칩)
RIGHT = [(0, 3, "Application", "OSI 7·6·5 를 흡수", "RFC 로 정의",       INFO, "3→1"),
         (3, 1, "Transport",   "TCP · UDP",        None,               OK,   "1:1"),
         (4, 1, "Internet",    "IP",               None,               WARN, "1:1"),
         (5, 2, "Link",        "Ethernet · MAC",   "물리+데이터링크 통합", ACC,  "2→1")]

for start, span, name, sub, sub2, c, ratio in RIGHT:
    y = Y0 + STRIDE * start
    h = STRIDE * span - (STRIDE - ROW_H)
    cy = y + h / 2
    d.tone(RX, y, COLW, h, c, 6, "12", 1.3)
    cx = RX + COLW / 2
    if sub2:                       # 흡수한 칸은 세 줄, 1:1 인 칸은 두 줄
        d.t(cx, cy - 6, name, 14, c, MONO, "middle", 600)
        d.t(cx, cy + 12, sub, 11, INK)
        d.t(cx, cy + 29, sub2, 10, MUTED)
    else:
        d.t(cx, cy - 2, name, 14, c, MONO, "middle", 600)
        d.t(cx, cy + 15, sub, 11, INK)

    if span == 1:                  # 1:1 은 줄기가 필요 없다 — 한 줄로 곧장 건너간다
        d.path(f"M {OUT} {cy} L {INN} {cy}", c, 1.5, m=_MK[c])
        d.chip((OUT + INN) / 2, cy, ratio, c, 9)
        continue
    rows = range(start, start + span)
    # 높이가 어긋나는 줄을 먼저 줄기로 꺾어 모으고, 이미 같은 높이인 줄은 그 뒤에 곧장 잇는다
    for i in [i for i in rows if row_cy(i) != cy]:
        d.path(f"M {OUT} {row_cy(i)} L {BUS} {row_cy(i)} L {BUS} {cy}", c, 1.5)
    for i in [i for i in rows if row_cy(i) == cy]:
        d.path(f"M {OUT} {cy} L {BUS} {cy}", c, 1.5)
    d.path(f"M {BUS} {cy} L {INN} {cy}", c, 1.5, m=_MK[c])
    d.chip((BUS + INN) / 2, cy, ratio, c, 9)

d.legend(594, [("여러 계층이 하나로 접힘", INFO), ("1:1 대응", OK), ("하위 2계층 통합", ACC)])
d.save("01-01.osi-tcpip-mapping.svg")
print("ok osi-tcpip-mapping")
