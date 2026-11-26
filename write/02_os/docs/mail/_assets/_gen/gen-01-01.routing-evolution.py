# 사실 출처: RFC 821 §3.6, RFC 974, RFC 5321 §3.6.1, RFC 5321 §5.1, RFC 5598 §4.3.2
# 타입 스펙: type-process
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 540
d = D(
    W, H,
    "MAIL SYSTEM THEORY · 01 ROUTING EVOLUTION",
    "메일 목적지 해석의 세 시대 (1970년대~현재)",
    "호스트 직접 연결에서 소스 라우트를 거쳐 DNS MX 동적 조회로의 진화 과정",
    "동일한 수신자를 지정하더라도 각 시대마다 클라이언트가 해석하는 주소와 실제 접속 대상이 달라집니다"
)

# 3개 시대 열(Column) 좌표 설정
CW = 280
CGAP = 36
X0 = 24
X1 = X0 + CW + CGAP      # 340
X2 = X1 + CW + CGAP      # 656
COLS = [X0, X1, X2]

Y_TOP = 104
CARD_H = 376

# 시대별 카드 배경 (Col 3은 focal ACC 톤)
d.box(X0, Y_TOP, CW, CARD_H, PAPER2, RULE, 1.0, 8)
d.box(X1, Y_TOP, CW, CARD_H, PAPER2, RULE, 1.0, 8)
d.tone(X2, Y_TOP, CW, CARD_H, ACC, r=8, op="12", sw=1.4)

