# 타입 스펙: type-tree
# 09-01 누가 누구를 쥐고 있나 (서버·미들웨어·멀티플렉서·핸들러 계층 트리)
# 사실 출처: NPG 09-02 Listing 9-15 (drainAndClose + serveMux + 3 endpoints), net/http/server.go
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 1000, 580
d = D(W, H, "NPG CH.9 §1 — HANDLER COMPOSITION TREE",
      "누가 누구를 쥐고 있나",
      "서버부터 보조 기능·경로 판별·비즈니스 로직까지 모두 ServeHTTP 를 구현하여 상위가 하위를 감싸 쥡니다",
      "상위 객체가 하위 객체를 감싸는 단일 소유 트리 구조이며, 요청마다 경로에 맞는 가지 하나를 따라 내려갑니다")

# 중심 X 좌표 (4의 배수)
CX = 480

# 1. 트리 직교 연결선 (노드보다 먼저 그려 z-order 준수)
# Root -> drainAndClose
d.line(CX, 168, CX, 204, RULE, 1.2)
d.path(f"M {CX-4} 200 L {CX} 206 L {CX+4} 200", RULE, 1.0)

# drainAndClose -> serveMux
d.line(CX, 260, CX, 296, RULE, 1.2)
d.path(f"M {CX-4} 292 L {CX} 298 L {CX+4} 292", RULE, 1.0)

# serveMux -> 버스
d.line(CX, 352, CX, 388, RULE, 1.2)

# 가로 버스 (Leaf 1, 2, 3 중심을 연결)
LX1, LX2, LX3 = 168, 480, 792
d.line(LX1, 388, LX3, 388, RULE, 1.2)

# 버스 -> 각 Leaf 수직 드롭
for lx in [LX1, LX2, LX3]:
    d.line(lx, 388, lx, 416, RULE, 1.2)
    d.path(f"M {lx-4} 412 L {lx} 418 L {lx+4} 412", RULE, 1.0)

# 2. 노드 상자 및 내용

# [뿌리: http.Server]
# 칸: Handler 필드가 drainAndClose 를 쥠, net.Listener 수신 (Server 는 Handler 가 아니므로 꼬리표 제외)
RX, RY, RW, RH = 336, 112, 288, 56
d.box(RX, RY, RW, RH, fill=PAPER2, stroke=INFO, sw=1.1)
d.t(CX, RY + 22, "http.Server", 13, INK, MONO, "middle", 600)
d.t(CX, RY + 42, "net.Listener 수신 · Handler 필드 소유", 11, INFO, KR, "middle")

# [중간 1: drainAndClose(serveMux)]
DX, DY, DW, DH = 336, 204, 288, 56
d.box(DX, DY, DW, DH, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(CX, DY + 22, "drainAndClose(serveMux)", 13, INK, MONO, "middle", 600)
d.t(CX, DY + 42, "보조 기능 미들웨어 · 요청 본문 정리", 11, MUTED, KR, "middle")
d.chip(DX + DW + 80, DY + 28, "ServeHTTP(w, r)", MUTED, 11)

# [중간 2: serveMux (FOCAL ACC Coral)]
MX, MY, MW, MH = 336, 296, 288, 56
d.tone(MX, MY, MW, MH, ACC, op="18", sw=1.4)
d.t(CX, MY + 22, "serveMux", 14, ACC, MONO, "middle", 600)
d.t(CX, MY + 42, "경로 판별 멀티플렉서 · 가장 구체적인 패턴 표", 11, INK, KR, "middle")
d.chip(MX + MW + 80, MY + 28, "ServeHTTP(w, r)", ACC, 11)

# [잎 셋: 엔드포인트 핸들러]
leaves = [
    (LX1, '"/"', "204 No Content", "비즈니스 로직 · 기본 경로", MUTED),
    (LX2, '"/hello"', '200 "Hello friend."', "비즈니스 로직 · 정확 일치", OK),
    (LX3, '"/hello/there/"', '200 "Why, hello there."', "비즈니스 로직 · 하위 트리", OK),
]

LW, LH = 240, 60
for cx, path, resp, desc, col in leaves:
    bx = cx - LW // 2
    by = 416
    d.box(bx, by, LW, LH, fill=PAPER2, stroke=col, sw=1.0)
    d.t(cx, by + 20, path, 13, INK, MONO, "middle", 600)
    d.t(cx, by + 37, resp, 11, col, MONO, "middle")
    d.t(cx, by + 51, desc, 11, MUTED, KR, "middle")
    d.chip(cx, by + LH + 26, "ServeHTTP(w, r)", col, 11)

# 3. 범례
d.legend(540, [
    ("서버 및 Handler 필드", INFO),
    ("미들웨어 래퍼 (보조 기능)", MUTED),
    ("멀티플렉서 (경로 판별)", ACC),
    ("엔드포인트 응답 (비즈니스 로직)", OK),
])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "09-01.handler-tree.svg"))
d.save(out)
print(f"saved: {out}")
