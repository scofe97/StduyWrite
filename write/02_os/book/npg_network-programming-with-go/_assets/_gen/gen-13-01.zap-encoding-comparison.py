# 타입 스펙: type-process
# 사실 출처: NPG Ch.13 Listing 13-7, 13-8, zapcore.EncoderConfig
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 940, 520
d = D(W, H, "ZAP ENCODING COMPARISON · PROCESS",
      "동일한 로그 엔트리가 JSON 인코더와 콘솔 인코더를 통과할 때의 출력 비교",
      "동일한 EncoderConfig 와 로그 엔트리라도 인코더 종류에 따라 "
      "기계 분석용 JSON 형식과 터미널 가독용 탭 구분 콘솔 텍스트로 완전히 다르게 직렬화됩니다.",
      lead="입력 엔트리는 동일하며 인코더 구현체에 의해 출력 줄의 구조가 결정됩니다.")

# 1. 좌측: 원본 로그 엔트리 상자
IX, IY, IW, IH = 36, 130, 240, 310
d.tone(IX, IY, IW, IH, INFO, 6, "10", 1.2)
d.t(IX + 20, IY + 26, "공통 로그 엔트리", 12, INFO, KR, "start", 600)
d.t(IX + 20, IY + 48, "zapcore.Entry + Fields", 11, SOFT, MONO, "start")
d.line(IX + 14, IY + 60, IX + IW - 14, IY + 60, RULE, 0.8)

fields = [
    ("Level", "InfoLevel"),
    ("Name", "\"example\""),
    ("Message", "\"test info message\""),
    ("Caller", "\"npg13-1/zap_test.go:44\""),
    ("Field", "version: \"go1.25.1\""),
]
for i, (k, v) in enumerate(fields):
    y = IY + 84 + i * 44
    d.t(IX + 20, y, k, 11, MUTED, KR, "start")
    d.t(IX + 20, y + 18, v, 10, INK, MONO, "start")

# 2. 중앙: 인코더 분기
MX, MY, MW, MH = 320, 130, 190, 310
d.box(MX, MY, MW, MH, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(MX + MW / 2, MY + 26, "EncoderConfig 적용", 12, INK, KR, "middle", 600)
d.t(MX + MW / 2, MY + 46, "MessageKey: \"msg\"", 10, SOFT, MONO, "middle")
d.t(MX + MW / 2, MY + 64, "LevelKey: \"level\"", 10, SOFT, MONO, "middle")
d.t(MX + MW / 2, MY + 82, "CallerKey: \"caller\"", 10, SOFT, MONO, "middle")

# JSON 인코더 상자
d.tone(MX + 16, MY + 106, MW - 32, 80, OK, 4, "15", 1.1)
d.t(MX + MW / 2, MY + 134, "NewJSONEncoder", 11, OK, MONO, "middle", 600)
d.t(MX + MW / 2, MY + 154, "키-값 구조화 직렬화", 11, SOFT, KR, "middle")

# 콘솔 인코더 상자
d.tone(MX + 16, MY + 206, MW - 32, 80, ACC, 4, "15", 1.1)
d.t(MX + MW / 2, MY + 234, "NewConsoleEncoder", 11, ACC, MONO, "middle", 600)
d.t(MX + MW / 2, MY + 254, "탭 구분 텍스트 직렬화", 11, SOFT, KR, "middle")

# 화살표: 입력 -> 인코더
d.arrow([(IX + IW, IY + 146), (MX + 16, MY + 146)], OK, "ok", 1.4)
d.arrow([(IX + IW, IY + 246), (MX + 16, MY + 246)], ACC, "acc", 1.4)

# 3. 우측: 출력 결과 비교
OX, OY, OW, OH = 550, 130, 354, 310

# JSON 결과
d.box(OX, OY, OW, 140, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(OX + 16, OY + 26, "JSON 인코더 출력 (기계 파싱 및 중앙 수집)", 11, OK, KR, "start", 600)
d.tone(OX + 16, OY + 40, OW - 32, 82, OK, 4, "12", 0.9)
d.t(OX + 24, OY + 64, "{\"level\":\"info\",\"name\":\"example\",", 10, INK, MONO, "start")
d.t(OX + 24, OY + 84, "\"caller\":\"npg13-1/zap_test.go:44\",", 10, INK, MONO, "start")
d.t(OX + 24, OY + 104, "\"msg\":\"test info message\",\"version\":\"go1.25.1\"}", 10, INK, MONO, "start")

# 콘솔 결과
d.box(OX, OY + 160, OW, 140, fill=PAPER2, stroke=ACC, sw=1.2, r=6)
d.t(OX + 16, OY + 186, "콘솔 인코더 출력 (사람 가독 및 터미널 모니터링)", 11, ACC, KR, "start", 600)
d.tone(OX + 16, OY + 200, OW - 32, 82, ACC, 4, "12", 0.9)
d.t(OX + 24, OY + 224, "info → example → npg13-1/zap_test.go:44 →", 10, INK, MONO, "start")
d.t(OX + 24, OY + 244, "test info message → {\"version\": \"go1.25.1\"}", 10, INK, MONO, "start")
d.t(OX + 24, OY + 266, "필드 간 구분자: \\t (탭 문자)", 11, SOFT, KR, "start")

# 화살표: 인코더 -> 출력
d.arrow([(MX + MW, MY + 146), (530, MY + 146), (530, OY + 70), (OX - 4, OY + 70)], OK, "ok", 1.4)
d.arrow([(MX + MW, MY + 246), (530, MY + 246), (530, OY + 230), (OX - 4, OY + 230)], ACC, "acc", 1.4)

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.zap-encoding-comparison.svg"
d.save(str(svg_path))
print("ok 13-01 zap-encoding-comparison")
