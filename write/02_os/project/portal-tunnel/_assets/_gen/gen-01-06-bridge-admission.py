# 타입 스펙: type-flowchart
# 사실 출처: portal/server.go:889,917,1034, portal/lease.go:201,232,271, portal/proxy.go:27,100, docs/maintainer/architecture.md
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 960
d = D(W, H, "PORTAL-TUNNEL · PUBLIC CONNECTION ADMISSION & BRIDGE FLOW",
      "공개 연결 인입부터 TCP 브리지 활성화까지의 다단계 관문",
      "검사 대기 슬롯(128)과 테넌트 예산(1024), 임대별 브리지 한도(128) 및 리버스 대기 후 재검증 흐름",
      lead="입장(admit)과 활성화(activate) 사이 10초 대기 중 발생할 수 있는 임대 취소를 2단계 검증으로 방어합니다")

def oval(x, y, w, h, fill=PAPER2, stroke=RULE, sw=1.2):
    r = h // 2
    d.box(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=r)

def diamond_path(cx, cy, w, h):
    return f"M {cx} {cy - h//2} L {cx + w//2} {cy} L {cx} {cy + h//2} L {cx - w//2} {cy} Z"

def draw_diamond(cx, cy, w, h, fill=PAPER2, stroke=RULE, sw=1.2):
    d.o.append(f'<path d="{diamond_path(cx, cy, w, h)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

cx = 360  # 주 흐름 중심선

# 1. Start Oval
s_y = 104
oval(cx - 120, s_y, 240, 38, fill=PAPER2, stroke=INFO, sw=1.4)
d.t(cx, s_y + 16, "PUBLIC TCP INGRESS", 9, INFO, MONO, "middle", 600)
d.t(cx, s_y + 30, "공개 TCP 연결 인입 (:443 기본)", 11, INK, KR, "middle", 600)

# Arrow: Start -> D1
d.arrow([(cx, s_y + 38), (cx, 164)], c=INFO, m="info", sw=1.4)

# 2. Decision 1: 검사 슬롯 가용 여부 (inspecting < 128)
d1_cy = 196
draw_diamond(cx, d1_cy, 240, 64, stroke=INFO)
d.t(cx, d1_cy - 7, "검사 슬롯 가용?", 11, INK, KR, "middle", 600)
d.t(cx, d1_cy + 9, "inspecting < 128", 10, MUTED, MONO, "middle")

# D1 -> Reject 1 (Right)
d.arrow([(cx + 120, d1_cy), (670, d1_cy)], c=BAD, m="bad", sw=1.4)
d.t(cx + 145, d1_cy - 8, "No", 10, BAD, MONO, "middle", 600)
oval(670, d1_cy - 18, 200, 36, fill=PAPER2, stroke=BAD, sw=1.2)
d.t(770, d1_cy + 4, "연결 닫힘 (HTTP 응답 없음)", 11, BAD, KR, "middle", 600)

# D1 -> Step 1 (Down)
d.arrow([(cx, d1_cy + 32), (cx, 252)], c=INFO, m="info", sw=1.4)
d.t(cx + 18, d1_cy + 45, "Yes", 10, OK, MONO, "middle", 600)

# 3. Step 1: SNI ClientHello 검사
s1_y = 252
d.box(cx - 130, s1_y, 260, 42, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(cx, s1_y + 18, "SNI ClientHello 검사 (≤2초)", 11, INK, KR, "middle", 600)
d.t(cx, s1_y + 34, "ClientHello 피크 검사", 11, MUTED, KR, "middle")

# Step 1 -> Step 2
d.arrow([(cx, s1_y + 42), (cx, 318)], c=INFO, m="info", sw=1.4)

# 4. Step 2: Lookup(host)
s2_y = 318
d.box(cx - 130, s2_y, 260, 42, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(cx, s2_y + 18, "Lookup(host) 호스트 검색", 11, INK, KR, "middle", 600)
d.t(cx, s2_y + 34, "정규 호스트 및 별칭 매칭", 11, MUTED, KR, "middle")

# Step 2 -> D2
d.arrow([(cx, s2_y + 42), (cx, 382)], c=INFO, m="info", sw=1.4)

# 5. Decision 2: 임대 발견 & Routable
d2_cy = 414
draw_diamond(cx, d2_cy, 240, 64, stroke=WARN)
d.t(cx, d2_cy - 7, "임대 존재 & Routable?", 11, INK, KR, "middle", 600)
d.t(cx, d2_cy + 9, "isRoutable 확인", 11, MUTED, KR, "middle")

# D2 -> Reject 2 (Right)
d.arrow([(cx + 120, d2_cy), (670, d2_cy)], c=BAD, m="bad", sw=1.4)
d.t(cx + 145, d2_cy - 8, "No", 10, BAD, MONO, "middle", 600)
oval(670, d2_cy - 18, 200, 36, fill=PAPER2, stroke=BAD, sw=1.2)
d.t(770, d2_cy + 4, "연결 닫힘 (HTTP 응답 없음)", 11, BAD, KR, "middle", 600)

# D2 -> D3 (Down)
d.arrow([(cx, d2_cy + 32), (cx, 468)], c=OK, m="ok", sw=1.4)
d.t(cx + 18, d2_cy + 45, "Yes", 10, OK, MONO, "middle", 600)

# 6. Decision 3: 브리지 예산 가용 여부
d3_cy = 500
draw_diamond(cx, d3_cy, 240, 64, stroke=WARN)
d.t(cx, d3_cy - 7, "브리지 예산 가용?", 11, INK, KR, "middle", 600)
d.t(cx, d3_cy + 9, "임대 128 · 서버 1024", 11, MUTED, KR, "middle")

# D3 -> Reject 3 (Right)
d.arrow([(cx + 120, d3_cy), (670, d3_cy)], c=BAD, m="bad", sw=1.4)
d.t(cx + 145, d3_cy - 8, "No", 10, BAD, MONO, "middle", 600)
oval(670, d3_cy - 18, 200, 36, fill=PAPER2, stroke=BAD, sw=1.2)
d.t(770, d3_cy + 4, "연결 닫힘 (HTTP 응답 없음)", 11, BAD, KR, "middle", 600)

# D3 -> Step 3 (Down)
d.arrow([(cx, d3_cy + 32), (cx, 556)], c=OK, m="ok", sw=1.4)
d.t(cx + 18, d3_cy + 45, "Yes", 10, OK, MONO, "middle", 600)

# 7. Step 3: admitBridge 등록 & Reverse.Acquire 대기
s3_y = 556
d.box(cx - 140, s3_y, 280, 44, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(cx, s3_y + 18, "admitBridge 등록 & Reverse 대기", 11, INK, KR, "middle", 600)
d.t(cx, s3_y + 34, "reverse.Acquire 대기 (≤10초)", 11, WARN, KR, "middle")

# Step 3 -> D4
d.arrow([(cx, s3_y + 44), (cx, 626)], c=WARN, m="warn", sw=1.4)

# 8. Decision 4: Reverse 획득 & 재검증 통과
d4_cy = 658
draw_diamond(cx, d4_cy, 240, 64, stroke=ACC)
d.t(cx, d4_cy - 7, "Reverse 획득 & 재검증?", 11, INK, KR, "middle", 600)
d.t(cx, d4_cy + 9, "activateBridge 확인", 11, MUTED, KR, "middle")

# D4 -> Reject 4 (Right)
d.arrow([(cx + 120, d4_cy), (670, d4_cy)], c=BAD, m="bad", sw=1.4)
d.t(cx + 145, d4_cy - 8, "No", 10, BAD, MONO, "middle", 600)
oval(670, d4_cy - 18, 200, 36, fill=PAPER2, stroke=BAD, sw=1.2)
d.t(770, d4_cy + 4, "연결 닫힘 (HTTP 응답 없음)", 11, BAD, KR, "middle", 600)

# D4 -> Step 4 (Down)
d.arrow([(cx, d4_cy + 32), (cx, 714)], c=ACC, m="acc", sw=1.6)
d.t(cx + 18, d4_cy + 45, "Yes", 10, ACC, MONO, "middle", 600)

# 9. Step 4: activateBridge (Focal)
s4_y = 714
d.box(cx - 150, s4_y, 300, 44, fill=PAPER2, stroke=ACC, sw=1.4, r=6)
d.t(cx, s4_y + 18, "activateBridge (소유권 확정)", 11, ACC, KR, "middle", 600)
d.t(cx, s4_y + 34, "0x02 마커 및 바인딩 프레임 기록", 11, MUTED, KR, "middle")

# Step 4 -> Step 5
d.arrow([(cx, s4_y + 44), (cx, 786)], c=OK, m="ok", sw=1.6)

# 10. Step 5: 양방향 copy 스트리밍
s5_y = 786
d.box(cx - 150, s5_y, 300, 44, fill=PAPER2, stroke=OK, sw=1.4, r=6)
d.t(cx, s5_y + 18, "양방향 copy 스트리밍", 11, OK, KR, "middle", 600)
d.t(cx, s5_y + 34, "32KB 청크 · BPS 페이싱 · closeWrite", 11, MUTED, KR, "middle")

# Step 5 -> End
d.arrow([(cx, s5_y + 44), (cx, 856)], c=MUTED, m="ar", sw=1.4)

# 11. End Oval
e_y = 856
oval(cx - 100, e_y, 200, 36, fill=PAPER2, stroke=MUTED, sw=1.2)
d.t(cx, e_y + 22, "세션 종료 (half-close 보존)", 11, MUTED, KR, "middle", 600)

# 범례 (Legend)
d.legend(912, [
    ("정상 흐름", OK),
    ("검사·조회", INFO),
    ("대기·예산", WARN),
    ("활성화 확정", ACC),
    ("거절·종료", BAD),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-06-bridge-admission.svg"))
d.save(out_path)
print(f"saved: {out_path}")
