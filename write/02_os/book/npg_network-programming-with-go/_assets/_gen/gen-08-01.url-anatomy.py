# 타입 스펙: type-nested — URL 전체 안에 전송 범위와 브라우저 로컬이 나뉘고, authority 안에 사용자·호스트·포트가 포함된다.
# 사실 출처: NPG Ch.8 Uniform Resource Locators (p.1-2)
# 패턴: scheme://user:password@host:port/path?key1=value1&key2=value2#table_of_contents
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, MONO, KR

W, H = 840, 500
d = D(W, H, "NPG CHAPTER 8 · UNIFORM RESOURCE LOCATORS",
      "URL 의 다섯 부분과 authority 포함 관계, fragment 경계",
      "URL 은 scheme, authority, path, query, fragment 로 나뉘며 authority 는 사용자정보·호스트·포트를 포함한다.",
      "scheme 과 host 는 필수이며 fragment 는 브라우저 내부 스크롤 식별자입니다")

# 1. 전체 URL 문자열 배너
BX, BY, BW, BH = 24, 100, 792, 38
d.box(BX, BY, BW, BH, PAPER2, RULE, 1.0, 6)
d.t(BX + 14, BY + 24, "URL 패턴", 11, SOFT, MONO, "start")
d.t(BX + 90, BY + 24, "scheme://user:password@host:port/path?key1=value1&key2=value2#table_of_contents", 12, INK, MONO, "start", 500)

# 2. 외곽 컨테이너 (URL 전체 - Nested Level 1)
OX, OY, OW, OH = 24, 150, 792, 270
d.box(OX, OY, OW, OH, PAPER2, RULE, 1.0, 8)
d.t(OX + 16, OY + 22, "URL 전체 구조", 11, SOFT, MONO, "start")

# 3. 좌측: 서버 전송 범위 (Nested Level 2 - HTTP 요청)
SX, SY, SW, SH = 36, 180, 584, 226
d.tone(SX, SY, SW, SH, INFO, 6, "08", 1.0)
d.t(SX + 14, SY + 22, "HTTP 요청 대상 (서버로 전송)", 11, INFO, KR, "start", 600)

# (1) scheme
d.box(48, 212, 80, 180, PAPER, OK, 1.0, 6)
d.t(88, 236, "scheme", 12, OK, MONO, "middle", 600)
d.chip(88, 260, "필수", OK, 11)
d.t(88, 305, "프로토콜", 11, MUTED, KR, "middle")
d.t(88, 335, "scheme://", 11, INK, MONO, "middle")

# (2) authority 컨테이너 (Nested Level 3)
AX, AY, AW, AH = 136, 212, 260, 180
d.tone(AX, AY, AW, AH, ACC, 6, "12", 1.2)
d.t(AX + 14, AY + 22, "authority (선택)", 11, ACC, KR, "start", 600)

# authority 내부 셋 (Nested Level 4)
# user:password
d.box(AX + 10, AY + 36, 88, 130, PAPER, MUTED, 0.8, 4)
d.t(AX + 54, AY + 58, "user:pw", 11, MUTED, MONO, "middle")
d.chip(AX + 54, AY + 82, "선택", MUTED, 11)
d.t(AX + 54, AY + 115, "자격증명", 11, SOFT, KR, "middle")
d.t(AX + 54, AY + 138, "user:pw@", 10, INK, MONO, "middle")

# host (focal)
d.tone(AX + 104, AY + 36, 82, 130, ACC, 4, "18", 1.4)
d.t(AX + 145, AY + 58, "host", 12, ACC, MONO, "middle", 600)
d.chip(AX + 145, AY + 82, "필수", ACC, 11)
d.t(AX + 145, AY + 115, "호스트명", 11, INK, KR, "middle")
d.t(AX + 145, AY + 138, "host", 11, INK, MONO, "middle")

# port
d.box(AX + 192, AY + 36, 58, 130, PAPER, MUTED, 0.8, 4)
d.t(AX + 221, AY + 58, "port", 11, MUTED, MONO, "middle")
d.chip(AX + 221, AY + 82, "선택", MUTED, 11)
d.t(AX + 221, AY + 115, "포트번호", 11, SOFT, KR, "middle")
d.t(AX + 221, AY + 138, ":port", 10, INK, MONO, "middle")

# (3) path
d.box(404, 212, 94, 180, PAPER, INFO, 1.0, 6)
d.t(451, 236, "path", 12, INFO, MONO, "middle", 600)
d.chip(451, 260, "자원경로", INFO, 11)
d.t(451, 305, "자원 위치", 11, MUTED, KR, "middle")
d.t(451, 335, "/path", 11, INK, MONO, "middle")

# (4) query
d.box(506, 212, 104, 180, PAPER, MUTED, 1.0, 6)
d.t(558, 236, "query", 12, MUTED, MONO, "middle", 600)
d.chip(558, 260, "선택", MUTED, 11)
d.t(558, 305, "매개변수", 11, MUTED, KR, "middle")
d.t(558, 335, "?key1=v1...", 10, INK, MONO, "middle")

# 4. 우측: 브라우저 로컬 (Nested Level 2 - fragment)
FX, FY, FW, FH = 628, 180, 176, 226
d.tone(FX, FY, FW, FH, WARN, 6, "08", 1.0)
d.t(FX + 14, FY + 22, "브라우저 로컬 (서버 미전송)", 11, WARN, KR, "start", 600)

d.box(FX + 14, 212, FW - 28, 180, PAPER, WARN, 1.0, 6)
d.t(FX + FW / 2, 236, "fragment", 12, WARN, MONO, "middle", 600)
d.chip(FX + FW / 2, 260, "선택", WARN, 11)
d.t(FX + FW / 2, 298, "문서 내부 구획", 11, INK, KR, "middle")
d.t(FX + FW / 2, 320, "스크롤 식별자", 11, MUTED, KR, "middle")
d.t(FX + FW / 2, 350, "#table_of_contents", 10, WARN, MONO, "middle")

# 5. 범례
d.legend(450, [("필수 요소", OK), ("선택 요소", MUTED), ("핵심 호스트", ACC), ("자원 경로", INFO), ("서버 미전송", WARN)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "08-01.url-anatomy.svg"))
d.save(out)
print(f"saved: {out}")
