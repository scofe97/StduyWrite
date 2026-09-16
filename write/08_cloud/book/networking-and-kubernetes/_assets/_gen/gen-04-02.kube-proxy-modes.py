# 04-02.kube-proxy-modes — 모드 다섯은 백엔드를 무엇으로 찾느냐로 갈린다
# 본문 요구: "모드는 다섯입니다 … kernelspace 와 nftables 는 iptables 를 쓰지 않습니다 …
#           '전부 iptables 에 의존'이 성립하는 것은 userspace·iptables·ipvs 세 모드까지 … userspace 는 1.26 에서 제거"
# 타입 스펙: type-dp-security-matrix — 행이 모드, 열이 조회 방식·현재 상태·iptables 사용. 원문 정오의 축인
#           iptables 사용 열에서 "미사용" 두 칸만 상태색으로 칠한다. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 560
d = D(W, H, "KUBE-PROXY · FIVE MODES · HOW EACH ONE LOOKS UP",
      "모드 다섯은 백엔드를 무엇으로 찾느냐로 갈린다",
      "userspace 는 제거됐고 iptables 가 기본이며 IPVS 는 해시, nftables 는 1.33 GA 후계, kernelspace 는 Windows 전용이다.",
      lead="책은 넷 · 전부 iptables 의존이라 적었지만, 지금은 다섯이고 둘은 iptables 미사용")

X0, GAP = 24, 12
COLS = [(172, "모드"), (300, "무엇으로 찾나"), (224, "지금 상태"), (232, "iptables 사용")]
HY, RY0, RH = 120, 136, 60
XS = []; x = X0
for w, name in COLS:
    XS.append((x, w)); d.t(x + w // 2, HY, name, 12, SOFT, KR, "middle", 600); x += w + GAP

ROWS = [
    ("userspace", SOFT, ("자체 프로세스 프록시", "유저 공간 왕복"), ("1.26 제거", BAD), ("사용했음", None)),
    ("iptables", INFO, ("규칙 순차 평가", "확률 규칙으로 선택"), ("기본값 · 최다 사용", INFO), ("사용", None)),
    ("ipvs", INK, ("커널 해시 테이블 조회", "스케줄러 6종 · 기본 rr"), ("대규모용", None), ("일부 병용", None)),
    ("nftables", OK, ("맵 · 집합 조회", "선형 순회 탈피"), ("1.33 GA · 후계", OK), ("미사용 · nft", WARN)),
    ("kernelspace", INK, ("Windows HNS · VFP", None), ("Windows 노드 전용", None), ("미사용 · HNS · VFP", WARN)),
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
    for i, (txt, c) in ((2, now), (3, ipt)):
        cx0, cw = cellbox(i, y, c)
        d.t(cx0 + cw // 2, y + 36, ddx.fit(txt, 13, cw - 24, txt), 13, c or MUTED, KR, "middle", 600 if c else 400)

d.legend(512, [("제거됨", BAD), ("기본값", INFO), ("GA 후계", OK), ("iptables 미사용", WARN)])
d.save("04-02.kube-proxy-modes.svg")
print("ok kube-proxy-modes")
