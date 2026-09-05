# 08-01 §6 — RFC 5424 헤더 일곱 필드 중 무엇을 비울 수 있는가.
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
# 주의: ABNF 에서 NILVALUE 대안을 가진 필드만 "-" 로 비울 수 있다. VERSION 에는 그 대안이 없으므로
#       원문의 "usually left out" 은 RFC 5424 형식에서는 성립하지 않는다. 그 자리가 focal 이다.
# 타입 스펙: type-dp-security-matrix — 행(필드) × 열(원문 서술 · ABNF · 비울 수 있나)의 격자에
#           값을 놓아 어긋난 칸 하나가 드러나게 한다. 축약: PRIVAL 범위와 구조화 데이터 문법은 본문이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 740
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §6",
      "표준을 읽으면 무엇을 비워도 되는지가 보인다",
      "RFC 5424 헤더 일곱 필드를 ABNF 정의와 나란히 놓은 격자. 오른쪽 열은 그 필드에 NILVALUE 대안이 "
      "있어 하이픈 하나로 비울 수 있는지를 뜻한다.",
      "저자가 보통 생략된다고 적은 필드가 사실은 비울 수 없는 유일한 필드입니다")

LX, LW = 24, 68
CW1, CW2, CW3 = 226, 348, 158
RH, HY, RY = 58, 152, 178
cols = [("원문이 붙인 설명", CW1), ("RFC 5424 ABNF", CW2), ("\"-\" 로 비울 수 있나", CW3)]
x = LX + LW
for name, cw in cols:
    d.t(x + cw / 2, HY, name, 12, MUTED, KR, "middle", 600)
    x += cw
d.line(LX, HY + 12, LX + LW + CW1 + CW2 + CW3, HY + 12, RULE, 1)

ROWS = [
    ("PRI", "시설과 심각도", '"<" PRIVAL ">"', "못 비운다", WARN),
    ("VER", "프로토콜 번호 — 보통 생략된다", "NONZERO-DIGIT 0*2DIGIT", "못 비운다", 9),
    ("TS", "생성 시각 — ISO 8601", "NILVALUE / FULL-DATE ...", "비울 수 있다", OK),
    ("HN", "보낸 기계", "NILVALUE / 1*255PRINTUSASCII", "비울 수 있다", OK),
    ("APP", "보낸 애플리케이션이나 장치", "NILVALUE / 1*48PRINTUSASCII", "비울 수 있다", OK),
    ("PID", "보낸 프로세스", "NILVALUE / 1*128PRINTUSASCII", "비울 수 있다", OK),
    ("MID", "선택적 메시지 ID", "NILVALUE / 1*32PRINTUSASCII", "비울 수 있다", OK),
]
for r, (fld, desc, abnf, nil, code) in enumerate(ROWS):
    y = RY + r * RH
    focal = (code == 9)
    if focal:
        d.tone(LX, y + 3, LW + CW1 + CW2 + CW3, RH - 6, ACC, 6, "12", 1.4)
    elif r % 2 == 0:
        d.box(LX, y + 3, LW + CW1 + CW2 + CW3, RH - 6, PAPER2, "none", 0, 6)
    col = ACC if focal else code
    d.t(LX + 14, y + RH / 2 + 5, fld, 14, col, MONO, "start", 600)
    d.t(LX + LW + 14, y + RH / 2 + 5, desc, 12, ACC if focal else INK, KR, "start")
    d.t(LX + LW + CW1 + 14, y + RH / 2 + 5, abnf, 11.5, MUTED, MONO, "start")
    d.t(LX + LW + CW1 + CW2 + CW3 / 2, y + RH / 2 + 5, nil, 12, col, KR, "middle", 600)

BY = RY + len(ROWS) * RH + 10
d.line(LX, BY, LX + LW + CW1 + CW2 + CW3, BY, RULE, 1)
d.t(LX, BY + 26, "NILVALUE 는 하이픈 한 글자입니다. 대안으로 그것을 가진 필드만 값 없이 보낼 수 있습니다.",
    12, MUTED, KR, "start")
d.t(LX, BY + 48, "전체 메시지는 HEADER SP STRUCTURED-DATA [SP MSG] 입니다. 값을 비우는 것과 자리가 없는 것은 다릅니다.",
    12, SOFT, KR, "start")
d.t(LX, BY + 70, "STRUCTURED-DATA 는 자리는 있되 - 로 비우고, MSG 는 ABNF 의 대괄호가 감싼 선택 요소라 자리 자체가 없을 수 있습니다.",
    12, SOFT, KR, "start")

d.legend(696, [("원문과 표준이 어긋난 칸", ACC), ("비울 수 있는 필드", OK),
                  ("비울 수 없는 필드", WARN)])
d.save("08-01.syslog-fields.svg")
print("ok 08-01.syslog-fields")
