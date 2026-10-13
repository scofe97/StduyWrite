# 타입 스펙: type-architecture — 지도 클라이언트가 세 서비스(위치·타일·길찾기)에 각각 다른 값을 보내는 구조. 흐름은 위에서 아래로, 연결은 직각만 쓴다.
# 사실 출처: 추출본 v1.txt 2847~2897행(위치 서비스·지도 렌더링의 CDN 과 정적 타일·길찾기 서비스의 지오코딩과 경로 계획)과 PDF 116쪽 그림(Load Balancer 가 위치·길찾기 서비스 앞, 타일은 CDN 으로 곧장·Geocoding DB·Road Segment DB·User Location DB·Static Map Images),
#   Google Maps JavaScript API 문서 Map and tile coordinates(시카고 41.85 -87.65, 줌 3 의 타일 (2, 2) 는 project() 식으로 계산), Routes API computeRoutes 문서(routingPreference TRAFFIC_AWARE,
#   computeAlternativeRoutes), Routes API 의 traffic 설정 문서(TRAFFIC_UNAWARE·TRAFFIC_AWARE·TRAFFIC_AWARE_OPTIMAL). 위치를 몇 초마다 보낸다는 설명은 설계 가정이다.
# Layout conventions: 클라이언트 y=104 높이 56, 버스 y=192, 로드 밸런서 y=216 높이 32(위치·길찾기 열 사이 한 칸), 1행 y=320 높이 72, 2행 y=440 높이 80, 3행 y=560 높이 52, 열 x=[24, 316, 608] 폭 [272, 272, 368]. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 724
d = D(W, H, "BYTEBYTEGO · 08-02 §5",
      "지도 서비스는 클라이언트가 보내는 값에 따라 세 갈래로 나뉜다",
      "좌표는 위치 서비스로, 타일 번호는 CDN 으로, 출발·도착 주소는 길찾기 서비스로 갑니다.",
      "좌표와 타일은 Google 문서의 시카고 예시이고 위치 전송 주기는 설계 가정입니다")
fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO

CX, CY, CW, CH = 300, 104, 304, 56
d.box(CX, CY, CW, CH, PAPER2, INFO, 1.0, 6)
d.t(CX + CW / 2, CY + 24, "모바일 클라이언트", 13, INK, KR, "middle", 600)
d.t(CX + CW / 2, CY + 44, "화면 · 위치 · 목적지", 13, MUTED, KR, "middle")

COLS = [(24, 272), (316, 272), (608, 368)]
YBUS, Y1, H1, Y2, H2, Y3, H3 = 192, 320, 72, 440, 80, 560, 52
LBY, LBH, LBW = 216, 32, 136
ccx = CX + CW / 2
# 클라이언트 → CDN(곧장) · 로드 밸런서 한 칸 → 위치·길찾기 서비스
LBX = (COLS[1][0] + COLS[1][1] / 2 + COLS[2][0] + COLS[2][1] / 2) / 2
YBUS2 = LBY + LBH + 20
cdx = COLS[0][0] + COLS[0][1] / 2
d.arrow([(ccx, CY + CH + 2), (ccx, YBUS), (cdx, YBUS), (cdx, Y1 - 4)], MUTED, "ar", 1.4)
d.arrow([(ccx, CY + CH + 2), (ccx, YBUS), (LBX, YBUS), (LBX, LBY - 4)], MUTED, "ar", 1.4)
d.box(LBX - LBW / 2, LBY, LBW, LBH, PAPER2, INFO, 1.0, 6)
d.t(LBX, LBY + 21, "로드 밸런서", 13, INK, KR, "middle", 600)
for cx0, w in COLS[1:]:
    tx = cx0 + w / 2
    d.arrow([(LBX, LBY + LBH + 2), (LBX, YBUS2), (tx, YBUS2), (tx, Y1 - 4)], MUTED, "ar", 1.4)


def side_chip(ax, y, txt, c=MUTED):
    """화살표 x 에서 16px 띄워 오른쪽에 칩을 둔다(칩 폭은 d.chip 과 같은 식)."""
    kr = any("가" <= ch <= "힣" for ch in txt)
    w = len(txt) * (13 * 1.0 if kr else 13 * 0.62) + 14
    d.chip(ax + 16 + w / 2, y, txt, c, 13)

YCHIP = Y1 - 20
side_chip(COLS[0][0] + COLS[0][1] / 2, YCHIP, "z=3 · x=2 · y=2")
side_chip(COLS[1][0] + COLS[1][1] / 2, YCHIP, "41.85, -87.65")
side_chip(COLS[2][0] + COLS[2][1] / 2, YCHIP, "출발 · 도착 주소")


def card(x, y, w, h, title, lines, c=INFO, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, c, 1.0, 6)
    tc = ACC if focal else INK
    d.t(x + w / 2, y + 26, title, 13, tc, fam(title), "middle", 600)
    for j, ln in enumerate(lines):
        d.t(x + w / 2, y + 48 + 20 * j, ln, 13, MUTED, fam(ln), "middle")


# 1행: 위치 서비스 · CDN · 길찾기 서비스
card(COLS[0][0], Y1, COLS[0][1], H1, "CDN", ["가까운 엣지에서 타일 전달"])
card(COLS[1][0], Y1, COLS[1][1], H1, "위치 서비스", ["몇 초마다 위치를 기록"])
card(COLS[2][0], Y1, COLS[2][1], H1, "길찾기 서비스", ["지오코딩 → 경로 계획"])

# 2행
card(COLS[0][0], Y2, COLS[0][1], H2, "객체 저장소", ["미리 만든 정적 타일", "줌 레벨별 이미지"])
card(COLS[1][0], Y2, COLS[1][1], H2, "사용자 위치 DB", ["도로 변경 감지", "실시간 교통 입력"])
GX, GW, PX, PW = 608, 160, 784, 192
card(GX, Y2, GW, H2, "지오코딩", ["주소 → 위도·경도"], INFO)
card(PX, Y2, PW, H2, "경로 계획", ["후보 K → 시간 → 순위", "TRAFFIC_AWARE"], INFO, focal=True)

# 1행 → 2행
for cx0, w in COLS[:2]:
    tx = cx0 + w / 2
    d.arrow([(tx, Y1 + H1 + 2), (tx, Y2 - 4)], MUTED, "ar", 1.4)
mx = COLS[2][0] + COLS[2][1] / 2
ybus2 = Y1 + H1 + 24
for tx in (GX + GW / 2, PX + PW / 2):
    d.arrow([(mx, Y1 + H1 + 2), (mx, ybus2), (tx, ybus2), (tx, Y2 - 4)], MUTED, "ar", 1.4)

# 3행: 지오코딩 DB · 도로 구간 DB
card(GX, Y3, GW, H3, "지오코딩 DB", [], INFO)
card(PX, Y3, PW, H3, "도로 구간 DB", [], INFO)
for tx, ty in ((GX + GW / 2, Y3), (PX + PW / 2, Y3)):
    d.arrow([(tx, Y2 + H2 + 2), (tx, ty - 4)], MUTED, "ar", 1.4)

d.legend(H - 56, [("요청 값", MUTED), ("서비스·저장소", INFO), ("이 절의 초점", ACC)])
d.save("08-02.map-services.svg")
