# 08-01 §2 「로그 한 줄의 실제 모양」 — RFC 5424 헤더 일곱 필드 중 무엇을 비울 수 있는가.
# 원문("Syslog"): "The Syslog format as defined in RFC 5424 has the following header fields (with TS and
#       HN the most often used): PRI(The message facility/severity), VER(The Syslog protocol number
#       (usually left out since it can only be 1)), TS(Contains the time when the message was generated
#       using ISO 8601 format), HN(Identifies the machine that sent the message), APP(Identifies the
#       application (or a device) that sent the message), PID(Identifies the process that sent the
#       message), MID(An optional message ID)."
# 1차 자료(RFC 5424 §6, §6.2.2): "HEADER = PRI VERSION SP TIMESTAMP SP HOSTNAME SP APP-NAME SP PROCID
#       SP MSGID" / "VERSION = NONZERO-DIGIT 0*2DIGIT" / "HOSTNAME = NILVALUE / 1*255PRINTUSASCII" /
#       "APP-NAME = NILVALUE / 1*48PRINTUSASCII" / "PROCID = NILVALUE / 1*128PRINTUSASCII" /
#       "MSGID = NILVALUE / 1*32PRINTUSASCII" / "TIMESTAMP = NILVALUE / FULL-DATE ..." /
#       "NILVALUE = \"-\"" / "PRI = \"<\" PRIVAL \">\"".
#       예시 줄은 본문이 옮긴 RFC 5424 §6.5 Examples 의 첫 줄이다:
#       <34>1 2003-10-11T22:14:15.003Z mymachine.example.com su - ID47 - BOM'su root' failed for lonvick on /dev/pts/8
# 주의: ABNF 에서 NILVALUE 대안을 가진 필드만 "-" 로 비울 수 있다. VERSION 에는 그 대안이 없으므로
#       원문의 "usually left out" 은 RFC 5424 형식에서는 성립하지 않는다. 그 자리가 focal 이다.
# 타입 스펙: type-dp-security-matrix — 행(필드) × 열(뜻 · ABNF · 비울 수 있나)의 격자에 값을 놓아
#           어긋난 칸 하나가 드러나게 한다. 격자 위에 실제 한 줄을 필드 경계대로 잘라 놓아, 격자의
#           "비울 수 있다" 가 실제 줄에서 하이픈 한 글자(PROCID·STRUCTURED-DATA)로 나타나는 모습을 보인다.
#           필드 이름은 RFC 이름을 쓰고 원문 약칭(TS·HN 등)은 그 아래에 붙인다.
#           축약: PRIVAL 범위와 구조화 데이터 문법은 본문이 맡는다. 토큰 상자 폭은 글자 수가 아니라
#           필드 이름이 들어갈 폭으로 맞췄다(PRI 와 VERSION 은 실제 줄에서 빈칸 없이 붙는다).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 772
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §2",
      "표준을 읽으면 무엇을 비워도 되는지가 보인다",
      "위는 RFC 5424 §6.5 의 예시 한 줄을 필드 경계대로 자른 것이고, 아래는 헤더 일곱 필드를 ABNF 정의와 "
      "나란히 놓은 격자다. 오른쪽 열은 그 필드에 NILVALUE 대안이 있어 하이픈 하나로 비울 수 있는지를 "
      "뜻하고, 예시 줄에서는 PROCID 와 STRUCTURED-DATA 가 실제로 하이픈으로 비어 있다.",
      "VERSION 은 비울 수 없고 이 형식에서 늘 1 입니다")

# ── 위: 실제 한 줄을 필드 경계대로 ──────────────────────────────────────────
LX = 24
d.t(LX, 108, "SYSLOG-MSG = HEADER SP STRUCTURED-DATA [SP MSG]", 12, SOFT, MONO, "start")
TH, CHW = 32, 6.9          # 토큰 상자 높이 · mono 11.5px 한 글자 폭 근사
# (값, 필드, 원문 약칭, 상태) — 상태: no=못 비움, yes=비울 수 있음, nil=이 줄에서 실제로 비움, ver=focal
ROW1 = [("<34>", "PRI", "", "no"), ("1", "VERSION", "VER", "ver"),
        ("2003-10-11T22:14:15.003Z", "TIMESTAMP", "TS", "yes"),
        ("mymachine.example.com", "HOSTNAME", "HN", "yes"),
        ("su", "APP-NAME", "APP", "yes"), ("-", "PROCID", "PID", "nil"), ("ID47", "MSGID", "MID", "yes")]
ROW2 = [("-", "STRUCTURED-DATA", "", "nil"),
        ("BOM'su root' failed for lonvick on /dev/pts/8", "MSG", "", "msg")]
COL = {"no": WARN, "yes": OK, "nil": INFO, "ver": ACC, "msg": MUTED}


