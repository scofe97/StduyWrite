# 타입 스펙: type-architecture — 웹메일 서버의 수신 경로(위)와 발신 경로(아래)가 가운데 저장 계층 하나를 공유하는 구조. 흐름은 왼쪽에서 오른쪽, 연결은 직각만 쓴다.
# 사실 출처: 추출본 v1.txt 2654~2696행(수신: 로드 밸런서 → SMTP 서버·수락 정책 → 수신 큐 → 메일 처리 일꾼 → 저장 계층 → 온라인은 실시간 서버 WebSocket, 오프라인은 웹 서버 REST),
#   2702~2757행(발신: 로드 밸런서 속도 제한 → 웹 서버 검증·같은 도메인 직접 저장 → 발신 큐·오류 큐 → SMTP 발신 일꾼 → 받는 서버, 재시도), 저장 계층 라벨은 PDF 108·110쪽 그림
#   (메타데이터 DB·검색 저장소·첨부 객체 저장소·최신 메일 캐시). 포트 25 는 RFC 6409, 재시도 30분 이상은 RFC 5321 §4.5.4.1, 25 MB 는 Gmail 도움말(개인 계정 첨부 한도, 넘으면 Drive 링크로 바뀜). 오류 큐는 PDF 110쪽 그림의 4.b 가지(웹 서버에서 갈라져 끝남).
# Layout conventions: 노드 폭 160·높이 84, 가로 stride 200(x=28+200k), 수신 행 y=120·발신 행 y=420, 저장 계층 zone y=252~368 폭 960, 수직 화살표 길이 48. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 704
d = D(W, H, "BYTEBYTEGO · 08-02 §3",
      "큐가 수신과 발신 일꾼을 가르고 저장 계층 하나를 함께 쓴다",
      "받은 메일은 위 줄을, 보낼 메일은 아래 줄을 따라가며 두 줄이 가운데 저장 계층에서 만납니다.",
      "메일 크기 한도는 서비스마다 다르며 Gmail 개인 계정은 첨부 합계 25 MB 입니다")

NW, NH, ST, X0 = 160, 84, 200, 28
YA, YB = 120, 420
ZY, ZH = 252, 116


def node(k, y, title, l1, l2, c=INFO):
    x = X0 + k * ST
    d.box(x, y, NW, NH, PAPER2, c, 1.0, 6)
    d.t(x + NW / 2, y + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + NW / 2, y + 48, l1, 13, MUTED, KR if any("가" <= c_ <= "힣" for c_ in l1) else MONO, "middle")
    d.t(x + NW / 2, y + 68, l2, 13, MUTED, KR if any("가" <= c_ <= "힣" for c_ in l2) else MONO, "middle")
    return x


def side_chip(ax, y, txt, c, right=True):
    """화살표 x 에서 16px 띄워 옆에 칩을 둔다(칩 폭은 d.chip 과 같은 식)."""
    kr = any("가" <= ch <= "힣" for ch in txt)
    w = len(txt) * (13 * 1.0 if kr else 13 * 0.62) + 14
    d.chip(ax + (16 + w / 2) * (1 if right else -1), y, txt, c, 13)


# 저장 계층 zone 을 노드와 화살표보다 먼저 깐다.
d.box(28, ZY, 960, ZH, "#FFFFFF08", RULE, 0.8, 8)
d.t(40, ZY + 24, "저장 계층", 13, ACC, KR, "start", 600)
stores = ["메타데이터 DB", "검색 저장소", "첨부 객체 저장소", "최신 메일 캐시"]
for i, nm in enumerate(stores):
    sx = 40 + i * 240
    d.tone(sx, ZY + 44, 216, 52, ACC, 6, "14", 1.2)
    d.t(sx + 108, ZY + 76, nm, 13, ACC, KR, "middle", 600)

d.t(28, YA - 12, "수신 경로", 13, SOFT, KR, "start")
d.t(28, YB - 12, "발신 경로", 13, SOFT, KR, "start")

# 수신 행
node(0, YA, "SMTP 로드 밸런서", "포트 25", "트래픽 분산")
node(1, YA, "SMTP 서버", "연결 단계 수락 정책", "잘못된 메일 반송")
node(2, YA, "수신 큐", "일꾼과 분리", "급증을 흡수")
node(3, YA, "메일 처리 일꾼", "스팸 검사", "바이러스 검사")
node(4, YA, "클라이언트 전달", "온라인 WebSocket", "오프라인 REST")
for k in range(4):
    x = X0 + k * ST
    d.arrow([(x + NW + 2, YA + NH / 2), (x + ST - 4, YA + NH / 2)], MUTED, "ar", 1.4)
# SMTP 서버 → 저장(큰 첨부), 일꾼 → 저장, 저장 → 클라이언트 전달(당김)
d.arrow([(X0 + 1 * ST + NW / 2, YA + NH + 2), (X0 + 1 * ST + NW / 2, ZY - 4)], INFO, "info", 1.4)
d.arrow([(X0 + 3 * ST + NW / 2, YA + NH + 2), (X0 + 3 * ST + NW / 2, ZY - 4)], OK, "ok", 1.4)
d.arrow([(X0 + 4 * ST + NW / 2, ZY - 2), (X0 + 4 * ST + NW / 2, YA + NH + 4)], WARN, "warn", 1.4, "5 4")
side_chip(X0 + 1 * ST + NW / 2, YA + NH + 24, "큰 첨부", INFO)
side_chip(X0 + 3 * ST + NW / 2, YA + NH + 24, "저장", OK)
side_chip(X0 + 4 * ST + NW / 2, YA + NH + 24, "당김", WARN, right=False)

# 발신 행
node(0, YB, "로드 밸런서", "속도 제한", "HTTPS")
node(1, YB, "웹 서버", "크기 한도 검증", "같은 도메인은 직접 저장")
node(2, YB, "발신 큐", "통과한 메일", "일꾼이 꺼냄")
node(3, YB, "SMTP 발신 일꾼", "스팸 · 바이러스", "재시도 30분 이상")
node(4, YB, "받는 쪽 메일 서버", "MX 조회 뒤 SMTP", "포트 25")
for k in range(4):
    x = X0 + k * ST
    d.arrow([(x + NW + 2, YB + NH / 2), (x + ST - 4, YB + NH / 2)], MUTED, "ar", 1.4)
d.arrow([(X0 + 1 * ST + NW / 2, YB - 2), (X0 + 1 * ST + NW / 2, ZY + ZH + 4)], OK, "ok", 1.4)
d.arrow([(X0 + 3 * ST + NW / 2, YB - 2), (X0 + 3 * ST + NW / 2, ZY + ZH + 4)], OK, "ok", 1.4)
side_chip(X0 + 1 * ST + NW / 2, YB - 24, "저장", OK)
side_chip(X0 + 3 * ST + NW / 2, YB - 24, "보낸 편지함", OK)

# 오류 큐: 웹 서버에서 갈라져 끝나는 가지(발신 일꾼으로 이어지지 않는다)
YE = YB + NH + 52
node(1, YE, "오류 큐", "검증에 실패한 메일", "발신 일꾼으로 가지 않음", BAD)
d.arrow([(X0 + 1 * ST + NW / 2, YB + NH + 2), (X0 + 1 * ST + NW / 2, YE - 4)], BAD, "bad", 1.4)
side_chip(X0 + 1 * ST + NW / 2, YB + NH + 26, "실패", BAD)

d.legend(H - 56, [("저장 계층", ACC), ("저장", OK), ("당김", WARN), ("전달 경로", INFO), ("실패", BAD)])
d.save("08-02.mail-paths.svg")
