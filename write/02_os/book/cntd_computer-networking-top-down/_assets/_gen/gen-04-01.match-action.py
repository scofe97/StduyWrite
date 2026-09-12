# 04-01 §6 — 원문 4.2 끝의 일치 후 동작. 장치 네 종이 같은 틀(무엇을 보고 → 무엇을 하나)로 읽힌다.
# 네 행의 일치·동작은 원문의 나열 그대로다. 다섯째 행은 본문의 노트가 04-04 로 이어 둔 것(여러 필드 · 틀은 같다)이라 INFO 로 구분했다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 행은 장치, 열은 일치·동작. 라우터 행의 일치 칸이 focal 이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 508
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §6",
      "무엇을 보고 무엇을 하나",
      "원문이 절을 닫으며 나열한 장치 넷. 목적지 주소를 조회해 출력 포트로 보내는 라우터의 일은 이 일반적 추상의 특수한 경우다.",
      "일치의 폭만 넓어지고 틀은 그대로입니다")

C0, C0W = 24, 232
C1, C1W = 272, 332
C2, C2W = 620, 356
HY, RH, RS = 108, 40, 48
ROWS = [("라우터",         "목적지 IP 주소",                         "지정된 출력 포트로",              True,  False),
        ("링크 층 스위치", "링크 층 목적지 주소",                    "패브릭으로 보내는 것 외에 여러 동작", False, False),
        ("방화벽",         "출발지·목적지 IP 와 트랜스포트 포트 조합", "버림",                            False, False),
        ("NAT",            "트랜스포트 포트 번호",                   "포트 번호를 다시 쓰고 전달",       False, False),
        ("일반화 포워딩 → 04-04", "헤더의 여러 필드",                 "틀은 같습니다",                   False, True)]

for x, w, lab in ((C0, C0W, "장치"), (C1, C1W, "일치 — 무엇을 보나"), (C2, C2W, "동작 — 무엇을 하나")):
    d.box(x, HY, w, RH, PAPER2, RULE, 0.9)
    d.t(x + w / 2, HY + 26, lab, 13, INK, KR, "middle", 600)

for i, (dev, match, action, focal, note) in enumerate(ROWS):
    y = HY + RH + 8 + i * RS
    c = INFO if note else INK
    d.box(C0, y, C0W, RH, PAPER2, RULE, 0.9)
    d.t(C0 + 16, y + 26, dev, 13, c, KR, "start", 600)
    if focal:
        d.tone(C1, y, C1W, RH, ACC, 6, "14", 1.4)
        d.t(C1 + C1W / 2, y + 26, match, 13, ACC, KR)
    else:
        d.box(C1, y, C1W, RH, PAPER2, RULE, 0.9)
        d.t(C1 + C1W / 2, y + 26, match, 13, c, KR)
    d.box(C2, y, C2W, RH, PAPER2, RULE, 0.9)
    d.t(C2 + 16, y + 26, action, 13, MUTED if not note else INFO, KR, "start")

BY = HY + RH + 8 + 5 * RS + 16
d.line(24, BY, 976, BY, RULE, 0.8)
d.t(24, BY + 26, "전통적 포워딩은 목적지 주소 하나만 봅니다. 일반화 포워딩은 여러 필드를 보는데, 틀은 그대로라 같은 하드웨어 위에 더 많은 정책이 얹힙니다.", 13, MUTED, KR, "start")

d.legend(H - 44, [("이 편이 다룬 경우", ACC), ("04-04 가 이어받는 것", INFO), ("원문의 나열", MUTED)])
d.save("04-01.match-action.svg")
