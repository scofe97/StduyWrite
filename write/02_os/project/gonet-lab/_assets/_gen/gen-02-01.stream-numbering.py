# 02-01.stream-numbering — 같은 조각이 사라졌을 때 TCP 한 줄과 QUIC 스트림별 줄
# 본문 요구(02-01 §4 HTTP 절 뒤 두 단락, 사용자 요청 2026-09-29 "설명이 도식에서 더 잘 드러나게" → 바이트 칸 판은 "더 이해가 안 감"):
#           조각 단위로만 그린다. TCP 는 받는 쪽 줄이 하나라 A2 빈자리 뒤의 B2 가 묶이고,
#           QUIC 은 A 줄과 B 줄이 따로라 A 줄에만 빈자리가 생겨 B 는 모두 넘어간다.
# 타입 스펙: type-flowchart — 좌우 두 패널, 각 패널 세 줄(보낸 조각 → 받는 쪽 줄 → 앱에 넘어감).
# 사실 출처: RFC 9000 §2.2, 02-01 본문.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, MONO, KR

W, H = 960, 470
CW, CH, ST = 56, 34, 64


def cell(d, x, y, txt, c=None, dash=False):
    if dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="5" fill="none" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
        d.t(x + CW / 2, y + 22, txt, 13, BAD, MONO, "middle", 600)
    elif c:
        d.tone(x, y, CW, CH, c, 5, "14", 1.2)
        d.t(x + CW / 2, y + 22, txt, 13, c, MONO, "middle", 600)
    else:
        d.box(x, y, CW, CH, r=5)
        d.t(x + CW / 2, y + 22, txt, 13, INK, MONO, "middle", 600)


d = D(W, H, "FLOW · 02-01 STREAM NUMBERING", "받는 쪽 줄이 하나냐 여럿이냐",
      "스트림 A 와 B 의 조각 A1 B1 A2 B2 를 보냈고 A2 만 사라졌다. TCP 는 받는 쪽에 줄이 하나뿐이라 A2 빈자리 뒤에 있는 B2 도 앱에 넘기지 못한다. "
      "QUIC 은 스트림마다 줄이 따로라 A 줄에만 빈자리가 생기고, B 줄은 B1 B2 가 다 차서 앱에 넘어간다.",
      lead="A·B 는 서로 무관한 요청 둘이고 A1·A2 는 요청 A 의 응답 조각입니다. 사라진 것은 둘 다 A2 하나입니다.")

X_T, X_Q = 150, 616
d.t(X_T, 110, "HTTP/2 · TCP", 13, SOFT, KR, "start", 600)
d.t(X_Q, 110, "HTTP/3 · QUIC", 13, SOFT, KR, "start", 600)
d.line(560, 100, 560, 400, RULE, 1.0, "3 6")

rows = [(128, "보낸 조각"), (200, "받는 쪽 줄"), (330, "앱에 넘어감")]
for y, lab in rows:
    d.t(24, y + 22, lab, 12, MUTED, KR, "start", 600)

# 보낸 조각 (양쪽 같음)
for x0 in (X_T, X_Q):
    for i, (t, dash) in enumerate((("A1", False), ("B1", False), ("A2", True), ("B2", False))):
        cell(d, x0 + i * ST, 128, t, dash=dash)
    d.t(x0 + 2 * ST + CW / 2, 180, "사라짐", 11, BAD, KR, "middle")

# TCP: 줄 하나
d.t(X_T - 8, 222, "", 11, MUTED)
cell(d, X_T, 200, "A1", OK)
cell(d, X_T + ST, 200, "B1", OK)
cell(d, X_T + 2 * ST, 200, "  ", dash=True)
cell(d, X_T + 3 * ST, 200, "B2", ACC)
d.t(X_T + 4 * ST + 4, 222, "한 줄", 12, MUTED, KR, "start")
d.t(X_T + 3 * ST + CW / 2, 254, "빈자리 뒤라 묶임", 11, ACC, KR, "middle")

# QUIC: 줄 둘
d.t(X_Q - 10, 222, "A 줄", 11, MUTED, KR, "end", 600)
cell(d, X_Q, 200, "A1", OK)
cell(d, X_Q + ST, 200, "  ", dash=True)
d.t(X_Q - 10, 270, "B 줄", 11, MUTED, KR, "end", 600)
cell(d, X_Q, 248, "B1", OK)
cell(d, X_Q + ST, 248, "B2", OK)
d.t(X_Q + 2 * ST + 4, 222, "A2 자리만 빔", 11, BAD, KR, "start")
d.t(X_Q + 2 * ST + 4, 270, "다 참", 11, OK, KR, "start")

# 앱에 넘어감
cell(d, X_T, 330, "A1", OK)
cell(d, X_T + ST, 330, "B1", OK)
d.tone(X_T + 2 * ST, 330, 2 * ST - 8, CH, ACC, 5, "14", 1.2)
d.t(X_T + 2 * ST + (2 * ST - 8) / 2, 352, "B2 대기", 12, ACC, KR, "middle", 600)
cell(d, X_Q, 330, "A1", OK)
cell(d, X_Q + ST, 330, "B1", OK)
cell(d, X_Q + 2 * ST, 330, "B2", OK)
d.tone(X_Q + 3 * ST, 330, 2 * ST - 8, CH, ACC, 5, "14", 1.2)
d.t(X_Q + 3 * ST + (2 * ST - 8) / 2, 352, "A2 만 대기", 12, ACC, KR, "middle", 600)

d.legend(420, [("앱에 넘어간 조각", OK), ("사라진 조각", BAD), ("도착했지만 기다리는 것", ACC)])
d.save("02-01.stream-numbering.svg")
print("ok stream-numbering v3")
