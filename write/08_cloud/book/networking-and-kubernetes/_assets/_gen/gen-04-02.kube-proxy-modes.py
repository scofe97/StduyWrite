# 04-02.kube-proxy-modes — 모드는 백엔드를 무엇으로 찾느냐로 갈린다
# 본문 요구: "Linux 의 모드는 iptables·ipvs·nftables 셋이고 Windows 는 kernelspace 하나 … nftables 와 kernelspace 는 iptables 를
#           쓰지 않습니다 … ipvs 는 1.35 에서 deprecated … userspace 는 1.26 에서 제거"
# 타입 스펙: type-dp-security-matrix — 행이 모드, 열이 조회 방식·1.37 상태·iptables 사용. 상태 열만 상태색으로 칠한다.
#           제거된 userspace 는 후보에서 빠진 행이라 격자 아래 띠로 내렸다. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼고
#           2026-11-08 에 Kubernetes 1.37 기준으로 다시 그렸다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 544
d = D(W, H, "KUBE-PROXY · MODES IN 1.37 · HOW EACH ONE LOOKS UP",
      "모드는 백엔드를 무엇으로 찾느냐로 갈린다",
      "Linux 모드는 iptables·ipvs·nftables 셋이고 iptables 가 기본이다. ipvs 는 폐기 예정이고 nftables 는 1.33 에서 GA 가 됐으며 kernelspace 는 Windows 전용이다.",
      lead="Linux 는 셋, Windows 는 하나 · ipvs 는 폐기 예정")

X0, GAP = 24, 12
COLS = [(172, "모드"), (300, "무엇으로 찾나"), (240, "1.37 상태"), (216, "iptables 사용")]
HY, RY0, RH = 120, 136, 60
XS = []; x = X0
for w, name in COLS:
    XS.append((x, w)); d.t(x + w // 2, HY, name, 12, SOFT, KR, "middle", 600); x += w + GAP

ROWS = [
    ("iptables", INFO, ("규칙 순차 평가", "확률 규칙으로 선택"), ("기본값", INFO), "사용"),
    ("ipvs", INK, ("커널 해시 테이블 조회", "스케줄러 11종 · 기본 rr"), ("1.35 deprecated", WARN), "일부 병용"),
    ("nftables", INK, ("맵 · 집합 조회", "iptables 의 후계 API"), ("1.33 GA · 커널 5.13+", OK), "미사용 · nft"),
    ("kernelspace", INK, ("Windows HNS · VFP", None), ("Windows 노드 전용", None), "미사용 · HNS · VFP"),
]


def cellbox(i, y, c):
    cx0, cw = XS[i]
    if c:
        d.o.append(f'<rect x="{cx0}" y="{y}" width="{cw}" height="{RH}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(cx0, y, cw, RH, PAPER2, RULE, 1.0, 6)
    return cx0, cw


for r, (mode, mc, how, now, ipt) in enumerate(ROWS):
    y = RY0 + r * (RH + GAP)
    cx0, cw = cellbox(0, y, None)
    d.t(cx0 + cw // 2, y + 36, mode, 13, mc, MONO, "middle", 600)
    cx0, cw = cellbox(1, y, None)
    t, s = how
    if s:
        d.t(cx0 + 20, y + 26, t, 13, INK, KR, "start", 600)
        d.t(cx0 + 20, y + 46, s, 12, MUTED, KR, "start")
    else:
        d.t(cx0 + 20, y + 36, t, 13, INK, KR, "start", 600)
    txt, c = now
    cx0, cw = cellbox(2, y, c)
    d.t(cx0 + cw // 2, y + 36, ddx.fit(txt, 13, cw - 24, txt), 13, c or MUTED, KR, "middle", 600 if c else 400)
    cx0, cw = cellbox(3, y, None)
    d.t(cx0 + cw // 2, y + 36, ddx.fit(ipt, 13, cw - 24, ipt), 13, MUTED, KR, "middle")

# 제거된 모드 — 격자 밖 띠
WY = RY0 + 4 * (RH + GAP) + 4
d.box(X0, WY, 952, 40, PAPER, RULE, 0.9, 6)
d.t(X0 + 20, WY + 26, "userspace", 13, SOFT, MONO, "start", 600)
d.t(X0 + 136, WY + 26, "자체 프로세스가 중계 · 1.23 deprecated · 1.26 에서 제거 · 선택 불가", 12, BAD, KR, "start")

d.legend(496, [("기본값", INFO), ("폐기 예정", WARN), ("GA", OK), ("제거됨", BAD)])
d.save("04-02.kube-proxy-modes.svg")
print("ok kube-proxy-modes")
