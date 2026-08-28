# 01-03.traceroute-probes — TTL 1·2·3 반복 프로브
# 본문: "일부러 1 부터 시작, 죽을 자리를 지정해 쏜다",
#       "매번 다른 라우터가 내가 버렸다고 답하므로 그 답들을 모으면 경로가 순서대로 드러난다"
# 타입 스펙: type-architecture.md — 노트북 · 라우터 둘 · 목적지를 잇는 구성도 셋. 밴드가 계층이 아니라 TTL 을 1씩 올린 세 번의 시도다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 784
d = D(W, H, "TRACEROUTE · TTL 1 -> 2 -> 3",
      "traceroute — 한 번에 한 대씩, 일부러 죽여서 알아낸다",
      "TTL 을 1 부터 올려 가며 여러 번 쏜다. 매번 다른 라우터가 항의하고, 그 항의의 출발지 IP 가 곧 그 홉의 정체다.",
      lead="TTL 을 1 부터 올려 가며 쏜다 · 항의가 돌아온 출발지 IP 가 곧 그 홉의 정체다")

PAD, SLOT_W, HALF = 36, 232, 56
CX = [PAD + j * SLOT_W + SLOT_W // 2 for j in range(4)]        # 152 384 616 848
NAMES = [("내 노트북", "traceroute"), ("라우터 1", "첫 홉"),
         ("라우터 2", "둘째 홉"), ("목적지", "최종 호스트")]
BANDS = [104, 304, 504]                                        # 각 띠 높이 184, 간격 16
BAND_H = 184

for r, top in enumerate(BANDS):                                # r = 0,1,2 → TTL r+1
    die = r + 1                                                # 죽는(또는 닿는) 노드 인덱스
    last = (r == 2)
    ddx.band(d, top, top + BAND_H,
             ["1 차 — 평소엔 64 를 쓰지만 여기서는 일부러 TTL 1 로 쏜다",
              "2 차 — TTL 2 · 한 칸 더 가서 버려진다",
              "3 차 — TTL 3 · 목적지에 닿아 다른 종류의 응답이 온다"][r],
             focal=(r == 0))
    cy, y_chip, y_icmp = top + 112, top + 64, top + 164

    for j, (t, s) in enumerate(NAMES):
        ddx.node(d, CX[j], cy, t, s,
                 c=(OK if (last and j == 3) else None),
                 focal=False, dim=(j > die))
    # 나가는 프로브 — 홉마다 1 씩 줄여 넘긴다
    for j in range(die):
        ddx.hop(d, CX[j], CX[j + 1], cy, INFO, "info")
        d.chip((CX[j] + CX[j + 1]) // 2, y_chip, f"TTL {die - j}", INFO, 12)
    # 죽는 자리 표시 (마지막 회차는 도착)
    ddx.tag(d, CX[die], y_chip,
            "여기서 멈춘다" if last else "TTL 0 → 버린다",
            OK if last else BAD, 140 if last else 148)
    # 항의가 돌아오는 길 — dashed
    d.path(f"M {CX[die]} {cy+30} L {CX[die]} {y_icmp} L {CX[0]+12} {y_icmp}",
           MUTED, 1.4, m="ar", dash="6 5")
    d.t(CX[0] + 24, y_icmp - 12,
        ["ICMP 11 — 출발지가 라우터 1 의 주소",
         "ICMP 11 — 출발지가 라우터 2 의 주소",
         "목적지가 직접 답한다 — 경로가 다 드러났다"][r], 12, MUTED, KR, "start")

d.legend(716, [("프로브", INFO), ("여기서 죽는다", BAD), ("도착", OK)])
d.save("01-03.traceroute-probes.svg")
print("ok traceroute")
