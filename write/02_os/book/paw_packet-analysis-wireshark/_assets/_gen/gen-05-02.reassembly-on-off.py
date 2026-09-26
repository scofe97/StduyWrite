# 05-02 §3 — TCP 재조립을 켰을 때와 껐을 때 같은 HTTP 응답의 http.time 이 어디서 끝나는가.
# 본문 요구: 재조립을 켜든 끄든 조각 수는 사라지지 않고 찍히는 자리만 옮긴다. http.time 도 붙는
#            프레임을 따라 옮겨, 끄면 첫 조각(32.352ms)에서, 켜면 마지막 조각(32.929ms)에서 잰다.
#            두 값의 차이는 첫 조각과 마지막 조각 사이, 곧 본문이 전송되는 동안의 시간이다.
# 왜 시간축인가: 2026-09-26 5장 Phase 4 에서 학습자가 두 값을 "서버 시각 대 클라이언트 시각"으로 읽고,
#            "끄고 나서도 마지막 조각은 받아오는데 무슨 차이인가"를 물었다. 행×열 격자는 어느 프레임에
#            붙는지만 보여 주고, 같은 캡처·같은 도착 시각 위에서 끝점만 달라진다는 흐름은 보여 주지 못했다.
#            그래서 도착 시각 한 줄 위에 두 설정의 막대를 겹친다.
# 값: 2026-09-21 tshark 4.6.8 실측. 루프백에서 HTTP/1.1 로 200KB 파일을 받은 응답 하나(프레임 #5 요청,
#     #7 ~ #33 응답 조각 15개). 켬은 -o tcp.desegment_tcp_streams:TRUE -2, 끔은 FALSE.
#     조각 사이 간격은 균등하게 그린 모식이고, #5 와 #7 사이(서버 처리)는 축을 생략해 줄였다.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간. 두 막대가 같은 출발점(#5)에서 다른 끝점으로 간다.
#           focal 은 재조립 켬의 http.time(마지막 조각까지).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 528
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §3",
      "재조립은 http.time 의 끝점을 옮긴다",
      "같은 캡처 파일을 재조립 켬과 끔으로 연 결과를 도착 시각 한 줄 위에 겹친다. 조각 15개는 두 설정에서 똑같이 같은 시각에 도착한다. 끄면 첫 조각 #7 에 HTTP 응답 줄이 붙어 http.time 이 32.352ms 에서 끝나고, 켜면 조각을 다 모은 마지막 조각 #33 에 붙어 32.929ms 에서 끝난다. 차이 0.577ms 는 본문 조각이 전송된 시간이다.",
      "패킷은 똑같이 도착합니다 — 끄면 첫 조각까지, 켜면 마지막 조각까지 잽니다")

LX = 24                      # 왼쪽 라벨 열
X_REQ, X_FIRST, PITCH = 248, 560, 24
FRAG_X = [X_FIRST + i * PITCH for i in range(15)]   # #7, #9 … #33 — 15개
X_LAST = FRAG_X[-1]                                  # 896
GAP0, GAP1 = 344, 456        # 축 생략 구간

# 도착 시각 축
AX_Y = 140
d.t(LX, AX_Y - 12, "캡처 시각", 13, INK, KR, "start", 600)
d.t(LX, AX_Y + 8, "선 위의 프레임", 12, MUTED, KR, "start")
d.line(X_REQ, AX_Y, GAP0, AX_Y, MUTED, 1.2)
d.line(GAP0, AX_Y, GAP1, AX_Y, SOFT, 1.2, "3 5")
d.line(GAP1, AX_Y, X_LAST + 16, AX_Y, MUTED, 1.2)
for x in [X_REQ] + FRAG_X:
    d.line(x, AX_Y - 5, x, AX_Y + 5, MUTED, 1.2)
