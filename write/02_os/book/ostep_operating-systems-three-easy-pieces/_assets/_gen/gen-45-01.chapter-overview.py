# 45-01 개념도 — 상대를 확인하는 두 길(개인 키로, 비밀번호로)이 같은 한계, 메시지 하나에서 멈춘다.
# 본문 요구(45-01 「학습 목표」 개념도 문단): 왼쪽 출발(원격 기계 §1), 위 갈래 믿음의 사슬(공개 키 §2 → 인증서 §2 → CA 공개 키 §2 → 미리 설치된 키 §2),
#           아래 갈래(암호화한 통로 §3 → 솔트 붙은 느린 해시 §3), 오른쪽 두 갈래가 멈추는 곳(메시지 하나 §4)과 예고(TLS·세션 인증 §4).
# 값 근거: 이 노트 「핵심 요약」 — 믿을 범위를 그 확인이 닿는 곳까지만 잡는다. 주황은 그 한 곳(오른쪽 멈추는 곳)에만 쓴다.
# 공식 근거: RFC 5280 §4.1.1.3·§6, NIST SP 800-63B-4 §3.1.1.2, OWASP Password Storage Cheat Sheet.
# 타입 스펙: type-flowchart — 한 출발점에서 두 길로 갈라져 한 판정 자리에서 합류하는 분기 그래프. 고른 이유: 이 편의 줄기가
#             「두 확인 방법이 서로 다른 길을 가다 같은 한계에 닿는다」는 갈림과 합류라 절 순서표나 격자로는 합류가 안 보인다.
#             위 갈래는 신뢰의 뿌리 쪽으로 내려가게 꺾었다. 스펙에 이 배치의 공식은 없어 좌표는 4 의 배수 stride 로 직접 잡았다.
#             (옛 판의 4행 × 3열 격자 공식 열 x = 60 + j·340 은 쓰지 않는다.)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 1000, 588


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "FLOWCHART · 45-01 OVERVIEW",
      "개인 키로 확인하든 비밀번호로 확인하든 메시지 하나에서 멈춘다",
      "45-01 의 키워드 개념도. 왼쪽 원격 기계에서는 비트만 보여 상대가 누구인지 확인해야 한다. 위 갈래는 개인 키로 확인하는 길이다. "
      "공개 키는 비밀이 아니어서 인증서가 이름과 키를 서명으로 묶고, 그 서명은 CA 공개 키로 확인하며, 그 키는 미리 설치된 것에서 신뢰가 출발한다. "
      "아래 갈래는 비밀번호로 확인하는 길이다. 암호화한 통로로 보내고 사이트는 솔트 붙은 느린 해시만 저장한다. "
      "두 길은 오른쪽에서 같은 한계에 닿는다. 확인되는 것은 지금 받은 메시지 하나의 진위뿐이고, 이후의 메시지를 묶는 TLS 와 세션 인증은 다음 편의 몫이다.")


def node(x, y, w, h, title, sub, c, sec, sub2=None):
    d.tone(x, y, w, h, c, 6, "14", 1.1)
    d.chip(x + 24, y + 14, sec, c, 11)
    d.t(x + w / 2, y + 40, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 58, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 74, sub2, 13, MUTED, kr(sub2), "middle")


NW, NH = 152, 64
X1, X2, X3 = 190, 406, 622
TOP, BOT = 148, 412

# 구역 머리 — 두 갈래
for y, cap in ((126, "개인 키로 확인"), (390, "비밀번호로 확인")):
    d.t(X1, y, cap, 13, MUTED, KR, "start", 600)
    d.line(X1, y + 8, X3 + NW, y + 8, RULE, 0.8)

# 출발
node(24, 272, 132, 84, "원격 기계", "비트만 보임", INFO, "§1", "누구인지 확인")
d.arrow([(158, 298), (174, 298), (174, TOP + 32), (188, TOP + 32)], SOFT, "soft", 1.3)
d.arrow([(158, 330), (174, 330), (174, BOT + 32), (188, BOT + 32)], SOFT, "soft", 1.3)

# 위 갈래 — 믿음의 사슬이 뿌리 쪽으로 내려간다
node(X1, TOP, NW, NH, "공개 키는 비밀 아님", "누구의 키인지가 문제", INFO, "§2")
node(X2, TOP, NW, NH, "인증서", "이름과 키를 묶음", OK, "§2")
node(X3, TOP, NW, NH, "CA 공개 키", "서명을 확인하는 키", OK, "§2")
node(X3, 260, NW, NH, "미리 설치된 키", "신뢰가 출발하는 곳", INFO, "§2")
d.arrow([(X1 + NW + 2, TOP + 32), (X2 - 4, TOP + 32)], INFO, "info", 1.4)
d.t((X1 + NW + X2) / 2, TOP + 22, "묶으려면", 13, MUTED, KR, "middle", 600)
d.arrow([(X2 + NW + 2, TOP + 32), (X3 - 4, TOP + 32)], OK, "ok", 1.4)
d.t((X2 + NW + X3) / 2, TOP + 22, "서명 확인", 13, MUTED, KR, "middle", 600)
d.arrow([(X3 + NW / 2, TOP + NH + 3), (X3 + NW / 2, 257)], OK, "ok", 1.4)
d.t(X3 + NW / 2 + 12, 240, "어디서 얻나", 13, MUTED, KR, "start", 600)

# 아래 갈래
node(X1, BOT, NW, NH, "암호화한 통로", "평문은 누구나 가로챔", OK, "§3")
node(X2, BOT, NW, NH, "솔트 붙은 느린 해시", "해시만 저장해 비교", OK, "§3")
d.arrow([(X1 + NW + 2, BOT + 32), (X2 - 4, BOT + 32)], OK, "ok", 1.4)
d.t((X1 + NW + X2) / 2, BOT + 22, "해시 저장", 13, MUTED, KR, "middle", 600)

# 오른쪽 — 두 갈래가 멈추는 곳 (주황은 이 한 곳)
SX, SY, SW, SH = 838, 260, 138, 92
node(SX, SY, SW, SH, "메시지 하나", "진위만 보임", ACC, "§4", "이후는 못 묶음")
d.arrow([(X3 + NW + 2, 292), (SX - 4, 292)], ACC, "acc", 1.5)
d.t((X3 + NW + SX) / 2, 282, "여기까지", 13, MUTED, KR, "middle", 600)
d.arrow([(X2 + NW + 2, BOT + 32), (806, BOT + 32), (806, 328), (SX - 4, 328)], ACC, "acc", 1.5)
d.t(682, BOT + 22, "지금 받은 메시지만", 13, MUTED, KR, "middle", 600)

# 예고 — 곁가지
node(SX, 412, SW, 84, "TLS", "세션 인증", MUTED, "§4", "다음 편에서")
d.arrow([(SX + SW / 2, SY + SH + 3), (SX + SW / 2, 409)], SOFT, "soft", 1.3, "4 3")
d.t(SX + SW / 2 - 6, 388, "이후를 묶으려면", 13, MUTED, KR, "end", 600)

d.legend(H - 40, [("전제 · 문제", INFO), ("대응", OK), ("믿을 범위의 끝", ACC), ("곁가지 · 예고", MUTED)])
d.save("45-01.chapter-overview.svg")
print("ok 45-01 overview")