# 1. 열 헤더 (시대 구분)
def draw_col_header(x, title, sub, color):
    d.t(x + CW // 2, Y_TOP + 24, title, 14, INK, KR, "middle", 600)
    d.t(x + CW // 2, Y_TOP + 42, sub, 12, color, MONO, "middle", 600)

draw_col_header(X0, "시대 1 · 호스트 직접 지정", "1970년대 · 1-HOP DIRECT", INFO)
draw_col_header(X1, "시대 2 · 소스 라우트", "RFC 821 §3.6 (1982)", WARN)
draw_col_header(X2, "시대 3 · DNS MX 동적 조회", "RFC 974 / RFC 5321", ACC)

# 열 사이 진화 화살표
d.arrow([(X0 + CW + 4, Y_TOP + 28), (X1 - 4, Y_TOP + 28)], MUTED, "ar", 1.4)
d.arrow([(X1 + CW + 4, Y_TOP + 28), (X2 - 4, Y_TOP + 28)], ACC, "acc", 1.4)

# 2. 슬롯 1: 수신 주소 표기 (Y = 160)
Y_S1 = 160
d.box(X0 + 12, Y_S1, CW - 24, 46, PAPER, RULE, 0.8, 4)
d.t(X0 + CW // 2, Y_S1 + 16, "수신 주소 표기", 11, SOFT, KR, "middle")
d.t(X0 + CW // 2, Y_S1 + 34, "bob@delta", 12, INK, MONO, "middle", 600)

d.box(X1 + 12, Y_S1, CW - 24, 46, PAPER, RULE, 0.8, 4)
d.t(X1 + CW // 2, Y_S1 + 16, "수신 주소 표기", 11, SOFT, KR, "middle")
d.t(X1 + CW // 2, Y_S1 + 34, "@alpha,@beta:bob@delta", 11, WARN, MONO, "middle", 600)

d.box(X2 + 12, Y_S1, CW - 24, 46, PAPER, ACC, 0.9, 4)
d.t(X2 + CW // 2, Y_S1 + 16, "수신 주소 표기", 11, SOFT, KR, "middle")
d.t(X2 + CW // 2, Y_S1 + 34, "bob@delta.arpa", 12, ACC, MONO, "middle", 600)

# 3. 슬롯 2: 접속 대상 해석 (Y = 218)
Y_S2 = 218
d.box(X0 + 12, Y_S2, CW - 24, 52, PAPER, RULE, 0.8, 4)
d.t(X0 + CW // 2, Y_S2 + 16, "1차 접속 대상", 11, SOFT, KR, "middle")
d.t(X0 + CW // 2, Y_S2 + 34, "delta 호스트 IP 직접 연결", 13, INK, KR, "middle")

d.box(X1 + 12, Y_S2, CW - 24, 52, PAPER, RULE, 0.8, 4)
d.t(X1 + CW // 2, Y_S2 + 16, "1차 접속 대상", 11, SOFT, KR, "middle")
d.t(X1 + CW // 2, Y_S2 + 34, "경로 맨 앞 alpha 호스트", 13, WARN, KR, "middle")

d.box(X2 + 12, Y_S2, CW - 24, 52, PAPER, RULE, 0.8, 4)
d.t(X2 + CW // 2, Y_S2 + 16, "1차 접속 대상", 11, SOFT, KR, "middle")
d.t(X2 + CW // 2, Y_S2 + 34, "MX 1순위 mx1.delta.arpa", 13, OK, KR, "middle")

# 4. 슬롯 3: 홉별 전달 메커니즘 (Y = 282)
Y_S3 = 282
# Col 1
d.box(X0 + 12, Y_S3, CW - 24, 96, PAPER, RULE, 0.8, 4)
d.t(X0 + CW // 2, Y_S3 + 18, "메일 전달 메커니즘", 11, SOFT, KR, "middle")
d.t(X0 + CW // 2, Y_S3 + 42, "송신자 → delta", 12, INK, MONO, "middle")
d.t(X0 + CW // 2, Y_S3 + 64, "단일 홉 직접 전송", 13, MUTED, KR, "middle")
d.t(X0 + CW // 2, Y_S3 + 84, "중계 및 우회 경로 없음", 13, MUTED, KR, "middle")

# Col 2
d.box(X1 + 12, Y_S3, CW - 24, 96, PAPER, RULE, 0.8, 4)
d.t(X1 + CW // 2, Y_S3 + 18, "메일 전달 메커니즘", 11, SOFT, KR, "middle")
d.t(X1 + CW // 2, Y_S3 + 42, "송신자 → alpha 인계", 12, INK, MONO, "middle")
d.t(X1 + CW // 2, Y_S3 + 64, "alpha → beta (경로 축소)", 12, MUTED, MONO, "middle")
d.t(X1 + CW // 2, Y_S3 + 84, "beta → delta 배달", 12, MUTED, MONO, "middle")

# Col 3
d.box(X2 + 12, Y_S3, CW - 24, 96, PAPER, RULE, 0.8, 4)
d.t(X2 + CW // 2, Y_S3 + 18, "메일 전달 메커니즘", 11, SOFT, KR, "middle")
d.t(X2 + CW // 2, Y_S3 + 42, "송신자 → DNS MX 질의", 13, INK, KR, "middle")
d.t(X2 + CW // 2, Y_S3 + 64, "우선순위 10 mx1 연결", 12, OK, MONO, "middle")
d.t(X2 + CW // 2, Y_S3 + 84, "장애 시 20 mx2 폴백", 12, ACC, MONO, "middle")

# 5. 슬롯 4: 특성 및 결과 (Y = 390)
Y_S4 = 390
d.box(X0 + 12, Y_S4, CW - 24, 76, PAPER, WARN, 0.8, 4)
d.t(X0 + CW // 2, Y_S4 + 22, "핵심 한계", 11, WARN, KR, "middle", 600)
d.t(X0 + CW // 2, Y_S4 + 44, "상대 호스트 상시 가동 필수", 13, INK, KR, "middle")
d.t(X0 + CW // 2, Y_S4 + 62, "이종 네트워크 전달 불가", 13, MUTED, KR, "middle")

d.box(X1 + 12, Y_S4, CW - 24, 76, PAPER, WARN, 0.8, 4)
d.t(X1 + CW // 2, Y_S4 + 22, "핵심 한계", 11, WARN, KR, "middle", 600)
d.t(X1 + CW // 2, Y_S4 + 44, "발송자가 전체 망 경로 숙지", 13, INK, KR, "middle")
d.t(X1 + CW // 2, Y_S4 + 62, "경로 해석 혼란 및 단절 위험", 13, MUTED, KR, "middle")

d.tone(X2 + 12, Y_S4, CW - 24, 76, OK, r=4, op="14", sw=1.0)
d.t(X2 + CW // 2, Y_S4 + 22, "해결된 구조", 11, OK, KR, "middle", 600)
d.t(X2 + CW // 2, Y_S4 + 44, "도메인과 수신 호스트 분리", 13, INK, KR, "middle")
d.t(X2 + CW // 2, Y_S4 + 62, "부하 분산 및 고가용성 보장", 13, OK, KR, "middle")

# 범례
d.legend(H - 42, [
    ("직접 연결 시대", INFO),
    ("경로 지정 및 제약", WARN),
    ("동적 조회 혁신 (현행)", ACC),
    ("해결 및 정상 전달", OK),
])

out = Path(__file__).parent.parent / "01-01.routing-evolution.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")
