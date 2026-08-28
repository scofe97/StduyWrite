# 01-02.chapter-overview — 이 편을 "신뢰성의 비용을 세는 순서"로 읽는 지도
# 본문 요구: 이 편의 결론은 §4 의 "12패킷 중 내용은 둘뿐"이다. 그래서 네 칸 중 셋째 칸만 붉고,
#           아래 한 줄이 "붉은 칸이 이 편의 결론"이라고 못 박는다. 마지막 칸에서 TLS 와 UDP 로
#           길이 갈리는 것도 같은 축이다 — 값을 더 낼지 안 낼지의 갈림이라 §5·6 이 한 칸에 든다.
# 타입 스펙: type-process.md — 단계 머리 + 한 줄 체인. 칸마다 같은 의미 슬롯(절 번호 · 이름 ·
#           한 줄 요약 · 꼬리표)이 같은 자리에 반복된다(semantic-patterns 의 "Stage framework
#           with semantic slots"). 화살표는 데이터가 아니라 읽는 순서를 나른다.
#           2026-08-28 type-data-flow 에서 옮겼다 — data-flow 정본은 "who does what at each
#           stage" 와 role-scoped lane 을 전제로 하는데, 편 지도에는 주체도 레인도 없다.
#           엄밀히는 두 정본 다 주체 기반이라 편 지도는 표의 공백에 가깝고, 주체 없이도 맞는
#           유일한 라우팅 규칙이 위 semantic-patterns 한 줄이라 그쪽을 따랐다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, KR, MONO

W, H = 1080, 406
X0, GAP, CARD_Y, CARD_H = 12, 26, 132, 196
CARD_W = (W - 48 - X0 - GAP * 3) / 4

d = D(W, H, "CHAPTER MAP · 01-02",
      "Transport 계층 해부 — 신뢰성의 비용을 세는 순서",
      "01-02편의 전체 구조. 무엇이 오가는지 보고, 연결을 세우는 절차를 익히고, 그 비용을 패킷 "
      "수로 센 뒤, 그 값을 낼지 말지 고르는 네 단계로 이어진다. 12패킷 중 데이터는 2개뿐이라는 "
      "사실이 결론이다.",
      lead="무엇이 오가나 → 연결을 세운다 → 비용을 센다 → 값을 낼지 고른다")

CARDS = [("§1·2", "무엇이 오가나",   "HTTP 요청과 TCP 헤더 필드",   INFO,
          ["· curl -vvv 로 본 L7", "· seq·ack 가 순서를 보증", "· 윈도우가 흐름을 조절"]),
         ("§3",   "연결을 세운다",    "3-way 로 열고 4-way 로 닫는다", INFO,
          ["· 번호가 양방향으로", "· 11개 상태를 오간다", "· TIME-WAIT 가 포트를 문다"]),
         ("§4",   "비용을 센다",      "12패킷 중 내용은 둘뿐",       BAD,
          ["· 나머지 열은 절차", "· tcpdump 로 실측", "· 이 편의 결론"]),
         ("§5·6", "값을 낼지 고른다", "더 내면 TLS, 안 내면 UDP",    OK,
          ["· TLS — 핸드셰이크 한 번 더", "· UDP — 확인을 포기", "· 같은 저울의 반대편"])]

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

d.t(W / 2, 350, "붉은 칸이 이 편의 결론입니다 — 마지막 칸에서 길이 갈립니다.", 10, MUTED)
d.legend(362, [("도입·전개", INFO), ("핵심·결론", BAD), ("다음으로 이어짐", OK)])
d.save("01-02.chapter-overview.svg")
print("ok chapter-overview")
