# 04-02.kube-proxy-timeline — kube-proxy 모드가 버전을 따라 퇴장하고 합류하는 순서
# 본문 요구: "userspace 는 1.23 에서 deprecated, 1.26 에서 제거 … nftables 는 1.29 alpha, 1.31 beta, 1.33 GA …
#           ipvs 는 1.35 deprecated, 1.40 부터 기본 비활성, 1.43 에서 제거 … 1.37 의 기본값은 iptables 이고
#           모드를 정하지 않으면 1.40 에서 nftables 로 바뀐다는 경고를 kube-proxy 가 남긴다 (v1.37.2 server_linux.go)"
# 타입 스펙: type-timeline — 사건이 시간 위에 놓인다. 시간축은 날짜가 아니라 Kubernetes 마이너 버전이고 한 칸이 한 버전이다.
#           라벨은 위아래 네 단으로 엇갈린다. focal 은 지금 시점(1.37).
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, KR, MONO

W, H = 1000, 480
d = D(W, H,
      "KUBE-PROXY MODES / BY KUBERNETES VERSION",
      "모드는 버전을 따라 빠지고 들어옵니다",
      "userspace 는 1.26 에서 제거됐고 nftables 는 1.33 에서 GA 가 됐다. ipvs 는 1.35 에서 deprecated 되어 1.40 에 기본 비활성이 되고 1.43 에서 제거된다. "
      "1.37 의 기본값은 iptables 이고, 모드를 정하지 않으면 1.40 에서 nftables 로 바뀐다고 kube-proxy 가 경고한다(코드 기준).",
      lead="세 모드의 퇴장과 합류가 한 축 위에 있다 · 기본값 전환은 1.40 예고")

V0, V1, STEP = 22, 46, 36        # 1.22 ~ 1.46
X0, AY = 60, 256


def x_of(minor):
    return X0 + (minor - V0) * STEP


d.line(X0, AY, x_of(V1), AY, RULE, 2)
for m in range(V0, V1 + 1):
    tx = x_of(m)
    d.line(tx, AY - 3, tx, AY + 3, MUTED, 1)

ROW_Y = {-2: 136, -1: 196, 1: 316, 2: 376}
# (마이너, 제목, 보조, 단, 정렬, 색, focal)
events = [
    (23, "userspace deprecated", "1.23 · 제거 예고", -1, "start", BAD, False),
    (26, "userspace 제거", "1.26 · 선택 불가", 1, "middle", BAD, False),
    (29, "nftables alpha", "1.29 · 기능 게이트로 켬", -2, "middle", OK, False),
    (31, "nftables beta", "1.31 · 검증 단계", -1, "middle", OK, False),
    (33, "nftables GA", "1.33 · 정식 제공", 2, "middle", OK, False),
    (35, "ipvs deprecated", "1.35 · 폐기 예고", -2, "middle", WARN, False),
    (37, "지금 · 기본값 iptables", "1.37 · 모드 기본값", 1, "middle", ACC, True),
    (40, "기본값 nftables 예고", "1.40 · 코드 경고 기준", 2, "end", OK, False),
    (40, "ipvs 기본 비활성", "1.40 · KubeProxyIPVS 게이트", -1, "middle", WARN, False),
    (43, "ipvs 제거", "1.43 · 완전 제거", 2, "middle", WARN, False),
]
for minor, title, sub, row, anchor, col, focal in events:
    ex = x_of(minor)
    ty = ROW_Y[row]
    if row < 0:
        d.line(ex, AY - 6, ex, ty + 28, RULE, 1)
    else:
        d.line(ex, AY + 6, ex, ty - 16, RULE, 1)
    r = 6 if focal else 4
    d.o.append(f'<circle cx="{ex}" cy="{AY}" r="{r}" fill="{col}"/>')
    lx = ex + (8 if anchor == "start" else -8 if anchor == "end" else 0)
    d.t(lx, ty, title, 13, ACC if focal else INK, KR, anchor, 600)
    d.t(lx, ty + 18, sub, 12, MUTED, KR, anchor)

d.legend(432, [("userspace", BAD), ("nftables", OK), ("ipvs", WARN), ("지금 시점", ACC)])
d.save("04-02.kube-proxy-timeline.svg")
print("ok kube-proxy-timeline")
