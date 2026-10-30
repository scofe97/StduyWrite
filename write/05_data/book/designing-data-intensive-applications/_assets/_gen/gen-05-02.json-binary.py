# 05-02 §3 — 텍스트 JSON과 MessagePack 이진 인코딩 바이트 구성 및 크기 비교.
# 사실 출처: 본문 §3(L76~L84), 원서 Figure 5-2(PDF p.8, Our record encoded using MessagePack).
# 칸의 "a+bB" 는 타입·길이 바이트 a 와 내용 바이트 b. 합: 타입·길이 1+1+1+1+1+1+3=9, 필드명 8+14+9=31, 값 6+2+18=26, 계 66.
# 타입 스펙: type-bar
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, KR, MONO

W = 880
PY = 104
LEG = 476
H = LEG + 56

d = D(W, H, "05-02 · §3 JSON BINARY", "텍스트 JSON과 MessagePack 이진 인코딩 비교",
      "스키마를 규정하지 않는 JSON 이진 변형은 객체 필드명을 데이터에 모두 포함해야 하므로 텍스트 대비 절감량이 제한적이다.",
      "동일 레코드 텍스트(81B) 대 MessagePack(66B) · 필드명 점유 바이트 분석")

X0, BW = 24, 832

# 1구간: 총 크기 비교 바 차트 (Y=104 ~ Y=200)
S1_Y = PY
S1_H = 100
d.box(X0, S1_Y, BW, S1_H, PAPER2, RULE, 0.9)
d.chip(X0 + 44, S1_Y + 20, "크기 비교", INFO, 11)
d.t(X0 + 88, S1_Y + 24, "동일 레코드 인코딩 바이트 수", 13, INK, KR, "start", 600)
d.t(X0 + BW - 16, S1_Y + 24, "공백 제거 텍스트 대비 15바이트(18.5%) 절감", 11.5, SOFT, KR, "end")
d.line(X0 + 12, S1_Y + 36, X0 + BW - 12, S1_Y + 36, RULE, 0.8)

# Bar 1: 텍스트 JSON (81B)
BAR_X = X0 + 150
BAR_MAX_W = 540
W_JSON = int(BAR_MAX_W * 81 / 81)
d.t(X0 + 20, S1_Y + 54, "텍스트 JSON", 12, INK, KR, "start", 600)
d.box(BAR_X, S1_Y + 42, W_JSON, 18, PAPER, RULE, 0.9, r=3)
d.t(BAR_X + W_JSON + 12, S1_Y + 55, "81 byte", 11.5, MUTED, MONO, "start")

# Bar 2: MessagePack (66B, focal: ACC)
W_MSGPACK = int(BAR_MAX_W * 66 / 81)
d.t(X0 + 20, S1_Y + 80, "MessagePack", 12, ACC, KR, "start", 600)
d.tone(BAR_X, S1_Y + 68, W_MSGPACK, 18, ACC, 3, "28", 1.2)
d.t(BAR_X + W_MSGPACK + 12, S1_Y + 81, "66 byte (필드명 포함 필수)", 11.5, ACC, KR, "start", 600)


# 2구간: MessagePack 바이트 스트림 구조 분해 (Figure 5-2)
S2_Y = S1_Y + S1_H + 14
S2_H = 142
d.box(X0, S2_Y, BW, S2_H, PAPER2, RULE, 0.9)
d.chip(X0 + 52, S2_Y + 20, "바이트 구조", ACC, 11)
d.t(X0 + 104, S2_Y + 24, "MessagePack 인코딩 바이트 스트림 분해", 13, INK, KR, "start", 600)
d.t(X0 + BW - 16, S2_Y + 24, "원서 Figure 5-2 · 앞 수는 타입·길이 바이트", 11.5, SOFT, KR, "end")
d.line(X0 + 12, S2_Y + 36, X0 + BW - 12, S2_Y + 36, RULE, 0.8)

# 4개 필드 그룹 카드 가로 배치
# Group 1: 객체 헤더
GX1, GW1 = X0 + 12, 116
d.box(GX1, S2_Y + 46, GW1, 82, PAPER, INFO, 0.9)
d.chip(GX1 + GW1 / 2, S2_Y + 62, "헤더", INFO, 11)
d.t(GX1 + GW1 / 2, S2_Y + 88, "0x83", 12, INK, MONO, "middle", 600)
d.t(GX1 + GW1 / 2, S2_Y + 110, "3개 필드 객체 (1B)", 11, MUTED, KR, "middle")

