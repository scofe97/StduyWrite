# 08-02 §2 — Go HTTP 클라이언트 연결 재사용과 본문 소진 루프
# 사실 출처: NPG Ch.8 Listing 8-2, 8-3 (p.156-159) · net/http Response.Body 공식 문서
# 타입 스펙: type-loop — 본문 소진과 닫기를 거쳐 유휴 풀로 돌아오는 고리와 미소진 폐기 갈래
import sys, os, math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 620
d = D(W, H, "NPG CHAPTER 8 · HTTP CLIENTS",
      "HTTP 커넥션 재사용과 본문 소진 루프",
      "응답 본문을 끝까지 읽고 닫아야 TCP 연결이 유휴 풀로 돌아와 다음 요청에 재사용됩니다. "
      "본문을 읽지 않고 닫으면 세션을 재사용하지 못할 수 있어 다음 요청은 새 핸드셰이크를 거쳐야 합니다.",
      "녹색 고리가 세션 재사용 경로이고 붉은 갈래가 재사용 실패 위험 경로입니다")

CX, CY, R = 280, 320, 172
SW, SH = 150, 48
HW, HH = 148, 72
N = 5

stations = [
    ("요청 전송", "http.Client.Do", False),
    ("응답 수신", "상태 코드 · 헤더 파싱", False),
    ("본문 전체 소진", "io.Copy(io.Discard)", True),
    ("응답 본문 닫기", "resp.Body.Close()", False),
    ("유휴 풀 반환", "TCP 세션 유휴 풀 보관", False),
]

def theta(k):
    return math.radians(-90 + k * (360 / N))

def center(k):
    a = theta(k)
    return (round((CX + R * math.cos(a)) / 4) * 4, round((CY + R * math.sin(a)) / 4) * 4)

def box_rect(k):
    cx, cy = center(k)
    return (cx - SW / 2, cy - SH / 2, cx + SW / 2, cy + SH / 2)

def circle_box_intersections(k):
    x1, y1, x2, y2 = box_rect(k)
    pts = []
    for x in (x1, x2):
        d2 = R**2 - (x - CX)**2
        if d2 >= 0:
            dy = math.sqrt(d2)
            for y in (CY - dy, CY + dy):
                if y1 - 1e-4 <= y <= y2 + 1e-4:
                    pts.append((x, y))
    for y in (y1, y2):
        d2 = R**2 - (y - CY)**2
        if d2 >= 0:
            dx = math.sqrt(d2)
            for x in (CX - dx, CX + dx):
                if x1 - 1e-4 <= x <= x2 + 1e-4:
                    pts.append((x, y))
    uniq = []
    for p in pts:
        if not any(math.hypot(p[0]-u[0], p[1]-u[1]) < 0.1 for u in uniq):
            uniq.append(p)
    th = theta(k)
    def rel_angle(p):
        a = math.atan2(p[1] - CY, p[0] - CX)
        return (a - th + math.pi) % (2 * math.pi) - math.pi
    uniq.sort(key=rel_angle)
    return uniq

# 링 원형 호 (A R R 0 0 1) — 상자 경계에서 출발하여 다음 상자 경계에 정확히 닿음
for k in range(N):
    nxt = (k + 1) % N
    pts_k = circle_box_intersections(k)
    pts_nxt = circle_box_intersections(nxt)
    x1, y1 = pts_k[1]
    x2_raw, y2_raw = pts_nxt[0]
    
    phi_entry = math.atan2(y2_raw - CY, x2_raw - CX)
    phi_end = phi_entry - 2.2 / R
    x2 = CX + R * math.cos(phi_end)
    y2 = CY + R * math.sin(phi_end)
    
    color = OK if k in (2, 3, 4) else MUTED
    m = "ok" if k in (2, 3, 4) else "ar"
    d.path(f"M {x1:.1f} {y1:.1f} A {R} {R} 0 0 1 {x2:.1f} {y2:.1f}", color, 1.4, m=m)

# 허브 상자
d.box(CX - HW / 2, CY - HH / 2, HW, HH, PAPER, INFO, 1.2, 8)
d.t(CX, CY - 14, "Transport 유휴 풀", 14, INFO, KR, "middle", 600)
d.t(CX, CY + 8, "net/http keep-alive", 12, MUTED, MONO)
d.t(CX, CY + 26, "유휴 커넥션 캐시", 12, SOFT, KR)

# 스포크 1: Station 4 -> 허브 (풀 반환)
d.path("M 191 276 L 204 295", OK, 1.2, m="ok", dash="5 4")

# 스포크 2: 허브 -> Station 0 (재사용 대여)
d.path(f"M {CX} 284 L {CX} 175", INFO, 1.2, m="info", dash="5 4")

# 루프 정거장들 그리기
for k, (name, sub, focal) in enumerate(stations):
    cx, cy = center(k)
    if focal:
        d.tone(cx - SW / 2, cy - SH / 2, SW, SH, OK, 6, "12", 1.4)
    else:
        d.box(cx - SW / 2, cy - SH / 2, SW, SH, PAPER2, RULE, 1.0)
    d.t(cx, cy - 6, name, 13, OK if focal else INK, KR, "middle", 600)
    d.t(cx, cy + 14, sub, 12, MUTED, MONO if "(" in sub else KR)

# 미소진 종료 갈래 (오른쪽 분기)
s1x, s1y = center(1)
BX = 716
BY = 268
BW, BH = 216, 54

# Station 1 에서 오른쪽으로 분기
d.path(f"M {s1x + SW / 2} {s1y} L {BX - BW / 2 - 2} {BY}", BAD, 1.3, m="bad", dash="4 4")
d.t((s1x + SW / 2 + BX - BW / 2) / 2, s1y - 10, "미소진 닫기", 12, BAD, KR, "middle", 600)

d.tone(BX - BW / 2, BY - BH / 2, BW, BH, BAD, 6, "12", 1.2)
d.t(BX, BY - 6, "재사용 못 할 수 있음", 13, BAD, KR, "middle", 600)
d.t(BX, BY + 14, "다음 요청은 새 연결·핸드셰이크", 12, MUTED, KR)

# 범례
d.legend(566, [
    ("정상 소진 (세션 재사용)", OK),
    ("유휴 풀 연결 흐름", INFO),
    ("미소진 종료 (재사용 불가 위험)", BAD)
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "08-02.conn-reuse.svg"))
d.save(out)
print(f"saved: {out}")
