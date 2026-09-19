# 02-03 §3 — I/O Graph 의 두 그래프를 같은 시간축에 겹친 모습. 값은 본문의
# `tshark -r io.pcap -q -z 'io,stat,1,,tcp.analysis.duplicate_ack'` 출력의 Frames 두 열을 그대로 옮긴다.
# 본문: "평소 1초에 4프레임이던 흐름이 6 <> 7 칸에서 22프레임으로 뛰었고, 그중 10개가 중복 ACK 입니다."
# 타입 스펙: type-line — 시간 인덱스(1초 칸 10개) 위의 연속 추세. 시리즈 2개, 초점(Graph2)만 점을 찍는다.
#           y 축은 0 을 포함하고 x 는 등간격. 비초점은 스타일 계약 토큰 muted.
#           축약: 스펙 viewBox 1000×500 대신 폴더 본문 폭 880 에 맞춘다(계약 표 880~1000).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, RULE, KR, MONO

W, H = 880, 520
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-03 §3",
      "중복 ACK 이 몰린 6초 칸",
      "문서용 주소로 만든 10초짜리 내려받기 캡처를 1초 간격으로 센 값. 모든 프레임(Graph1)은 평소 4프레임에서 6초 칸에 22프레임으로 뛰고, 같은 칸에서 tcp.analysis.duplicate_ack(Graph2)가 0 에서 10 으로 솟는다.",
      "두 선을 같은 축에 겹치면 급증의 절반 가까이가 중복 ACK 이라는 것이 한눈에 갈립니다")

PL, PR, PT, PB = 80, W - 40, 112, 400
ticks = [str(i) for i in range(10)]
all_frames = [7, 4, 4, 4, 4, 4, 22, 4, 4, 4]
dup_ack    = [0, 0, 0, 0, 0, 0, 10, 0, 0, 0]
YMAX = 25
def X(i): return PL + i * (PR - PL) / (len(ticks) - 1)
def Y(v): return PB - v / YMAX * (PB - PT)

for g in range(0, YMAX + 1, 5):
    d.line(PL, Y(g), PR, Y(g), RULE, 1.0 if g == 0 else 0.8)
    d.t(PL - 12, Y(g) + 4, f"{g}", 12, SOFT, MONO, "end")
d.t(PL - 12, PT - 16, "프레임", 12, SOFT, KR, "end")
d.line(PL, PT, PL, PB, RULE, 0.8)
for i, tk in enumerate(ticks):
    d.line(X(i), PB, X(i), PB + 6, RULE, 0.8)
    d.t(X(i), PB + 24, tk, 12, MUTED, MONO)
d.t((PL + PR) / 2, PB + 48, "캡처 시작부터 초 · 칸 간격 1초", 12, SOFT, KR)

def series(vals, color, sw, dots):
    pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
    d.o.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>')
    if dots:
        for i, v in enumerate(vals):
            d.o.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4" fill="{color}"/>')

series(all_frames, MUTED, 1.2, False)
series(dup_ack, ACC, 1.8, True)

# 논점 하나만 값으로 못 박는다 — 6초 칸의 두 값
d.t(X(6), Y(22) - 14, "22 프레임", 12, INK, KR, "middle", 600)
# 7초 칸부터는 두 선이 모두 내려앉아 비어 있으므로, 점에서 가로 지시선을 끌어 그 자리에 값을 적는다
d.line(X(6) + 6, Y(10), X(7) + 8, Y(10), ACC, 0.8, "2,3")
d.t(X(7) + 14, Y(10) - 8, "중복 ACK 10", 12, ACC, KR, "start", 600)
d.t(X(0) + 12, Y(7) - 12, "연결을 여는 세 프레임 포함 7", 12, SOFT, KR, "start")
d.t(X(2), Y(4) + 24, "평소 4", 12, MUTED, KR, "middle")

d.legend(472, [("모든 프레임 · Graph1", MUTED), ("tcp.analysis.duplicate_ack · Graph2", ACC)])
d.save("02-03.io-graph.svg")