d.t(X_REQ, AX_Y - 14, "#5 GET", 12, INK, MONO, "middle", 600)
d.t(X_FIRST, AX_Y - 14, "#7", 12, INK, MONO, "middle", 600)
d.t((FRAG_X[1] + FRAG_X[-2]) / 2, AX_Y - 14, "#9 ~ #32", 12, MUTED, MONO)
d.t(X_LAST, AX_Y - 14, "#33", 12, INK, MONO, "middle", 600)
d.t(X_REQ, AX_Y + 24, "0 ms", 12, MUTED, MONO)
d.t((GAP0 + GAP1) / 2, AX_Y + 24, "축 생략 · 서버 처리", 12, SOFT, KR)
d.t(X_FIRST, AX_Y + 24, "32.352 ms", 12, MUTED, MONO)
d.t(X_LAST, AX_Y + 24, "32.929 ms", 12, MUTED, MONO)

def row(y0, name, sub, sub_c=MUTED):
    d.t(LX, y0 + 36, name, 13, INK, KR, "start", 600)
    d.t(LX, y0 + 56, sub, 12, sub_c, KR, "start", 600 if sub_c != MUTED else 400)

def frag(x, cy, c, filled):
    if filled:
        d.tone(x - 5, cy - 8, 10, 16, c, 2, "55", 1.1)
    else:
        d.box(x - 5, cy - 8, 10, 16, PAPER2, c, 1.0, 2)

def bar(y, x2, txt, c, focal=False):
    if focal:
        d.o.append(f'<rect x="{X_REQ}" y="{y}" width="{x2 - X_REQ}" height="24" rx="4" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(X_REQ, y, x2 - X_REQ, 24, c, 4)
    d.t(X_REQ + 10, y + 17, txt, 12, c, MONO, "start", 600)

# 재조립 끔 — 첫 조각에 응답 줄, 나머지는 Continuation
R1 = 196
row(R1, "재조립 끔", "끝점 · 첫 조각 #7")
d.t(X_FIRST, R1 + 12, "HTTP/1.1 200 OK", 12, OK, MONO, "middle", 600)
for i, x in enumerate(FRAG_X):
    frag(x, R1 + 32, OK if i == 0 else INFO, True)
d.t((FRAG_X[1] + X_LAST) / 2, R1 + 60, "Continuation 14줄", 12, INFO, MONO)
bar(R1 + 72, X_FIRST, "http.time 32.352 ms", OK)

# 재조립 켬 — 조각 줄은 남고 마지막 조각에 응답 줄과 재조립 목록
R2 = 316
row(R2, "재조립 켬", "끝점 · 마지막 조각 #33", ACC)
d.t(X_LAST + 8, R2 + 12, "HTTP/1.1 200 OK", 12, ACC, MONO, "end", 600)
for i, x in enumerate(FRAG_X):
    frag(x, R2 + 32, ACC if i == 14 else SOFT, i == 14)
d.t(648, R2 + 60, "reassembled in 33 · 14줄", 12, MUTED, MONO)
d.t(X_LAST + 8, R2 + 60, "tcp.segment.count 15", 12, ACC, MONO, "end")
bar(R2 + 72, X_LAST, "http.time 32.929 ms", ACC, focal=True)

# 두 값의 차이 — 본문 전송
R3 = 440
d.t(LX, R3 + 4, "두 값의 차이", 13, INK, KR, "start", 600)
d.t(LX, R3 + 24, "같은 캡처 · 같은 도착 시각", 12, MUTED, KR, "start")
d.line(X_FIRST, R3 - 8, X_FIRST, R3 + 8, INFO, 1.4)
d.line(X_LAST, R3 - 8, X_LAST, R3 + 8, INFO, 1.4)
d.line(X_FIRST, R3, X_LAST, R3, INFO, 1.4)
d.t((X_FIRST + X_LAST) / 2, R3 + 24, "0.577 ms · 본문 조각 15개 전송", 12, INFO, KR, "middle", 600)
d.t(X_REQ, R3 + 24, "tshark 4.6.8 실측 · 200KB 응답", 12, SOFT, KR, "start")

d.legend(H - 40, [("켬 · 마지막 조각까지", ACC), ("끔 · 첫 조각까지", OK), ("Continuation 줄", INFO)])
d.save("05-02.reassembly-on-off.svg")
