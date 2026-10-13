# 타입 스펙: type-process — 일곱 절(캐시·CDN·무상태·데이터 센터·메시지 큐·샤딩·전체 정리)을 절마다 같은 슬롯(번호·이름·한 줄 문제·값 둘)으로 반복해 단계 지도로 보인다.
# 사실 출처: 추출본 v2.txt 219~547행. 캐시 exptime 3600 은 PDF 15쪽 코드 조각(cache.set('myKey','hi there',3600*SECONDS)), 센터 x%·(100−x)% 는 v2.txt 371~374행,
#   user_id % 4 는 v2.txt 467~471행, 샤드 0~3 은 PDF 29쪽 그림, A·B 가 서버 1·2 로 갈리는 서술은 v2.txt 346~354행.
#   max-age=86400·Age: 3600 은 설계 가정(CloudFront 기본 TTL 24시간 = 86400초, RFC 9111 §5.1 Age 는 초 단위).
# Layout conventions: 카드 폭 124·높이 176, 카드 stride 140(폭 124 + 간격 16), 카드 위쪽 y=104, 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 372
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 01-02",
      "수백만 사용자까지 일곱 단계로 덧붙인다",
      "읽기를 줄이고, 웹 계층과 센터를 늘리고, 느린 일과 데이터를 나눈 뒤 전체 구조로 묶는다.",
      "절마다 문제 하나와 값 둘")

Y_TOP, H_CARD, W_CARD, GAP, X0 = 104, 176, 124, 16, 16


def fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in txt) else MONO


steps = [
    ("01", "캐시", "DB 읽기를 줄임", "get myKey", "exptime 3600", INFO),
    ("02", "CDN", "정적 파일을 가까이", "max-age=86400", "Age: 3600", INFO),
    ("03", "무상태 웹", "세션을 밖으로", "A → 서버 1", "A → 서버 2", ACC),
    ("04", "데이터 센터", "지역 장애 대비", "US-East x%", "US-West 100−x%", OK),
    ("05", "메시지 큐", "느린 일을 떼어냄", "publish", "consume", WARN),
    ("06", "샤딩", "DB 를 수평으로", "user_id % 4", "샤드 0~3", WARN),
    ("07", "전체 정리", "여덟 가지 원칙", "원칙 8개", "로그·메트릭", MUTED),
]
for i, (num, title, sub, c1, c2, col) in enumerate(steps):
    x = X0 + i * (W_CARD + GAP)
    cx = x + W_CARD / 2
    if col == ACC:
        d.tone(x, Y_TOP, W_CARD, H_CARD, ACC, r=6, op="12", sw=1.4)
    else:
        d.box(x, Y_TOP, W_CARD, H_CARD, PAPER2, RULE, sw=0.9, r=6)
    d.chip(x + 28, Y_TOP + 24, num, col, size=11)
    d.t(cx, Y_TOP + 68, title, 14, INK, KR, "middle", 600)
    d.t(cx, Y_TOP + 92, sub, 13, MUTED, KR, "middle")
    d.line(x + 12, Y_TOP + 108, x + W_CARD - 12, Y_TOP + 108, RULE, 0.6)
    d.box(x + 8, Y_TOP + 120, W_CARD - 16, 44, PAPER, RULE, sw=0.7, r=4)
    d.t(cx, Y_TOP + 138, c1, 13 if fam(c1) == KR else 11, col, fam(c1), "middle", 600)
    d.t(cx, Y_TOP + 156, c2, 13 if fam(c2) == KR else 11, MUTED, fam(c2), "middle")
    if i < len(steps) - 1:
        ax = x + W_CARD
        d.arrow([(ax + 2, Y_TOP + 88), (ax + GAP - 2, Y_TOP + 88)], MUTED, "ar", 1.2)

d.legend(H - 56, [("읽기 줄이기", INFO), ("센터 늘리기", OK), ("일·데이터 나누기", WARN), ("핵심 전제", ACC)])
d.save("01-02.chapter-overview.svg")
