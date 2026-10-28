# 본문 요구: ### 함정·관찰: 환경 변수 프록시. ProxyFromEnvironment 가 요청마다 프록시를 고르는 순서와, 서버 프로세스에서 HTTP_PROXY 가 업스트림 호출을 프록시로 보내는 조건.
# 타입 스펙: type-flowchart
# 사실 출처: go1.25.1 src/net/http/transport.go:486-500,955-966, vendor/golang.org/x/net/http/httpproxy/proxy.go:127-145,170-185, 실측 보고서 시험 4
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 1000, 468

d = D(W, H,
      "HTTP PROXYFROMENVIRONMENT DECISION FLOW",
      "ProxyFromEnvironment 프록시 결정 흐름",
      "요청마다 스킴과 CGI 환경·루프백·NO_PROXY 규칙을 차례로 검사해 프록시 경유 여부와 직접 연결을 결정합니다",
      "요청 스킴과 환경 변수를 검사해 직접 연결·CGI 에러·프록시 경유 중 하나를 반환합니다")

def custom_chip(cx, cy, txt, c=MUTED, size=11, pad=7):
    tw = sum(1.0 if '가' <= ch <= '힣' else 0.62 for ch in str(txt)) * size
    w = tw + pad * 2
    d.o.append(f'<rect x="{cx-w/2:.1f}" y="{cy-10}" width="{w:.1f}" height="20" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="0.8"/>')
    d.t(cx, cy + 4, txt, size, c, MONO if not any('가' <= ch <= '힣' for ch in str(txt)) else KR)

d.chip = custom_chip

def diamond(cx, cy, hw, hh, c, title, sub=None, title_size=12):
    d.o.append(f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, title, title_size, INK, KR, "middle", 600)
    if sub:
        # 코드 라벨을 마름모 위쪽 바깥으로 배치해 마름모 테두리와 겹치지 않게 분리
        d.t(cx, cy - hh - 8, sub, 10, SOFT, MONO, "middle")

YC = 172

