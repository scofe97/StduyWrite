# 타입 스펙: type-architecture — 사용자 요청이 DNS·CDN·로드 밸런서를 지나 웹 서버에 닿고, 웹 서버가 캐시·샤드 DB·NoSQL·메시지 큐로 갈라지는 최종 구조. 존은 데이터 센터와 도구.
# 사실 출처: 추출본 v2.txt 437~441행(메시지 큐·도구 추가)·502~504행(샤딩과 NoSQL), PDF 31쪽 그림 위쪽 호스트 이름 www.mysite.com·api.mysite.com,
#   PDF 23쪽 그림의 DC1 US-East 와 DC2 US-West, 캐시 get/exptime 은 §1 도식과 같은 값, 정적 파일 경로는 §2 도식의 GET /image.png.
# Layout conventions: 노드 높이 56~64, 세로 stride 132(웹 서버 행 y=344, 저장소 행 y=476), DC1 존 폭 700, 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 736
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 01-02 §7",
      "수백만 사용자를 받는 구조",
      "정적 파일은 CDN 이, 요청은 로드 밸런서가 받고, 데이터 센터 안에서는 웹 서버가 캐시·샤드·큐로 일을 가른다.",
      "화살표 위 값은 앞 절의 도식과 같은 값")


def fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in txt) else MONO


def node(x, y, w, h, title, sub, c, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.tone(x, y, w, h, c, 6, "10", 1.1)
    d.t(x + w / 2, y + h / 2 - 2, title, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, sub, 13 if fam(sub) == KR else 11, MUTED, fam(sub))


# 상단 한 줄 — DNS · 사용자 · CDN
node(24, 96, 160, 64, "DNS", "geoDNS", INFO)
node(340, 96, 320, 64, "사용자", "브라우저 · 모바일 앱", MUTED)
node(816, 96, 160, 64, "CDN", "max-age=86400", INFO)
d.arrow([(336, 124), (190, 124)], MUTED, "ar", 1.4)
d.arrow([(664, 124), (810, 124)], MUTED, "ar", 1.4)
d.chip(738, 98, "GET /image.png", MUTED, 11)

# 로드 밸런서 — 사용자에서 ㄱ자 경로
node(48, 212, 176, 56, "로드 밸런서", "웹 서버 N 대로 분산", INFO)
d.arrow([(420, 164), (420, 196), (136, 196), (136, 208)], MUTED, "ar", 1.4)
d.chip(250, 170, "www.mysite.com", MUTED, 11)
d.arrow([(580, 164), (580, 240), (228, 240)], MUTED, "ar", 1.4)
d.chip(500, 214, "api.mysite.com", MUTED, 11)
d.arrow([(228, 256), (864, 256), (864, 296)], MUTED, "ar", 1.4)
d.chip(700, 230, "100−x%", MUTED, 11)
d.chip(170, 288, "x%", MUTED, 11)

# DC1 존
d.box(24, 300, 700, 268, PAPER2, RULE, 0.9, 8)
d.t(712, 320, "DC1 · US-EAST · x%", 9, SOFT, MONO, "end")

# 행 a — 웹 서버 → 메시지 큐 → 워커
node(48, 344, 176, 64, "웹 서버", "무상태 · 세션은 밖", OK)
node(312, 344, 176, 64, "메시지 큐", "사진 처리 작업", WARN)
node(576, 344, 124, 64, "워커", "사진 처리", OK)
d.arrow([(228, 376), (308, 376)], MUTED, "ar", 1.4)
d.chip(268, 350, "publish", MUTED, 11)
d.arrow([(492, 376), (572, 376)], MUTED, "ar", 1.4)
d.chip(532, 350, "consume", MUTED, 11)
d.arrow([(136, 272), (136, 340)], MUTED, "ar", 1.4)

# 행 b — 캐시 · 샤드 DB · NoSQL
node(48, 476, 176, 64, "캐시", "get myKey · 3600", WARN)
node(312, 476, 176, 64, "샤드 DB", "user_id % 4 → 샤드 0~3", WARN, focal=True)
node(776, 476, 176, 64, "NoSQL", "비관계형 기능", WARN)
d.arrow([(100, 412), (100, 472)], MUTED, "ar", 1.4)
d.arrow([(160, 412), (160, 456), (400, 456), (400, 472)], MUTED, "ar", 1.4)
d.arrow([(212, 412), (212, 440), (840, 440), (840, 472)], MUTED, "ar", 1.4)
d.arrow([(900, 416), (900, 472)], MUTED, "ar", 1.4)

# 오른쪽 — DC2
d.box(752, 300, 224, 112, PAPER2, RULE, 0.9, 8)
d.t(764, 320, "DC2 · US-WEST · 100−x%", 9, SOFT, MONO, "start")
d.t(864, 364, "같은 구성", 13, INK, KR, "middle", 600)
d.t(864, 388, "센터 간 데이터 복제", 13, MUTED, KR, "middle")

# 도구 존
d.box(24, 616, 700, 48, PAPER2, RULE, 0.9, 8)
d.t(36, 634, "TOOLS", 9, SOFT, MONO, "start")
for cx, name in ((200, "로그"), (340, "메트릭"), (480, "모니터링"), (620, "자동화")):
    d.chip(cx, 648, name, MUTED, 13)
d.arrow([(374, 612), (374, 572)], MUTED, "ar", 1.4)

d.legend(H - 44, [("입구", INFO), ("애플리케이션", OK), ("저장소", WARN), ("나눈 데이터", ACC)])
d.save("01-02.scaled-architecture.svg")
