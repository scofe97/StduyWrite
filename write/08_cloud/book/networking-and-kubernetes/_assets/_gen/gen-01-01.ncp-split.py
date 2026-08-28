# 01-01.ncp-split — 하나였던 프로토콜이 둘로 갈라진 자리
# 본문 요구: "NCP 는 하나가 모든 일을 했고, 다양성을 감당하지 못했다. 1974 TCP, 1981
#           RFC 791 이 IP 를 떼어 내 책임을 덜었다" — 무엇이 쪼개졌는지가 논점.
# 타입 스펙: type-data-flow.md — 단계 머리(연도) + 한 줄 체인. 이 폴더의 chapter-overview 들이
#           쓰는 stage_chain 과 같은 형태다. 다만 흐르는 것은 데이터가 아니라 *책임*이다 —
#           신뢰성·주소·전달 세 슬롯이 세 세대를 지나며 어느 상자에 담기는지가 바뀐다.
#           마지막 칸에서 한 상자가 둘로 갈라지는 자리가 이 그림의 논지라 거기만 focal 이다.
#           type-timeline 은 아니다 — 기준선·눈금·원이 없고, 연도는 축이 아니라 칸 머리글이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 500
d = D(W, H, "1970 → 1981 · RESPONSIBILITY SPLIT",
      "하나가 다 하던 프로토콜이 둘로 갈라진 자리",
      "NCP 는 신뢰성과 주소와 전달을 한 몸에 지녔고, RFC 791 이 IP 를 떼어 내 TCP 의 책임을 덜었다.",
      lead="계층 분리는 이론이 아니라 확장 실패에 대한 대응이었다")

CX, BW, BY, BH = [156, 500, 844], 224, 172, 168   # 상자 224 · 사이 120 은 4의 배수
# focal 테두리가 BY-12 에서 시작하므로 단계 라벨은 그보다 위에 둔다 — 겹치면 라벨을 관통한다
STAGE = [("1970", "NCP"), ("1974", "TCP · RFC 675 초안"), ("1981", "RFC 791")]
for cx, (yr, nm) in zip(CX, STAGE):
    d.t(cx, 124, yr, 11, SOFT, MONO)
    d.t(cx, 148, ddx.fit(nm, 12, BW, nm), 12, MUTED, KR, "middle", 600)

def cell(cx, y, h, title, chips, c, focal=False):
    x = cx - BW // 2
    if focal:
        d.tone(x, y, BW, h, ACC, 6, "12", 1.4); tc = ACC
    else:
        d.box(x, y, BW, h, PAPER2, c, 1.1, 6); tc = c
    d.t(cx, y + 32, ddx.fit(title, 14, BW - 24, title), 14, tc, KR, "middle", 600)
    for i, ch in enumerate(chips):
        d.t(cx, y + 68 + i * 32, ddx.fit(ch, 12, BW - 32, ch), 12, MUTED, KR)

cell(CX[0], BY, BH, "NCP 하나", ["신뢰성", "주소", "전달"], WARN)
cell(CX[1], BY, BH, "TCP 하나", ["신뢰성", "주소 · 전달"], INFO)
cell(CX[2], BY, 76, "TCP", ["신뢰성"], INFO)
cell(CX[2], BY + 92, 76, "IP", ["주소 · 전달"], INFO)
d.o.append(f'<rect x="{CX[2]-BW//2-12}" y="{BY-12}" width="{BW+24}" height="{BH+24}" rx="8" '
           f'fill="none" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX[2], BY + BH + 36, "여기서 책임이 갈렸다", 12, ACC, KR)

for i, lines in enumerate([["네트워크 종류가", "다양해지자 못 버팀"], ["IP 를 떼어 내", "책임을 덜다"]]):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.path(f"M {a+8} {BY+96} L {b-10} {BY+96}", MUTED, 1.5, m="ar")
    for j, ln in enumerate(lines):
        d.t((a + b) // 2, BY + 56 + j * 20, ddx.fit(ln, 11, b - a, ln), 11, MUTED, KR)

d.t(36, 424, "쪼갠 뒤에야 새 종류의 네트워크가 붙어도 한쪽만 고치면 됐다 — 모듈성이 오른 자리가 여기다",
    12, MUTED, KR, "start")
d.legend(436, [("한 몸에 다 지님", WARN), ("나뉜 책임", INFO), ("갈라진 자리", ACC)])
d.save("01-01.ncp-split.svg")
print("ok ncp-split")
