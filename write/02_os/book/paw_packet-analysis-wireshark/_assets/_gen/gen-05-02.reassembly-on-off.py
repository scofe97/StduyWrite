# 05-02 §3 — TCP 재조립을 켰을 때와 껐을 때 같은 HTTP 응답이 목록과 상세 창에 어떻게 찍히는가.
# 본문 요구: 원문은 재조립을 끄는 이유를 "continuation 패킷이 몇 개인지 아는 데 도움" 이라 적는다.
#            3장 원문은 재조립을 켠 채 tcp.segment.count 로 같은 개수를 센다. 조각 수는 어느 쪽에서도
#            사라지지 않고 자리만 옮긴다는 것, http.time 이 붙는 프레임도 옮긴다는 것을 보인다.
# 값: 2026-09-21 tshark 4.6.8 실측. 루프백에서 HTTP/1.1 로 200KB 파일을 받은 응답 하나(프레임 #5 요청,
#     #7 ~ #33 응답 조각 15개). 켬은 -o tcp.desegment_tcp_streams:TRUE -2, 끔은 FALSE.
# 타입 스펙: type-dp-security-matrix — 행(프레임) × 열(설정) 격자로 같은 줄이 설정에 따라 어떻게 바뀌는지
#           본다. 04-03.key-exchange-matrix 의 칸 문법을 따른다. focal 은 켰을 때 조각 수가 남는 상세 창 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

LABEL_W, COL_W, ROW_H = 264, 320, 68
COLS = ["재조립 켬", "재조립 끔"]
N, F, C, H_ = None, "focal", INFO, OK      # 칸 종류 — 중립 · focal · Continuation · HTTP 응답 줄
ROWS = [
    ("#5", "요청",
     [("GET /big.bin", "요청 줄", N), ("GET /big.bin", "요청 줄", N)]),
    ("#7", "응답 첫 조각 · 204B",
     [("TCP PDU reassembled in 33", "조각 줄로 남음", N), ("HTTP/1.1 200 OK", "http.time 32.352 ms", H_)]),
    ("#9 ~ #32", "가운데 조각 13개",
     [("TCP PDU reassembled in 33", "13줄", N), ("Continuation", "13줄", C)]),
    ("#33", "응답 마지막 조각",
     [("HTTP/1.1 200 OK", "http.time 32.929 ms", H_), ("Continuation", "1줄", C)]),
    ("#33 상세 창", "TCP 층",
     [("15 Reassembled TCP Segments", "tcp.segment.count 15", F), ("재조립 목록 없음", "조각 수는 목록에서 셈", N)]),
]
X0, Y0 = 24, 124
W = X0 + LABEL_W + len(COLS) * COL_W + 24
H = Y0 + 40 + len(ROWS) * ROW_H + 112

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §3",
      "재조립은 조각 수를 숨기지 않고 자리를 옮긴다",
      "같은 HTTP 응답 하나를 재조립 켬과 끔으로 연 결과. 켜면 조각 줄은 목록에 남고 마지막 조각에 HTTP 응답 줄과 재조립 목록이 붙는다. 끄면 첫 조각에 HTTP 응답 줄이 붙고 나머지가 Continuation 으로 늘어선다. http.time 도 붙는 프레임을 따라 옮긴다.",
      "켜면 조각 수가 상세 창으로, 끄면 목록으로 갑니다 — http.time 은 마지막 조각과 첫 조각에서 잽니다")

d.t(X0 + 8, Y0 + 4, "프레임", 12, SOFT, KR, "start", 600)
for j, c in enumerate(COLS):
    d.t(X0 + LABEL_W + j * COL_W + (COL_W - 12) / 2, Y0 + 4, c, 13, INK, KR, "middle", 600)
d.line(X0, Y0 + 18, W - 24, Y0 + 18, RULE, 0.8)

for i, (fr, hint, cells) in enumerate(ROWS):
    y = Y0 + 40 + i * ROW_H
    d.box(X0, y, LABEL_W - 12, ROW_H - 12, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 24, fr, 13, INK, kr(fr), "start", 600)
    d.t(X0 + 16, y + 44, hint, 12, MUTED, kr(hint), "start")
    for j, (val, sub, kind) in enumerate(cells):
        x = X0 + LABEL_W + j * COL_W
        cw = COL_W - 12
        if kind == F:
            d.o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ROW_H - 12}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            col = ACC
        elif kind is None:
            d.box(x, y, cw, ROW_H - 12, PAPER, RULE, 0.8, 6)
            col = INK
        else:
            d.tone(x, y, cw, ROW_H - 12, kind, 6)
            col = kind
        d.t(x + cw / 2, y + 24, val, 13, col, kr(val), "middle", 600)
        d.t(x + cw / 2, y + 44, sub, 12, MUTED, kr(sub))

d.t(X0 + 8, Y0 + 40 + len(ROWS) * ROW_H + 8,
    "2026-09-21 tshark 4.6.8 실측 · 루프백 HTTP/1.1 · 200KB 응답 하나 · 조각 15개",
    12, SOFT, KR, "start")
d.legend(H - 56, [("켰을 때 조각 수가 남는 자리", ACC), ("HTTP 응답 줄 · http.time", OK), ("Continuation 줄", INFO)])
d.save("05-02.reassembly-on-off.svg")