# Group 2: userName (Martin)
GX2, GW2 = GX1 + GW1 + 8, 218
d.box(GX2, S2_Y + 46, GW2, 82, PAPER, RULE, 0.8)
d.tone(GX2 + 6, S2_Y + 54, GW2 - 12, 32, ACC, 4, "18", 1.0)
d.t(GX2 + 14, S2_Y + 74, "0xa8 + userName", 11.5, ACC, MONO, "start", 600)
d.t(GX2 + GW2 - 14, S2_Y + 74, "1+8B", 11, ACC, KR, "end")
d.tone(GX2 + 6, S2_Y + 90, GW2 - 12, 32, OK, 4, "14", 1.0)
d.t(GX2 + 14, S2_Y + 110, '0xa6 + "Martin"', 11.5, OK, MONO, "start", 600)
d.t(GX2 + GW2 - 14, S2_Y + 110, "문자열 1+6B", 11, OK, KR, "end")

# Group 3: favoriteNumber (1337)
GX3, GW3 = GX2 + GW2 + 8, 238
d.box(GX3, S2_Y + 46, GW3, 82, PAPER, RULE, 0.8)
d.tone(GX3 + 6, S2_Y + 54, GW3 - 12, 32, ACC, 4, "18", 1.0)
d.t(GX3 + 14, S2_Y + 74, "0xae + favoriteNumber", 11.5, ACC, MONO, "start", 600)
d.t(GX3 + GW3 - 14, S2_Y + 74, "1+14B", 11, ACC, KR, "end")
d.tone(GX3 + 6, S2_Y + 90, GW3 - 12, 32, OK, 4, "14", 1.0)
d.t(GX3 + 14, S2_Y + 110, "0xcd 0x05 0x39 (1337)", 11.5, OK, MONO, "start", 600)
d.t(GX3 + GW3 - 14, S2_Y + 110, "정수 1+2B", 11, OK, KR, "end")

# Group 4: interests (daydreaming, hacking)
GX4, GW4 = GX3 + GW3 + 8, 212
d.box(GX4, S2_Y + 46, GW4, 82, PAPER, RULE, 0.8)
d.tone(GX4 + 6, S2_Y + 54, GW4 - 12, 32, ACC, 4, "18", 1.0)
d.t(GX4 + 14, S2_Y + 74, "0xa9 + interests", 11.5, ACC, MONO, "start", 600)
d.t(GX4 + GW4 - 14, S2_Y + 74, "1+9B", 11, ACC, KR, "end")
d.tone(GX4 + 6, S2_Y + 90, GW4 - 12, 32, OK, 4, "14", 1.0)
d.t(GX4 + 14, S2_Y + 110, "0x92 + 2개 문자열", 11.5, OK, MONO, "start", 600)
d.t(GX4 + GW4 - 14, S2_Y + 110, "배열 3+18B", 11, OK, KR, "end")


# 3구간: 바이트 점유 비중 분석 (누적 바)
S3_Y = S2_Y + S2_H + 14
S3_H = 88
d.box(X0, S3_Y, BW, S3_H, PAPER2, RULE, 0.9)
d.chip(X0 + 52, S3_Y + 20, "비중 분석", SOFT, 11)
d.t(X0 + 104, S3_Y + 24, "MessagePack 66바이트 점유 구성", 13, INK, KR, "start", 600)
d.t(X0 + BW - 16, S3_Y + 24, "스키마가 없어 66B 중 31B 가 필드명", 11.5, ACC, KR, "end", 600)
d.line(X0 + 12, S3_Y + 36, X0 + BW - 12, S3_Y + 36, RULE, 0.8)

# 스택 바: 필드명 31B(47.0%) + 헤더 9B(13.6%) + 값 26B(39.4%) = 66B
ST_X = X0 + 20
ST_W = BW - 40
W_FN = int(ST_W * 31 / 66)
W_HD = int(ST_W * 9 / 66)
W_VAL = ST_W - W_FN - W_HD

# 필드명 구간 (ACC)
d.tone(ST_X, S3_Y + 46, W_FN, 26, ACC, 3, "28", 1.2)
d.t(ST_X + W_FN / 2, S3_Y + 63, "필드명 문자열 31B (47.0%)", 11.5, INK, KR, "middle", 600)

# 헤더 프리픽스 구간 (INFO)
d.tone(ST_X + W_FN, S3_Y + 46, W_HD, 26, INFO, 3, "20", 1.0)
d.t(ST_X + W_FN + W_HD / 2, S3_Y + 63, "타입·길이 9B", 11, INK, KR, "middle")

# 값 구간 (OK)
d.tone(ST_X + W_FN + W_HD, S3_Y + 46, W_VAL, 26, OK, 3, "20", 1.0)
d.t(ST_X + W_FN + W_HD + W_VAL / 2, S3_Y + 63, "실제 값 데이터 26B (39.4%)", 11.5, INK, KR, "middle", 600)

d.legend(LEG, [("필드명 — 스키마 부재로 포함 필수", ACC), ("실제 값 데이터", OK), ("타입·길이 프리픽스 바이트", INFO)])
d.save("05-02.json-binary.svg")
