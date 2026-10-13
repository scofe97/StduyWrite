# 타입 스펙: type-process — 같은 통을 시각 네 칸에 반복해 그리고, 줄마다(도착 · 토큰 전 · 토큰 후 · 결과) 같은 슬롯에 토큰이 줄고 다시 차는 것을 개수로 보인다.
# 사실 출처: 추출본 v2.txt 980~981행(버킷 크기 4 · 보충 4개 / 1분), 975~979행(요청 하나가 토큰 하나를 소비 · 없으면 버림). 장면 값 1:00:00 토큰 4 · 요청 1 / 1:00:05 토큰 3 · 요청 3 / 1:00:20 토큰 0 · 요청 1 버림 / 1:01:00 4개 보충 은 PDF 쪽 57 그림에서 직접 읽었다.
# Layout conventions: 행 이름 열 x=24, 시각 칸 폭 184 · 간격 16(x=140 부터 stride 200), 머리 y=100, 줄 y=148·204·260·316 높이 40. 토큰 반지름 12 · 간격 40, 요청 칸 20 · 간격 28. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 444
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01 §3",
      "토큰 버킷은 요청마다 토큰을 하나씩 꺼낸다",
      "버킷 크기 4에 분당 4개를 채우는 통에서 1:00:00 요청 1건은 토큰 4개 중 하나를 쓰고, 1:00:05 요청 3건이 나머지를 비우고, 1:00:20 요청은 토큰이 없어 버려지며, 1:01:00 에 4개가 다시 찬다.",
      "버킷 크기 4 · 분당 4개 보충")

X0, CW, STRIDE = 140, 184, 200
HY = 100
RA, RB, RC, RD = 148, 204, 260, 316

# (시각, 도착, 토큰 전, 토큰 후, 결과 문구, 결과 색)
FRAMES = (
    ("1:00:00", 1, 4, 3, "통과 1", OK),
    ("1:00:05", 3, 3, 0, "통과 3", OK),
    ("1:00:20", 1, 0, 0, "버림 1", BAD),
    ("1:01:00", 0, 0, 4, "보충 4", WARN),
)

# 버려지는 칸 — focal
fx = X0 + STRIDE * 2
d.tone(fx - 8, HY - 8, CW + 16, 272, ACC, 8, "10", 1.4)

for r, y, tag in ((0, RA, "도착"), (1, RB, "토큰 전"), (2, RC, "토큰 후"), (3, RD, "결과")):
    d.t(24, y + 26, tag, 14, SOFT, KR, "start", 600)


def tokens(x, y, n):
    for i in range(4):
        cx, cy = x + 36 + 40 * i, y + 20
        if i < n:
            d.o.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="{WARN}33" stroke="{WARN}" stroke-width="1.4"/>')
        else:
            d.o.append(f'<circle cx="{cx}" cy="{cy}" r="12" fill="none" stroke="{RULE}" stroke-width="1.2"/>')


for i, (t, req, before, after, res, rc) in enumerate(FRAMES):
    x = X0 + STRIDE * i
    d.t(x + CW / 2, HY + 24, t, 14, INK, MONO, "middle", 600)
    # 도착 요청
    for k in range(req):
        d.tone(x + 24 + 28 * k, RA + 8, 20, 20, INFO, 3, "22", 1.1)
    d.t(x + 24 + 28 * req + (4 if req else 0), RA + 24, f"{req}건", 13, MUTED, KR, "start")
    tokens(x, RB, before)
    tokens(x, RC, after)
    d.chip(x + CW / 2, RD + 20, res, rc, 13)

d.legend(H - 56, [("요청", INFO), ("토큰", WARN), ("통과", OK), ("버림", BAD), ("버려지는 칸", ACC)])
d.save("04-01.token-bucket-frames.svg")
