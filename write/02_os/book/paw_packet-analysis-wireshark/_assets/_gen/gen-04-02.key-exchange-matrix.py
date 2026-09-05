# 04-02 §1 — 키 교환 방식마다 Server Key Exchange 가 오는지, 전방 비밀성이 있는지,
# 서버 개인키만으로 복호화되는지. 원문이 적지 않은 칸은 비워 두고 "원문 미기재"로 표시한다.
# 타입 스펙: type-dp-security-matrix — 어느 조합이 되고 안 되는가를 행×열 격자로 본다.
#           축약: 스펙의 역할·컴포넌트 어휘 대신 키 교환 방식 × 성질 축을 쓴다
#           (visual-diagram-selection §알려진 공백의 일반 대조표 선례). focal 은 복호화가
#           가능한 유일한 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, COL_W, ROW_H = 300, 200, 72
COLS = ["Server Key Exchange", "전방 비밀성", "개인키만으로 복호화"]
ROWS = [
    ("RSA", "서버 공개키로 pre_master 암호화",
     [("오지 않음", BAD), ("없음", BAD), ("가능", None)]),
    ("DH_DSS · DH_RSA", "정적 DH — 원문이 불법이라 적음",
     [("오지 않음", BAD), ("원문 미기재", MUTED), ("원문 미기재", MUTED)]),
    ("DHE_DSS · DHE_RSA · DH_anon", "임시 DH",
     [("옵니다", OK), ("있음", OK), ("불가", BAD)]),
    ("ECDHE_*", "타원곡선 임시 DH",
     [("원문 목록 밖", MUTED), ("있음", OK), ("불가", BAD)]),
]
X0, Y0 = 24, 152
W = X0 + LABEL_W + len(COLS) * COL_W + 24
H = Y0 + 40 + len(ROWS) * ROW_H + 96

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02 §1",
      "키 교환 방식이 정하는 것",
      "Server Hello 에서 고른 cipher suite 의 키 교환 부분이 세 가지를 한꺼번에 정한다. Server Key Exchange 메시지가 오는지, 전방 비밀성이 있는지, 그리고 서버 개인키만으로 복호화가 되는지.",
      "복호화가 되는 칸은 하나뿐이고, 그것은 전방 비밀성이 없다는 뜻이기도 합니다")

d.t(X0 + 8, Y0 + 4, "키 교환 방식", 11, SOFT, KR, "start", 600)
for j, c in enumerate(COLS):
    d.t(X0 + LABEL_W + j * COL_W + COL_W / 2, Y0 + 4, c, 11, SOFT, KR)
d.line(X0, Y0 + 18, W - 24, Y0 + 18, RULE, 0.8)

for i, (name, hint, cells) in enumerate(ROWS):
    y = Y0 + 40 + i * ROW_H
    d.box(X0, y, LABEL_W - 12, ROW_H - 12, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 16, y + 24, name, 12, INK, MONO, "start", 600)
    d.t(X0 + 16, y + 44, hint, 11, MUTED, KR, "start")
    for j, (val, c) in enumerate(cells):
        x = X0 + LABEL_W + j * COL_W
        if c is None:
            d.o.append(f'<rect x="{x}" y="{y}" width="{COL_W - 12}" height="{ROW_H - 12}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + (COL_W - 12) / 2, y + 26, val, 13, ACC, KR, "middle", 600)
            d.t(x + (COL_W - 12) / 2, y + 44, "서버 개인키 등록", 11, MUTED, KR)
        elif c is MUTED:
            d.box(x, y, COL_W - 12, ROW_H - 12, PAPER, RULE, 0.8, 6)
            d.t(x + (COL_W - 12) / 2, y + 36, val, 12, MUTED, KR, "middle")
        else:
            d.tone(x, y, COL_W - 12, ROW_H - 12, c, 6)
            d.t(x + (COL_W - 12) / 2, y + 36, val, 13, c, KR, "middle", 600)

d.legend(H - 72, [("복호화가 되는 유일한 칸", ACC), ("있음·옵니다", OK), ("없음·불가", BAD)])
d.save("04-02.key-exchange-matrix.svg")
