# a0-01 §3 프로파일이 켜는 컴포넌트.
# 값 근거: istio.io 「Installation Configuration Profiles」의 컴포넌트 표(Istio 1.32 문서, 2026-11-25 확인)
#       https://istio.io/latest/docs/setup/additional-setup/config-profiles/
#       - 행(배포 프로파일): default · demo · minimal · remote · ambient · empty · preview
#       - 열(핵심 컴포넌트): istiod · istio-ingressgateway · istio-egressgateway · CNI · Ztunnel
#       - ✔: default = ingressgateway + istiod / demo = egressgateway + ingressgateway + istiod / minimal = istiod /
#            remote = 없음 / ambient = istiod + CNI + Ztunnel / empty = 없음 / preview = ingressgateway + istiod
#       - remote 행의 「CRD 와 주입 웹훅」: istioctl 1.32.0 `manifest generate --set profile=remote` 출력(CRD 15 · MutatingWebhookConfiguration 1 · Deployment 0)과
#         `--set profile=empty` 출력(0 바이트)을 맞댄 것(본문 §3).
#       - 한 줄 설명은 같은 문서의 프로파일 목록. demo 와 empty 는 §4 의 두 리소스(control-plane · ingress-gateway)가 쓰고,
#         minimal 은 같은 문서의 게이트웨이 설치 안내가 컨트롤 플레인 출발점으로 든다(본문 §4).
# 타입 스펙: type-dp-security-matrix — 행×열 교차에서 어느 조합이 켜지고 꺼지는지를 격자로 비교한다.
#           고른 이유: 이 절의 논점이 「프로파일마다 무엇이 켜지는가」이고 tree 가 아니라 교차표 모양이어서다.
#           축약: 보안 매트릭스의 구간 헤더는 쓰지 않고 칸 하나를 켜짐(색 점) 또는 꺼짐(빈 칸)으로만 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W = 1000
COLS = ["istiod", "istio-ingressgateway", "istio-egressgateway", "CNI", "Ztunnel"]
ROWS = [
    ("default", "운영 배포 권장", (1, 1, 0, 0, 0), False),
    ("demo", "적은 자원으로 기능을 보이는 시연용", (1, 1, 1, 0, 0), True),
    ("minimal", "default 에서 컨트롤 플레인만", (1, 0, 0, 0, 0), True),
    ("remote", "원격 클러스터용 · CRD 와 주입 웹훅만", (0, 0, 0, 0, 0), False),
    ("ambient", "ambient 모드 시작용", (1, 0, 0, 1, 1), False),
    ("empty", "아무것도 배포하지 않음", (0, 0, 0, 0, 0), True),
    ("preview", "실험적 기능, 보장 없음", (1, 1, 0, 0, 0), False),
]

LX, CX0, CW, RH, HY = 28, 270, 140, 56, 116
H = HY + 40 + len(ROWS) * RH + 120

d = D(W, H, "ISTIO IN ACTION · A0-01 §3",
      "프로파일마다 켜지는 컴포넌트가 다르다",
      "배포 프로파일 일곱을 행으로, 핵심 컴포넌트 다섯을 열로 놓고 켜지는 칸에 점을 찍었다. "
      "default 는 인그레스 게이트웨이와 istiod 를 켜고 demo 는 이그레스 게이트웨이까지 켠다. "
      "minimal 은 istiod 만, empty 와 remote 는 컴포넌트를 켜지 않는다. remote 는 그래도 CRD 와 주입 웹훅을 올린다. 색이 붙은 행이 다음 절이 쓰는 프로파일이다.",
      "istioctl 로 설치할 때만 프로파일이 컴포넌트까지 고릅니다")

for j, c in enumerate(COLS):
    d.t(CX0 + j * CW + CW / 2, HY, c, 10, MUTED, MONO, "middle", 600)
d.line(LX, HY + 14, CX0 + len(COLS) * CW, HY + 14, RULE, 0.8)

for i, (name, sub, marks, focal) in enumerate(ROWS):
    y = HY + 30 + i * RH
    if focal:
        d.o.append(f'<rect x="{LX - 8}" y="{y - 8}" width="{CX0 + len(COLS) * CW - LX + 8}" height="{RH - 4}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.0"/>')
    d.t(LX + 4, y + 16, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(LX + 4, y + 34, sub, 11, MUTED, KR, "start")
    for j, on in enumerate(marks):
        cx = CX0 + j * CW + CW / 2
        if on:
            d.o.append(f'<circle cx="{cx}" cy="{y + 19}" r="8" fill="{ACC if focal else INFO}" />')
        else:
            d.line(cx - 6, y + 19, cx + 6, y + 19, SOFT, 1.0)

FY = HY + 30 + len(ROWS) * RH + 14
d.t(LX, FY, "이그레스 게이트웨이를 켜는 프로파일: demo 하나", 11, INK, KR, "start")
d.t(LX, FY + 24, "remote 와 empty 의 차이: remote 는 CRD 와 주입 웹훅을 올리고 empty 는 아무것도 올리지 않는다", 11, MUTED, KR, "start")
d.legend(FY + 50, [("다음 절이 쓰는 프로파일", ACC), ("그 밖의 프로파일", INFO)])
d.save("a0-01.profile-map.svg")
