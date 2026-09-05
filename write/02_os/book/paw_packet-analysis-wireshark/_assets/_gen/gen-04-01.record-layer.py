# 04-01 §5 — 레코드 계층이 애플리케이션 데이터를 어떤 순서로 처리하는가.
# 원문: "The Application Data message is carried by the record layer and fragmented, compressed,
# and encrypted." TLS 1.3 에서 압축 단계가 빠진 것을 색으로 구분한다.
# 타입 스펙: type-process — 단계마다 같은 의미 슬롯(번호 · 하는 일 · 남는 것)이 반복되고
#           화살표가 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 344
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §5",
      "레코드 계층이 하는 일",
      "핸드셰이크가 끝나면 애플리케이션 데이터가 레코드 계층을 지난다. 원문이 적는 순서는 조각내기·압축·암호화 셋이며, TLS 1.3 은 이 중 압축을 없앴다.",
      "Wireshark 가 보는 것은 마지막 칸의 결과입니다 — 그 안은 키가 있어야 열립니다")

CW, CH, GAP, X0, Y = 208, 108, 24, 24, 128     # stride = 232
cards = [
    ("00", "애플리케이션 데이터", "HTTP 요청·응답 그대로", None),
    ("01", "조각내기", "레코드 크기로 자릅니다", None),
    ("02", "압축", "TLS 1.3 에서 없어졌습니다", BAD),
    ("03", "암호화", "content_type == 23 로 나갑니다", ACC),
]

for i, (n, title, sub, c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if c == ACC:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, Y, CW, CH, c, 8)
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    col = c if c else INK
    d.t(x + 20, Y + 28, n, 11, col if c else SOFT, MONO, "start", 600)
    d.t(x + 20, Y + 56, title, 15, col, KR, "start", 600)
    d.t(x + 20, Y + 80, sub, 12, MUTED, KR, "start")
    if i:
        d.arrow([(x - GAP, Y + CH / 2), (x - 4, Y + CH / 2)], MUTED, "ar", 1.4)

d.t(X0 + 2 * (CW + GAP) + CW / 2, Y + CH + 28, "RFC 8446 이 없앤 단계", 11, BAD, KR)

d.legend(H - 60, [("Wireshark 가 보는 결과", ACC), ("TLS 1.3 에서 사라진 단계", BAD)])
d.save("04-01.record-layer.svg")
