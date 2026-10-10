# 타입 스펙: type-line — persist 타이머 만료 간격의 지수적 백오프 증가 곡선.
# 사실 출처: 원서 §15.5.3.1 실험 실측치 — 패킷 8(5.160s) win 0 수신 후, 패킷 9(6.970s, 직전 대비 1.810s 약 2s), 패킷 11(10.782s, 직전 대비 3.812s 약 4s), 패킷 13(18.408s, 직전 대비 7.626s 약 8s).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 430
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-02 §2",
      "persist 타이머의 지수적 백오프 간격 증가",
      "0 창 상태가 지속되면 persist 타이머는 직전 탐침 대비 약 2초, 4초, 8초로 만료 간격을 두 배씩 늘린다. 재전송 타이머와 마찬가지로 망에 과도한 탐침 부하를 주지 않도록 지수 백오프를 적용한다.",
      "직전 대비 간격이 2초·4초·8초로 지수 백오프되어 망 부하를 줄입니다")

X_ORIGIN, Y_ORIGIN = 140, 320
X_LEN, Y_LEN = 680, 190

# 축 그리기
d.line(X_ORIGIN, Y_ORIGIN, X_ORIGIN + X_LEN, Y_ORIGIN, RULE, 1.2)
d.line(X_ORIGIN, Y_ORIGIN, X_ORIGIN, Y_ORIGIN - Y_LEN, RULE, 1.2)

d.t(X_ORIGIN - 10, Y_ORIGIN - Y_LEN - 12, "간격(초)", 12, MUTED, KR, "middle")
d.t(X_ORIGIN + X_LEN, Y_ORIGIN + 28, "탐침 회차 →", 12, MUTED, KR, "end")

# Y 축 눈금 (0s, 2s, 4s, 6s, 8s, 10s)
for sec in range(0, 11, 2):
    y_pos = Y_ORIGIN - (sec / 10.0) * Y_LEN
    d.line(X_ORIGIN - 6, y_pos, X_ORIGIN, y_pos, RULE, 0.8)
    d.t(X_ORIGIN - 12, y_pos + 4, f"{sec}s", 11, SOFT, MONO, "end")
    if sec > 0:
        d.line(X_ORIGIN, y_pos, X_ORIGIN + X_LEN, y_pos, RULE, 0.5, dash="3 5")

# 데이터 포인트: (회차, 간격값, 시각라벨, 서브라벨, 칩 cx_offset, 칩 cy_offset)
points = [
    (1, 1.81, "1회차 (6.970s)", "간격 ~2초", 0, -42),
    (2, 3.81, "2회차 (10.782s)", "간격 ~4초", -40, -48),
    (3, 7.63, "3회차 (18.408s)", "간격 ~8초", 0, -44),
]

coords = []
x_step = X_LEN / 4.0
for n, val, label, sub, ox, oy in points:
    px = X_ORIGIN + n * x_step
    py = Y_ORIGIN - (val / 10.0) * Y_LEN
    coords.append((px, py))
    # X축 수직 보조선 및 눈금
    d.line(px, Y_ORIGIN, px, py, RULE, 0.6, dash="2 3")
    d.line(px, Y_ORIGIN, px, Y_ORIGIN + 6, RULE, 0.8)
    d.t(px, Y_ORIGIN + 22, f"{n}회 탐침", 12, INK, KR, "middle", 500)

# 선 연결
for i in range(len(coords) - 1):
    d.line(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1], ACC, 2.0)

# 포인트 칩 및 지시선
for i, (n, val, label, sub, ox, oy) in enumerate(points):
    px, py = coords[i]
    cx = px + ox
    cy = py + oy
    # 점과 칩 연결 지시선 (칩 박스 외곽에서 멈춤)
    d.line(px, py - 6, cx, cy + 12, ACC, 0.9, dash="2 2")
    # 점 그리기
    d.o.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{ACC}" stroke="{PAPER}" stroke-width="2"/>')
    # 칩 배치
    d.chip(cx, cy, f"{val:.2f}s ({sub})", ACC, 11)

d.legend(H - 46, [("실측 직전 대비 탐침 간격 (지수 백오프)", ACC)])
d.save("15-02.persist-backoff.svg")
