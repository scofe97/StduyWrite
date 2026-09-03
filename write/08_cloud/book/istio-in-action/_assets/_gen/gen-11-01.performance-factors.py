# 11-01 §3 컨트롤 플레인 성능을 정하는 네 가지 — 원문 그림 11.3.
# 본문(원문 11.1.2): 변경률(높을수록 데이터 플레인을 맞추는 처리가 늘어난다), 할당 자원(수요가 istiod 에
#       준 자원을 넘으면 일이 큐에 쌓여 배포가 느려진다), 갱신할 워크로드 수(더 많은 처리 능력과 대역폭이
#       필요하다), 설정 크기(큰 Envoy 설정을 배포하려면 더 많은 처리 능력과 대역폭이 필요하다).
# accent 는 설정 크기다 — 저자가 11.3.4 끝에서 "사이드카 설정을 정의하는 것만으로 이득의 대부분을 얻는다"고
#       적어 네 뼈대 중 이것 하나를 확정된 첫 손잡이로 지목한다.
# 타입 스펙: type-fishbone — 관찰된 결과 하나, 범주별 원인, 범주에 달린 하위 원인. 척추는 가로선,
#           뼈대는 대각(이 타입의 문법이라 직각 엘보 예외), 확정된 근본 원인 뼈대 하나를 accent.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 660
d = D(W, H, "ISTIO IN ACTION · 11-01 §3",
      "네 갈래가 같은 증상으로 모인다",
      "저자가 든 성능 요인 넷을 결과 하나에 붙였다. 색이 붙은 뼈대가 저자가 첫 손잡이로 지목한 것이고, "
      "나머지 셋은 그것을 다 돌린 뒤에 본다.",
      "변경률만은 우리 손 밖입니다 — 나머지 셋은 설정으로 줄일 수 있습니다")

CY, HEAD = 328, 684
d.path(f"M 96 {CY} L {HEAD - 8} {CY}", INK, 1.2, m="ar")

bones = [
    ("변경률", ["서비스가 뜨고 진다", "복제본 수가 바뀐다"], -1, False),
    ("할당 자원", ["CPU 가 먼저 포화된다", "모자라면 큐에 쌓인다"], 1, False),
    ("워크로드 수", ["갱신 대상이 늘어난다", "대역폭이 함께 든다"], -1, False),
    ("설정 크기", ["기본은 모두가 모두를 안다", "워크로드당 2MB"], 1, True),
]
for k, (cat, subs, side, focal) in enumerate(bones):
    ax = HEAD - 116 - (k + 1) * 108
    fx, fy = ax - 68, CY + side * 156
    c = ACC if focal else MUTED
    d.line(ax, CY, fx, fy, c, 1.4 if focal else 1.1)
    tw = len(cat) * 13 + 28
    bx, by = fx - tw / 2, fy - (28 if side < 0 else 0)
    if focal:
        d.o.append(f'<rect x="{bx}" y="{by}" width="{tw}" height="28" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(bx, by, tw, 28, PAPER2, RULE, 1.0, 4)
    d.t(fx, by + 19, cat, 12, ACC if focal else INK, KR, "middle", 600)
    for j, sc in enumerate(subs):
        t = 0.34 + j * 0.30
        tx, ty = ax + (fx - ax) * t, CY + (fy - CY) * t
        d.line(tx, ty, tx + 28, ty, SOFT, 1.0)
        d.t(tx + 36, ty + 4, sc, 11, ACC if focal else MUTED, KR, "start")

d.o.append(f'<rect x="{HEAD}" y="{CY - 48}" width="{W - HEAD - 24}" height="96" rx="6" fill="{INK}07" stroke="{INK}44" stroke-width="1.2"/>')
d.t(HEAD + (W - HEAD - 24) / 2, CY - 16, "데이터 플레인이", 13, INK, KR, "middle", 600)
d.t(HEAD + (W - HEAD - 24) / 2, CY + 6, "제때 갱신되지 않는다", 13, INK, KR, "middle", 600)
d.t(HEAD + (W - HEAD - 24) / 2, CY + 32, "낡은 설정의 수명이 길어진다", 11, MUTED, KR, "middle")

d.t(32, 556, "저자가 못 박는 문장 — 사이드카 설정을 정의하는 것만으로 이득의 대부분을 얻는다", 11, SOFT, KR, "start")
d.t(32, 580, "변경률은 운영자가 정하는 값이 아니다 — 대신 얼마나 묶을지를 정할 수 있다", 11, MUTED, KR, "start")
d.legend(608, [("저자가 첫 손잡이로 지목한 갈래", ACC), ("그다음에 보는 갈래", MUTED)])
d.save("11-01.performance-factors.svg")
