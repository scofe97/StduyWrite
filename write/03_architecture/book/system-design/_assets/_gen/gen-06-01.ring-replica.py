# 타입 스펙: type-process — 링을 가로로 펴서 서버 s0~s7 을 순서대로 놓고 key0 에서 시계 방향(오른쪽)으로 N = 3 개를 고르는 걸음과, 가상 노드에서 같은 서버를 건너뛰는 걸음을 위아래 두 줄에 보인다.
# 사실 출처: s0~s7 · key0 은 s0 과 s1 사이 · N = 3 복제는 s1·s2·s3 는 추출본 v2.txt 1613~1631행(PDF 93·94쪽 그림), 고유 서버만 고르는 규칙은 v2.txt 1636~1638행과 Dynamo 논문 §4.3.
#   아래 줄의 위치 p1~p5 와 서버 A·B·C 는 설계 예시이다.
# Layout conventions: 칩 폭 56 · 높이 40, x stride 104(윗줄 중심 52부터 · 아랫줄 중심 156부터), 윗줄 y=152 · 아랫줄 y=300, 링 선 y=172·320. 모든 좌표 4의 배수에 가깝게 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, RULE, SOFT, INFO, KR, MONO

W, H = 960, 440
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-01 §4",
      "key0 은 시계 방향 서버 3개에 복제된다",
      "링을 가로로 펴서 key0 에서 오른쪽으로 걷고, 같은 서버가 다시 나오면 건너뛰어 서로 다른 서버 3개를 고른다.",
      "N = 3")

SW, SH = 56, 40


def chip(cx, cy, txt, c, dash=None, fill="14"):
    d.o.append(f'<rect x="{cx - SW // 2}" y="{cy - SH // 2}" width="{SW}" height="{SH}" rx="6" fill="{PAPER}"/>')
    d.o.append(f'<rect x="{cx - SW // 2}" y="{cy - SH // 2}" width="{SW}" height="{SH}" rx="6" fill="{c}{fill}" stroke="{c}" stroke-width="1.2"' + (f' stroke-dasharray="{dash}"' if dash else "") + "/>")
    d.t(cx, cy + 5, txt, 13, c, MONO, "middle", 600)


# 윗줄 — 서버 8대
Y1 = 172
d.t(12, 118, "서버 8대", 13, MUTED, KR, "start", 600)
d.line(24, Y1, 920, Y1, RULE, 0.8, "3 6")
C1 = [52 + 104 * i for i in range(8)]
for i, cx in enumerate(C1):
    copy = i in (1, 2, 3)
    chip(cx, Y1, f"s{i}", OK if copy else MUTED)
    if copy:
        d.t(cx, Y1 + 40, f"복제 {i}", 13, OK, KR, "middle", 600)
chip(884, Y1, "s0", MUTED, "4 4", "08")
d.t(884, Y1 + 40, "다시 s0", 12, SOFT, KR, "middle")
# key0 은 s0 과 s1 사이 — focal
kx = 104
d.o.append(f'<circle cx="{kx}" cy="{Y1}" r="6" fill="{ACC}"/>')
d.t(kx, Y1 - 36, "key0", 13, ACC, MONO, "middle", 600)
d.arrow([(kx + 8, Y1), (C1[1] - SW // 2 - 4, Y1)], ACC, "acc", 1.6)
for i in (1, 2):
    d.arrow([(C1[i] + SW // 2 + 2, Y1), (C1[i + 1] - SW // 2 - 4, Y1)], OK, "ok", 1.6)

# 아랫줄 — 가상 노드
Y2 = 320
d.t(12, 268, "가상 노드", 13, MUTED, KR, "start", 600)
d.line(24, Y2, 920, Y2, RULE, 0.8, "3 6")
OWN = ("A", "A", "B", "A", "C")
PICK = {0: 1, 2: 2, 4: 3}
C2 = [156 + 104 * i for i in range(5)]
d.o.append(f'<circle cx="{kx}" cy="{Y2}" r="6" fill="{ACC}"/>')
d.t(kx, Y2 - 36, "key0", 13, ACC, MONO, "middle", 600)
d.arrow([(kx + 8, Y2), (C2[0] - SW // 2 - 4, Y2)], ACC, "acc", 1.6)
for i, cx in enumerate(C2):
    if i in PICK:
        chip(cx, Y2, f"p{i + 1} {OWN[i]}", OK)
        d.t(cx, Y2 + 40, f"복제 {PICK[i]}", 13, OK, KR, "middle", 600)
    else:
        chip(cx, Y2, f"p{i + 1} {OWN[i]}", WARN, "4 4")
        d.t(cx, Y2 + 40, "건너뜀", 13, WARN, KR, "middle")
    if i < 4:
        d.arrow([(cx + SW // 2 + 2, Y2), (C2[i + 1] - SW // 2 - 4, Y2)], MUTED, "ar", 1.4)
d.box(700, Y2 - 20, 208, 40, PAPER, PAPER, 0, 6)
d.tone(700, Y2 - 20, 208, 40, OK, 6, "12", 1.2)
d.t(804, Y2 + 6, "복제본 A · B · C", 14, OK, KR, "middle", 600)

d.legend(H - 56, [("복제 서버", OK), ("건너뛴 위치", WARN), ("키 위치", ACC), ("링 순서", MUTED)])
d.save("06-01.ring-replica.svg")
