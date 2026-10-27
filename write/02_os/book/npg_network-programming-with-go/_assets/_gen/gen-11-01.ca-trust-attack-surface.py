# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.11 In Certificate Authorities We Trust, How to Compromise TLS (사본 116~122, 128~132, 134, 136줄)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 544
d = D(W, H, "ARCHITECTURE · CA TRUST & ATTACK SURFACES",
      "CA 신뢰 체계와 TLS 를 무너뜨리는 세 가지 공격 지점",
      "CA 서명 확인 관문을 통과하는 위조 공격과 관문 밖 서버를 침해하는 공격의 경로 대조",
      lead="가짜 인증서는 CA 서명 확인 관문을 통과해 사칭하고, 서버 호스트 침해는 관문 밖에서 통신 내용을 탈취합니다.")

# 4개 행 Y 좌표 및 높이 (모두 4의 배수)
y_r1 = 140
y_r2 = 224
y_r3 = 308
y_r4 = 400
RH = 56

# X 좌표 컬럼 정의 (모두 4의 배수)
x_c1 = 28
w_c1 = 200

x_c2 = 276
w_c2 = 208

x_gate = 528
w_gate = 176
y_gate_top = 92
h_gate = 280

x_c4 = 748
w_c4 = 188

# =========================================================================
# 중심 관문: CA 서명 확인 (Focal ACC 1곳 - Row 1~3 관통)
# =========================================================================
d.tone(x_gate, y_gate_top, w_gate, h_gate, ACC, r=8, op="10", sw=1.6)
d.t(x_gate + w_gate / 2, 114, "관문: CA 서명 확인", 13, ACC, KR, "middle", 600)
d.t(x_gate + w_gate / 2, 130, "클라이언트 신뢰 사슬 검증", 11, MUTED, KR, "middle")

# =========================================================================
# Row 1: 공격 1 — CA 오발급 (TURKTRUST, 2011·2012)
# =========================================================================
mid_y1 = y_r1 + RH / 2  # 168

# Col 1: 원인
d.tone(x_c1, y_r1, w_c1, RH, BAD, 6, "16", 1.1)
d.t(x_c1 + w_c1 / 2, y_r1 + 24, "공격 1: CA 오발급", 13, BAD, KR, "middle", 600)
d.t(x_c1 + w_c1 / 2, y_r1 + 44, "중간 CA 오발급 (TURKTRUST)", 11, MUTED, KR, "middle")

# 화살표 1: Col 1 -> Col 2
d.arrow([(x_c1 + w_c1, mid_y1), (x_c2 - 4, mid_y1)], c=BAD, m="bad")

# Col 2: 인증서
d.tone(x_c2, y_r1, w_c2, RH, BAD, 6, "16", 1.1)
d.t(x_c2 + w_c2 / 2, y_r1 + 24, "가짜 *.google.com 인증서", 13, BAD, MONO, "middle", 600)
d.t(x_c2 + w_c2 / 2, y_r1 + 44, "진짜 중간 CA 서명 보유", 11, MUTED, KR, "middle")

# 화살표 2: Col 2 -> 관문 내부 칩
d.arrow([(x_c2 + w_c2, mid_y1), (x_gate + 24, mid_y1)], c=BAD, m="bad")

# 관문 내부 칩
d.chip(x_gate + w_gate / 2, mid_y1, "진짜 CA 서명 통과", BAD, 11, 4)

# 화살표 3: 관문 내부 칩 -> Col 4
d.arrow([(x_gate + w_gate - 24, mid_y1), (x_c4 - 4, mid_y1)], c=BAD, m="bad")

# Col 4: 결과
d.tone(x_c4, y_r1, w_c4, RH, BAD, 6, "18", 1.2)
d.t(x_c4 + w_c4 / 2, y_r1 + 24, "사칭", 14, BAD, KR, "middle", 600)
d.t(x_c4 + w_c4 / 2, y_r1 + 44, "가짜 서버 연결 수용", 11, MUTED, KR, "middle")

# =========================================================================
# Row 2: 정상 검증 사슬 (서버 인증서 ← 중간 CA 서명 ← 루트 CA)
# =========================================================================
mid_y2 = y_r2 + RH / 2  # 252

# Col 1: 서버 및 인증서
d.tone(x_c1, y_r2, w_c1, RH, OK, 6, "16", 1.1)
d.t(x_c1 + w_c1 / 2, y_r2 + 24, "서버 인증서 (*.google.com)", 13, OK, MONO, "middle", 600)
d.t(x_c1 + w_c1 / 2, y_r2 + 44, "진짜 서버 호스트 제시", 11, MUTED, KR, "middle")

# 화살표: Col 1 -> Col 2
d.arrow([(x_c1 + w_c1, mid_y2), (x_c2 - 4, mid_y2)], c=OK, m="ok")

# Col 2: 서명 사슬 대조
d.tone(x_c2, y_r2, w_c2, RH, OK, 6, "16", 1.1)
d.t(x_c2 + w_c2 / 2, y_r2 + 24, "중간 CA 서명 ← 루트 CA", 13, OK, KR, "middle", 600)
d.t(x_c2 + w_c2 / 2, y_r2 + 44, "신뢰 저장소 루트 CA 사슬 일치", 11, MUTED, KR, "middle")

# 화살표: Col 2 -> 관문 내부 칩
d.arrow([(x_c2 + w_c2, mid_y2), (x_gate + 24, mid_y2)], c=OK, m="ok")

