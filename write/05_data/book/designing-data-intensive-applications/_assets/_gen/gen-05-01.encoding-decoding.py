# 05-01 §1 — 인메모리 포인터 구조체와 네트워크·파일용 자족적 바이트 시퀀스의 인코딩·디코딩 데이터 흐름.
# 사실 출처: 05-01 §1(L33~L45), 원서 Ch.5 Formats for Encoding Data (PDF p.3). 예시 레코드 값은 원서 Figure 5-1(PDF p.3)의 Person 레코드에서 photoURL 을 뺀 것
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY1 = 104
BH1 = 200
PY2 = 328
BH2 = 84
LEG = 444
H = LEG + 56

d = D(W, H, "05-01 · ENCODING & DECODING DATA FLOW", "인메모리 객체와 자족적 바이트 시퀀스의 번역 흐름",
      "인메모리 포인터 구조체를 파일·네트워크용 자족적 바이트 시퀀스로 인코딩하고 다른 프로세스에서 디코딩하는 데이터 흐름.",
      "인메모리 포인터 구조체 · 자족적 바이트 시퀀스 · 인코딩과 디코딩 번역 · zero-copy 대안")

col_x = [24, 320, 616]
col_w = [240, 240, 240]

# --- 1. 프로세스 A: 인메모리 표현 ---
x0 = col_x[0]
w0 = col_w[0]
d.box(x0, PY1, w0, BH1, PAPER2, RULE, 0.9)
d.chip(x0 + 80, PY1 + 22, "프로세스 A 메모리", INFO, 11)
d.t(x0 + w0 / 2, PY1 + 46, "인메모리 객체 표현", 13, INK, KR, "middle", 600)
d.t(x0 + w0 / 2, PY1 + 64, "CPU 효율 접근 · 포인터", 12, SOFT, KR, "middle")

# 내부 구조체 박스
d.box(x0 + 12, PY1 + 76, w0 - 24, 80, PAPER, RULE, 0.8)
d.t(x0 + 20, PY1 + 96, "Person", 11, INFO, MONO, "start", 600)
d.t(x0 + 20, PY1 + 116, "favoriteNumber: 1337", 12, INK, MONO, "start")
d.t(x0 + 20, PY1 + 132, "userName: *ptr -> \"Martin\"", 11, MUTED, MONO, "start")
d.t(x0 + 20, PY1 + 148, "interests: *ptr -> [\"hacking\"]", 11, MUTED, MONO, "start")

d.tone(x0 + 12, PY1 + 164, w0 - 24, 24, INFO, 4, "14", 0.9)
d.t(x0 + w0 / 2, PY1 + 180, "포인터는 다른 프로세스에 무의미", 12, INFO, KR, "middle")

# --- 2. 중계: 자족적 바이트 시퀀스 (FOCAL) ---
x1 = col_x[1]
w1 = col_w[1]
d.tone(x1, PY1, w1, BH1, ACC, 6, "18", 1.4)
d.chip(x1 + 80, PY1 + 22, "파일 · 네트워크", ACC, 11)
d.t(x1 + w1 / 2, PY1 + 46, "자족적 바이트 시퀀스", 13, INK, KR, "middle", 600)
d.t(x1 + w1 / 2, PY1 + 64, "직렬화된 평평한 바이트 열", 12, ACC, KR, "middle")

# 내부 JSON 바이트 박스
d.box(x1 + 12, PY1 + 76, w1 - 24, 80, PAPER, ACC, 0.8)
d.t(x1 + 20, PY1 + 96, "JSON 문서", 11, ACC, KR, "start", 600)
d.t(x1 + 20, PY1 + 116, "{\"userName\":\"Martin\",", 11, INK, MONO, "start")
d.t(x1 + 20, PY1 + 132, " \"favoriteNumber\":1337,", 11, INK, MONO, "start")
d.t(x1 + 20, PY1 + 148, " \"interests\":[\"hacking\"]}", 11, INK, MONO, "start")

d.tone(x1 + 12, PY1 + 164, w1 - 24, 24, ACC, 4, "20", 0.9)
d.t(x1 + w1 / 2, PY1 + 180, "포인터 없는 자족적 표현", 12, ACC, KR, "middle")

# --- 3. 프로세스 B: 디코딩된 인메모리 복원 ---
x2 = col_x[2]
w2 = col_w[2]
d.box(x2, PY1, w2, BH1, PAPER2, RULE, 0.9)
d.chip(x2 + 80, PY1 + 22, "프로세스 B 메모리", INFO, 11)
d.t(x2 + w2 / 2, PY1 + 46, "복원된 인메모리 객체", 13, INK, KR, "middle", 600)
d.t(x2 + w2 / 2, PY1 + 64, "CPU 효율 접근 · 포인터", 12, SOFT, KR, "middle")

# 내부 구조체 박스
d.box(x2 + 12, PY1 + 76, w2 - 24, 80, PAPER, RULE, 0.8)
d.t(x2 + 20, PY1 + 96, "Person", 11, INFO, MONO, "start", 600)
d.t(x2 + 20, PY1 + 116, "favoriteNumber: 1337", 12, INK, MONO, "start")
d.t(x2 + 20, PY1 + 132, "userName: *ptr -> \"Martin\"", 11, MUTED, MONO, "start")
d.t(x2 + 20, PY1 + 148, "interests: *ptr -> [\"hacking\"]", 11, MUTED, MONO, "start")

d.tone(x2 + 12, PY1 + 164, w2 - 24, 24, INFO, 4, "14", 0.9)
d.t(x2 + w2 / 2, PY1 + 180, "파싱 · 언마샬링", 12, INFO, KR, "middle")

# 변환 화살표 (수평)
y_arr = PY1 + 116
d.arrow([(x0 + w0, y_arr), (x1, y_arr)], ACC, "acc", 1.4)
d.t((x0 + w0 + x1) / 2, y_arr - 12, "인코딩", 12, ACC, KR, "middle", 600)
d.t((x0 + w0 + x1) / 2, y_arr + 16, "직렬화", 12, MUTED, KR, "middle")

d.arrow([(x1 + w1, y_arr), (x2, y_arr)], INFO, "info", 1.4)
d.t((x1 + w1 + x2) / 2, y_arr - 12, "디코딩", 12, INFO, KR, "middle", 600)
d.t((x1 + w1 + x2) / 2, y_arr + 16, "역직렬화", 12, MUTED, KR, "middle")

# --- 4. 하단 트랙: zero-copy 대안 (명시적 변환 생략) ---
d.box(24, PY2, W - 48, BH2, PAPER2, RULE, 0.9)
d.chip(112, PY2 + 22, "변환 생략 대안", OK, 11)
d.t(360, PY2 + 24, "zero-copy 형식과 압축 데이터 직접 연산", 13, INK, KR, "middle", 600)

d.tone(36, PY2 + 40, 388, 32, OK, 4, "16", 1.0)
d.t(230, PY2 + 60, "Cap'n Proto · FlatBuffers (zero-copy)", 12, OK, MONO, "middle")

d.tone(456, PY2 + 40, 388, 32, OK, 4, "16", 1.0)
d.t(650, PY2 + 60, "디스크에서 로드한 압축 데이터에 직접 연산", 12, OK, KR, "middle")

d.legend(LEG, [("핵심 전송 표현 (focal)", ACC), ("인메모리 자료구조", INFO), ("변환 생략 최적화", OK), ("보조 정보·설명", MUTED)])
d.save("05-01.encoding-decoding.svg")
