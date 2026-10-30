# 05-02 §1 — 2^53 초과 정수의 JSON 파싱 정밀도 손실과 십진 문자열 우회(X post ID).
# 사실 출처: 본문 §1(L35) · 원서 Ch.5 JSON, XML, and Binary Variants (PDF p.5) — 2^53 초과 정수의 배정밀도 파싱 부정확성과 X 의 post ID 이중 전송(숫자·십진 문자열).
# 원서·본문에 구체 ID 값과 필드 이름이 없으므로 도식에도 두지 않는다. 2^53 값만 계산으로 확인해 둔다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, BAD, KR, MONO

W = 880
PY = 104
PH = 228
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "05-02 · §1 NUMBER PRECISION", "2^53 초과 정수의 JSON 파싱 정밀도 손실과 문자열 우회",
      "2^53 보다 큰 정수를 JavaScript 가 배정밀도 부동소수로 파싱하면 부정확해지고, X 가 post ID 를 숫자와 십진 문자열로 두 번 담아 이를 우회하는 경로를 보인다.",
      "원본 64비트 정수 → JSON API 직렬화 → JavaScript 부동소수 파싱 분기")

X1, W1 = 24, 236
X2, W2 = 296, 268
X3, W3 = 600, 256

# 구간 1: 원본 64비트 정수 (X 서버 post ID)
d.box(X1, PY, W1, PH, PAPER2, RULE, 0.9)
d.chip(X1 + 44, PY + 22, "1단계", INFO, 11)
d.t(X1 + W1 / 2 + 18, PY + 26, "원본 64비트 정수", 13, INK, KR, "middle", 600)
d.t(X1 + W1 / 2, PY + 46, "X 의 post 식별자", 12, SOFT, KR, "middle")
d.line(X1 + 12, PY + 56, X1 + W1 - 12, PY + 56, RULE, 0.8)

d.box(X1 + 12, PY + 68, W1 - 24, 60, PAPER, RULE, 0.8)
d.t(X1 + W1 / 2, PY + 88, "post ID", 12, MUTED, KR, "middle")
d.t(X1 + W1 / 2, PY + 112, "64비트 숫자", 12.5, INK, KR, "middle", 600)

d.tone(X1 + 12, PY + 140, W1 - 24, 72, INFO, 6, "14", 1.0)
d.t(X1 + W1 / 2, PY + 162, "2^53 정밀도 한계 초과", 12, INFO, KR, "middle", 600)
d.t(X1 + W1 / 2, PY + 182, "2^53 = 9007199254740992", 11, MUTED, MONO, "middle")
d.t(X1 + W1 / 2, PY + 200, "배정밀도로 정확히 표현 못 함", 11.5, MUTED, KR, "middle")

# 구간 1 → 구간 2 연결 화살표
d.arrow([(X1 + W1, PY + PH / 2), (X2 - 4, PY + PH / 2)], SOFT, "soft", 1.3)

# 구간 2: JSON API 응답 페이로드 (이중 필드)
d.box(X2, PY, W2, PH, PAPER2, RULE, 0.9)
d.chip(X2 + 44, PY + 22, "2단계", INFO, 11)
d.t(X2 + W2 / 2 + 18, PY + 26, "JSON API 응답", 13, INK, KR, "middle", 600)
d.t(X2 + W2 / 2, PY + 46, "post ID 를 두 번 담음", 12, SOFT, KR, "middle")
d.line(X2 + 12, PY + 56, X2 + W2 - 12, PY + 56, RULE, 0.8)

# 상단: id 필드 (숫자)
d.box(X2 + 12, PY + 68, W2 - 24, 68, PAPER, BAD, 0.8)
d.t(X2 + 24, PY + 88, "숫자로 한 번", 12, BAD, KR, "start", 600)
d.t(X2 + 24, PY + 112, "JSON number", 11.5, INK, MONO, "start")

# 하단: id_str 필드 (문자열)
d.box(X2 + 12, PY + 144, W2 - 24, 68, PAPER, ACC, 0.8)
d.t(X2 + 24, PY + 164, "십진 문자열로 한 번 (우회)", 12, ACC, KR, "start", 600)
d.t(X2 + 24, PY + 188, "JSON string (decimal)", 11.5, INK, MONO, "start")

# 구간 2 → 구간 3 연결 화살표 (두 갈래)
d.arrow([(X2 + W2, PY + 102), (X3 - 4, PY + 102)], BAD, "bad", 1.3)
d.arrow([(X2 + W2, PY + 178), (X3 - 4, PY + 178)], ACC, "acc", 1.3)

# 구간 3: JavaScript 파싱 결과
# 상단: 숫자 파싱 실패 (BAD)
d.box(X3, PY, W3, 102, PAPER2, BAD, 1.2)
d.chip(X3 + 52, PY + 22, "경로 A", BAD, 11)
d.t(X3 + W3 / 2 + 24, PY + 26, "숫자로 파싱", 12.5, INK, KR, "middle", 600)
d.t(X3 + W3 / 2, PY + 48, "IEEE 754 배정밀도 변환", 12, SOFT, KR, "middle")
d.box(X3 + 12, PY + 58, W3 - 24, 34, PAPER, BAD, 0.8)
d.t(X3 + W3 / 2, PY + 73, "값이 부정확해짐", 12, BAD, KR, "middle", 600)
d.t(X3 + W3 / 2, PY + 87, "2^53 초과분 정밀도 손실", 11, MUTED, KR, "middle")

# 하단: 문자열 파싱 성공 (ACC)
d.box(X3, PY + 126, W3, 102, PAPER2, ACC, 1.4)
d.chip(X3 + 52, PY + 148, "경로 B", ACC, 11)
d.t(X3 + W3 / 2 + 24, PY + 152, "문자열로 받기 (우회)", 12.5, INK, KR, "middle", 600)
d.t(X3 + W3 / 2, PY + 174, "부동소수 변환을 거치지 않음", 12, SOFT, KR, "middle")
d.box(X3 + 12, PY + 184, W3 - 24, 34, PAPER, ACC, 0.8)
d.t(X3 + W3 / 2, PY + 199, "십진 문자열 그대로", 12, ACC, KR, "middle", 600)
d.t(X3 + W3 / 2, PY + 213, "정밀도 보존", 11.5, ACC, KR, "middle", 600)

d.legend(LEG, [("문자열 우회 — 정밀도 보존", ACC), ("부동소수 파싱 — 부정확", BAD), ("전송 페이로드", INFO)])
d.save("05-02.number-precision.svg")
