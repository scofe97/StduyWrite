# 07-01 §9 — 여러 줄에 걸릴 때 가장 긴 접두사가 이긴다.
# 원서 결손: 저자는 route -n 과 ip route 의 칸 뜻까지만 적고, 한 주소가 여러 줄에 걸릴 때
#       무엇이 이기는지를 말하지 않는다. 기본 경로가 왜 0.0.0.0/0 인지도 따라서 설명되지 않는다.
#       2026-09-06 학습 회차에서 학습자가 이 자리를 iptables 의 순차 매칭으로 답해 결손이 드러났다.
# 근거: RFC 1812 §5.2.4.3 "Next Hop Address" 가 정하는 최장 일치 규칙. 본문 각주 참조.
# 타입 스펙: type-nested — 접두사는 포함 관계다. /8 이 /16 을 품고 /16 이 /24 를 품는다.
#       바깥이 넓고 안쪽이 구체적이며, coral 은 가장 안쪽 하나뿐이라 그것이 곧 이기는 줄이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 880, 692
d = D(W, H, "LEARNING MODERN LINUX · 07-01 §9",
      "가장 안쪽의 최장 접두사 선택",
      "라우팅 테이블에서 한 주소는 여러 줄에 걸릴 수 있다. 그때 이기는 것은 먼저 적힌 줄이 아니라 "
      "접두사가 가장 긴 줄이다. 접두사가 길수록 덮는 범위가 좁고, 좁을수록 구체적으로 아는 것이기 때문이다.",
      "10.1.2.3 대상 네 경로 동시 매칭 시 LPM 판단")

# 링: 바깥이 넓고 안쪽이 구체적이다. 가로 30 · 세로 34 로 인셋을 고정한다.
rings = [
    (110, 150, 660, 340, "0.0.0.0/0", "기본 경로 · 43억 개 전부", "rgba(139,152,169,0.30)", "none"),
    (140, 184, 600, 272, "10.0.0.0/8", "약 1,678만 개", "rgba(139,152,169,0.45)", "none"),
    (170, 218, 540, 204, "10.1.0.0/16", "65,536 개", MUTED, "none"),
    (200, 252, 480, 136, "10.1.2.0/24", "이긴 줄 · 256 개", ACC, f"{ACC}12"),
]


for x, y, w, h, label, count, stroke, fill in rings:
    focal = (stroke is ACC)
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{1.5 if focal else 1.1}"/>')
    # 라벨은 테두리에 얹지 않고 링 안쪽 위에 둔다. 테두리에 걸치면 dd-lint 가 text-box 로 잡는다.
    d.t(x + 18, y + 20, label, 8.5, ACC if focal else MUTED, MONO, "start", 600)
    d.t(x + w - 18, y + 20, count, 11.5, ACC if focal else SOFT, KR, "end")

d.chip(440, 300, "10.1.2.3 검색 대상", INK, 12)
d.t(440, 344, "네 경로 동시 매칭 중 최장 일치 선택 (최소 범위)", 11.5, ACC, KR)
d.t(440, 366, "접두사 길이 비례 구체성 (RFC 1812 포워딩 규칙)", 11.5, MUTED, KR)

d.tone(24, 510, W - 48, 118, ACC, 6, "10", 1.2)
d.t(44, 540, "규칙 순서가 아닌 접두사 길이(구체성) 기준 선택", 12.5, INK, KR, "start", 600)
d.t(44, 568, "순차 매칭(방화벽)과 달리 후보 경로 전체 조회 후 최장 프리픽스 선택", 11.5, MUTED, KR, "start")
d.t(44, 590, "기본 게이트웨이(0.0.0.0/0) — 길이 0으로 다른 세부 경로 미매칭 시 최종 선택",
    11.5, MUTED, KR, "start")
d.t(44, 612, "Destination 및 Genmask 쌍으로 목적지 네트워크 범위 정의",
    11.5, MUTED, KR, "start")

d.legend(648, [("바깥일수록 넓다", MUTED), ("가장 안쪽이 이긴다", ACC)])
d.save("07-01.longest-prefix.svg")
print("ok 07-01.longest-prefix")
