# 01-01.chapter-overview — 이 장을 "실패 → 언어 → 경쟁 → 남은 것" 네 박자로 읽는 지도
# 본문 요구: 본문이 도식 앞에서 규격을 직접 적어 둔다 — "붉은색이 칠해진 3단계가 이 장에서
#           가장 자주 오해되는 자리입니다. OSI 는 표준 경쟁에서 졌는데도 용어만 살아남았다는
#           사실이 그것입니다. 마지막 칸이 초록인 이유는 그 둘(4계층 모델과 Go 서버)이 이 장을
#           넘어 다음 편들로 이어지기 때문입니다." 그래서 색은 장식이 아니라 본문이 지정한 값이다.
#           칸 위 머리글의 절 번호도 "각 칸 위의 머리글에 그 대목을 다루는 절 번호가 붙어 있다"는
#           문장이 요구한 것이라, 임의로 떼면 본문이 틀려진다.
# 타입 스펙: type-process.md — 단계마다 같은 의미 슬롯(절 번호 · 이름 · 한 줄 요약 · 항목 셋)이
#           같은 자리에 반복된다(semantic-patterns 의 "Stage framework with semantic slots").
#           화살표는 데이터가 아니라 읽는 순서를 나른다 — 01-02.chapter-overview 와 같은 판단이다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, KR, MONO

W, H = 1080, 406
X0, GAP, CARD_Y, CARD_H = 12, 26, 132, 196
CARD_W = (W - 48 - X0 - GAP * 3) / 4

d = D(W, H, "CHAPTER MAP · 01-01",
      "네트워킹 역사와 OSI 모델 — 네 박자로 읽는 지도",
      "01-01편의 전체 구조. 단일 프로토콜 NCP의 실패에서 출발해 그것을 설명하는 언어(OSI "
      "7계층)를 얻고, 표준 경쟁에서 TCP/IP가 이겼으며, 그럼에도 OSI의 용어만 남아 오늘까지 "
      "쓰인다는 네 단계로 이어진다.",
      lead="단일 프로토콜의 실패 → 그것을 설명하는 언어 → 표준 경쟁 → 남은 것")

CARDS = [("§1",   "실패",      "하나가 다 하던 NCP가 무너졌다", INFO,
          ["· 네트워크가 다양해짐", "· 한 프로토콜이 병목", "· 신뢰성과 전달을 쪼갬"]),
         ("§2",   "개념 틀",   "책임을 나누는 언어를 얻었다",   INFO,
          ["· OSI 7계층", "· 캡슐화 — 감싸고 벗긴다", "· 각 계층은 자기 헤더만"]),
         ("§3",   "표준 경쟁", "OSI 는 졌는데 용어는 남았다",   BAD,
          ["· TCP/IP 가 실무 표준", "· OSI 는 교육 도구로", "· 가장 자주 오해되는 자리"]),
         ("§4·5", "남은 것",   "4계층 모델과 실습으로 이어진다", OK,
          ["· OSI 7 ↔ TCP/IP 4", "· 이름으로 부른다", "· 다음 편들의 토대"])]

for i, (tag, title, sub, c, bullets) in enumerate(CARDS):
    x = X0 + (CARD_W + GAP) * i
    cx = x + CARD_W / 2
    d.t(cx, 118, tag, 9, SOFT, MONO)
    d.tone(x, CARD_Y, CARD_W, CARD_H, c, 6, "10", 1.4)
    d.t(cx, 166, title, 14, c, KR, "middle", 600)
    d.line(x + 18, 182, x + CARD_W - 18, 182, f"{c}44", 0.9)
    d.t(cx, 206, sub, 11, INK)
    for j, b in enumerate(bullets):
        d.t(x + 18, 236 + j * 24, b, 10, MUTED, KR, "start")
    if i < len(CARDS) - 1:
        d.path(f"M {x+CARD_W+3} {CARD_Y+CARD_H/2} L {x+CARD_W+GAP-4} {CARD_Y+CARD_H/2}",
               MUTED, 1.6, m="ar")

d.t(W / 2, 350, "붉은 칸이 이 장에서 가장 자주 오해되는 자리입니다 — 졌지만 용어는 살아남았습니다.",
    10, MUTED)
d.legend(362, [("도입·전개", INFO), ("핵심·결론", BAD), ("다음으로 이어짐", OK)])
d.save("01-01.chapter-overview.svg")
print("ok chapter-overview")
