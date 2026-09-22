# 2026-09-21 A(배포하지 않은 아침) 문항 · 문제 소개 — 무대.
# 노드 한 대 안에서 라우팅 테이블 하나를 두 주체가 채운다는 구조를 그린다. 사건은 boot-vs-restart 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 둘이 함께 쓰는 표가 focal.
#           type-dependency 는 "누가 누구에 기대는가" 라 기각. 여기서는 기대는 관계가 아니라 같은 자리에 쓰는 관계다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-21 A",
      "라우팅 테이블 하나를 둘이 채웁니다",
      "쿠버네티스 노드 한 대의 안쪽이다. systemd-networkd 는 자기 설정 파일에 적힌 경로를 넣고, "
      "CNI 에이전트는 Pod 대역 경로를 같은 표에 넣는다. Pod 사이 트래픽은 그 표를 보고 나간다. "
      "그 옆에 이미지에 든 타이머가 정해진 창에 자동 보안 업데이트를 깨우고, 업데이트는 systemd 패키지를 갈며 networkd 를 다시 띄운다.",
      lead="표는 하나인데 넣는 쪽이 둘이라, 한쪽이 다시 뜰 때 다른 쪽의 줄이 어떻게 되느냐가 갈립니다")

# ── 노드 경계 ─────────────────────────────────────────────────
ZX, ZY, ZW, ZH = 32, 100, 936, 440
d.o.append(f'<rect x="{ZX}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="none" '
           f'stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 3"/>')
d.o.append(f'<rect x="{ZX + 16}" y="{ZY - 7}" width="330" height="14" rx="2" fill="{PAPER}"/>')
d.t(ZX + 24, ZY + 4, "쿠버네티스 노드 · Ubuntu 22.04 · systemd v249", 11, SOFT, MONO, "start")

LX, CX, RX, BW = 72, 384, 696, 232
ROW = 372          # 표에 쓰는 줄의 높이 중앙

# ── 화살표 먼저 — 박스가 위에 덮이도록 ───────────────────────────
d.arrow([(LX + BW // 2, 196), (LX + BW // 2, 238)], MUTED, "ar", 1.2)
d.t(LX + BW // 2 + 12, 222, "깨움", 11, MUTED, KR, "start")
d.arrow([(LX + BW // 2, 296), (LX + BW // 2, 334)], MUTED, "ar", 1.2)
d.t(LX + BW // 2 + 12, 320, "재시작", 11, MUTED, KR, "start")

d.arrow([(LX + BW, ROW), (CX - 2, ROW)], INFO, "info", 1.6)
d.arrow([(RX, ROW), (CX + BW + 2, ROW)], OK, "ok", 1.6)
d.arrow([(CX + BW // 2, 468), (CX + BW // 2, 432)], MUTED, "ar", 1.2, "4 3")
d.t(CX + BW // 2 + 12, 456, "조회", 11, MUTED, KR, "start")

# ── 계기 — 타이머와 자동 업데이트 ───────────────────────────────
d.box(LX, 136, BW, 60, PAPER2, RULE, 0.9, 6)
d.t(LX + BW // 2, 162, "systemd 타이머", 13, INK, KR, "middle", 600)
d.t(LX + BW // 2, 182, "06:00~07:00 UTC", 11, MUTED, MONO)
d.box(LX, 238, BW, 58, PAPER2, RULE, 0.9, 6)
d.t(LX + BW // 2, 263, "자동 보안 업데이트", 13, INK, KR, "middle", 600)
d.t(LX + BW // 2, 282, "systemd 패키지 갱신", 11, MUTED, KR)

# ── 표에 쓰는 두 주체 ─────────────────────────────────────────
d.box(LX, 336, BW, 72, PAPER2, INFO, 1.1, 6)
d.t(LX + BW // 2, 364, "systemd-networkd", 13, INFO, MONO, "middle", 600)
d.t(LX + BW // 2, 386, ".network 파일의 경로", 11, MUTED, KR)
d.box(RX, 336, BW, 72, PAPER2, OK, 1.1, 6)
d.t(RX + BW // 2, 364, "CNI 에이전트", 13, OK, KR, "middle", 600)
d.t(RX + BW // 2, 386, "Cilium · Pod 대역 경로", 11, MUTED, KR)

# ── 둘이 함께 쓰는 표 — focal ─────────────────────────────────
d.tone(CX, 312, BW, 120, ACC, 8)
d.t(CX + BW // 2, 338, "라우팅 테이블", 13, ACC, KR, "middle", 600)
d.box(CX + 14, 352, BW - 28, 30, PAPER, INFO, 0.9, 4)
d.t(CX + 26, 372, "default via 10.0.0.1", 11, INFO, MONO, "start")
d.box(CX + 14, 390, BW - 28, 30, PAPER, OK, 0.9, 4)
d.t(CX + 26, 410, "10.244.3.0/24 via 노드 3", 11, OK, MONO, "start")

# ── 표를 쓰는 트래픽 ──────────────────────────────────────────
d.box(CX, 470, BW, 44, PAPER2, RULE, 0.9, 6)
d.t(CX + BW // 2, 497, "Pod 사이 트래픽", 12, INK, KR, "middle", 600)

d.legend(H - 64, [("둘이 함께 쓰는 표", ACC), ("networkd 가 넣은 줄", INFO), ("CNI 가 넣은 줄", OK)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.two-writers-one-table.svg"))
print("ok")
