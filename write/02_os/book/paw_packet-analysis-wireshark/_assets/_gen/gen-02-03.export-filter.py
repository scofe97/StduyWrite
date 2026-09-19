# 02-03 §5 — 디스플레이 필터로 내보낼 때 새 파일에 어느 프레임이 들어가는가. 본문의 두 명령
# `-Y 'http.response.code == 200' -w ok.pcapng` 와 `-Y 'tcp.stream == 0' -w stream0.pcapng` 을
# tshark 4.6.8 로 실행한 결과(1 프레임 · 10 프레임)를 그대로 옮긴다.
# 타입 스펙: type-swimlane — 레인은 내보내기 필터 둘이고, 각 프레임은 그 필터의 새 파일에 들어갔을 때만
#           그 레인에 놓인다. 축약: 가로축이 절차의 순서가 아니라 원본 파일 안의 프레임 번호다. 그래서 화살표가
#           없고, 맨 위에 원본 19 프레임을 통째로 두어 레인마다 같은 x 에 떨어뜨린다(02-02 fact-guess-judgment 와
#           같은 관례). 들어가지 않은 프레임은 빈 점선 칸으로 남긴다. focal 은 따라오지 않은 응답 머리(9번) 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-03 §5",
      "필터가 고른 프레임만 새 파일에 들어갑니다",
      "두 HTTP 연결이 섞인 원본 19 프레임에서, 200 응답 필터는 재조립 결과가 얹힌 10번 한 프레임만 새 파일에 쓰고 응답 머리인 9번은 남긴다. 스트림 번호 필터는 0번 연결의 10 프레임을 모두 쓴다.",
      "응답 끝 조각만 담긴 파일에서는 받는 쪽이 HTTP 를 알아볼 수 없습니다")

STREAM = [0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1]   # 원본 프레임 1~19 의 tcp.stream
X0, STRIDE, CW, CH = 240, 32, 26, 28
def cx(n): return X0 + (n - 1) * STRIDE              # 프레임 n 칸의 왼쪽 x

# 원본
TOP = 116
d.t(24, TOP + 12, "원본 http.pcap", 13, INK, KR, "start", 600)
d.t(24, TOP + 31, "두 연결이 번갈아 나옴", 12, MUTED, KR, "start")
for n, s in enumerate(STREAM, 1):
    c = INFO if s == 0 else SOFT
    d.tone(cx(n), TOP, CW, CH, c, 4, "18" if s == 0 else "10", 1.0)
    d.t(cx(n) + CW / 2, TOP + 19, str(n), 12, INK if s == 0 else MUTED, MONO)
d.t((cx(9) + cx(10) + CW) / 2, TOP - 10, "응답 머리 · 본문 끝", 12, SOFT, KR)
d.line(24, 164, W - 24, 164, RULE, 0.8)

LANES = [  # (필터, 결과, 색, 새 파일에 들어간 프레임)
    ("http.response.code == 200", "1 프레임 · TCP 로만 보임", WARN, {10}),
    ("tcp.stream == 0", "10 프레임 · 200 응답 남음", OK,
     {n for n, s in enumerate(STREAM, 1) if s == 0}),
]
Y0, RS = 176, 88
for i, (flt, res, c, keep) in enumerate(LANES):
    y = Y0 + i * RS
    if i:
        d.line(24, y - 6, W - 24, y - 6, RULE, 0.6)
    d.t(24, y + 26, flt, 12, INK, MONO, "start", 600)
    d.t(24, y + 46, res, 12, c, KR, "start", 600)
    cy = y + 16
    for n in range(1, len(STREAM) + 1):
        if n in keep:
            d.tone(cx(n), cy, CW, CH, c, 4)
            d.t(cx(n) + CW / 2, cy + 19, str(n), 12, c, MONO)
        elif i == 0 and n == 9:                          # focal — 재조립에 쓰였지만 따라오지 않은 머리
            d.o.append(f'<rect x="{cx(n)}" y="{cy}" width="{CW}" height="{CH}" rx="4" fill="{ACC}12" '
                       f'stroke="{ACC}" stroke-width="1.4" stroke-dasharray="4,3"/>')
            d.t(cx(n) + CW / 2, cy + 19, "9", 12, ACC, MONO)
        else:
            d.o.append(f'<rect x="{cx(n)}" y="{cy}" width="{CW}" height="{CH}" rx="4" fill="none" '
                       f'stroke="{SOFT}" stroke-opacity="0.45" stroke-width="0.8" stroke-dasharray="3,3"/>')
    if i == 0:
        d.t(cx(9) + CW / 2, cy + CH + 20, "9번 머리가 따라오지 않음", 12, ACC, KR, "middle", 600)

d.legend(364, [("0번 연결", INFO), ("1번 연결", SOFT), ("빠진 응답 머리", ACC), ("깨지는 파일", WARN), ("온전한 파일", OK)])
d.save("02-03.export-filter.svg")