# ── 0. 입구: 환경 변수 읽기 ────────────────────────────────────
X0, W0 = 20, 116
d.box(X0, YC - 32, W0, 64, fill=PAPER2, stroke=INFO, sw=1.1, r=6)
d.t(X0 + W0 // 2, YC - 10, "환경 변수 로드", 12, INFO, KR, "middle", 600)
d.t(X0 + W0 // 2, YC + 16, "envProxyOnce", 11, INK, MONO, "middle")

# 0 -> 1 화살표
d.arrow([(X0 + W0 + 2, YC), (164, YC)], c=MUTED, m="ar", sw=1.3)

# ── 1. 스킴 판정: https / http ───────────────────────────────
X1, W1 = 168, 128
d.box(X1, YC - 32, W1, 64, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t(X1 + W1 // 2, YC - 10, "스킴별 프록시", 12, INK, KR, "middle", 600)
d.t(X1 + W1 // 2, YC + 16, "HTTPS / HTTP_PROXY", 11, INFO, MONO, "middle")

# 1 -> 2 화살표
d.arrow([(X1 + W1 + 2, YC), (324, YC)], c=MUTED, m="ar", sw=1.3)

# ── 2. CGI 환경 검사 ──────────────────────────────────────────
CX2, HW2, HH2 = 376, 48, 38
diamond(CX2, YC, HW2, HH2, MUTED, "CGI 환경?", "REQUEST_METHOD")

# 2 -> 아래 (CGI 에러)
d.arrow([(CX2, YC + HH2 + 2), (CX2, 280)], c=BAD, m="bad", sw=1.4)
d.chip(CX2, YC + HH2 + 24, "예 (http · HTTP_PROXY 있음)", BAD, 11)

# 2 -> 3 (정상 통과)
d.arrow([(CX2 + HW2 + 2, YC), (470, YC)], c=MUTED, m="ar", sw=1.3)
d.chip(448, YC - 16, "아니오", MUTED, 11)

# ── 3. 프록시 값 존재 검사 ─────────────────────────────────────
CX3, HW3, HH3 = 522, 48, 38
diamond(CX3, YC, HW3, HH3, MUTED, "프록시 값?", "proxy != nil")

# 3 -> 아래 (직접 연결)
d.arrow([(CX3, YC + HH3 + 2), (CX3, 280)], c=MUTED, m="ar", sw=1.3)
d.chip(CX3, YC + HH3 + 24, "없음", MUTED, 11)

# 3 -> 4 (프록시 설정 있음)
d.arrow([(CX3 + HW3 + 2, YC), (614, YC)], c=MUTED, m="ar", sw=1.3)
d.chip(594, YC - 16, "있음", MUTED, 11)

# ── 4. 루프백 대상 검사 (localhost 포함) ──────────────────────
CX4, HW4, HH4 = 678, 60, 38
diamond(CX4, YC, HW4, HH4, MUTED, "localhost·루프백?", "IsLoopback()", title_size=11)

# 4 -> 아래 (직접 연결)
d.arrow([(CX4, YC + HH4 + 2), (CX4, 280)], c=MUTED, m="ar", sw=1.3)
d.chip(CX4, YC + HH4 + 24, "루프백", MUTED, 11)

# 4 -> 5 (일반 호스트)
d.arrow([(CX4 + HW4 + 2, YC), (772, YC)], c=MUTED, m="ar", sw=1.3)
d.chip(756, YC - 16, "아니오", MUTED, 11)

# ── 5. NO_PROXY 일치 검사 ─────────────────────────────────────
CX5, HW5, HH5 = 824, 48, 38
diamond(CX5, YC, HW5, HH5, MUTED, "NO_PROXY?", "useProxy()")

# 5 -> 아래 (직접 연결)
d.arrow([(CX5, YC + HH5 + 2), (CX5, 280)], c=MUTED, m="ar", sw=1.3)
d.chip(CX5, YC + HH5 + 24, "일치", MUTED, 11)

# 5 -> 6 (그 밖 -> 프록시 경유)
d.arrow([(CX5 + HW5 + 2, YC), (918, YC)], c=ACC, m="acc", sw=1.4)
d.chip(895, YC - 16, "불일치", ACC, 11)

# ── 6. 끝: 프록시 경유 (focal) ─────────────────────────────────
X6, W6 = 922, 72
d.box(X6, YC - 32, W6, 64, fill=f"{ACC}14", stroke=ACC, sw=1.4, r=16)
d.t(X6 + W6 // 2, YC - 6, "프록시 경유", 12, ACC, KR, "middle", 600)
d.t(X6 + W6 // 2, YC + 14, "(focal)", 11, ACC, MONO, "middle", 600)

# Step 6 아래 점선 유도선
d.path(f"M {X6 + W6 // 2} {YC + 32} L {X6 + W6 // 2} 280", c=ACC, sw=1.2, m="acc", dash="3 3")

# ── 하단 1: 판정 규칙 요약 (좌측) ──────────────────────────────
d.box(16, 280, 250, 92, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.t(24, 302, "판정 핵심 규칙 (httpproxy)", 12, INK, KR, "start", 600)
d.line(24, 312, 258, 312, RULE, 0.7)
d.t(24, 330, "1. 환경 변수는 첫 호출 때 1회만 파싱", 11, SOFT, KR, "start")
d.t(24, 348, "2. 루프백 IP 는 httpproxy 주석이 규정", 11, SOFT, KR, "start")
d.t(24, 364, "3. CGI + HTTP_PROXY 면 http 요청 거부", 11, BAD, KR, "start")

# ── 하단 2: CGI 보안 차단 (에러) ──────────────────────────────
EX, EW = 270, 212
d.box(EX, 280, EW, 92, fill=f"{BAD}14", stroke=BAD, sw=1.2, r=6)
d.t(EX + EW // 2, 302, "CGI 보안 차단 (에러)", 12, BAD, KR, "middle", 600)
d.t(EX + EW // 2, 322, "refusing HTTP_PROXY", 10, SOFT, MONO, "middle")
d.t(EX + EW // 2, 344, "REQUEST_METHOD + HTTP_PROXY 시", 11, INK, KR, "middle")
d.t(EX + EW // 2, 362, "http 대상 전체 거부 (실측)", 11, BAD, KR, "middle")

# ── 하단 3: 직접 연결 (url nil) ────────────────────────────────
DX, DW = 490, 386
d.box(DX, 280, DW, 92, fill=f"{OK}14", stroke=OK, sw=1.2, r=6)
d.t(DX + DW // 2, 302, "직접 연결 (url=nil · 프록시 미사용)", 12, OK, KR, "middle", 600)
d.line(DX + 16, 312, DX + DW - 16, 312, RULE, 0.7)
d.t(DX + 16, 330, "미설정: 환경변수 없음 (기본 직접 연결)", 11, SOFT, KR, "start")
d.t(DX + 16, 348, "루프백 실측: localhost · 127.0.0.1 · [::1]", 11, INK, MONO, "start")
d.t(DX + 16, 364, "NO_PROXY 실측: 10.0.0.0/8 시 10.0.0.5 직접", 11, OK, KR, "start")

# ── 하단 4: 프록시 경유 실측 대상 (우측) ───────────────────────
FX, FW = 896, 88
d.box(FX, 280, FW, 92, fill=PAPER2, stroke=ACC, sw=1.0, r=6)
d.t(FX + FW // 2, 302, "프록시 실측", 11, ACC, KR, "middle", 600)
d.t(FX + FW // 2, 324, "10.0.0.5", 11, INK, MONO, "middle")
d.t(FX + FW // 2, 342, "example.com", 11, INK, MONO, "middle")
d.t(FX + FW // 2, 362, "프록시 (실측)", 11, SOFT, KR, "middle")

# ── 7. 범례 ──────────────────────────────────────────────────
d.legend(412, [
    ("프록시 경유 (focal)", ACC),
    ("직접 연결 (nil)", OK),
    ("CGI 거부 차단", BAD),
    ("입구 및 스킴 선택", INFO),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.dt-proxy-decision.svg"))
d.save(out_path)
print("Saved:", out_path)
