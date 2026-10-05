# 12-01 §3 — 원서 Figure 12-1(송신자의 창, 크기 3)과 그 뒤 ACK 4 가 도착한 장면을 같은 격자 두 줄로 잇는다.
# 원문 12.1.2: 창 = 보냈지만 아직 확인받지 못한 패킷(또는 그 번호)의 모음. 그림의 창은 4·5·6 이고
#   3 은 이미 보내고 확인받아 사본을 버릴 수 있으며, 7 은 준비됐지만 창 밖이라 못 보낸다.
#   ACK 4 가 오면 창이 오른쪽으로 한 칸 "미끄러져" 4 의 사본을 버리고 7 을 보낼 수 있다.
# 타입 스펙: type-dp-security-matrix — 윗줄과 아랫줄이 같은 열(패킷 번호)을 공유하고, 셀 색만 바뀐다.
#           축약: 열이 역할이 아니라 패킷 번호 1–9 라 열 수가 스펙 상한 6 을 넘는다. role_col_w 148 → 64,
#           role_col_gap 16 → 8 로 줄이고 행 높이·행 간격·헤더 공식은 그대로 쓴다.
#           두 줄 위의 괄호가 창의 범위이고, 괄호가 한 칸 옮겨 간 것이 곧 "미끄러짐"이다.
#           focal 은 아랫줄에서 새로 보낼 수 있게 된 7 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

left_pad, right_pad = 12, 48
comp_col_w, comp_role_gap = 208, 12
col_w, col_gap = 64, 8
row_h = 36
N = 9
W = left_pad + comp_col_w + comp_role_gap + N * col_w + (N - 1) * col_gap + right_pad   # 912
def cx(i): return left_pad + comp_col_w + comp_role_gap + i * (col_w + col_gap)

ROWS = [   # (이름, 부제, 창 시작 번호, 창 끝 번호)
    ("ACK 4 받기 전", "원서 그림 12-1", 4, 6),
    ("ACK 4 받은 뒤", "창이 한 칸 이동", 5, 7),
]
Y_HEAD = 104
Y_ROW = [192, 296]      # 행 사이에 괄호 띠(28px)를 둘 자리를 둔다

H = Y_ROW[-1] + row_h + 140
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §3",
      "송신자의 창이 미끄러지는 한 걸음",
      "윗줄은 원서 그림 12-1 의 상태로 창 크기는 3 이다. 1–3 은 보내고 확인까지 받아 사본을 버렸고, 4–6 은 창 안이라 보냈거나 보낼 수 있으며, "
      "7 부터는 창 밖이라 준비돼 있어도 못 보낸다. 아랫줄은 ACK 4 가 도착한 직후로, 창이 한 칸 오른쪽으로 옮겨 4 의 사본을 버리고 7 을 보낼 수 있게 됐다.",
      "칸 색이 바뀌는 자리는 창의 양 끝 두 곳뿐입니다")

# 헤더 행 — 패킷 번호
d.box(left_pad, Y_HEAD, comp_col_w, 44, PAPER2, RULE, 0.8, 6)
d.t(left_pad + comp_col_w / 2, Y_HEAD + 27, "패킷 번호 →", 13, MUTED, KR)
for i in range(N):
    d.box(cx(i), Y_HEAD, col_w, 44, "#2A3140", RULE, 0.8, 6)
    d.t(cx(i) + col_w / 2, Y_HEAD + 28, str(i + 1), 15, INK, MONO, "middle", 600)

for r, (name, sub, ws, we) in enumerate(ROWS):
    y = Y_ROW[r]
    d.box(left_pad, y, comp_col_w, row_h, PAPER2, RULE, 0.8, 4)
    d.t(left_pad + 12, y + 23, name, 13, INK, KR, "start", 600)
    d.t(left_pad + comp_col_w - 12, y + 23, sub, 11, MUTED, KR, "end")
    # 창 괄호 — 행 위 띠
    bx0, bx1 = cx(ws - 1), cx(we - 1) + col_w
    by = y - 16
    d.path(f"M {bx0} {by + 8} V {by} H {bx1} V {by + 8}", INFO, 1.3)
    d.t((bx0 + bx1) / 2, by - 6, "창 · 크기 3", 11, INFO, KR, "middle", 600)
    for i in range(N):
        n = i + 1; x = cx(i)
        if r == 1 and n == 7:
            d.o.append(f'<rect x="{x}" y="{y}" width="{col_w}" height="{row_h}" rx="4" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + col_w / 2, y + 23, "보냄", 12, ACC, KR, "middle", 600)
        elif n < ws:
            d.tone(x, y, col_w, row_h, OK, 4, "14", 0.9)
            d.t(x + col_w / 2, y + 23, "확인", 12, OK, KR, "middle", 600)
        elif n <= we:
            d.tone(x, y, col_w, row_h, INFO, 4, "14", 0.9)
            d.t(x + col_w / 2, y + 23, "창 안", 12, INFO, KR, "middle", 600)
        else:
            d.box(x, y, col_w, row_h, PAPER, RULE, 0.8, 4)
            d.t(x + col_w / 2, y + 23, "대기", 12, SOFT, KR, "middle")

# 두 줄 사이 — ACK 4 도착
ay = Y_ROW[0] + row_h + 24
d.chip(cx(3) + col_w / 2, ay, "ACK 4 도착", MUTED, 12)

# 바닥 해설 — 두 끝에서 일어나는 일
yb = Y_ROW[1] + row_h + 36
d.t(cx(3) + col_w / 2, yb, "왼쪽 끝 · 4 의 사본 해제", 12, OK, KR)
d.t(cx(6) + col_w / 2, yb + 22, "오른쪽 끝 · 7 송신 허용", 12, ACC, KR)

d.legend(H - 56, [("새로 보낼 수 있게 된 칸", ACC), ("보내고 확인 끝", OK), ("창 안 · 보냈거나 보낼 수 있음", INFO), ("창 밖 · 아직 못 보냄", SOFT)])
d.save("12-01.sliding-window.svg")
