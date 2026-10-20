# 타입 스펙: type-data-flow
# 사실 출처: NPG Ch.13 Listing 13-5 (Leveled Log Entries)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 940, 520
d = D(W, H, "LEVELED LOG DISPATCH · DATA FLOW",
      "코드 내 레벨별 로그 호출이 목적지 Writer 로 분기되는 흐름",
      "log 패키지는 자체 레벨이 없으므로 lDebug 와 lError 로거를 따로 만듭니다. "
      "lError 는 sustainedMultiWriter 를 통해 파일과 표준 출력 둘 다로 전달되고, "
      "lDebug 는 표준 출력으로만 흘러 디스크 용량을 아낍니다.",
      lead="동일한 비즈니스 코드에서 발생한 두 호출이 서로 다른 writer 집합에 도달합니다.")

# 1. 좌측: 애플리케이션 코드 호출 영역
d.box(36, 120, 240, 320, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(52, 146, "애플리케이션 로그 호출", 12, INK, KR, "start", 600)
d.t(52, 168, "동일 코드베이스 내 발생", 11, SOFT, KR, "start")

# 호출 1: lError
d.tone(52, 190, 208, 90, BAD, 4, "15", 1.2)
d.t(66, 214, "lError.Print(...)", 12, BAD, MONO, "start", 600)
d.t(66, 236, "\"cannot communicate...\"", 10, INK, MONO, "start")
d.t(66, 258, "심각도: High (장애 알림)", 11, SOFT, KR, "start")

# 호출 2: lDebug
d.tone(52, 320, 208, 90, INFO, 4, "15", 1.2)
d.t(66, 344, "lDebug.Print(...)", 12, INFO, MONO, "start", 600)
d.t(66, 366, "\"you cannot hum...\"", 10, INK, MONO, "start")
d.t(66, 388, "심각도: Low (개발 추적)", 11, SOFT, KR, "start")

# 2. 중앙: 로거 및 Writer 디스패처
# lError 디스패처 (SustainedMultiWriter)
d.box(330, 185, 220, 100, fill=PAPER2, stroke=BAD, sw=1.2, r=6)
d.t(440, 210, "lError (SustainedMultiWriter)", 11, BAD, MONO, "middle", 600)
d.t(440, 230, "logFile + lDebug.Writer()", 11, INK, MONO, "middle")
d.t(440, 254, "다중 출력 분기 복제", 11, SOFT, KR, "middle")

# lDebug 디스패처
d.box(330, 320, 220, 90, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(440, 348, "lDebug 로거", 12, INFO, KR, "middle", 600)
d.t(440, 372, "os.Stdout 단일 대상", 11, INK, MONO, "middle")
d.t(440, 392, "파일 쓰기 제외", 11, SOFT, KR, "middle")

# 화살표: 호출 -> 디스패처
d.arrow([(260, 235), (328, 235)], BAD, "bad", 1.4)
d.arrow([(260, 365), (328, 365)], INFO, "info", 1.4)

# 3. 우측: 최종 목적지
# 목적지 A: logFile (*bytes.Buffer)
d.box(620, 150, 280, 110, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(636, 176, "로그 파일 (logFile)", 12, OK, KR, "start", 600)
d.t(636, 198, "보존 대상 (ERROR 만 보관)", 11, SOFT, KR, "start")
d.tone(636, 212, 248, 36, OK, 4, "15", 1.0)
d.t(648, 234, "ERROR: log_test.go:48: cannot...", 9, INK, MONO, "start")

# 목적지 B: 표준 출력 (os.Stdout)
d.box(620, 300, 280, 150, fill=PAPER2, stroke=ACC, sw=1.2, r=6)
d.t(636, 326, "표준 출력 (os.Stdout)", 12, ACC, KR, "start", 600)
d.t(636, 348, "실시간 콘솔 (ERROR + DEBUG)", 11, SOFT, KR, "start")
d.tone(636, 362, 248, 34, BAD, 4, "15", 1.0)
d.t(648, 384, "ERROR: log_test.go:48: cannot...", 9, INK, MONO, "start")
d.tone(636, 404, 248, 34, INFO, 4, "15", 1.0)
d.t(648, 426, "DEBUG: log_test.go:49: you cannot...", 9, INK, MONO, "start")

# 화살표: 디스패처 -> 목적지
# lError -> logFile
d.arrow([(550, 220), (584, 220), (584, 190), (618, 190)], BAD, "bad", 1.4)
# lError -> os.Stdout
d.arrow([(550, 250), (584, 250), (584, 350), (618, 350)], BAD, "bad", 1.4)
# lDebug -> os.Stdout
d.arrow([(550, 375), (584, 375), (584, 410), (618, 410)], INFO, "info", 1.4)

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.leveled-log-dispatch.svg"
d.save(str(svg_path))
print("ok 13-01 leveled-log-dispatch")
