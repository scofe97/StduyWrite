# 01-03.packet-journey — 3 기둥 + 빈 칸이 요점
# 본문: "가운데 기둥에 Transport·Application 칸이 비어 있는 것이 이 그림의 요점이다.
#        라우터는 IP 헤더까지만 읽고 그 위는 화물로 넘기므로 포트도 HTTP 도 볼 일이 없다."
# 타입 스펙: type-layers.md — 계층은 위에서 아래로, 같은 계층은 기둥을 가로질러 같은 높이.
#           높이·폭 범위 안에서 고정하고 stride 는 4 의 배수.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 664
d = D(W, H, "ONE PACKET · FULL STACK JOURNEY",
      "패킷 하나의 전 계층 여정 — 라우터는 L3 까지만 올라온다",
      "가운데 기둥에 Application·Transport 칸이 없는 것이 이 그림의 요점이다. 괄호는 그 자리에서의 PDU 이름이다.",
      lead="가운데 기둥에 Application·Transport 칸이 없는 것이 요점 · 괄호는 그 자리의 PDU 이름")

CY   = [212, 296, 380, 472]                    # Application · Transport · Network · Link
BW, BH = 176, 64
L, M, R = 168, 500, 832
HALF = BW // 2

ddx.band(d, 104, 596, "양 끝은 끝까지 올라가고 라우터는 L3 에서 멈춘다")
for cx, t in zip([L, M, R], ["출발 호스트", "중간 라우터", "목적 호스트"]):
    d.t(cx, 156, t, 13, INK, KR, "middle", 600)

def cell(cx, cy, title, sub, tag, c=None, w=BW):
    x, y = cx - w // 2, cy - BH // 2
    d.box(x, y, w, BH, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 10, ddx.fit(title, 12, w - 20, title), 12, c or INK, KR, "middle", 600)
    d.t(cx, cy + 8,  ddx.fit(sub, 11, w - 20, sub), 11, MUTED, KR)
    ascii_only = all(ord(ch) < 128 for ch in tag)
    d.t(cx, cy + 26, tag, 9 if ascii_only else 10, SOFT, MONO if ascii_only else KR)

# ── 출발 호스트 — 내려가며 감싼다 ──────────────────────────
for cy, (t, s, g) in zip(CY, [("Application", "HTTP GET 을 만든다", "DATA"),
                              ("Transport", "TCP 헤더 · 포트", "SEGMENT"),
                              ("Network", "IP 헤더 · 주소", "PACKET"),
                              ("Link", "Ethernet · MAC", "FRAME")]):
    cell(L, cy, t, s, g)
for a, b in zip(CY, CY[1:]):
    d.path(f"M {L} {a+BH//2+4} L {L} {b-BH//2-10}", MUTED, 1.4, m="ar")

# ── 목적 호스트 — 올라가며 벗긴다 ──────────────────────────
for cy, (t, s, g) in zip(CY, [("Application", "cURL 이 받는다", "IP 는 이미 없다"),
                              ("Transport", "포트로 소켓 판별", "SEGMENT 해제"),
                              ("Network", "내 IP 인지 확인", "PACKET 해제"),
                              ("Link", "MAC 을 벗긴다", "FRAME 해제")]):
    cell(R, cy, t, s, g, OK if t == "Application" else None)
for a, b in zip(CY[1:], CY):
    d.path(f"M {R} {a-BH//2-4} L {R} {b+BH//2+10}", MUTED, 1.4, m="ar")

# ── 중간 라우터 — 위 두 칸이 비어 있다 (focal) ─────────────
ey0, ey1 = CY[0] - BH // 2, CY[1] + BH // 2
d.o.append(f'<rect x="{M-136}" y="{ey0}" width="272" height="{ey1-ey0}" rx="8" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="7 6"/>')
d.t(M, CY[0] + 24, "여기는 열리지 않는다", 13, ACC, KR, "middle", 600)
d.t(M, CY[1] - 24, "Application · Transport 칸이 없다", 12, ACC, KR)
d.t(M, CY[1] + 0, "포트도 HTTP 도 볼 일이 없다", 11, MUTED, KR)

cell(M, CY[2], "Network", "IP 로 다음 홉", "L3 · 여기가 천장", INFO)
cell(M - 70, CY[3], "Link 수신", "MAC 을 벗긴다", "L2", w=132)
cell(M + 70, CY[3], "Link 송신", "새 MAC 을 쓴다", "L2", w=132)
d.path(f"M {M-70} {CY[3]-BH//2-4} L {M-70} {CY[2]+BH//2+10}", INFO, 1.4, m="info")
d.path(f"M {M+70} {CY[2]+BH//2+4} L {M+70} {CY[3]-BH//2-10}", INFO, 1.4, m="info")

# ── 기둥 사이 — 프레임은 홉마다 새로 만들어진다 ────────────
d.path(f"M {L+HALF+8} {CY[3]} L {M-136-10} {CY[3]}", MUTED, 1.5, m="ar")
d.t((L + HALF + M - 136) // 2, CY[3] - 14, "프레임", 11, MUTED, KR)
d.path(f"M {M+136+8} {CY[3]} L {R-HALF-10} {CY[3]}", MUTED, 1.5, m="ar")
d.t((M + 136 + R - HALF) // 2, CY[3] - 14, "새 프레임", 11, MUTED, KR)

d.t(36, 570, "라우터가 IP 헤더까지만 읽는다는 사실이 세로로 잘린 기둥 하나로 드러난다 — "
             "MAC 은 매 홉 새로 쓰이고 IP 는 끝까지 그대로다", 12, MUTED, KR, "start")
d.legend(616, [("L3 가 천장", INFO), ("도착", OK), ("열리지 않는 칸", ACC)])
d.save("01-03.packet-journey.svg")
print("ok packet-journey")
