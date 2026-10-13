# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: 추출본 v1.txt 3507~3605행(쿼드트리 · Yelp 근처 식당 찾기, 사업장 2억 곳·잎 100 곳 기준·재구축 수 분·`LIKE '01%'`)과 3847~3890행(색인 1.71GB·읽기 복제본 권고),
#   PDF 143~145쪽 그림(서비스 둘·복제본 셋·주 DB 하나·경로 /search/nearby·/businesses/{id}), 쪽 번호는 그림 아래 인쇄 쪽 142~144 + 1.
# Layout conventions: 카드 폭 296·높이 148, 가로 stride 320(x=40+320k), 행 y=112·308, 행 간 화살표는 ㄷ자(수직→수평→수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 516
d = D(W, H, "BYTEBYTEGO · 09-01",
      "근처 식당 한 번의 검색이 지나는 여섯 자리와 값",
      "행을 전부 비교하는 질의에서 격자 색인, 메모리 트리, 읽기 복제본까지 같은 질의가 지나는 자리를 값으로 따라갑니다.",
      "사업장 2억 곳과 색인 1.71 GB 는 설계 가정입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


CW, CH, STRIDE, X0, Y0, Y1 = 296, 148, 320, 40, 112, 308
cards = [
    ("§1", "근접 질의가 느린 까닭", "2억 행 · 거리 2억 번", "위도·경도 열을 행마다 비교", "색인으로 못 좁힘", INFO),
    ("§2", "서비스 둘", "LBS 읽기 · 사업장 쓰기", "복제본 3 · 주 DB 1", "/search/nearby", INFO),
    ("§3", "지오해시", "0110 · LIKE '01%'", "경도·위도 비트를 번갈아", "경계는 이웃 칸으로", INFO),
    ("§4", "쿼드트리", "100 초과 → 넷으로", "잎 100 이하 · 메모리", "이웃 잎에서 채움", INFO),
    ("§5", "트리 재구축", "몇 분 · 트래픽 불가", "서버 일부씩 배포", "나머지가 요청을 받음", INFO),
    ("§6", "복제본 대 샤딩", "1.71 GB → 복제본", "한 서버 메모리에 들어감", "샤딩 논리는 불필요", ACC),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    row, col = divmod(k, 3)
    x = X0 + col * STRIDE
    y = Y0 if row == 0 else Y1
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, y, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, y + 28, tag, 13, SOFT, MONO, "start")
    d.t(cx, y + 28, title, 13, c if c == ACC else INK, _kr(title), "middle", 600)
    d.line(x + 12, y + 44, x + CW - 12, y + 44, RULE, 0.6)
    d.t(cx, y + 76, v1, 13, c if c == ACC else INFO, _kr(v1), "middle", 600)
    d.t(cx, y + 100, v2, 13, INK, _kr(v2), "middle")
    d.t(cx, y + 128, sub, 13, MUTED, _kr(sub), "middle")
    if col < 2:
        d.arrow([(x + CW + 2, y + CH / 2), (x + STRIDE - 4, y + CH / 2)], MUTED, "ar", 1.4)

xe = X0 + 2 * STRIDE + CW / 2
xs = X0 + CW / 2
d.arrow([(xe, Y0 + CH + 2), (xe, Y0 + CH + 24), (xs, Y0 + CH + 24), (xs, Y1 - 4)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("09-01.chapter-overview.svg")
