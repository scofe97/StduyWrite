# 타입 스펙: type-process — 대화 후보 네 줄이 깊이 팔 곳·고수준에서 끝낸 곳·시간만 쓰는 곳으로 갈린다.
# 사실 출처: 추출본 v2.txt 783~795행(상세 설계는 우선순위 높은 구성 요소 선택 · 순위 알고리즘 상세는 시간 낭비), 3036~3066행(피드 발행 상세: 웹 서버의 인증·처리율 제한, 팬아웃 서비스의 쓸 때 밀기·읽을 때 당기기, 나머지 구성 요소는 고수준에서 다룸)
# Layout conventions: 후보 열 x=24 폭 280, 판정 열 x=400 폭 520, 줄 stride 76(y=120~), 노드 높이 56, 화살표 y 는 줄 +28. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 508
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 03-01 §4",
      "상세 설계는 대화 후보 가운데 둘만 깊이 판다",
      "웹 서버는 인증과 처리율 제한, 팬아웃 서비스는 쓸 때 밀기와 읽을 때 당기기로 깊어지고, 게시 서비스와 알림 서비스는 고수준에서 끝나며, 순위 알고리즘 세부는 확장 설계 신호가 없어 접는다.",
      "뉴스 피드 예시의 발행 흐름")

QX, QW = 24, 280
AX, AW = 400, 520
NH, STRIDE, Y0 = 56, 76, 120

d.t(QX, Y0 - 16, "대화 후보", 13, SOFT, KR, "start", 600)
d.t(AX, Y0 - 16, "다음 대화", 13, SOFT, KR, "start", 600)

ROWS = (
    ("웹 서버", "인증 · 처리율 제한", OK),
    ("팬아웃 서비스", "쓸 때 밀기 · 읽을 때 당기기", OK),
    ("게시 · 알림 서비스", "고수준에서 다룸", None),
    ("순위 알고리즘 세부", "확장 설계 신호 없음", BAD),
)
for i, (q, a, c) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    d.box(QX, y, QW, NH, PAPER2, RULE, 0.9, 6)
    d.t(QX + QW / 2, y + 34, q, 14, INK, KR, "middle", 600)
    if c is None:
        d.box(AX, y, AW, NH, PAPER2, RULE, 0.9, 6)
        d.t(AX + AW / 2, y + 34, a, 14, MUTED, KR, "middle", 600)
        d.arrow([(QX + QW + 2, y + 28), (AX - 6, y + 28)], MUTED, "ar", 1.5)
    else:
        d.tone(AX, y, AW, NH, c, 6, "12", 1.2)
        d.t(AX + AW / 2, y + 34, a, 14, c, KR, "middle", 600)
        m = {OK: "ok", BAD: "bad"}[c]
        d.arrow([(QX + QW + 2, y + 28), (AX - 6, y + 28)], c, m, 1.6)

d.legend(H - 56, [("깊이 파는 곳", OK), ("고수준에서 끝", MUTED), ("접는 곳", BAD)])
d.save("03-01.deep-dive-pick.svg")
