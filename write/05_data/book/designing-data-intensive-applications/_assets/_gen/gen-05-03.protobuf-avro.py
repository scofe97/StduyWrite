# 05-03 §1 — Protocol Buffers 필드 태그 기반 33바이트 이진 인코딩 구조와 스키마 진화 규칙.
# 사실 출처: 05-03 본문 §1(L32~L54), 원서 Figure 5-3(PDF p.10, Our record encoded using Protocol Buffers). 합 8+3+13+9=33.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
H = 556
LEG = 500

d = D(W, H, "05-03 · PROTOCOL BUFFERS", "Protocol Buffers field tag 이진 구조와 스키마 진화",
      "필드명 대신 숫자 tag와 타입 주석을 1바이트로 결합해 33바이트로 압축하고, 미지 태그 건너뜀으로 forward 호환을 유지한다.",
      "레코드 IDL 정의 · 33바이트 필드 청크 분해 · 태그 기반 forward·backward 호환 규칙")

X0 = 24
BOX_W = 832

# 1구간: 원본 레코드 및 IDL 스키마 요약
S1_Y = PY
S1_H = 48
d.box(X0, S1_Y, BOX_W, S1_H, PAPER2, RULE, 0.9)
d.chip(X0 + 44, S1_Y + 24, "IDL 정의", INFO, 11.5)
d.t(X0 + 94, S1_Y + 28, "Person { 1: user_name · 2: favorite_number · 3: repeated interests }", 11.5, INK, MONO, "start", 600)

# 2구간: 33바이트 바이너리 시퀀스 4개 청크 (가로 4열)
S2_Y = S1_Y + S1_H + 16
CW = 196
GAP = 16

chunks = [
    ("tag 1 · user_name", "8바이트 (문자열)", [
        ("tag 1 + type 2 (0x0a)", "타입 주석 1바이트", ACC),
        ("length 0x06", "문자열 길이 1바이트", INFO),
        ("'Martin'", "UTF-8 바이트 6바이트", INK)
    ]),
    ("tag 2 · favorite_number", "3바이트 (정수)", [
        ("tag 2 + type 0 (0x10)", "타입 주석 1바이트", ACC),
        ("1337 (0xb9 0x0a)", "가변 정수 2바이트", INFO),
        ("(varint 압축)", "상위 비트 연속 플래그", MUTED)
    ]),
    ("tag 3 · interests [0]", "13바이트 (첫 요소)", [
        ("tag 3 + type 2 (0x1a)", "타입 주석 1바이트", ACC),
        ("length 0x0b", "문자열 길이 1바이트", INFO),
        ("'daydreaming'", "UTF-8 바이트 11바이트", INK)
    ]),
    ("tag 3 · interests [1]", "9바이트 (둘째 요소)", [
        ("tag 3 + type 2 (0x1a)", "같은 태그 반복 1바이트", ACC),
        ("length 0x07", "문자열 길이 1바이트", INFO),
        ("'hacking'", "UTF-8 바이트 7바이트", INK)
    ])
]

for i, (title, size_str, parts) in enumerate(chunks):
    cx = X0 + i * (CW + GAP)
    d.box(cx, S2_Y, CW, 184, PAPER2, RULE, 0.9)
    d.t(cx + CW / 2, S2_Y + 20, title, 12, INK, MONO if "tag" in title else KR, "middle", 600)
    d.t(cx + CW / 2, S2_Y + 36, size_str, 11.5, ACC, KR, "middle")
    d.line(cx + 8, S2_Y + 44, cx + CW - 8, S2_Y + 44, RULE, 0.8)
    
    for j, (p_top, p_bot, col) in enumerate(parts):
        py = S2_Y + 52 + j * 42
        d.box(cx + 8, py, CW - 16, 36, PAPER, RULE, 0.8)
        d.t(cx + CW / 2, py + 16, p_top, 11.5, col, MONO if "0x" in p_top or "'" in p_top else KR, "middle", 600)
        d.t(cx + CW / 2, py + 30, p_bot, 11.5, SOFT, KR, "middle")

# 33바이트 연결 흐름 화살표
d.arrow([(W / 2, S2_Y + 186), (W / 2, S2_Y + 198)], SOFT, "soft", 1.2)

# 3구간: 스키마 진화와 호환성 3대 원칙
S3_Y = S2_Y + 200
EW = 268
EGAP = 14

evol_cards = [
    ("새 필드 추가 (forward)", [
        "옛 코드가 새 데이터 읽기",
        "미지 tag 타입 주석으로 바이트 건너뜀",
        "알 수 없는 필드 데이터 무시 및 보존"
    ], OK),
    ("옛 데이터 읽기 (backward)", [
        "새 코드가 옛 데이터 읽기",
        "필드마다 고유 tag 번호 유지 보장",
        "새 스키마 추가 필드는 기본값 보충"
    ], OK),
    ("필드명 변경과 태그 불변", [
        "필드명 변경 허용 (인코딩 미포함)",
        "tag 번호 변경 불가 (기존 데이터 파손)",
        "삭제 tag는 reserved (재사용 금지)"
    ], WARN)
]

for i, (e_title, e_items, e_col) in enumerate(evol_cards):
    ex = X0 + i * (EW + EGAP)
    d.box(ex, S3_Y, EW, 106, PAPER2, e_col, 1.1 if e_col == WARN else 0.9)
    d.chip(ex + 28, S3_Y + 18, "규칙", e_col, 11.5)
    d.t(ex + 48, S3_Y + 22, e_title, 12, INK, KR, "start", 600)
    d.line(ex + 8, S3_Y + 34, ex + EW - 8, S3_Y + 34, RULE, 0.8)
    
    for j, item in enumerate(e_items):
        iy = S3_Y + 44 + j * 19
        d.t(ex + 14, iy + 11, f"· {item}", 11.5, MUTED if e_col != WARN or j < 1 else WARN, KR, "start")

d.legend(LEG, [("태그·타입 결합 바이트", ACC), ("필드 데이터·길이 접두사", INFO), ("호환성 보장 메커니즘", OK), ("태그 불변 제약·주의", WARN)])
d.save("05-03.protobuf-avro.svg")
