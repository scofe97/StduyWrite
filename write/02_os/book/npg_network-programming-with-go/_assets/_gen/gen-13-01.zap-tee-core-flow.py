# 타입 스펙: type-data-flow
# 사실 출처: NPG Ch.13 Listing 13-9, 13-10 (zapcore.NewTee)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 940, 520
d = D(W, H, "ZAP TEE CORE FLOW · DATA FLOW",
      "zapcore.NewTee 로 묶인 두 코어의 레벨 필터링과 다중 출력 분기",
      "NewTee 로 결합된 복수 코어는 동일한 로그 호출을 각자의 레벨과 인코더로 평가합니다. "
      "Debug 엔트리는 파일 코어에서 버려지고 콘솔 코어에만 전달되며, "
      "Info 엔트리는 양쪽 코어 모두에서 인코딩되어 출력됩니다.",
      lead="한 번의 호출이 서로 다른 레벨 임계치와 인코더를 가진 두 코어로 동시에 전달됩니다.")

# 1. 좌측: 입력 로그 호출
IX, IY, IW, IH = 36, 120, 210, 340
d.box(IX, IY, IW, IH, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(IX + 16, IY + 26, "로그 호출 입력", 12, INK, KR, "start", 600)
d.t(IX + 16, IY + 48, "클론된 zl 인스턴스", 11, SOFT, MONO, "start")

# 호출 1: Debug
d.tone(IX + 14, IY + 70, IW - 28, 110, INFO, 4, "15", 1.2)
d.t(IX + 24, IY + 96, "1. zl.Debug(...)", 12, INFO, MONO, "start", 600)
d.t(IX + 24, IY + 118, "\"this is only logged...\"", 9, INK, MONO, "start")
d.t(IX + 24, IY + 140, "심각도: DebugLevel", 11, SOFT, KR, "start")

# 호출 2: Info
d.tone(IX + 14, IY + 200, IW - 28, 110, OK, 4, "15", 1.2)
d.t(IX + 24, IY + 226, "2. zl.Info(...)", 12, OK, MONO, "start", 600)
d.t(IX + 24, IY + 248, "\"this is logged as...\"", 9, INK, MONO, "start")
d.t(IX + 24, IY + 270, "심각도: InfoLevel", 11, SOFT, KR, "start")

# 2. 중앙: NewTee 분기 허브
TX, TY, TW, TH = 286, 170, 160, 240
d.tone(TX, TY, TW, TH, ACC, 6, "10", 1.2)
d.t(TX + TW / 2, TY + 30, "zapcore.NewTee", 12, ACC, MONO, "middle", 600)
d.t(TX + TW / 2, TY + 52, "코어 복제 결합", 11, MUTED, KR, "middle")
d.line(TX + 12, TY + 64, TX + TW - 12, TY + 64, RULE, 0.8)
d.t(TX + TW / 2, TY + 100, "모든 엔트리를", 11, INK, KR, "middle")
d.t(TX + TW / 2, TY + 122, "c1 과 c2 에", 11, INK, KR, "middle")
d.t(TX + TW / 2, TY + 144, "동시 디스패치", 11, INK, KR, "middle")
d.t(TX + TW / 2, TY + 180, "독립 레벨 평가", 11, SOFT, KR, "middle")

# 화살표: 입력 -> NewTee
d.arrow([(IX + IW, IY + 125), (266, IY + 125), (266, TY + 100), (TX, TY + 100)], INFO, "info", 1.4)
d.arrow([(IX + IW, IY + 255), (266, IY + 255), (266, TY + 140), (TX, TY + 140)], OK, "ok", 1.4)

# 3. 우측 상단: 코어 1 (파일 JSON 코어)
C1_X, C1_Y, C1_W, C1_H = 486, 120, 418, 150
d.box(C1_X, C1_Y, C1_W, C1_H, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(C1_X + 16, C1_Y + 24, "코어 1 · 기존 코어 (c1)", 12, OK, KR, "start", 600)
d.t(C1_X + 205, C1_Y + 24, "JSONEncoder · logFile · InfoLevel", 10, SOFT, MONO, "start")

# 레벨 평가 결과
d.tone(C1_X + 16, C1_Y + 40, C1_W - 32, 44, BAD, 4, "12", 0.9)
d.t(C1_X + 24, C1_Y + 66, "Debug 엔트리: InfoLevel 미달 → 차단 (Drop)", 11, BAD, KR, "start", 600)

d.tone(C1_X + 16, C1_Y + 92, C1_W - 32, 44, OK, 4, "12", 0.9)
d.t(C1_X + 24, C1_Y + 112, "Info 엔트리: 통과 → logFile 에 JSON 기록", 11, OK, KR, "start", 600)
d.t(C1_X + 24, C1_Y + 128, "{\"level\":\"info\",\"msg\":\"this is logged as...\"}", 9, INK, MONO, "start")

# 4. 우측 하단: 코어 2 (콘솔 코어)
C2_X, C2_Y, C2_W, C2_H = 486, 300, 418, 160
d.box(C2_X, C2_Y, C2_W, C2_H, fill=PAPER2, stroke=ACC, sw=1.2, r=6)
d.t(C2_X + 16, C2_Y + 24, "코어 2 · 추가 코어 (c2)", 12, ACC, KR, "start", 600)
d.t(C2_X + 205, C2_Y + 24, "Console · os.Stdout · DebugLevel", 10, SOFT, MONO, "start")

# 레벨 평가 결과
d.tone(C2_X + 16, C2_Y + 40, C2_W - 32, 48, INFO, 4, "12", 0.9)
d.t(C2_X + 24, C2_Y + 60, "Debug 엔트리: 통과 → 표준 출력 (콘솔)", 11, INFO, KR, "start", 600)
d.t(C2_X + 24, C2_Y + 78, "DEBUG  this is only logged as console encoding", 9, INK, MONO, "start")

d.tone(C2_X + 16, C2_Y + 98, C2_W - 32, 48, ACC, 4, "12", 0.9)
d.t(C2_X + 24, C2_Y + 118, "Info 엔트리: 통과 → 표준 출력 (콘솔)", 11, ACC, KR, "start", 600)
d.t(C2_X + 24, C2_Y + 136, "INFO   this is logged as console encoding and JSON", 9, INK, MONO, "start")

# 화살표: NewTee -> 코어 1 & 2
d.arrow([(TX + TW, TY + 60), (466, TY + 60), (466, C1_Y + 70), (C1_X - 4, C1_Y + 70)], OK, "ok", 1.4)
d.arrow([(TX + TW, TY + 180), (466, TY + 180), (466, C2_Y + 80), (C2_X - 4, C2_Y + 80)], ACC, "acc", 1.4)

svg_path = pathlib.Path(__file__).resolve().parent.parent / "13-01.zap-tee-core-flow.svg"
d.save(str(svg_path))
print("ok 13-01 zap-tee-core-flow")
