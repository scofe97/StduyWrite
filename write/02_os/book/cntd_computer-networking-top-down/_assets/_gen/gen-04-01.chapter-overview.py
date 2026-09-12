# 04-01.chapter-overview — 이 편을 "누가 채우나 → 무엇을 약속하나 → 상자 안 → 조회 → 옮김 → 추상" 여섯 박자로 읽는 지도
# 카드의 절 번호·이름·한 줄·항목 셋은 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다. 없는 사실은 넣지 않았다.
# 타입 스펙: type-process — 단계마다 같은 의미 슬롯(절 번호 · 이름 · 한 줄 · 항목 셋)이 같은 자리에 반복된다
#           (semantic-patterns 의 "Stage framework with semantic slots"). 화살표는 데이터가 아니라 읽는 순서다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, OK, INFO, KR, MONO

W, H = 1000, 406
X0, GAP, CARD_Y, CARD_H = 12, 16, 132, 196
N = 6
CARD_W = (W - 48 - X0 - GAP * (N - 1)) / N

d = D(W, H, "CHAPTER MAP · 04-01",
      "라우터는 안에서 무엇을 하는가 — 여섯 박자로 읽는 지도",
      "04-01 편의 전체 구조. 포워딩 테이블을 누가 채우는가라는 물음에서 출발해, 망이 무엇을 약속하는지, 상자 안의 네 부분, 조회와 스위칭을 거쳐 일치 후 동작이라는 추상에 닿는다.",
      lead="누가 채우나 → 무엇을 약속하나 → 상자 안 넷 → 조회 → 옮김 → 하나의 틀")

CARDS = [("§1", "두 평면",      "테이블을 누가 채우나", INFO, ["· 전통: 라우터 안", "· SDN: 원격 컨트롤러", "· 5장으로 이어짐"]),
         ("§2", "서비스 모델",  "망은 무엇을 약속하나", INFO, ["· 후보는 다섯", "· 고른 것은 최선 노력", "· 위가 메운다"]),
         ("§3", "네 부분",      "상자 안의 넷",         ACC,  ["· 입력·패브릭·출력", "· 라우팅 프로세서", "· 셋은 나노초"]),
         ("§4", "조회",         "접두로 찾는다",        INFO, ["· 항목 넷이면 된다", "· 긴 접두가 이긴다", "· TCAM 한 클록"]),
         ("§5", "스위칭",       "옮기는 방법 셋",       INFO, ["· 메모리 B/2", "· 버스 하나씩", "· 크로스바 나란히"]),
         ("§6", "일치 후 동작", "장치들의 공통 틀",     OK,   ["· 라우터·스위치", "· 방화벽·NAT", "· 04-04 로"])]

for i, (tag, title, sub, c, bullets) in enumerate(CARDS):
    x = X0 + (CARD_W + GAP) * i
    cx = x + CARD_W / 2
    d.t(cx, 118, tag, 9, SOFT, MONO)
    d.tone(x, CARD_Y, CARD_W, CARD_H, c, 6, "10", 1.4)
    d.t(cx, 166, title, 14, c, KR, "middle", 600)
    d.line(x + 14, 182, x + CARD_W - 14, 182, f"{c}44", 0.9)
    d.t(cx, 206, sub, 12, INK)
    for j, b in enumerate(bullets):
        d.t(x + 12, 236 + j * 24, b, 12, MUTED, KR, "start")
    if i < N - 1:
        d.path(f"M {x+CARD_W+2} {CARD_Y+CARD_H/2} L {x+CARD_W+GAP-3} {CARD_Y+CARD_H/2}", MUTED, 1.4, m="ar")

d.t(W / 2, 350, "강조된 칸이 이 편의 축입니다 — 데이터 평면은 나노초, 제어 평면은 초. 그 차이가 나머지 절을 설명합니다.", 12, MUTED)
d.legend(362, [("도입·전개", INFO), ("이 편의 축", ACC), ("다음 편으로", OK)])
d.save("04-01.chapter-overview.svg")
