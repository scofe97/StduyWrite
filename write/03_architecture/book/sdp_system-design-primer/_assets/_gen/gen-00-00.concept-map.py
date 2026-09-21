# README 맨 위 전체 지도 — primer 가 다루는 부품을 요청 하나가 지나가는 경로 위에 놓는다.
# 본문이 "요청 하나가 클라이언트에서 데이터까지 가는 길에 부품이 놓이고, 장 번호가 그 부품에 붙는다"고 말한다.
# 타입 스펙: type-architecture — 구성요소와 연결. 주 흐름은 좌→우, zone 셋(진입 경로 · 애플리케이션 · 데이터).
#           위아래 띠는 구성요소가 아니라 모든 구성요소에 걸리는 장(02 · 08 · 09)이라 zone 밖에 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 580
d = D(W, H, "THE SYSTEM DESIGN PRIMER · CONCEPT MAP",
      "요청 하나가 지나가는 길 위의 부품",
      "클라이언트의 요청이 DNS · CDN · 로드 밸런서를 거쳐 앱 서버에 닿고, 캐시와 데이터베이스와 메시지 큐로 갈라지는 경로. 각 부품에 primer 의 장 번호를 붙였고, 트레이드오프 · 통신 · 보안은 모든 부품에 걸리는 띠로 그렸다.",
      "부품마다 붙은 숫자가 이 인덱스의 장 번호입니다")

ROW, NH = 96, 56                       # 행 stride 96, 노드 높이 56
Y = [184, 184 + ROW, 184 + 2 * ROW]    # 184 · 280 · 376
ZY, ZH = Y[0] - 32, Y[2] + NH + 16 - (Y[0] - 32)

def zone(x, w, label):
    d.o.append(f'<rect x="{x}" y="{ZY}" width="{w}" height="{ZH}" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.12)" stroke-width="0.8" stroke-dasharray="4 3"/>')
    d.t(x + 16, ZY + 20, label, 12, SOFT, KR, "start", 600)

def node(x, y, w, ch, title, sub):
    d.box(x, y, w, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + w - 10, y + 17, ch, 11, INFO, MONO, "end", 600)
    d.t(x + 12, y + 25, title, 13, INK, KR, "start", 600)
    d.t(x + 12, y + 44, sub, 12, MUTED, KR, "start")

# 띠 — 02 (focal)
d.o.append(f'<rect x="24" y="96" width="832" height="36" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(40, 119, "02", 11, ACC, MONO, "start", 600)
d.t(68, 119, "트레이드오프", 13, ACC, KR, "start", 600)
for i, pair in enumerate(("성능 · 확장성", "지연 · 처리량", "가용성 · 일관성")):
    d.chip(252 + i * 160, 114, pair, MUTED, 12, 10)

# zone
zone(152, 200, "진입 경로")
zone(376, 236, "애플리케이션")
zone(636, 220, "데이터")

# 연결선 먼저 (z-order)
d.arrow([(76, Y[1]), (76, Y[0] + 28), (168, Y[0] + 28)], MUTED, "ar", 1.4)            # client → DNS
d.arrow([(128, Y[1] + 28), (168, Y[1] + 28)], MUTED, "ar", 1.4)                      # client → LB
d.arrow([(76, Y[1] + NH), (76, Y[2] + 28), (168, Y[2] + 28)], MUTED, "ar", 1.4)      # client → CDN
d.arrow([(336, Y[1] + 28), (392, Y[1] + 28)], MUTED, "ar", 1.4)                      # LB → app
d.arrow([(494, Y[1]), (494, Y[0] + NH)], SOFT, "soft", 1.0, "4 3")                   # app → discovery
d.arrow([(494, Y[1] + NH), (494, Y[2])], SOFT, "soft", 1.0, "4 3")                   # app → queue
d.arrow([(596, Y[1] + 16), (624, Y[1] + 16), (624, Y[0] + 28), (652, Y[0] + 28)], MUTED, "ar", 1.4)  # app → cache
d.arrow([(596, Y[1] + 40), (652, Y[1] + 40)], MUTED, "ar", 1.4)                      # app → DB
d.arrow([(746, Y[1] + NH), (746, Y[2])], MUTED, "ar", 1.4)                           # DB → replica

# 노드
d.box(24, Y[1], 104, NH, PAPER2, RULE, 1.0, 6)
d.t(76, Y[1] + 33, "클라이언트", 13, INK, KR, "middle", 600)
node(168, Y[0], 168, "03", "DNS", "이름 조회 · 라우팅 정책")
node(168, Y[1], 168, "03", "로드 밸런서", "L4 · L7 · 리버스 프록시")
node(168, Y[2], 168, "03", "CDN", "push · pull")
node(392, Y[0], 204, "04", "서비스 디스커버리", "마이크로서비스 등록 · 조회")
node(392, Y[1], 204, "04", "앱 서버", "무상태 · 수평 확장")
node(392, Y[2], 204, "07", "메시지 큐 · 워커", "태스크 큐 · 백프레셔")
node(652, Y[0], 188, "06", "캐시", "cache-aside · write-through")
node(652, Y[1], 188, "05", "데이터베이스", "RDBMS · NoSQL")
node(652, Y[2], 188, "05", "복제본 · 샤드", "복제 · federation · 샤딩")

# 띠 — 08 · 09
d.box(24, 464, 408, 36, PAPER2, RULE, 1.0, 6)
d.t(40, 487, "08", 11, INFO, MONO, "start", 600)
d.t(68, 487, "통신", 13, INK, KR, "start", 600)
d.t(108, 487, "TCP · UDP · HTTP · RPC · REST", 12, MUTED, MONO, "start")
d.box(448, 464, 408, 36, PAPER2, RULE, 1.0, 6)
d.t(464, 487, "09", 11, INFO, MONO, "start", 600)
d.t(492, 487, "보안", 13, INK, KR, "start", 600)
d.t(532, 487, "암호화 · 입력 검증 · 최소 권한", 12, MUTED, KR, "start")

d.legend(524, [("요청 경로", MUTED), ("보조 · 비동기 경로", SOFT), ("장 번호", INFO), ("모든 선택의 기준", ACC)])
d.save("00-00.concept-map.svg")