def strip(y, row, first_gap=None):
    x = LX
    for k, (val, fld, ab, st) in enumerate(row):
        w = max(len(val) * CHW, len(fld) * 6.6) + 16
        c = COL[st]
        if st == "nil":
            d.tone(x, y, w, TH, c, 4, "2E", 1.3)
        elif st == "ver":
            d.tone(x, y, w, TH, c, 4, "1F", 1.4)
        else:
            d.box(x, y, w, TH, PAPER2, c, 1.1, 4)
        d.t(x + w / 2, y + 21, val, 11.5, INK if st != "msg" else MUTED, MONO, "middle", 600)
        d.t(x + w / 2, y + TH + 16, fld, 11, c if st != "msg" else SOFT, MONO, "middle", 600)
        gap = 2 if (first_gap and k == 0) else 8
        x += w + gap
    return x


Y1 = 124
end1 = strip(Y1, ROW1, first_gap=True)
d.line(LX, Y1 - 6, end1 - 8, Y1 - 6, SOFT, 0.8)
d.t(end1, Y1 + 21, "HEADER", 11, SOFT, MONO, "start", 600)
Y2 = Y1 + TH + 36
strip(Y2, ROW2)
d.t(LX, Y2 + TH + 40, "RFC 5424 §6.5 첫 예시 · PRI 와 VERSION 은 빈칸 없이 붙음", 11, SOFT, KR, "start")

# ── 아래: 일곱 필드 격자 ──────────────────────────────────────────────────
GX, LW = 24, 132
CW1, CW2, CW3 = 196, 330, 150
GWD = LW + CW1 + CW2 + CW3
RH = 48
HY = Y2 + TH + 84
RY = HY + 20
cols = [("필드 뜻", CW1), ("RFC 5424 ABNF", CW2), ("\"-\" 로 비울 수 있나", CW3)]
x = GX + LW
for name, cw in cols:
    d.t(x + cw / 2, HY, name, 12, MUTED, KR, "middle", 600)
    x += cw
d.line(GX, HY + 10, GX + GWD, HY + 10, RULE, 1)

ROWS = [
    ("PRI", "", "시설과 심각도", '"<" PRIVAL ">"', "못 비운다", WARN),
    ("VERSION", "VER", "프로토콜 번호 — 이 형식에서 1", "NONZERO-DIGIT 0*2DIGIT", "못 비운다", None),
    ("TIMESTAMP", "TS", "생성 시각 — ISO 8601", "NILVALUE / FULL-DATE ...", "비울 수 있다", OK),
    ("HOSTNAME", "HN", "보낸 기계", "NILVALUE / 1*255PRINTUSASCII", "비울 수 있다", OK),
    ("APP-NAME", "APP", "보낸 애플리케이션이나 장치", "NILVALUE / 1*48PRINTUSASCII", "비울 수 있다", OK),
    ("PROCID", "PID", "보낸 프로세스", "NILVALUE / 1*128PRINTUSASCII", "비울 수 있다", OK),
    ("MSGID", "MID", "선택적 메시지 ID", "NILVALUE / 1*32PRINTUSASCII", "비울 수 있다", OK),
]
for r, (fld, ab, desc, abnf, nil, code) in enumerate(ROWS):
    y = RY + r * RH
    focal = code is None
    if focal:
        d.tone(GX, y + 3, GWD, RH - 6, ACC, 6, "12", 1.4)
    elif r % 2 == 0:
        d.box(GX, y + 3, GWD, RH - 6, PAPER2, "none", 0, 6)
    col = ACC if focal else code
    if ab:
        d.t(GX + 14, y + RH / 2 + 1, fld, 13, col, MONO, "start", 600)
        d.t(GX + 14, y + RH / 2 + 16, ab, 11, SOFT, MONO, "start")
    else:
        d.t(GX + 14, y + RH / 2 + 5, fld, 13, col, MONO, "start", 600)
    d.t(GX + LW + 14, y + RH / 2 + 5, desc, 12, ACC if focal else INK, KR, "start")
    d.t(GX + LW + CW1 + 14, y + RH / 2 + 5, abnf, 11.5, MUTED, MONO, "start")
    d.t(GX + LW + CW1 + CW2 + CW3 / 2, y + RH / 2 + 5, nil, 12, col, KR, "middle", 600)

BY = RY + len(ROWS) * RH + 8
d.line(GX, BY, GX + GWD, BY, RULE, 1)
d.t(GX, BY + 24, "NILVALUE = \"-\" · 그 대안을 가진 필드만 비움 · MSG 는 자리 자체가 선택",
    11.5, MUTED, KR, "start")

d.legend(BY + 48, [("늘 값이 있는 VERSION", ACC), ("비울 수 있는 필드", OK),
                   ("비울 수 없는 필드", WARN), ("예시에서 \"-\" 로 비움", INFO)])
d.save("08-01.syslog-fields.svg")
print("ok 08-01.syslog-fields")
