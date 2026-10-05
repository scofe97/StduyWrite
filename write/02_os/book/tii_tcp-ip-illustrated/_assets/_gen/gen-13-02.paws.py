# 13-02 §5 — PAWS: 한 바퀴 돈 순서 번호를 타임스탬프가 가려낸다. 원서 Table 13-2 를 본문 서술로 재구성했다(원서 표는 그림이라 값이 텍스트에 없음).
# 원문 13.3.4 서술: 창 약 1GB(2^30), 창 하나마다 타임스탬프 1 증가, 6GB 전송, G = 1,073,741,824.
#   시각 B 에 세그먼트 하나가 사라져 재전송되고, 32비트 순서 번호는 D 와 E 사이에서 한 바퀴 돈다. 사라졌던 세그먼트가 F 에 다시 나타나는데
#   타임스탬프 2 가 가장 최근 유효 값(5 또는 6)보다 작아 PAWS 가 버린다.
# 재구성 가정: 시각마다 1G 씩 보내고 타임스탬프는 1~6. 순서 번호는 4G 에서 0 으로 돌아간다(32비트 = 4G).
# 타입 스펙: type-dp-security-matrix — 행(시각)마다 같은 열(보낸 바이트 · 순서 번호 · 타임스탬프 · 수신 판정)이 반복되는 격자.
#           축약: 열 4개, role_col_w 148 → 152. focal 은 F 에 다시 나타난 B 의 세그먼트가 버려지는 판정 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2, RULE, KR, MONO

left_pad, right_pad = 12, 48
comp_col_w, gap = 200, 12
col_w, col_gap = 152, 12
cols = ["보낸 바이트", "순서 번호", "타임스탬프", "수신 판정"]
rows = [
    ("A", "", ("0G:1G", "0G:1G", "1", "받음"), None),
    ("B", "이 세그먼트가 사라짐", ("1G:2G", "1G:2G", "2", "사라짐 · 재전송"), "lost"),
    ("C", "", ("2G:3G", "2G:3G", "3", "받음"), None),
    ("D", "", ("3G:4G", "3G:4G", "4", "받음"), None),
    ("E", "번호가 한 바퀴", ("4G:5G", "0G:1G", "5", "받음"), "wrap"),
    ("F", "", ("5G:6G", "1G:2G", "6", "받음"), None),
    ("F", "B 의 사본이 다시 나타남", ("1G:2G", "1G:2G", "2", "2 < 6 · 버림"), "focal"),
]
W = left_pad + comp_col_w + gap + len(cols) * col_w + (len(cols) - 1) * col_gap + right_pad
def cx(j): return left_pad + comp_col_w + gap + j * (col_w + col_gap)
HEAD_Y, ROW_Y0, RH, RS = 104, 172, 36, 44
H = ROW_Y0 + len(rows) * RS + 96

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-02 §5",
      "한 바퀴 돈 순서 번호를 타임스탬프가 가려낸다",
      "창 1GB 로 6GB 를 보내며 창마다 타임스탬프를 1 씩 올린다고 하자. 32비트 순서 번호는 4G 에서 0 으로 돌아가므로 E 부터 번호가 겹친다. "
      "B 에서 사라진 세그먼트가 F 에 다시 나타나면 순서 번호(1G:2G)만으로는 F 의 새 데이터와 구분되지 않지만, 타임스탬프 2 가 최근 값 6 보다 작아 버려진다. 원서 표 13-2 를 본문 서술로 재구성했다.",
      "타임스탬프가 순서 번호에 32비트를 덧붙인 셈입니다")

d.box(left_pad, HEAD_Y, comp_col_w, 52, PAPER2, RULE, 0.8, 6)
d.t(left_pad + comp_col_w / 2, HEAD_Y + 31, "시각", 13, INK, KR, "middle", 600)
for j, c in enumerate(cols):
    d.box(cx(j), HEAD_Y, col_w, 52, "#2A3140", RULE, 0.8, 6)
    d.t(cx(j) + col_w / 2, HEAD_Y + 31, c, 13, INK, KR, "middle", 600)

for k, (t, note, vals, kind) in enumerate(rows):
    y = ROW_Y0 + k * RS
    d.box(left_pad, y, comp_col_w, RH, PAPER2, RULE, 0.8, 4)
    d.t(left_pad + 14, y + 23, t, 14, INK, MONO, "start", 600)
    if note:
        d.t(left_pad + 40, y + 23, note, 12, WARN if kind in ("lost", "wrap") else ACC if kind == "focal" else MUTED, KR, "start")
    for j, v in enumerate(vals):
        x = cx(j)
        if kind == "focal" and j == 3:
            d.o.append(f'<rect x="{x}" y="{y}" width="{col_w}" height="{RH}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
        elif kind == "lost" and j == 3:
            d.tone(x, y, col_w, RH, BAD, 4, "12", 0.9); c = BAD
        elif kind == "wrap" and j == 1:
            d.tone(x, y, col_w, RH, WARN, 4, "12", 0.9); c = WARN
        elif j == 3:
            d.tone(x, y, col_w, RH, OK, 4, "10", 0.8); c = OK
        elif kind == "focal":
            d.box(x, y, col_w, RH, PAPER, ACC, 0.8, 4); c = INK
        else:
            d.box(x, y, col_w, RH, PAPER, RULE, 0.6, 4); c = INK
        d.t(x + col_w / 2, y + 23, v, 12, c, MONO if all(ord(ch) < 128 for ch in v) else KR, "middle", 600 if j == 3 else 400)

d.legend(H - 56, [("PAWS 가 버리는 옛 사본", ACC), ("받음", OK), ("번호가 한 바퀴 돎", WARN), ("사라진 세그먼트", BAD)])
d.save("13-02.paws.svg")
