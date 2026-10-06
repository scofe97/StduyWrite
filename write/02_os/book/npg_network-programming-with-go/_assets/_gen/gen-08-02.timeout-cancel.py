# 08-02 §3 — Go HTTP 클라이언트 타임아웃과 context 데드라인 만료 타임라인
# 사실 출처: NPG Ch.8 Listing 8-4, 8-5 (p.159-161)
# 타입 스펙: type-timeline — 시간 축 위의 사건들과 데드라인 만료가 논지다.
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 540
d = D(W, H, "NPG CHAPTER 8 · HTTP CLIENTS",
      "HTTP 요청 타임아웃과 context 데드라인 만료 타임라인",
      "서버가 select {} 로 응답하지 않아도 5초 데드라인에 도달하면 클라이언트는 context.DeadlineExceeded 로 깨어납니다. "
      "기본 클라이언트는 타임아웃이 없어 영구 블로킹에 빠집니다.",
      "가로축은 초 단위 실제 경과 시간입니다")

X0 = 216
PX = 74

def X(t):
    return X0 + int(t * PX)

Y1 = 170
Y2 = 300
Y_AXIS = 430

# 배경 시간 보조선
for t in range(7):
    d.line(X(t), 136, X(t), Y_AXIS, RULE, 0.6, dash="2 4")

# 기준 시간축
d.line(X(0), Y_AXIS, X(6) + 30, Y_AXIS, RULE, 1.0)
for t in range(7):
    x = X(t)
    d.line(x, Y_AXIS, x, Y_AXIS + 6, RULE, 1.0)
    d.t(x, Y_AXIS + 20, f"{t}s", 12, SOFT, MONO)

# ── 위 행: 기본 클라이언트 (http.Get, 데드라인 없음) ──
d.t(X0 - 14, Y1 - 6, "기본 클라이언트", 13, INK, KR, "end", 600)
d.t(X0 - 14, Y1 + 14, "http.Get · 데드라인 없음", 12, MUTED, MONO, "end")

# 시작 시점 (t = 0s)
d.o.append(f'<circle cx="{X(0)}" cy="{Y1}" r="4" fill="{INFO}" stroke="{PAPER}" stroke-width="1.2"/>')

# 0s ~ 5s: 서버 select {} 무응답 침묵 대기 구간
d.tone(X(0), Y1 - 18, X(5) - X(0), 36, WARN, 4, "12", 1.0)
d.t((X(0) + X(5)) / 2, Y1 + 4, "서버 핸들러 select {} 무응답 침묵 대기 (데드라인 없음)", 12, WARN, KR, "middle", 600)

# 5s ~ 6s: 끝없이 이어지는 막대 (영구 대기)
d.tone(X(5), Y1 - 18, X(6) - X(5), 36, BAD, 4, "12", 1.0)
d.t((X(5) + X(6)) / 2, Y1 + 4, "영구 대기", 12, BAD, KR, "middle", 600)

# 끝에 go test -timeout 이 멈춤
d.path(f"M {X(6)} {Y1} L {X(6) + 12} {Y1}", BAD, 1.2, m="bad")
BW1, BH1 = 176, 44
bx1 = X(6) + 14
d.tone(bx1, Y1 - 22, BW1, BH1, BAD, 6, "12", 1.2)
d.t(bx1 + BW1 / 2, Y1 - 4, "기본 클라이언트 무한 대기", 12, BAD, KR, "middle", 600)
d.t(bx1 + BW1 / 2, Y1 + 14, "go test -timeout 강제 중단", 11, MUTED, KR)

# ── 아래 행: context 클라이언트 (NewRequestWithContext, 5초 타임아웃) ──
d.t(X0 - 14, Y2 - 6, "context 클라이언트", 13, INK, KR, "end", 600)
d.t(X0 - 14, Y2 + 14, "NewRequestWithContext (5초)", 11, MUTED, MONO, "end")

# 시작 시점 (t = 0s)
d.o.append(f'<circle cx="{X(0)}" cy="{Y2}" r="4" fill="{INFO}" stroke="{PAPER}" stroke-width="1.2"/>')

# 0s ~ 5s: 서버 select {} 무응답 침묵 대기 구간
d.tone(X(0), Y2 - 18, X(5) - X(0), 36, WARN, 4, "12", 1.0)
d.t((X(0) + X(5)) / 2, Y2 + 4, "서버 핸들러 select {} 무응답 침묵 대기 (5초 블로킹)", 12, WARN, KR, "middle", 600)

# 5.0s 데드라인 만료 마일스톤 (상단 라벨)
d.line(X(5), Y2 - 18, X(5), Y2 - 46, ACC, 1.2)
d.o.append(f'<circle cx="{X(5)}" cy="{Y2}" r="6" fill="{ACC}" stroke="{PAPER}" stroke-width="1.5"/>')
d.t(X(5), Y2 - 66, "5초 데드라인 만료", 13, ACC, KR, "middle", 600)
d.t(X(5), Y2 - 50, "context 기한 초과 신호 발생", 12, MUTED, KR)

# 5.0s Do 오류 반환 녹색 상자 (하단 라벨)
d.path(f"M {X(5)} {Y2 + 18} L {X(5)} {Y2 + 42}", OK, 1.2, m="ok")
BW2, BH2 = 240, 46
bx2 = X(5) - BW2 / 2
by2 = Y2 + 44
d.tone(bx2, by2, BW2, BH2, OK, 6, "12", 1.2)
d.t(X(5), by2 + 19, "클라이언트 Do(req) 오류 반환", 13, OK, KR, "middle", 600)
d.t(X(5), by2 + 37, "errors.Is(err, DeadlineExceeded)", 11, MUTED, MONO)

# 범례
d.legend(486, [
    ("5초 기한 만료", ACC),
    ("요청 시작 시점", INFO),
    ("정상 에러 반환", OK),
    ("서버 무응답 대기", WARN),
    ("무한 블로킹", BAD)
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "08-02.timeout-cancel.svg"))
d.save(out)
print(f"saved: {out}")