# 관문 내부 칩
d.chip(x_gate + w_gate / 2, mid_y2, "정상 사슬 검증", OK, 11, 4)

# 화살표: 관문 내부 칩 -> Col 4
d.arrow([(x_gate + w_gate - 24, mid_y2), (x_c4 - 4, mid_y2)], c=OK, m="ok")

# Col 4: 결과
d.tone(x_c4, y_r2, w_c4, RH, OK, 6, "18", 1.2)
d.t(x_c4 + w_c4 / 2, y_r2 + 24, "통과", 14, OK, KR, "middle", 600)
d.t(x_c4 + w_c4 / 2, y_r2 + 44, "정상 암호화 통신 수립", 11, MUTED, KR, "middle")

# =========================================================================
# Row 3: 공격 2 — 클라이언트 신뢰 저장소 변조
# =========================================================================
mid_y3 = y_r3 + RH / 2  # 336

# Col 1: 원인
d.tone(x_c1, y_r3, w_c1, RH, BAD, 6, "16", 1.1)
d.t(x_c1 + w_c1 / 2, y_r3 + 24, "공격 2: 저장소 변조", 13, BAD, KR, "middle", 600)
d.t(x_c1 + w_c1 / 2, y_r3 + 44, "공격자 루트 CA 등록", 11, MUTED, KR, "middle")

# 화살표: Col 1 -> Col 2
d.arrow([(x_c1 + w_c1, mid_y3), (x_c2 - 4, mid_y3)], c=BAD, m="bad")

# Col 2: 인증서
d.tone(x_c2, y_r3, w_c2, RH, BAD, 6, "16", 1.1)
d.t(x_c2 + w_c2 / 2, y_r3 + 24, "공격자가 서명한 인증서", 13, BAD, KR, "middle", 600)
d.t(x_c2 + w_c2 / 2, y_r3 + 44, "등록된 공격자 루트 CA 로 서명", 11, MUTED, KR, "middle")

# 화살표: Col 2 -> 관문 내부 칩
d.arrow([(x_c2 + w_c2, mid_y3), (x_gate + 24, mid_y3)], c=BAD, m="bad")

# 관문 내부 칩
d.chip(x_gate + w_gate / 2, mid_y3, "등록된 루트 통과", BAD, 11, 4)

# 화살표: 관문 내부 칩 -> Col 4
d.arrow([(x_gate + w_gate - 24, mid_y3), (x_c4 - 4, mid_y3)], c=BAD, m="bad")

# Col 4: 결과
d.tone(x_c4, y_r3, w_c4, RH, BAD, 6, "18", 1.2)
d.t(x_c4 + w_c4 / 2, y_r3 + 24, "사칭", 14, BAD, KR, "middle", 600)
d.t(x_c4 + w_c4 / 2, y_r3 + 44, "가짜 서버 연결 수용", 11, MUTED, KR, "middle")

# =========================================================================
# Row 4: 공격 3 — 서버 호스트 침해 (관문 밖 서버 직접 장악, 관문 우회)
# =========================================================================
mid_y4 = y_r4 + RH / 2  # 428

# Col 1: 원인
d.tone(x_c1, y_r4, w_c1, RH, BAD, 6, "16", 1.1)
d.t(x_c1 + w_c1 / 2, y_r4 + 24, "공격 3: 서버 호스트 침해", 13, BAD, KR, "middle", 600)
d.t(x_c1 + w_c1 / 2, y_r4 + 44, "서버 침해 · 호스트 장악", 11, MUTED, KR, "middle")

# 화살표: Col 1 -> Col 2
d.arrow([(x_c1 + w_c1, mid_y4), (x_c2 - 4, mid_y4)], c=BAD, m="bad")

# Col 2: 장악된 진짜 서버
d.tone(x_c2, y_r4, w_c2, RH, BAD, 6, "16", 1.1)
d.t(x_c2 + w_c2 / 2, y_r4 + 24, "진짜 서버 (*.google.com)", 13, BAD, MONO, "middle", 600)
d.t(x_c2 + w_c2 / 2, y_r4 + 44, "서버 메모리에서 세션 키 탈취", 11, MUTED, KR, "middle")

# 화살표: Col 2 -> 관문 우회 칩 (관문 y_gate_top+h_gate=372 아래로 직접 통과)
d.arrow([(x_c2 + w_c2, mid_y4), (x_gate + 12, mid_y4)], c=BAD, m="bad")

# 관문 우회 표지 칩
d.chip(x_gate + w_gate / 2, mid_y4, "관문 우회 · 직접 탈취", BAD, 11, 4)

# 화살표: 관문 우회 칩 -> Col 4
d.arrow([(x_gate + w_gate - 12, mid_y4), (x_c4 - 4, mid_y4)], c=BAD, m="bad")

# Col 4: 결과 (사칭 아님, 통신 내용 탈취)
d.tone(x_c4, y_r4, w_c4, RH, BAD, 6, "18", 1.2)
d.t(x_c4 + w_c4 / 2, y_r4 + 24, "사칭 아님, 통신 내용 탈취", 12, BAD, KR, "middle", 600)
d.t(x_c4 + w_c4 / 2, y_r4 + 44, "활성 세션 키로 복호화", 11, MUTED, KR, "middle")

# =========================================================================
# 범례
# =========================================================================
d.legend(496, [("정상 신뢰 사슬", OK), ("침해 · 위조 공격", BAD), ("검증 관문 (focal)", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.ca-trust-attack-surface.svg"
d.save(str(svg_path))
print("ok 11-01 ca-trust-attack-surface")
