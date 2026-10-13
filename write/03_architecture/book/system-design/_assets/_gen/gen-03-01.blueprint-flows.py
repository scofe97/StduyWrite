# 타입 스펙: type-process — 개략 설계의 두 흐름(피드 발행·피드 조회)을 같은 열 위치에 놓고, 발행이 쓰는 뉴스 피드 캐시를 조회가 읽는 자리를 잇는다.
# 사실 출처: 추출본 v2.txt 769~774행·2989~2993행(두 흐름), 2999~3030행(POST /v1/me/feed · GET /v1/me/feed · 로드 밸런서 · 웹 서버 · 게시·팬아웃·알림 서비스 · 뉴스 피드 서비스 · 뉴스 피드 캐시는 피드 ID 저장)
# Layout conventions: 노드 폭 144·높이 56, 열 x=24·208·392·576·760(stride 184), 발행 줄 y=124·196·268(stride 72), 조회 줄 y=372, 분기 버스 x=556. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 524
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 03-01 §3",
      "개략 설계는 피드 발행과 피드 조회 두 흐름으로 나뉜다",
      "발행은 사용자가 POST /v1/me/feed 를 보내 게시 서비스·팬아웃 서비스·알림 서비스로 갈라지고, 조회는 GET /v1/me/feed 가 뉴스 피드 서비스를 거쳐 뉴스 피드 캐시에서 피드 ID 를 읽는다.",
      "같은 뉴스 피드 캐시를 발행이 쓰고 조회가 읽는다")

NW, NH = 144, 56
XS = (24, 208, 392, 576, 760)
PUB = (124, 196, 268)
BLD = 372


def kr(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


def node(x, y, title, sub, c):
    d.tone(x, y, NW, NH, c, 6, "12", 1.2)
    d.t(x + NW / 2, y + 24, title, 13, c, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 44, sub, 13, MUTED, kr(sub))


def hop(x0, x1, y, c=MUTED, m="ar"):
    d.arrow([(x0 + NW + 2, y), (x1 - 6, y)], c, m, 1.5)


d.t(24, 104, "피드 발행", 13, INK, KR, "start", 600)
d.t(24, 352, "피드 조회", 13, INK, KR, "start", 600)

# 발행 줄
mid = PUB[1]
node(XS[0], mid, "사용자", "POST /v1/me/feed", INFO)
node(XS[1], mid, "로드 밸런서", "트래픽 분산", OK)
node(XS[2], mid, "웹 서버", "서비스로 전달", OK)
hop(XS[0], XS[1], mid + 28)
hop(XS[1], XS[2], mid + 28)

node(XS[3], PUB[0], "게시 서비스", "저장 · 캐시", OK)
node(XS[3], PUB[1], "알림 서비스", "푸시 알림", OK)
node(XS[3], PUB[2], "팬아웃 서비스", "친구 피드로", OK)
BUS = 556
for y in (PUB[0], PUB[2]):
    d.arrow([(XS[2] + NW + 2, mid + 28), (BUS, mid + 28), (BUS, y + 28), (XS[3] - 6, y + 28)], MUTED, "ar", 1.5)
hop(XS[2], XS[3], mid + 28)

node(XS[4], PUB[0], "게시 DB · 캐시", "글", INFO)
node(XS[4], PUB[2], "뉴스 피드 캐시", "피드 ID", ACC)
for y in (PUB[0], PUB[2]):
    hop(XS[3], XS[4], y + 28)

# 조회 줄
node(XS[0], BLD, "사용자", "GET /v1/me/feed", INFO)
node(XS[1], BLD, "로드 밸런서", "트래픽 분산", OK)
node(XS[2], BLD, "웹 서버", "서비스로 전달", OK)
node(XS[3], BLD, "뉴스 피드 서비스", "캐시에서 읽기", OK)
node(XS[4], BLD, "뉴스 피드 캐시", "피드 ID", ACC)
for i in range(4):
    hop(XS[i], XS[i + 1], BLD + 28)

# 발행이 쓴 캐시를 조회가 읽는다
cx = XS[4] + NW / 2
d.arrow([(cx, PUB[2] + NH + 4), (cx, BLD - 6)], ACC, "acc", 1.6, "5 4")
d.chip(cx - 80, (PUB[2] + NH + BLD) / 2, "쓰기 → 읽기", ACC, 13)

d.legend(H - 56, [("서비스", OK), ("사용자 · 저장소", INFO), ("발행이 쓰고 조회가 읽는 자리", ACC)])
d.save("03-01.blueprint-flows.svg")
