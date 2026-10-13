# 타입 스펙: type-architecture — 서비스 N 개가 알림 서버를 부르고, 알림 서버가 캐시·DB 를 읽은 뒤 유형별 큐에 넣으면 작업자가 꺼내 제3자 서비스로 보낸다. 번호가 여섯 단계 순서를 나른다.
# 사실 출처: 추출본 v2.txt 2810~2840행(서비스·알림 서버·캐시·DB·큐·작업자·제3자와 여섯 단계)·2819~2821행(이메일 보내기 API 예), PDF 158쪽 그림(큐 이름 iOS PN·Android PN·SMS·Email, retry on error 화살표),
#   PDF 159쪽 요청 본문 그림(user_id 123456), Apple 문서의 /3/device/<device_token> 경로는 §2 도식과 같은 값.
# Layout conventions: 노드 높이 56·알림 서버 112, 열 x = 24(서비스)·216(알림 서버)·448(큐)·640(작업자)·800(제3자), 행 stride 92(y=164·256·348·440), 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, KR, MONO

W, H = 1000, 664
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 10-01 §5",
      "유형별 큐 뒤에서 작업자가 제3자로 보낸다",
      "알림 서버는 알림을 큐에 넣고 돌아서며, 작업자가 큐에서 꺼내 APNs·FCM·SMS·이메일 서비스로 보낸다. 큐가 유형마다 따로라 한 제공자의 장애가 번지지 않는다.",
      "번호는 알림 한 건이 지나는 여섯 단계")


def fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in txt) else MONO


def node(x, y, w, h, title, sub, c, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.tone(x, y, w, h, c, 6, "10", 1.1)
    d.t(x + w / 2, y + h / 2 - 2, title, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, sub, 13 if fam(sub) == KR else 11, MUTED, fam(sub))


# 서비스 1·2·N — 알림 서버 호출
for y, nm in ((210, "서비스 1"), (302, "서비스 2"), (394, "서비스 N")):
    node(24, y, 108, 56, nm, "API 호출", MUTED)
    d.line(132, y + 28, 160, y + 28, MUTED, 1.4)
d.line(160, 238, 160, 422, MUTED, 1.4)
d.arrow([(160, 330), (212, 330)], MUTED, "ar", 1.4)
d.chip(292, 252, "1 POST /v/email/send", MUTED, 11)

# 알림 서버 · 캐시 · DB
node(216, 274, 152, 112, "알림 서버", "인증 · 검증 · 조회", INFO)
d.arrow([(292, 390), (292, 442)], MUTED, "ar", 1.4)
d.chip(344, 416, "2 조회", MUTED, 13)
node(216, 446, 152, 56, "캐시", "user 123456 · 이메일", INFO)
d.arrow([(292, 506), (292, 542)], MUTED, "ar", 1.4)
node(216, 546, 152, 56, "DB", "사용자 · 알림 설정", INFO)

# 유형별 큐 — 서버 오른쪽 버스에서 갈라진다
d.line(368, 330, 424, 330, MUTED, 1.4)
d.line(424, 192, 424, 468, MUTED, 1.4)
d.chip(396, 308, "3", MUTED, 11)
QUEUES = ((164, "iOS PN 큐", "APNs", "iOS 기기"),
          (256, "Android PN 큐", "FCM", "Android 기기"),
          (348, "SMS 큐", "SMS 서비스", "휴대전화"),
          (440, "이메일 큐", "이메일 서비스", "받는 사람"))
for y, qn, tp, dev in QUEUES:
    cy = y + 28
    d.arrow([(424, cy), (444, cy)], MUTED, "ar", 1.4)
    node(448, y, 128, 56, qn, "알림 이벤트", WARN, focal=(y == 440))
    d.arrow([(576, cy), (636, cy)], MUTED, "ar", 1.4)
    node(640, y, 96, 56, "작업자", "pull · 전송", OK)
    d.arrow([(736, cy), (796, cy)], MUTED, "ar", 1.4)
    node(800, y, 176, 56, tp, "6 → " + dev, MUTED)
d.chip(608, 448, "4", MUTED, 11)
d.chip(768, 448, "5", MUTED, 11)

# 실패하면 같은 큐로 되돌린다
d.arrow([(688, 500), (688, 520), (512, 520), (512, 500)], WARN, "warn", 1.4)
d.chip(600, 538, "재시도", WARN, 13)

d.legend(H - 44, [("서비스·제3자", MUTED), ("알림 서버·저장소", INFO), ("큐", WARN), ("작업자", OK), ("예시 흐름의 큐", ACC)])
d.save("10-01.queue-architecture.svg")
