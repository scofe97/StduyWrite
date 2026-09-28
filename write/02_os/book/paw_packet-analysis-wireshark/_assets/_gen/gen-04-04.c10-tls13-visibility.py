# 04-04 C10 — 같은 TLS 1.3 캡처(c10-tls13.pcap)를 키 없이·키 로그를 물려 읽은 두 tshark 출력의 대조. 실측값만 쓴다.
# 타입 스펙: type-dp-security-matrix — 프레임 × 읽는 조건 격자로 "무엇이 보이는가"를 본다.
#           축약: 역할·컴포넌트 어휘 대신 프레임×조건 축을 쓴다(02-02 filter-direction-matrix 와 같은 선례).
#           level 어휘는 보임/안 보임 두 단계, focal 은 다섯 종류가 한꺼번에 드러나는 셀 하나.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _tls_lab import W, EYEBROW, D, kr, ACC, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
LABEL_W, COL_W, ROW_H = 272, 280, 76
COLS = ["키 없이", "키 로그를 물림"]
ROWS = [("프레임 4", "ClientHello", [("1", OK, None), ("1", OK, None)]),
        ("프레임 6", "ServerHello 와 뒤따르는 넷", [("2", OK, None), ("2 · 8 · 11 · 15 · 20", None, "인증서(11) 포함")]),
        ("프레임 10 · 11", "핸드셰이크가 끝난 뒤", [("종류 안 읽힘", BAD, None), ("4", OK, "NewSessionTicket")])]
X0, Y0 = 24, 136
H = Y0 + 40 + len(ROWS) * ROW_H + 80
d = D(W, H, EYEBROW + "C10", "C10 · 같은 1.3 캡처, 두 번 읽기",
      "키 없이 읽으면 handshake.type 이 1 과 2 둘뿐이다. 같은 캡처에 키 로그를 물리면 프레임 6 에서 8·11·15·20 이 함께 드러나고, 프레임 10·11 은 NewSessionTicket(4) 로 읽힌다.",
      "인증서(11)는 오지 않은 것이 아니라 암호화돼 있었습니다")
d.t(X0 + 8, Y0 + 4, "tshark 출력의 프레임", 11, SOFT, KR, "start", 600)
for j, name in enumerate(COLS):
    d.t(X0 + LABEL_W + j * COL_W + (COL_W - 12) / 2, Y0 + 4, name, 12, SOFT, KR, "middle", 600)
d.line(X0, Y0 + 18, W - 24, Y0 + 18, RULE, 0.8)
for i, (name, hint, cells) in enumerate(ROWS):
    y = Y0 + 40 + i * ROW_H
    d.box(X0, y, LABEL_W - 12, ROW_H - 12, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 26, name, 13, INK, KR, "start", 600)
    d.t(X0 + 16, y + 46, hint, 11, MUTED, kr(hint), "start")
    for j, (val, c, sub) in enumerate(cells):
        x = X0 + LABEL_W + j * COL_W; cw = COL_W - 12; cx = x + cw / 2
        if c is None:
            d.o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ROW_H - 12}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            c = ACC
        else:
            d.tone(x, y, cw, ROW_H - 12, c, 6)
        if sub:
            d.t(cx, y + 28, val, 13, c, kr(val), "middle", 600)
            d.t(cx, y + 48, sub, 11, MUTED, kr(sub))
        else:
            d.t(cx, y + 38, val, 13, c, kr(val), "middle", 600)
d.legend(H - 56, [("키로 드러난 인증서 구간", ACC), ("읽힘", OK), ("읽히지 않음", BAD)])
d.save("04-04.c10-tls13-visibility.svg")
