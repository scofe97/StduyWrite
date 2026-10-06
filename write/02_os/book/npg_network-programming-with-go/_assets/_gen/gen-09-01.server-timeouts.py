# 타입 스펙: type-gantt
# 09-01 HTTP 서버 연결 시간축과 타임아웃 적용 구간
# 사실 출처: NPG Ch.9 Listing 9-1 (ReadHeaderTimeout 1m, IdleTimeout 5m) 및 pkg.go.dev/net/http#Server 명세
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 450
d = D(W, H, "NPG CH.9 — SERVER TIMEOUTS",
      "HTTP 서버 연결 시간축과 타임아웃 적용 구간",
      "요청 헤더·본문·핸들러·응답·유휴 각 구간에 대응하는 http.Server 타임아웃 필드",
      "Listing 9-1 의 ReadHeaderTimeout(1분)과 IdleTimeout(5분) 설정 기준")

# Timeline boundaries
# Left column: x=24..200
# Timeline area: x=210..850 (width 640px)
# 5 Phases:
# P1: 210..330 (120px) 요청 헤더 읽기
# P2: 330..460 (130px) 본문 읽기
# P3: 460..590 (130px) 핸들러 실행
# P4: 590..720 (130px) 응답 쓰기
# P5: 720..850 (130px) 유휴 대기

# 1. Timeline Header (한국어 일반 라벨 12px, 오해를 주는 고정폭 가상 API 제거)
d.t(270, 114, "1. 요청 헤더 읽기", 12, INK, KR, "middle", 600)
d.t(395, 114, "2. 본문 읽기", 12, INK, KR, "middle", 600)
d.t(525, 114, "3. 핸들러 실행", 12, INK, KR, "middle", 600)
d.t(655, 114, "4. 응답 전송", 12, INK, KR, "middle", 600)
d.t(785, 114, "5. 다음 요청 유휴", 12, INK, KR, "middle", 600)

# Hairline separator under headers
d.line(24, 130, 850, 130, c=RULE, sw=0.8)

# Vertical grid lines
for gx in (210, 330, 460, 590, 720, 850):
    d.line(gx, 130, gx, 340, c=RULE, sw=0.7, dash="3 4")

# 2. Rows
# Row 1: ReadHeaderTimeout (Focal - ACC)
y1 = 145
d.t(24, y1 + 12, "권장 설정", 12, ACC, KR, "start", 600)
d.t(24, y1 + 27, "ReadHeaderTimeout", 11, INK, MONO, "start", 600)
d.tone(210, y1 + 5, 120, 24, ACC, op="22", sw=1.3)
d.t(270, y1 + 21, "1m (Listing 9-1)", 10, ACC, MONO, "middle", 600)

# Row 2: ReadTimeout (INFO) - 중복 설명 제거하고 API 이름 단독 배치
y2 = 195
d.t(24, y2 + 20, "ReadTimeout", 11, INK, MONO, "start", 600)
d.tone(210, y2 + 5, 250, 24, INFO, op="18", sw=1.1)
d.t(335, y2 + 21, "헤더 읽기 시작 ~ 본문 읽기 완료", 12, INK, KR, "middle")

# Row 3: WriteTimeout (WARN) - 중복 설명 제거하고 API 이름 단독 배치
y3 = 245
d.t(24, y3 + 20, "WriteTimeout", 11, INK, MONO, "start", 600)
d.tone(330, y3 + 5, 390, 24, WARN, op="18", sw=1.1)
d.t(525, y3 + 21, "헤더 읽은 직후 리셋 ~ 응답 쓰기 완료", 12, INK, KR, "middle")

# Row 4: IdleTimeout (OK)
y4 = 295
d.t(24, y4 + 12, "권장 설정", 12, OK, KR, "start", 600)
d.t(24, y4 + 27, "IdleTimeout", 11, INK, MONO, "start", 600)
d.tone(720, y4 + 5, 130, 24, OK, op="22", sw=1.3)
d.t(785, y4 + 21, "5m (Listing 9-1)", 10, OK, MONO, "middle", 600)

# Bottom border of rows
d.line(24, 340, 850, 340, c=RULE, sw=0.8)

# 3. Legend
d.legend(375, [
    ("원문 권장 (1분)", ACC),
    ("유휴 관리 (5분)", OK),
    ("전체 요청 읽기", INFO),
    ("응답 쓰기 제한", WARN),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "09-01.server-timeouts.svg"))
d.save(out)
print(f"saved: {out}")
