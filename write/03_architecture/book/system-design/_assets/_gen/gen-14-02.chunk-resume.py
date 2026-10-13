# 타입 스펙: type-process — 영상 300 MB 를 조각 4 개로 올릴 때 3 번째 조각만 실패하면 시도 2 에서 그 조각만 다시 올린다. 조각이 줄이고 시도가 열이며 칸에 실제 크기가 적힌다.
# 사실 출처: 구조는 추출본 v2.txt 4183~4196행(GOP 경계로 잘라 올리면 실패한 업로드를 빠르게 이어 올린다, 클라이언트가 분할). 300 MB 는 14-01 편의 평균 영상 크기 가정(v2.txt 3934행),
#   조각 4 개와 3 번째 실패는 설명용 가정이다. 계산: 300 MB ÷ 4 = 75 MB, 다시 올리는 양 75 MB ÷ 300 MB = 1/4.
# Layout conventions: 줄 이름 열 x=24 폭 148, 열 셋 폭 252·stride 264(x=188·452·716), 머리 y=100 높이 36, 줄 y=148 부터 stride 76 높이 64, 합계 줄 y=472. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, INK, PAPER2, RULE, SOFT, KR, MONO

W, H = 984, 612
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 14-02 §5",
      "조각으로 올리면 실패한 조각만 다시 올린다",
      "300 MB 영상을 75 MB 조각 4 개로 올리다 3 번째가 실패하면 그 조각 75 MB 만 다시 올리고, 통째로 올렸다면 300 MB 를 다시 올린다. 조각 수와 실패 위치는 설명용 가정이다.",
      "조각 경계는 GOP 경계 · 칸에 크기가 적힌다")

X0, CW, ST = 188, 252, 264
HY, RY, RS, RH = 100, 148, 76, 64
COLS = ("시도 1 · 조각 병렬", "시도 2 · 실패분만", "다시 올린 양")

for i, name in enumerate(COLS):
    x = X0 + ST * i
    d.box(x, HY, CW, 36, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 24, name, 14, INK, KR, "middle", 600)

# (조각, 시도 1 상태, 시도 2 상태, 다시 올린 양)
ROWS = (
    ("조각 1", "ok", "skip", "0 MB"),
    ("조각 2", "ok", "skip", "0 MB"),
    ("조각 3", "bad", "ok", "75 MB"),
    ("조각 4", "ok", "skip", "0 MB"),
)
for r, (nm, a, b, amt) in enumerate(ROWS):
    y = RY + RS * r
    d.t(24, y + 28, nm, 14, INK, KR, "start", 600)
    d.t(24, y + 50, "75 MB", 12, MUTED, MONO, "start")
    for i, st in enumerate((a, b)):
        x = X0 + ST * i
        if st == "ok":
            d.tone(x, y, CW, RH, OK, 6, "12", 1.2)
            d.t(x + CW / 2, y + 38, "75 MB 도착", 14, OK, KR, "middle", 600)
        elif st == "bad":
            d.tone(x, y, CW, RH, BAD, 6, "12", 1.2)
            d.t(x + CW / 2, y + 38, "전송 실패", 14, BAD, KR, "middle", 600)
        else:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
            d.t(x + CW / 2, y + 38, "다시 보내지 않음", 13, SOFT, KR, "middle")
    x = X0 + ST * 2
    hot = amt != "0 MB"
    if hot:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, RH, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, y + 38, amt, 15, ACC if hot else MUTED, MONO, "middle", 600)

# 통째로 올린 경우와의 비교 — 값 바로 위에 라벨을 둔다
SY = RY + RS * 4 + 4
d.line(24, SY - 8, W - 24, SY - 8, RULE, 0.8)
cx = X0 + ST * 2 + CW / 2
d.t(cx, SY + 24, "통째로 올렸다면", 14, INK, KR, "middle", 600)
d.t(cx, SY + 52, "300 MB", 15, BAD, MONO, "middle", 600)
d.t(cx, SY + 76, "조각이면 75 MB", 13, MUTED, KR, "middle")

d.legend(H - 56, [("도착", OK), ("실패", BAD), ("다시 올린 조각", ACC)])
d.save("14-02.chunk-resume.svg")
