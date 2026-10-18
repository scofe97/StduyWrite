# 타입 스펙: type-layers
# 사실 출처: docs/src/routes/architecture/+page.md §Browser reverse transport (306-328행),
#   portal/transport/stream_mux.go:31-61,244-294,
#   portal/transport/reverse_framing.go:16,64,
#   docs/maintainer/architecture.md TCP bridge ownership (181-189행).
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 640
d = D(W, H,
      "PORTAL-TUNNEL · WEBSOCKET YAMUX CARRIER STACK",
      "브라우저 리버스 캐리어 계층 구조",
      "소켓 하이잭이 불가능한 브라우저·WASM을 위한 단일 연결 위 yamux 7계층 다중화",
      lead="단일 연결 위 yamux 다중화와 스트림별 인증을 거쳐 테넌트 암호문으로 연결되는 스택")

# 좌측 방향 표시 (abstraction ↑)
d.t(48, 120, "추상화 ↑", 10, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(48, 520), (48, 134)], SOFT, "soft", 1.2)
d.t(48, 536, "물리 전송", 10, SOFT, fam=KR, anchor="middle")

LX, LW = 96, 848
layers = [
    ("L7", "마커 프레이밍", "transport/reverse_framing.go",
     "0x02 바인딩", "암호문 패스스루 · 0x00 keepalive",
     PAPER2, RULE, INK),
    ("L6", "스트림별 Capability 인증", "transport/stream_mux.go:161",
     "2B len + cap", "1B 승인(0)/거절(1) · 8 KiB 상한",
     PAPER2, RULE, INK),
    ("L5", "논리 스트림 N개", "ReverseMux.Open · Accept",
     "독립 net.Conn", "ready=2 풀 합류 · 개별 스트림 수명 관리",
     PAPER2, RULE, INK),
    ("L4", "yamux 세션 다중화", "github.com/hashicorp/yamux",
     "12B Header", "다중 스트림 · 256 KiB 윈도우 제어",
     f"{ACC}14", ACC, ACC),
    ("L3", "WebSocket 전송", "github.com/coder/websocket",
     "portal.reverse.v1", "서브프로토콜 · 바이너리 프레임",
     PAPER2, RULE, INK),
    ("L2", "Relay API TLS", "cmd/relay-server (TLS)",
     "TLS 1.3", "릴레이 인증서 종단 · 보안 전송 채널",
     PAPER2, RULE, INK),
    ("L1", "기본 TCP 전송", "net.Dial / L4 Socket",
     "단일 TCP 소켓", "브라우저 환경 원시 소켓 직접 제어 불가",
     PAPER2, RULE, INK),
]

y0 = 104
h_layer = 56
gap = 8

for i, (tag, name, path_txt, chip_txt, note, fill, stroke, text_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 태그
    d.box(LX + 16, y + 14, 32, 28, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 32, y + 32, tag, 11, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 계층 이름 및 경로
    d.t(LX + 64, y + 24, name, 13, text_col, fam=KR if any("가" <= c <= "힣" for c in name) else MONO, anchor="start", weight=600)
    d.t(LX + 64, y + 44, path_txt, 11, MUTED if not is_focal else INK, fam=MONO, anchor="start")

    # 칩
    d.chip(LX + 490, y + 28, chip_txt, stroke if is_focal else INFO, size=11)

    # 설명 노트
    d.t(LX + LW - 18, y + 32, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
d.legend(568, [
    ("표준 전송·캡슐화 계층", MUTED),
    ("yamux 다중화 세션 (Focal)", ACC),
    ("프로토콜 식별 칩", INFO),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-05-carrier-stack.svg"))
d.save(out)
print(f"saved: {out}")
