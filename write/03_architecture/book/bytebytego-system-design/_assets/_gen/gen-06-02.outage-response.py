# 타입 스펙: type-process — 대형 장애에서 지나간 단계 다섯 칸. 칸마다 그 사건의 실제 값(위)과 그 단계에 놓을 장치(아래)가 같은 자리에 반복된다(Stage framework with semantic slots).
# 사실 출처: 사건의 값 = 추출본 v1.txt 1265~1318행과 쪽 49~50(금요일 21시, 운영 대시보드 모든 줄이 0, 상사의 전화로 전체 중단 확인, 50명이 10시간, 클라우드 관리 소프트웨어의 확인창 버그, 메모리캐시 풀 하나를 끄려다 전체 종료, 전체 설명은 받지 못하고 코드 구조는 추측만 가능)
#   · 장치 = Google SRE Book "Managing Incidents"(선언 기준 셋, 지휘·작업·소통·계획 네 역할, 작업 담당만 시스템을 바꿈)와 "Postmortem Culture"(비난 없는 사후 검토, 사후 검토를 열 기준).
# Layout conventions: 카드 폭 176·높이 212, 가로 stride 192(x=24+192k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 992, 392
d = D(W, H, "BYTEBYTEGO · 06-02 §3",
      "지표가 전부 0이던 밤과 그 뒤의 다섯 단계",
      "윗줄은 그 사건에서 있었던 값이고 아랫줄은 그 단계에 놓을 장치입니다",
      "일간 사용자 약 3,000만 명 소셜 게임의 장애")

CW, CH, STRIDE, X0, Y0 = 176, 212, 192, 24, 112
cards = [
    ("01", "감지", "금요일 21시", "지표 전부 0", "경보와 대시보드", INFO),
    ("02", "호출 · 선언", "상사의 전화", "전체 중단 확인", "선언 기준 셋", INFO),
    ("03", "역할 분담", "50명 동원", "10시간 복구", "지휘·작업·소통·계획", ACC),
    ("04", "원인", "확인창 버그", "일부 표시 · 전체 종료", "작업 담당만 변경", INFO),
    ("05", "사후 검토", "전체 설명 못 받음", "코드 구조는 추측만", "비난 없는 기록", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, KR, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR, "middle")
    d.line(x + 12, Y0 + 152, x + CW - 12, Y0 + 152, RULE, 0.6)
    d.t(cx, Y0 + 184, sub, 12, WARN, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("역할 분담 초점", ACC), ("사건의 값", INFO), ("그 단계의 장치", WARN)])
d.save("06-02.outage-response.svg")
