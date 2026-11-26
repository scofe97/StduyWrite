# 사실 출처: htpasswd -nbB -C 10 3회 실측 · BCrypt 더미 해시 비교 원리
# 타입 스펙: type-bar
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 500
d = D(
    W, H,
    "BAR · RESPONSE TIMING",
    "경우별 로그인 실패 응답 시간",
    "없는 이메일에서 해시 비교를 건너뛸 때와 가짜 해시를 비교할 때의 응답 시간 차이",
    "BCrypt 해시 연산 유무에 따른 응답 지연 분석"
)

# 차트 영역 설정
X0 = 290
X_MAX = 850
Y_BASE = 330
TICKS = [0, 10, 20, 30, 40, 50, 60]

def x_val(ms):
    return X0 + int((ms / 60.0) * (X_MAX - X0))

# 눈금선 (그리드)
for ms in TICKS:
    x = x_val(ms)
    d.line(x, 120, x, Y_BASE, "rgba(191,192,192,0.12)", 0.8)
    unit = "ms" if ms == 60 else ""
    lab = f"{ms}{unit}"
    d.t(x, Y_BASE + 18, lab, 10, MUTED, MONO, "middle")

# X축 베이스라인
d.line(X0, Y_BASE, X_MAX, Y_BASE, RULE, 1.0)
d.t((X0 + X_MAX) / 2, Y_BASE + 34, "응답 시간 (ms)", 11, SOFT, KR, "middle")

# 데이터 막대 3종
# 1. 없는 이메일 · 비교 건너뜀 (수 ms · BAD)
y1 = 140
h_bar = 28
d.t(X0 - 16, y1 + 19, "없는 이메일 · 비교 건너뜀", 12, INK, KR, "end", 600)
# 수 ms는 매우 짧은 막대 (약 2ms 폭)
w1 = max(14, int((2 / 60.0) * (X_MAX - X0)))
d.tone(X0, y1, w1, h_bar, BAD, r=4, op="22", sw=1.2)
d.t(X0 + w1 + 10, y1 + 19, "수 ms · 개략", 11, BAD, KR, "start")

# 1과 2 사이 시간 차 표시 (ACC)
y_diff = 186
x_end1 = X0 + w1
x_end2 = x_val(50)
cx_chip = (x_end1 + x_end2) / 2
chip_w = 170
d.line(x_end1, y1 + h_bar + 2, x_end1, y_diff, RULE, 0.8, dash="2 2")
d.line(x_end2, y1 + h_bar + 2, x_end2, y_diff, RULE, 0.8, dash="2 2")
d.line(x_end1, y_diff, cx_chip - chip_w / 2, y_diff, ACC, 1.0, dash="3 3")
d.line(cx_chip + chip_w / 2, y_diff, x_end2, y_diff, ACC, 1.0, dash="3 3")
d.chip(cx_chip, y_diff, "시간 차 = 계정 존재 신호", ACC, 11)

# 2. 있는 이메일 · 틀린 비밀번호 (약 50ms · INFO)
y2 = 214
d.t(X0 - 16, y2 + 19, "있는 이메일 · 틀린 비밀번호", 12, INK, KR, "end", 600)
w2 = x_val(50) - X0
d.tone(X0, y2, w2, h_bar, INFO, r=4, op="22", sw=1.2)
d.t(X0 + w2 + 10, y2 + 19, "약 50ms", 11, INFO, MONO, "start")

# 3. 없는 이메일 · 가짜 해시 비교 (약 50ms · OK)
y3 = 268
d.t(X0 - 16, y3 + 19, "없는 이메일 · 가짜 해시 비교", 12, INK, KR, "end", 600)
w3 = x_val(50) - X0
d.tone(X0, y3, w3, h_bar, OK, r=4, op="22", sw=1.2)
d.t(X0 + w3 + 10, y3 + 19, "약 50ms", 11, OK, MONO, "start")

# 바닥 주석
d.t(X0 - 16, 396, "BCrypt 강도 10, 개발 PC 실측 0.05~0.06초 · 기기마다 다름", 11, MUTED, KR, "start")

# 범례
d.legend(H - 44, [
    ("취약 (단축 지연)", BAD),
    ("비교 기준 지연", INFO),
    ("보호 (동일 지연)", OK),
    ("탐지 신호", ACC),
])

out_path = Path(__file__).parent.parent / "03-01.timing.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")
