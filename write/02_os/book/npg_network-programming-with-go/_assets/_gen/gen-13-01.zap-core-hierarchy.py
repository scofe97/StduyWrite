# 타입 스펙: type-nested
# 사실 출처: NPG Ch.13 Structured Logging (p.303-305), go.uber.org/zap
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 520
d = D(W, H, "ZAP CORE HIERARCHY · NESTED ARCHITECTURE",
      "zap.Logger 의 내부 구조와 zapcore.Core 3요소",
      "zap.Logger 는 편의 메서드와 옵션을 감싸는 래퍼이고, "
      "실제 로그 처리는 zapcore.Core 안의 인코더·출력 싱커·레벨 활성화기가 전담합니다.",
      lead="Core 는 Encoder, WriteSyncer, LevelEnabler 세 컴포넌트로 구성됩니다.")

# 1. 외곽 컨테이너: zap.Logger
OX, OY, OW, OH = 36, 110, 808, 370
d.box(OX, OY, OW, OH, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(OX + 20, OY + 28, "zap.Logger", 14, INFO, MONO, "start", 600)
d.t(OX + 120, OY + 28, "외곽 래퍼 인터페이스 (API 계층)", 12, MUTED, KR, "start")

# 상단 옵션 배너
d.tone(OX + 20, OY + 44, OW - 40, 48, INFO, 4, "0a", 0.9)
d.t(OX + 32, OY + 66, "부가 옵션 (Options)", 11, INFO, KR, "start", 600)
d.t(OX + 32, OY + 84, "zap.AddCaller()  zap.Fields(version)  zl.Named(\"example\")", 11, INK, MONO, "start")

# 2. 중간 컨테이너: zapcore.Core
CX, CY, CW, CH = 56, 216, 768, 244
d.tone(CX, CY, CW, CH, ACC, 6, "10", 1.2)
d.t(CX + 20, CY + 26, "zapcore.Core", 13, ACC, MONO, "start", 600)
d.t(CX + 130, CY + 26, "로그 처리 엔진 인터페이스", 11, SOFT, KR, "start")

# Core 내부 3요소
col_w = 232
gap = 20
y_elem = CY + 46
h_elem = 180

# (1) Encoder
x1 = CX + 20
d.box(x1, y_elem, col_w, h_elem, fill=PAPER, stroke=OK, sw=1.1, r=6)
d.t(x1 + col_w / 2, y_elem + 24, "1. Encoder", 12, OK, MONO, "middle", 600)
d.t(x1 + col_w / 2, y_elem + 44, "바이트 직렬화", 11, MUTED, KR, "middle")
d.line(x1 + 12, y_elem + 56, x1 + col_w - 12, y_elem + 56, RULE, 0.8)
d.t(x1 + 16, y_elem + 78, "EncoderConfig", 11, INK, MONO, "start")
d.t(x1 + 16, y_elem + 98, "MessageKey / LevelKey", 11, SOFT, MONO, "start")
d.t(x1 + 16, y_elem + 118, "CallerKey / TimeKey", 11, SOFT, MONO, "start")
d.t(x1 + 16, y_elem + 140, "구현체:", 11, INK, KR, "start")
d.t(x1 + 16, y_elem + 158, "JSONEncoder / Console", 11, OK, MONO, "start")

# (2) WriteSyncer
x2 = x1 + col_w + gap
d.box(x2, y_elem, col_w, h_elem, fill=PAPER, stroke=WARN, sw=1.1, r=6)
d.t(x2 + col_w / 2, y_elem + 24, "2. WriteSyncer", 12, WARN, MONO, "middle", 600)
d.t(x2 + col_w / 2, y_elem + 44, "출력 및 플러시", 11, MUTED, KR, "middle")
d.line(x2 + 12, y_elem + 56, x2 + col_w - 12, y_elem + 56, RULE, 0.8)
d.t(x2 + 16, y_elem + 78, "인터페이스 정의", 11, INK, KR, "start")
d.t(x2 + 16, y_elem + 98, "io.Writer + Sync()", 11, SOFT, MONO, "start")
d.t(x2 + 16, y_elem + 118, "동시성 및 어댑터", 11, INK, KR, "start")
d.t(x2 + 16, y_elem + 138, "zapcore.Lock() 락 보호", 11, SOFT, KR, "start")
d.t(x2 + 16, y_elem + 158, "zapcore.AddSync() 변환", 11, WARN, MONO, "start")

# (3) LevelEnabler
x3 = x2 + col_w + gap
d.box(x3, y_elem, col_w, h_elem, fill=PAPER, stroke=ACC, sw=1.1, r=6)
d.t(x3 + col_w / 2, y_elem + 24, "3. LevelEnabler", 12, ACC, MONO, "middle", 600)
d.t(x3 + col_w / 2, y_elem + 44, "로그 레벨 필터링", 11, MUTED, KR, "middle")
d.line(x3 + 12, y_elem + 56, x3 + col_w - 12, y_elem + 56, RULE, 0.8)
d.t(x3 + 16, y_elem + 78, "최소 심각도 판별", 11, INK, KR, "start")
d.t(x3 + 16, y_elem + 98, "Enabled(Level) bool", 11, SOFT, MONO, "start")
d.t(x3 + 16, y_elem + 118, "지원 7단계 레벨", 11, INK, KR, "start")
d.t(x3 + 16, y_elem + 138, "Debug < Info < Warn", 10.5, SOFT, MONO, "start")
d.t(x3 + 16, y_elem + 158, "Error < DPanic < Panic < Fatal", 10.5, ACC, MONO, "start")

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.zap-core-hierarchy.svg"
d.save(str(svg_path))
print("ok 13-01 zap-core-hierarchy")
