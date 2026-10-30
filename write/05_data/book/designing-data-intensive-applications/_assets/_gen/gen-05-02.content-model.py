# 05-02 §2 — JSON Schema의 open 대 closed content model 검증 판정 비교.
# 사실 출처: 본문 §2(L50~L52) · 원서 Ch.5 JSON Schema (PDF p.6) — port 제약(1~65535), additionalProperties 기본값(true)과 open/closed 판정 차이, "금지된 것의 정의".
# 원서·본문에 구체 페이로드 값이 없으므로 예시는 제약에서 파생한 자리 표시(<…>)로만 적는다.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, BAD, KR, MONO

W = 880
HY = 104
HH = 52
RY0 = 168
RSTR = 92
RH = 82
LEG = RY0 + 3 * RSTR + 24
H = LEG + 56

d = D(W, H, "05-02 · §2 CONTENT MODEL", "JSON Schema open 대 closed content model 검증 비교",
      "정의된 필드와 미정의 추가 필드, 제약 위반 필드가 들어왔을 때 두 모델의 검증 판정과 금지된 것 정의 메커니즘을 대조한다.",
      "스키마 제약: port (1~65535) · 입력 페이로드별 두 모델 검증 판정 대조")

LX, LW = 24, 316
CX1, CW = 352, 246
CX2 = CX1 + CW + 12

# 상단 헤더: 컬럼 타이틀
d.box(LX, HY, LW, HH, PAPER2, RULE, 0.9)
d.t(LX + 14, HY + 24, "검증 대상 입력 페이로드", 13, INK, KR, "start", 600)
d.t(LX + 14, HY + 42, "스키마 기준: port (integer, 1~65535)", 11.5, SOFT, KR, "start")

d.box(CX1, HY, CW, HH, PAPER2, RULE, 0.9)
d.t(CX1 + CW / 2, HY + 22, "Open Content Model", 13, INK, KR, "middle", 600)
d.t(CX1 + CW / 2, HY + 42, "additionalProperties: true (기본)", 11.5, SOFT, MONO, "middle")

d.box(CX2, HY, CW, HH, PAPER2, RULE, 0.9)
d.t(CX2 + CW / 2, HY + 22, "Closed Content Model", 13, INK, KR, "middle", 600)
d.t(CX2 + CW / 2, HY + 42, "additionalProperties: false", 11.5, SOFT, MONO, "middle")

rows = [
    # 행 1: 정상 필드
    ("사례 1", "정의된 정상 필드", '{"port": <1~65535>}', "정의된 필드 · 범위 안 값",
     ("검증 통과 (VALID)", "정의된 정상 값 수용", OK),
     ("검증 통과 (VALID)", "명시된 필드 일치", OK)),
    # 행 2: 미정의 추가 필드 (핵심 차이 - FOCAL)
    ("사례 2", "미정의 추가 필드", '{"port": <1~65535>, "<extra>": …}', "스키마에 없는 필드 포함",
     ("검증 통과 (VALID)", "미정의 필드 허용 (금지된 것만 검사)", ACC),
     ("검증 거부 (INVALID)", "명시되지 않은 추가 속성 차단", BAD)),
    # 행 3: 제약 위반 필드
    ("사례 3", "제약 위반 필드", '{"port": <n > 65535>}', "정의된 port 의 최대값(65535) 초과",
     ("검증 거부 (INVALID)", "정의된 제약(maximum) 위반 감지", BAD),
     ("검증 거부 (INVALID)", "정의된 제약(maximum) 위반 감지", BAD)),
]

for r, (case_badge, case_title, code_txt, sub_txt, col1, col2) in enumerate(rows):
    y = RY0 + r * RSTR
    is_focal_row = (r == 1)

    # 페이로드 설명 셀
    d.box(LX, y, LW, RH, PAPER2, ACC if is_focal_row else RULE, 1.2 if is_focal_row else 0.8)
    d.chip(LX + 34, y + 20, case_badge, ACC if is_focal_row else SOFT, 11)
    d.t(LX + 76, y + 24, case_title, 12, INK, KR, "start", 600)
    d.t(LX + 14, y + 46, code_txt, 11, ACC if is_focal_row else INK, MONO, "start")
    d.t(LX + 14, y + 68, sub_txt, 11.5, MUTED, KR, "start")

    # Col 1 (Open Model)
    c1_txt, c1_sub, c1_color = col1
    if is_focal_row:
        d.tone(CX1, y, CW, RH, ACC, 6, "22", 1.4)
        d.t(CX1 + CW / 2, y + 32, c1_txt, 13, INK, KR, "middle", 600)
        d.t(CX1 + CW / 2, y + 54, c1_sub, 12, ACC, KR, "middle", 600)
    else:
        d.box(CX1, y, CW, RH, PAPER, RULE, 0.8)
        d.t(CX1 + CW / 2, y + 32, c1_txt, 12.5, c1_color, KR, "middle", 600)
        d.t(CX1 + CW / 2, y + 54, c1_sub, 11.5, MUTED, KR, "middle")

    # Col 2 (Closed Model)
    c2_txt, c2_sub, c2_color = col2
    d.box(CX2, y, CW, RH, PAPER, RULE, 0.8)
    d.t(CX2 + CW / 2, y + 32, c2_txt, 12.5, c2_color, KR, "middle", 600)
    d.t(CX2 + CW / 2, y + 54, c2_sub, 11.5, MUTED, KR, "middle")

d.legend(LEG, [("핵심 차이 — 미정의 필드 허용", ACC), ("검증 통과 — 규칙 충족", OK), ("검증 거부 — 스키마 위반", BAD)])
d.save("05-02.content-model.svg")
