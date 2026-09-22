# 01-02.chapter-overview — 이 편을 "새 연결의 값과 남는 상태를 읽는 순서"로 보는 지도
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
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
# 이력: 2026-09-21 편의 역할을 "신뢰성의 비용 세기"에서 "새 연결·재사용·남는 상태의 운영 판단"으로 바꾸며
#       네 칸을 다시 짰다. 붉은 칸은 §4(12패킷)에서 §2(새 연결의 값)로 옮겼다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, KR, MONO

W, H = 1000, 392   # 캔버스 상한 준수 (CARD_W 는 W 에서 파생)
X0, GAP, CARD_Y, CARD_H = 12, 26, 132, 196
CARD_W = (W - 48 - X0 - GAP * 3) / 4

d = D(W, H, "CHAPTER MAP · 01-02",
      "HTTP 요청 아래의 연결 — 비용·상태·판단을 읽는 순서",
      "01-02편의 전체 구조. HTTP 요청 하나가 TCP 연결과 TLS 위에서 차례로 성공해야 한다는 데서 출발해, "
      "새 연결이 매번 치르는 절차와 재사용의 의미를 보고, 연결을 닫은 뒤 남는 상태를 운영 신호로 읽은 다음, "
      "TLS·이름·UDP 로 이어진다. 새 연결과 재사용의 차이가 중심이다.",
      lead="세 단계 성공 → 새 연결의 값 → 닫은 뒤 남는 상태 → 얹고 고르기")

CARDS = [("§1",    "요청이 지나는 단계", "TCP · TLS · HTTP 차례로",  INFO,
          ["· 단계마다 다른 실패", "· 시간 제한도 단계별", "· curl 한 줄로 보기"]),
         ("§2",    "새 연결의 값",       "수립 · 전송 · 종료를 매번", BAD,
          ["· 캡처로 세 구간 보기", "· 패킷 수와 시간은 별개", "· 재사용이 나눠 내는 값"]),
         ("§3",    "닫은 뒤 남는 상태",  "TIME-WAIT · CLOSE-WAIT",   INFO,
          ["· 먼저 닫은 쪽의 2MSL", "· 앱이 안 닫은 소켓", "· 생성 빈도로 읽기"]),
         ("§4~§6", "얹고 고르기",        "TLS · 이름 셋 · UDP",      OK,
          ["· TLS — 합의 한 번 더", "· DNS·SNI·Host 의 목적", "· UDP — 앱이 떠안는 책임"])]

for i, (tag, title, sub, c, bullets) in enumerate(CARDS):
    x = X0 + (CARD_W + GAP) * i
    cx = x + CARD_W / 2
    d.t(cx, 118, tag, 9, SOFT, MONO)
    d.tone(x, CARD_Y, CARD_W, CARD_H, c, 6, "10", 1.4)
    d.t(cx, 166, title, 14, c, KR, "middle", 600)
    d.line(x + 18, 182, x + CARD_W - 18, 182, f"{c}44", 0.9)
    d.t(cx, 206, sub, 11, INK)
    for j, b in enumerate(bullets):
        d.t(x + 18, 236 + j * 24, b, 11, MUTED, KR, "start")
    if i < len(CARDS) - 1:
        d.path(f"M {x+CARD_W+3} {CARD_Y+CARD_H/2} L {x+CARD_W+GAP-4} {CARD_Y+CARD_H/2}",
               MUTED, 1.6, m="ar")

# 하단 해설(붉은 칸이 결론)은 도식 앞 본문 문단이 말한다 — 뺐다
d.legend(352, [("도입·전개", INFO), ("핵심·결론", BAD), ("다음으로 이어짐", OK)])
d.save("01-02.chapter-overview.svg")
print("ok chapter-overview")
