# 03-04.build-stage-choice — 같은 바이너리가 어느 베이스에 얹히느냐로 45배가 갈린다
# 본문 요구: §3 의 실측이 "multistage 를 썼는데도 1.08GB, 베이스만 alpine 으로 바꾸니 23.8MB".
#           즉 갈림은 빌드 방식이 아니라 실행 스테이지의 베이스 선택 한 곳에서 일어난다.
#           그 한 곳을 분기점으로 세워야 "multistage 는 자유를 줄 뿐"이 그림으로 보인다.
# 타입 스펙: type-flowchart.md — 한 줄기가 판단 한 곳에서 두 갈래로 갈리고 결과가 다르다.
#           갈림 이후 두 경로의 y 를 대칭으로 두어 같은 입력이라는 것을 좌표로 보인다.
# 좌표: Layout conventions 타입이라 공식이 없다. 가로 stride 224 하나, 갈래 y 오프셋 ±88.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 540
BW, BH, MID = 176, 76, 232
COL = [40, 264, 512, 760]     # stride 224·248 — 분기 뒤 라벨 자리를 넓게 둔다
ARM = 88

d = D(W, H, "MULTISTAGE · WHERE THE SIZE IS DECIDED",
      "같은 바이너리, 다른 베이스 — 45배는 여기서 갈린다",
      "multistage 빌드에서 실행 스테이지의 베이스를 무엇으로 두느냐에 따라 최종 이미지 크기가 갈리는 흐름. "
      "빌드 스테이지와 산출 바이너리는 두 갈래가 공유하고, 갈리는 지점은 두 번째 FROM 한 줄뿐이다.",
      lead="multistage 는 크기를 줄이는 장치가 아니라 실행 베이스를 고를 자유를 주는 장치입니다")


def box(cx, cy, t, sub, tag, c=None, focal=False):
    x, y = cx - BW // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = ACC
    else:
        d.box(x, y, BW, BH, PAPER2, c or RULE, 1.1, 6)
        tc = c or INK
    d.t(cx, cy - 16, ddx.fit(t, 13, BW - 18, t), 13, tc,
        MONO if all(ord(ch) < 128 or ch in ':.' for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(sub, 11, BW - 16, sub), 11, MUTED, KR)
    d.t(cx, cy + 24, ddx.fit(tag, 11, BW - 14, tag), 11, c or SOFT,
        MONO if all(ord(ch) < 128 or ch in '·.' for ch in tag) else KR)


CX = [c + BW // 2 for c in COL]
box(CX[0], MID, "web-server.go", "소스 한 파일", "COPY 대상", INFO)
box(CX[1], MID, "golang:1.15", "빌드 스테이지 — 컴파일", "1.07GB · 여기서만 필요", INFO)
box(CX[2], MID, "web-server", "정적 링크 바이너리", "9.2MB · 두 갈래가 공유", ACC)

d.path(f"M {CX[0]+BW//2+8} {MID} L {CX[1]-BW//2-10} {MID}", MUTED, 1.5, m="ar")
d.path(f"M {CX[1]+BW//2+8} {MID} L {CX[2]-BW//2-10} {MID}", MUTED, 1.5, m="ar")
d.t((CX[1] + CX[2]) // 2, MID - 18, "go build", 11, MUTED, MONO)

# 갈림 — 두 번째 FROM 한 줄이 정하는 자리
BR = CX[2] + BW // 2 + 40
d.path(f"M {CX[2]+BW//2+8} {MID} L {BR} {MID}", ACC, 1.5)
d.path(f"M {BR} {MID} L {BR} {MID-ARM} L {CX[3]-BW//2-10} {MID-ARM}", MUTED, 1.5, m="ar")
d.path(f"M {BR} {MID} L {BR} {MID+ARM} L {CX[3]-BW//2-10} {MID+ARM}", ACC, 1.5, m="acc")
d.t(BR + 8, MID + 4, "두 번째 FROM", 11, ACC, KR, "start")

box(CX[3], MID - ARM, "1.08GB", "FROM golang:1.15", "베이스를 그대로 둔 판", BAD)
box(CX[3], MID + ARM, "23.8MB", "FROM alpine:3.20", "베이스만 갈아 끼운 판", None, focal=True)

d.t(40, MID + ARM + 96,
    "빌드 스테이지도 바이너리도 두 갈래가 똑같습니다. 달라진 것은 두 번째 FROM 한 줄뿐이고, 거기서 45배가 갈립니다.",
    12, MUTED, KR, "start")
d.t(40, MID + ARM + 120,
    "캐시는 COPY 부터 깨집니다. COPY 만 파일 내용을 캐시 키에 넣기 때문에, 소스를 고치면 그 아래가 전부 다시 돕니다.",
    12, MUTED, KR, "start")
d.legend(MID + ARM + 144, [("두 갈래가 공유", ACC), ("빌드에만 필요", INFO), ("안 줄어든 판", BAD)])
d.save("03-04.build-stage-choice.svg")
print("ok build-stage-choice")
