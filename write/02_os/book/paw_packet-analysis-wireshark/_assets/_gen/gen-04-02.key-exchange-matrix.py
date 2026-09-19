# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가를 행×열 격자로 본다.
#           축약: 스펙의 역할·컴포넌트 어휘 대신 키 교환 방식 × 성질 축을 쓴다
#           (visual-diagram-selection §알려진 공백의 일반 대조표 선례). focal 은 복호화가
#           RSA 개인키 경로의 조건부 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, COL_W, ROW_H = 300, 200, 72
COLS = ["Server Key Exchange", "전방 비밀성", "서버 장기 개인키 복호화"]
ROWS = [
    ("RSA", "서버 공개키로 pre_master 암호화",
     [("오지 않음", BAD), ("없음", BAD), ("조건부 가능", None)]),
    ("DH_DSS · DH_RSA", "정적 DH — 임시 키 교환 아님",
     [("오지 않음", BAD), ("없음", BAD), ("RSA 등록 경로 밖", MUTED)]),
    ("DHE_DSS · DHE_RSA", "임시 DH — 매번 새 키",
     [("반드시 옴", OK), ("있음", OK), ("불가", BAD)]),
    ("ECDHE_*", "타원곡선 임시 DH",
     [("반드시 옴", OK), ("있음", OK), ("불가", BAD)]),
    ("DH_anon", "익명 DH — 서버 인증이 없음",
     [("반드시 옴", OK), ("임시 키 사용 시", WARN), ("불가", BAD)]),
]
X0, Y0 = 24, 152
W = X0 + LABEL_W + len(COLS) * COL_W + 24
H = Y0 + 40 + len(ROWS) * ROW_H + 120

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02 §1",
      "키 교환 방식이 정하는 것",
      "TLS 1.2 전체 핸드셰이크의 키 교환 비교. RSA 개인키 복호화에는 일치하는 키와 원래의 전체 핸드셰이크가 필요하다. DHE와 ECDHE도 해당 세션 비밀값으로 복호화할 수 있다.",
      "TLS 1.2 전체 핸드셰이크 기준 · 세션 비밀값을 이용한 복호화는 별도 경로입니다")

d.t(X0 + 8, Y0 + 4, "키 교환 방식", 12, SOFT, KR, "start", 600)
for j, c in enumerate(COLS):
    d.t(X0 + LABEL_W + j * COL_W + COL_W / 2, Y0 + 4, c, 12, SOFT, KR)
d.line(X0, Y0 + 18, W - 24, Y0 + 18, RULE, 0.8)

for i, (name, hint, cells) in enumerate(ROWS):
    y = Y0 + 40 + i * ROW_H
    d.box(X0, y, LABEL_W - 12, ROW_H - 12, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 24, name, 12, INK, MONO, "start", 600)
    d.t(X0 + 16, y + 44, hint, 12, MUTED, KR, "start")
    for j, (val, c) in enumerate(cells):
        x = X0 + LABEL_W + j * COL_W
        if c is None:
            d.o.append(f'<rect x="{x}" y="{y}" width="{COL_W - 12}" height="{ROW_H - 12}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + (COL_W - 12) / 2, y + 26, val, 13, ACC, KR, "middle", 600)
            d.t(x + (COL_W - 12) / 2, y + 44, "키 일치 · 전체 handshake", 12, MUTED, KR)
        elif c is MUTED:
            d.box(x, y, COL_W - 12, ROW_H - 12, PAPER, RULE, 0.8, 6)
            d.t(x + (COL_W - 12) / 2, y + 36, val, 12, MUTED, KR, "middle")
        else:
            d.tone(x, y, COL_W - 12, ROW_H - 12, c, 6)
            d.t(x + (COL_W - 12) / 2, y + 36, val, 13, c, KR, "middle", 600)

d.t(X0 + 8, Y0 + 40 + len(ROWS) * ROW_H + 6,
    "DHE·ECDHE: 세션 비밀값으로 복호화 가능 · DH_anon: 서버 인증 없음",
    12, WARN, KR, "start")
d.legend(H - 72, [("RSA 복호화 조건", ACC), ("있음·옵니다", OK), ("없음·불가", BAD)])
d.save("04-02.key-exchange-matrix.svg")
