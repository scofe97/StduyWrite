# 사실 출처: net/conf.go, net/lookup_unix.go, go doc net "Name Resolution" (go1.25.1)
# 타입 스펙: type-flowchart
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 560

d = D(W, H,
      "RESOLVER STRATEGY & DUAL PATH FLOWCHART",
      "Resolver 호스트 조회 시 전략 판정 및 순수 Go·cgo 분기 흐름도",
      "conf 모듈의 판정 단계에 따라 순수 Go 리졸버와 cgo 리졸버 경로로 갈린다",
      "고루틴 I/O 기반의 순수 Go 리졸버와 OS 스레드를 점유하는 cgo 리졸버의 선택 규칙")

# ── 1. 판별 노드 (좌측 열, x = 48, w = 400, h = 36) ──
# ── 2. 판별 결과 (우측 열, x = 520, w = 392, h = 36) ──
BX, BW, BH = 48, 400, 40
RX, RW, RH = 520, 392, 40

steps = [
    (96,  "mustUseGoResolver(r)", "순수 Go 리졸버 경로", "netdns=go · PreferGo · netgo · cgo 없음", OK),
    (156, "c.preferCgo || c.netCgo", "cgo 리졸버 경로", "Darwin·iOS·Windows·Android · netcgo · 환경 변수", WARN),
    (216, "hostname 에 특수문자 ('\\' 또는 '%')", "cgo 리졸버 경로", "특수 형식 호스트는 libc 위임", INFO),
    (240 + 36, "resolv.conf 오류 또는 미지원 옵션", "cgo 리졸버 경로", "읽기 실패 · unknownOpt 발견 시 전환", INFO),
    (300 + 36, "nsswitch.conf 특수 모듈 (mdns 등)", "cgo 리졸버 경로", "mdns+.local · myhostname 자기 호스트 · 모르는 소스", INFO),
]

for i, (y, cond, title, desc, col) in enumerate(steps):
    is_focal = (col == OK)
    # 좌측 조건 상자 — focal 은 범례의 순수 Go(OK) 색으로 칠한다
    d.box(BX, y, BW, BH, fill=PAPER2, stroke=OK if is_focal else RULE, sw=1.2 if is_focal else 0.9)
    d.t(BX + 16, y + 25, cond, 11, OK if is_focal else INK, fam=MONO if "(" in cond else KR, anchor="start", weight=600 if is_focal else 400)

    # Yes 화살표 (수평 직선: BX + BW -> RX, 길이 72px)
    d.arrow([(BX + BW, y + 20), (RX, y + 20)], col, "ar", 1.4)
    d.chip(BX + BW + 36, y + 9, "Yes", col, 9)

    # 우측 결과 상자
    d.box(RX, y, RW, RH, fill=PAPER2, stroke=col, sw=1.2 if is_focal else 1.0)
    d.t(RX + 16, y + 16, title, 11, col, fam=KR, anchor="start", weight=600)
    d.t(RX + 16, y + 33, desc, 11, MUTED, fam=KR, anchor="start")

    # No 화살표 (수직 직선: y+BH -> next_y)
    if i < len(steps) - 1:
        next_y = steps[i+1][0]
        d.arrow([(BX + BW // 2, y + BH), (BX + BW // 2, next_y)], MUTED, "ar", 1.0)
        # 상자 사이 20px 에 칩을 넣으면 위아래 상자에 닿으므로 화살표 옆 글자로 둔다
        d.t(BX + BW // 2 + 10, y + BH + 14, "No", 9, SOFT, fam=MONO, anchor="start")

# 마지막 No 분기: 표준 Unix 기본값 (Files -> DNS)
last_y = steps[-1][0]
d.arrow([(BX + BW // 2, last_y + BH), (BX + BW // 2, last_y + BH + 28)], MUTED, "ar", 1.0)
d.t(BX + BW // 2 + 10, last_y + BH + 18, "No", 9, SOFT, fam=MONO, anchor="start")

DEF_Y = last_y + BH + 28
d.box(BX, DEF_Y, BW, 40, fill=PAPER2, stroke=OK, sw=1.2)
d.t(BX + 16, DEF_Y + 16, "nsswitch 순서 (기본 hostLookupFilesDNS)", 11, OK, fam=KR, anchor="start", weight=600)
d.t(BX + 16, DEF_Y + 32, "/etc/hosts 먼저 확인 후 순수 Go DNS 질의", 11, MUTED, fam=KR, anchor="start")

# 연결 화살표: 기본 순서 -> 순수 Go 결과
d.arrow([(BX + BW, DEF_Y + 20), (RX, DEF_Y + 20)], OK, "ar", 1.4)
d.box(RX, DEF_Y, RW, 40, fill=PAPER2, stroke=OK, sw=1.2)
d.t(RX + 16, DEF_Y + 16, "goLookupIPCNAMEOrder (순수 Go 질의)", 11, OK, fam=KR, anchor="start", weight=600)
d.t(RX + 16, DEF_Y + 32, "고루틴 논블로킹 I/O · netpoller 위에서 대기", 11, MUTED, fam=KR, anchor="start")

# 범례 (y = 516)
d.legend(516, [
    ("순수 Go 리졸버 (focal)", OK),
    ("플랫폼 기본 cgo", WARN),
    ("설정·기능 부재로 cgo 전환", INFO)
])

out_name = "05-01.resolver-lookup-flow.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
