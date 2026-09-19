# 04-01 §4 「인증서를 그대로 베낀 중간자가 왜 아무것도 못 하는가」 — 두 시도가 서로 다른 검사에서 막힌다.
# 본문 요구: "인증서를 복사하면 개인키가 없고, 공개키를 바꾸면 유효한 발급자 서명이 없습니다."
#            정적 RSA 에서는 "비밀을 못 푼다", 인증된 DHE·ECDHE 에서는 "서명을 못 만든다" 로 바뀐다.
#            산문으로 두 갈래와 두 키 교환을 한꺼번에 따라가면 어디서 막히는지가 섞인다.
# semantic pattern: Paired policy-evaluation traces — 비슷한 두 시도가 같은 순서의 규칙을 지나며
#                   처음 갈리는 자리가 논지다. 막힌 시도는 뒤 규칙을 돈 것처럼 잇지 않고 '도달 안 함' 으로 둔다.
# 타입 스펙: type-flowchart — 패턴의 nearest visual type. 스펙은 위→아래를 관례로 두지만 방향이 논지라
#           계약(방향이 핵심이면 노드를 가로로)에 따라 가로로 편다. 열 stride 는 칸 폭 + 36, 행 간격 152.
#           focal 은 규칙 1 열 — 두 시도가 처음 갈리는 단 한 자리. 패턴의 static fallback 대로
#           열 위에 괄호와 라벨로 표시한다(열을 사각형으로 두르면 들어오는 화살촉 바로 앞에서 테두리와 교차한다).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 556
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-01 §4",
      "베낀 인증서와 바꾼 공개키는 서로 다른 자리에서 막힌다",
      "공격자가 할 수 있는 일은 둘이다. 인증서를 그대로 복사하면 서명 검증은 통과하지만 짝이 되는 개인키가 없어, "
      "정적 RSA 에서는 비밀을 풀지 못하고 인증된 ECDHE 에서는 키 교환 파라미터에 서명하지 못한다. "
      "공개키를 자기 것으로 바꾸면 CA 서명이 맞지 않아 첫 검사에서 거절되고 뒤 검사까지 가지 않는다.",
      "복사하면 개인키가 없고, 바꾸면 CA 서명이 맞지 않습니다")

CX = [144, 392, 624, 844]        # 시도 · 규칙 1 · 규칙 2 · 결과
CW = [232, 192, 192, 176]
CH = 64
YA, YB = 248, 400

def left(i): return CX[i] - CW[i] / 2
def right(i): return CX[i] + CW[i] / 2

# 처음 갈리는 자리 — 규칙 1 열 머리 위에 괄호 하나(focal 1곳)
d.t(CX[1], 136, "처음 갈리는 자리", 12, ACC, KR, "middle", 600)
d.path(f"M {left(1)} 156 L {left(1)} 148 L {right(1)} 148 L {right(1)} 156", ACC, 1.4)

for i, lab in enumerate(("공격자가 한 일", "규칙 1 · 인증서 서명 검증", "규칙 2 · 개인키가 필요한 일", "결과")):
    d.t(CX[i], 172, lab, 13, SOFT, KR)

# 연결선 먼저(z-order)
for y in (YA, YB):
    d.arrow([(right(0), y), (left(1) - 8, y)], MUTED, "ar", 1.4)
d.arrow([(right(1), YA), (left(2) - 8, YA)], MUTED, "ar", 1.4)
FORK = right(2) + 16
OA1, OA2 = YA - 36, YA + 36      # 시도 A 의 결과 둘 — 키 교환 방식마다
for oy in (OA1, OA2):
    d.arrow([(right(2), YA), (FORK, YA), (FORK, oy), (left(3) - 8, oy)], BAD, "bad", 1.4)
# 시도 B 는 규칙 2 를 돌지 않는다 — 그 칸 아래로 비켜 결과로 간다
DET = YB + CH / 2 + 24
d.arrow([(right(1), YB), (right(1) + 16, YB), (right(1) + 16, DET), (CX[3], DET), (CX[3], YB + CH / 2 + 8)],
        BAD, "bad", 1.4)
d.t(CX[2], DET + 20, "뒤 검사로 가지 않음", 12, BAD, KR)

def cell(i, y, title, sub, c=None, dash=False, h=CH):
    x = left(i); top = y - h / 2
    if dash:
        d.o.append(f'<rect x="{x}" y="{top}" width="{CW[i]}" height="{h}" rx="8" fill="{PAPER}" '
                   f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="4 4"/>')
    elif c:
        d.tone(x, top, CW[i], h, c, 8)
    else:
        d.box(x, top, CW[i], h, PAPER2, RULE, 1.0, 8)
    d.t(CX[i], top + h / 2 - 4, title, 13, (SOFT if dash else (c or INK)), KR, "middle", 600)
    d.t(CX[i], top + h / 2 + 16, sub, 12, MUTED, KR)

# 시도 A — 그대로 복사
cell(0, YA, "인증서를 그대로 복사", "원본 바이트 그대로")
cell(1, YA, "통과", "서명이 원본 그대로", OK)
cell(2, YA, "실패", "짝이 되는 개인키 없음", BAD)
cell(3, OA1, "정적 RSA", "비밀을 풀 수 없음", BAD, h=56)
cell(3, OA2, "인증된 ECDHE", "서명을 만들 수 없음", BAD, h=56)

# 시도 B — 공개키 교체
cell(0, YB, "공개키를 자기 것으로 교체", "개인키는 공격자 것")
cell(1, YB, "실패", "CA 서명 불일치", BAD)
cell(2, YB, "도달 안 함", "앞에서 멈춤", dash=True)
cell(3, YB, "검증 거절", "인증서를 받지 않음", BAD)

d.legend(H - 40, [("처음 갈리는 자리", ACC), ("통과", OK), ("막힘", BAD), ("도달 안 함", SOFT)])
d.save("04-01.cert-copy-mitm.svg")
