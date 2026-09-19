# 04-01 학습 목표 뒤 전체 지도 — 절 여섯을 핸드셰이크가 진행되는 순서로 잇는다.
# 절 배열은 학습 순서다. 버전(§1), 메시지 종류(§2), 협상(§3), 조건부 메시지(§4),
# 암호화 경계(§5)를 읽고 Alert 해석과 캡처 판독 연습(§6)에 적용한다.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 이름 · 그 절이 답하는 것)이 반복되고
#           화살표가 읽는 순서를 나른다. 주체가 없는 단계 지도라 lanes 를 쓰지 않는다.
#           focal 은 방향별 보호 전환을 다루는 칸 하나(§5 경계)다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 512
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01",
      "TLS 핸드셰이크 읽기 — 읽는 순서",
      "4장 전반부 노트의 절 여섯을 핸드셰이크가 진행되는 순서로 이은 지도. 버전을 가리는 데서 출발해 "
      "메시지 종류와 협상 결과를 읽고, 조건부 메시지와 암호화 경계를 구분한다. "
      "마지막 절에서는 Alert 해석과 캡처 판독을 연습한다.",
      "TLS 1.2 최초 전체 핸드셰이크를 중심으로 읽습니다. 마지막 절에서 캡처에 적용합니다")

CW, CH, GAP, X0 = 400, 80, 24, 24
ROW, Y0 = 112, 116
cards = [
    ("§1", "버전을 아는 것이 먼저",      "TLS 1.2 와 1.3 의 차이",     None),
    ("§2", "네 단계와 열 가지 메시지",    "번호는 순서가 아니라 종류",   None),
    ("§3", "제안하고 고른다",            "목록과 선택 · SNI · 이름 분해", None),
    ("§4", "인증서와 조건부 메시지",      "안 온 메시지가 설정을 말함",   None),
    ("§5", "암호화가 시작되는 지점",      "방향마다 Finished 부터 보호", "focal"),
    ("§6", "Alert 와 캡처 판독 연습",    "전송 방향 · 코드 · 직전 메시지", BAD),
]

def pos(i):
    return X0 + (i % 2) * (CW + GAP), Y0 + (i // 2) * ROW

for i, (num, title, q, mark) in enumerate(cards):
    x, y = pos(i)
    if mark == "focal":
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        col = ACC
    elif mark:
        d.tone(x, y, CW, CH, mark, 8); col = mark
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8); col = INK
    d.t(x + 20, y + 32, num, 12, SOFT, MONO, "start", 600)
    d.t(x + 56, y + 32, title, 14, col, KR, "start", 600)
    d.t(x + 56, y + 56, q, 13, MUTED, KR, "start")

# 읽는 순서 — 좌우로 한 칸, 그다음 줄로 내려간다
for i in range(len(cards) - 1):
    x0, y0 = pos(i); x1, y1 = pos(i + 1)
    if y0 == y1:
        d.arrow([(x0 + CW, y0 + CH / 2), (x1 - 6, y1 + CH / 2)], MUTED, "ar", 1.4)
    else:
        d.arrow([(x0 + CW / 2, y0 + CH), (x0 + CW / 2, y0 + CH + 16),
                 (x1 + CW / 2, y0 + CH + 16), (x1 + CW / 2, y1 - 6)], MUTED, "ar", 1.4)

d.t(24, 452, "범위: 최초 전체 핸드셰이크 · 세션 재개·재협상 제외 · TLS 1.3 은 암호화 경계가 다름",
     12, SOFT, KR, "start")

d.legend(H - 44, [("암호화 경계", ACC), ("Alert 와 판독 연습", BAD)])
d.save("04-01.chapter-overview.svg")
