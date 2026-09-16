# 01-02.tcp-header-layout — TCP 헤더는 32비트 줄을 쌓아 만든다
# 본문 요구(01-02 §2 "헤더 필드와 9개 플래그"): "표에서는 필드가 한 줄씩 나열되지만 실제 헤더는
#           32비트 폭의 줄을 쌓은 격자"이고, "크기가 배치로 드러나면" 옵션이 가변이라 Data offset 이
#           필요하다는 것과 플래그가 1비트씩이라 SYN-ACK 가 한 패킷이 된다는 것이 설명된다.
#           그래서 칸 너비를 비트 수에 정확히 비례시켰다(1비트 = 25px) — 너비가 곧 필드 크기다.
#           플래그 칸이 논지라 focal, Data offset 은 옵션 가변과 짝이라 warn.
# 타입 스펙: type-layers — 줄 다섯 + 옵션이 위에서 아래로 쌓인다(헤더의 바이트 순서). 스펙은 한 층에
#           이름 하나를 두지만, 이 그림은 층 안을 비트 폭 비례 칸으로 가른 변형이다. 카탈로그에
#           "비트 필드 격자" 타입이 없어 layers 로 축약했다.
# 사실 출처: 칸 구성·비트 수는 2026-09-09 손 SVG 원본, 필드 이름·역할은 본문 §2 표. 3비트 칸(원본 "예약 3")과
#           5행 오른쪽 16비트(원본 "긴급 포인터")는 원본 이름을 옮겼다 — 2026-09-16 누락 복원.
# 이력: 2026-09-15 신설. 손 SVG 를 생성기로 옮기며 하단 해설 네 문장(본문 도식 뒤 두 문단과 같은 말)을
#       뺐고, 10px 이하였던 한글·비트 라벨을 11px 이상으로 올렸다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 500
X0, BITW, RY0, RH = 100, 25, 156, 48          # 32비트 × 25px = 800px 폭, 줄 높이 48
# 줄마다 (비트 수, 이름, 부제, 색) — 색 None 은 중립 칸
ROWS = [[(16, "Source port", "16 bit", None), (16, "Destination port", "16 bit", None)],
        [(32, "Sequence number", "32 bit · 바이트 순번", INFO)],
        [(32, "Acknowledgment number", "32 bit · 다음에 기대하는 번호", INFO)],
        [(4, "Data offset", "4 bit", WARN), (3, "Reserved", "3 bit", None),
         (9, "Flags", "9 bit · SYN ACK FIN RST …", ACC), (16, "Window size", "16 bit · 흐름 제어", None)],
        [(16, "Checksum", "16 bit", None), (16, "Urgent pointer", "16 bit", None)]]

d = D(W, H, "LAYER STACK · 01-02 TCP HEADER",
      "TCP 헤더는 32비트 줄을 쌓아 만든다",
      "TCP 세그먼트 헤더를 32비트 폭의 격자로 그린 배치도. 고정 다섯 줄에 포트·시퀀스 번호·확인 번호·"
      "Data offset·플래그·윈도우·체크섬이 들어가고, 그 아래 옵션은 가변이라 헤더 길이가 변한다. "
      "아홉 비트가 나란히 붙은 플래그 칸을 초점으로 강조했다.",
      lead="한 줄이 32비트입니다. 칸 너비가 곧 필드 크기입니다.")

# 비트 눈금
d.line(X0, 128, X0 + 32 * BITW, 128, RULE, 0.8)
for bit, anchor in ((0, "start"), (8, "middle"), (16, "middle"), (24, "middle"), (31, "end")):
    x = X0 + bit * BITW if bit < 31 else X0 + 32 * BITW
    d.t(x, 148, str(bit), 11, SOFT, MONO, anchor)

for r, cells in enumerate(ROWS):
    y = RY0 + 4 + r * RH
    x = X0
    for bits, name, sub, c in cells:
        w = bits * BITW
        if c is ACC:
            d.tone(x, y, w, RH, ACC, 0, "14", 1.4)
        elif c:
            d.tone(x, y, w, RH, c, 0, "12", 1.0)
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 0)
        cx = x + w // 2
        if name:
            d.t(cx, y + 21, ddx.fit(name, 12, w - 12, name), 12, c or INK, MONO, "middle", 600)
        if sub:
            d.t(cx, y + (39 if name else 29), ddx.fit(sub, 11, w - 12, sub), 11, c or SOFT,
                MONO if all(ord(ch) < 128 or ch == '…' for ch in sub) else KR)
        x += w
    d.t(X0 + 32 * BITW + 16, y + 29, str(r + 1), 11, SOFT, MONO, "start")

# 옵션 — 가변 길이라 점선 칸
oy = RY0 + 4 + 5 * RH
d.o.append(f'<rect x="{X0}" y="{oy}" width="{32 * BITW}" height="40" fill="{PAPER}" '
           f'stroke="{RULE}" stroke-width="1" stroke-dasharray="5 4"/>')
d.t(X0 + 16 * BITW, oy + 25, "Options · Padding — 가변 길이", 12, SOFT, KR)

d.legend(460, [("바이트 번호", INFO), ("헤더 길이 칸", WARN), ("플래그 · 각 1비트", ACC)])
d.save("01-02.tcp-header-layout.svg")
print("ok tcp-header-layout")
