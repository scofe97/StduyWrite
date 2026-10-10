# 타입 스펙: type-process — 송신 창의 세 시점 바이트 띠 변화(초기 → 왼쪽 끝 전진 → 오른쪽 끝 전진).
# 사실 출처: 원서 §15.5.1 Figure 15-9 — 바이트 번호 2~12, SND.UNA=4, SND.NXT=7, WND=6. ACK 로 닫힘(왼쪽 전진), 창 갱신으로 열림(오른쪽 전진).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W = 920
left_pad = 20
label_col_w = 170
gap_col = 14
N = 11  # 바이트 2 ~ 12
cell_w = 58
cell_gap = 6
cell_h = 34

ROWS = [
    ("1. 초기 상태", "제공 창 6 (4~9)", 4, 9, 7),
    ("2. ACK 7 도착", "왼쪽 끝 전진(닫힘)", 7, 9, 7),
    ("3. 창 업데이트", "오른쪽 끝 전진(열림)", 7, 12, 7),
]

Y_HEAD = 100
Y_ROWS = [174, 268, 362]
H = 470

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-02 §1",
      "슬라이딩 윈도 경계의 닫힘과 열림",
      "송신 창의 왼쪽 끝은 ACK 가 도착할 때 오른쪽으로 전진하며 창을 닫고, 오른쪽 끝은 수신자가 새 창을 광고할 때 전진하며 창을 연다. 오른쪽 끝이 왼쪽으로 후퇴하는 창 줄어듦은 강하게 막는다(SHOULD NOT).",
      "ACK 는 왼쪽 끝을 밀어 닫고 새 창 광고는 오른쪽 끝을 밀어 엽니다")

def cx(idx):
    return left_pad + label_col_w + gap_col + idx * (cell_w + cell_gap)

# 헤더: 바이트 번호 2 ~ 12
d.box(left_pad, Y_HEAD, label_col_w, 36, PAPER2, RULE, 0.9, 6)
d.t(left_pad + label_col_w / 2, Y_HEAD + 22, "바이트 번호 →", 12, MUTED, KR, "middle")

for i in range(N):
    byte_num = i + 2
    x = cx(i)
    d.box(x, Y_HEAD, cell_w, 36, PAPER2, RULE, 0.9, 6)
    d.t(x + cell_w / 2, Y_HEAD + 23, str(byte_num), 14, INK, MONO, "middle", 600)

for r_idx, (r_title, r_desc, w_start, w_end, nxt) in enumerate(ROWS):
    y = Y_ROWS[r_idx]
    d.box(left_pad, y, label_col_w, cell_h, PAPER2, RULE, 0.9, 6)
    d.t(left_pad + 12, y + 16, r_title, 12, INK, KR, "start", 600)
    d.t(left_pad + 12, y + 29, r_desc, 11, MUTED, KR, "start")

    # 창 범위 브래킷 상단
    x_s = cx(w_start - 2)
    x_e = cx(w_end - 2) + cell_w
    by = y - 10
    d.path(f"M {x_s} {by + 5} V {by} H {x_e} V {by + 5}", INFO, 1.2)
    d.t((x_s + x_e) / 2, by - 4, f"제공 창 {w_end - w_start + 1}B", 11, INFO, KR, "middle", 500)

    for i in range(N):
        b = i + 2
        x = cx(i)
        if b < w_start:
            d.tone(x, y, cell_w, cell_h, OK, 4, "15", 0.9)
            d.t(x + cell_w / 2, y + 21, "확인", 12, OK, KR, "middle", 500)
        elif b < nxt:
            d.tone(x, y, cell_w, cell_h, WARN, 4, "15", 0.9)
            d.t(x + cell_w / 2, y + 21, "미확인", 12, WARN, KR, "middle", 500)
        elif b <= w_end:
            d.tone(x, y, cell_w, cell_h, ACC, 4, "18", 1.0)
            d.t(x + cell_w / 2, y + 21, "송신 가능", 11, ACC, KR, "middle", 600)
        else:
            d.box(x, y, cell_w, cell_h, PAPER, RULE, 0.8, 4)
            d.t(x + cell_w / 2, y + 21, "창 밖", 11, SOFT, KR, "middle")

d.legend(H - 46, [("송신 및 확인 완료", OK), ("송신했으나 미확인", WARN), ("사용 가능 창", ACC), ("제공 창 범위", INFO), ("창 밖 (송신 불가)", SOFT)])
d.save("15-02.window-movement.svg")
