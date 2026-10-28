# 본문 요구: ### 함정·관찰: 공용 전역 객체 수정. 한 프로세스의 여러 호출 경로가 DefaultTransport 하나와 그 풀 하나를 같이 쓰므로 필드 하나를 고치면 모두 바뀐다는 것, Clone 은 필드만 복사하고 풀은 빈 채로 시작한다는 것.
# 타입 스펙: type-data-flow
# 사실 출처: go1.25.1 src/net/http/transport.go:45-56, src/net/http/transport.go:329-373, src/net/http/transport.go:99,101,110, src/net/http/client.go:40-44, 실측 보고서 시험 5
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 520

d = D(W, H,
      "HTTP DEFAULTTRANSPORT SHARED INSTANCE",
      "공용 DefaultTransport 와 Clone 사본의 풀 격리",
      "한 프로세스의 여러 호출 경로가 DefaultTransport 하나와 연결 풀을 공유하며 전역 필드 수정이 전체에 적용되고 Clone 은 빈 풀로 격리됩니다",
      "DefaultTransport 필드 수정은 모든 기본 호출 경로에 전파되며 Clone 사본은 필드만 복사하고 빈 풀에서 시작합니다")

# ── 1. 상단: 전역 쓰기 수정 화살표 ──────────────────────────────
WX, WY, WW, WH = 448, 98, 248, 26
d.box(WX, WY, WW, WH, fill=f"{WARN}14", stroke=WARN, sw=1.1, r=4)
d.t(WX + WW // 2, WY + 17, "MaxIdleConnsPerHost = 50", 11, WARN, fam=MONO, weight=600)
# 쓰기 화살표: 상자 밑변에서 DefaultTransport 윗변으로
d.path(f"M {WX + WW // 2} {WY + WH} L {WX + WW // 2} 142", c=WARN, sw=1.4, m="warn", dash="3 3")
d.t(WX + WW // 2 + 12, 136, "모든 경로에 적용", 11, WARN, fam=KR, anchor="start", weight=600)

# ── 2. 왼쪽 열: 4개 출발 호출 경로 (fan-in) ───────────────────
callers = [
    ("http.Get(...)", None),
    ("http.Post(...)", None),
    ("http.DefaultClient", "Transport nil"),
    ("Client{}", "Transport nil (내부)"),
]

CX_L, CW_L = 24, 196
Y_BASE = 146
ROW_H = 45

for i, (name, sub) in enumerate(callers):
    cy = Y_BASE + i * ROW_H
    d.box(CX_L, cy, CW_L, 38, fill=PAPER2, stroke=RULE, sw=0.8, r=4)
    if sub:
        d.t(CX_L + 12, cy + 15, name, 11, INK, fam=MONO, anchor="start", weight=600)
        d.t(CX_L + 12, cy + 30, sub, 11, SOFT, fam=KR, anchor="start")
    else:
        d.t(CX_L + 12, cy + 24, name, 12, INK, fam=MONO, anchor="start", weight=600)
    # 오른쪽으로 나가는 수평 화살표 (DefaultTransport 로 fan-in)
    mid_y = cy + 19
    d.arrow([(CX_L + CW_L + 2, mid_y), (284, mid_y)], c=MUTED, m="ar", sw=1.2)

d.t(254, 138, "공용 참조", 11, SOFT, fam=KR, anchor="middle")

# ── 3. 가운데: DefaultTransport 단일 인스턴스 (focal 공유 풀) ────
TX, TY, TW, TH = 288, 146, 568, 180
d.box(TX, TY, TW, TH, fill=PAPER2, stroke=RULE, sw=1.0, r=8)
d.t(TX + 16, TY + 20, "DefaultTransport", 12, INK, fam=MONO, anchor="start", weight=600)
d.t(TX + TW - 16, TY + 20, "transport.go:45", 11, SOFT, fam=MONO, anchor="end")

# focal: 가운데 공유 연결 풀
PX, PY, PW, PH = TX + 16, TY + 30, TW - 32, 134
d.tone(PX, PY, PW, PH, ACC, r=6, op="14", sw=1.4)
d.t(PX + 14, PY + 20, "공유 연결 풀 (focal · idleConn)", 12, ACC, fam=KR, anchor="start", weight=600)
d.t(PX + 14, PY + 42, "풀 하나 · 호스트당 빈 연결 2 (기본값)", 12, INK, fam=KR, anchor="start")
d.t(PX + 14, PY + 64, "http.Get 동시 10 2라운드 새 연결:", 11, SOFT, fam=KR, anchor="start")
d.t(PX + 14, PY + 84, "새 연결 8 → 0 (실측 시험 5)", 12, ACC, fam=KR, anchor="start", weight=600)
d.t(PX + 14, PY + 106, "모든 기본 호출 경로가 풀 하나 공유", 11, SOFT, fam=KR, anchor="start")
d.t(PX + 14, PY + 124, "필드 하나 수정 시 전체 경로 변경", 11, WARN, fam=KR, anchor="start")

# ── 4. 아래 갈래: Clone() → 사본 Transport → 전용 Client ──────
# DefaultTransport 밑변에서 아래로 내려오는 화살표
d.path(f"M 458 {TY + TH + 2} L 458 356", c=MUTED, sw=1.4, m="ar")
d.t(472, 344, "t.Clone()", 11, MUTED, fam=MONO, anchor="start")

# 왼쪽 하단: 격리 원칙 요약
IX, IY, IW, IH = CX_L, 360, CW_L, 88
d.box(IX, IY, IW, IH, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
d.t(IX + 12, IY + 22, "격리 원칙", 12, INK, fam=KR, anchor="start", weight=600)
d.t(IX + 12, IY + 44, "전역 객체 직접 수정 피하기", 11, WARN, fam=KR, anchor="start")
d.t(IX + 12, IY + 64, "Clone() 사본 사용 권장", 11, OK, fam=KR, anchor="start")

# 가운데 하단: 사본 Transport
MX, MY, MW, MH = TX, 360, 340, 88
d.box(MX, MY, MW, MH, fill=PAPER2, stroke=OK, sw=1.1, r=6)
d.t(MX + 16, MY + 20, "사본 Transport", 12, OK, fam=MONO, anchor="start", weight=600)
d.t(MX + MW - 16, MY + 20, "transport.go:329", 11, SOFT, fam=MONO, anchor="end")
d.t(MX + 16, MY + 40, "필드 복사 · 풀 비어 있음 (nil)", 12, INK, fam=KR, anchor="start")
d.t(MX + 16, MY + 60, "사본 수정 시 원본 불변 (0 · 7 실측)", 12, OK, fam=KR, anchor="start", weight=600)
d.t(MX + 16, MY + 78, "원본 50개 있어도 사본 첫 요청은 새 소켓", 11, SOFT, fam=KR, anchor="start")

# 사본에서 전용 Client 로 나가는 화살표
d.arrow([(MX + MW + 2, MY + 44), (TX + TW - 192, MY + 44)], c=OK, m="ok", sw=1.4)
d.t(646, MY + 35, "주입", 11, OK, fam=KR, anchor="middle", weight=600)

# 오른쪽 하단: 전용 Client
QX, QY, QW, QH = TX + TW - 188, 360, 188, 88
d.box(QX, QY, QW, QH, fill=PAPER2, stroke=OK, sw=0.9, r=6)
d.t(QX + 14, QY + 22, "전용 Client", 12, INK, fam=MONO, anchor="start", weight=600)
d.t(QX + 14, QY + 44, "Transport: cloneTr", 11, OK, fam=MONO, anchor="start")
d.t(QX + 14, QY + 64, "독립 풀 사용 · 전역 격리", 11, SOFT, fam=KR, anchor="start")

# ── 5. 범례 ──────────────────────────────────────────────────
d.legend(468, [
    ("공유 연결 풀 (focal)", ACC),
    ("사본 풀 격리 및 정상", OK),
    ("전역 필드 쓰기 및 권고", WARN),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.dt-shared-global.svg"))
d.save(out_path)
print("Saved:", out_path)
