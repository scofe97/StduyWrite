# 타입 스펙: type-process — 주체 없는 단계 지도(semantic-patterns 의 Stage framework with semantic slots). 네 단계 칸마다 같은 슬롯(그림 · 구성 · 해소한 병목)이 반복된다.
# 사실 출처: 추출본 v2.txt 64~218행(단일 서버 71 · 데이터베이스 100 · 로드밸런서 144 · DB 복제 168), 최종 설계 그림 PDF 14쪽(웹 2 · 주 DB 1 · 부 DB 1 · 쓰기는 주, 읽기는 부)
# Layout conventions: 칸 폭 200 · 칸 간격 28 · 칸 x 시작 40, 그림 영역 y=136~352, 행 stride 56(y=148·216·304), 노드 높이 36, 모든 좌표 4의 배수.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, ACC, OK, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 516
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 01-01",
      "서버 한 대에서 네 단계로 자란다",
      "서버 한 대에서 웹과 DB 를 나누고, 웹 앞에 로드밸런서를 두고, DB 를 주와 부로 복제하는 네 단계의 구성과 해소한 병목.",
      "단계마다 부품이 하나씩 늘고 막힌 곳이 하나씩 풀립니다")

COLX = (40, 268, 496, 724)
CW = 200
TITLES = ("§1 서버 한 대", "§2 웹과 DB 분리", "§3 로드밸런서", "§4 DB 복제")
CAPS = (("웹 + DB 한 대", "출발점"),
        ("웹 1 · DB 1", "계층별로 따로 확장"),
        ("LB 1 · 웹 2 · DB 1", "웹 장애·과부하 분산"),
        ("LB 1 · 웹 2 · 주 1 · 부 1", "DB 장애·읽기 부하 분산"))
Y0, Y1 = 136, 352      # 그림 영역
RL, RW, RD = 148, 216, 304   # LB · 웹 · DB 행 상단


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, w, h, label, c, size=13):
    d.tone(x, y, w, h, c, 6, "12", 1.2)
    d.t(x + w / 2, y + h / 2 + 5, label, size, c, kr(label), "middle", 600)


for i, x in enumerate(COLX):
    cx = x + CW // 2
    d.t(x, 124, TITLES[i], 14, MUTED, KR, "start", 600)
    d.box(x, Y0, CW, Y1 - Y0, PAPER2, RULE, 0.9, 8)
    d.t(cx, 384, CAPS[i][0], 13, INK, KR, "middle", 600)
    d.t(cx, 412, CAPS[i][1], 13, MUTED, KR, "middle")
    if i < 3:
        d.arrow([(x + CW + 2, 244), (COLX[i + 1] - 4, 244)], SOFT, "soft", 1.4)

# §1 — 웹 + DB 한 대
x, cx = COLX[0], COLX[0] + CW // 2
node(cx - 60, 216, 120, 124, "웹 + DB", OK)

# §2 — 웹 · DB 분리
x, cx = COLX[1], COLX[1] + CW // 2
node(cx - 60, 216, 120, 60, "웹", OK)
d.arrow([(cx, 276), (cx, 300)], MUTED, "ar", 1.4)
node(cx - 60, 304, 120, 36, "DB", INFO)

# §3 — LB · 웹 둘 · DB
x, cx = COLX[2], COLX[2] + CW // 2
d.box(cx - 60, RL, 120, 36, PAPER, RULE, 1.0, 6)
d.t(cx, RL + 23, "로드밸런서", 13, INK, KR, "middle", 600)
d.arrow([(cx, RL + 36), (cx, 212)], MUTED, "ar", 1.4)
d.box(cx - 96, 216, 192, 60, PAPER, RULE, 0.9, 6)
node(cx - 84, 224, 80, 36, "웹 1", OK)
node(cx + 4, 224, 80, 36, "웹 2", OK)
d.arrow([(cx, 276), (cx, 300)], MUTED, "ar", 1.4)
node(cx - 60, 304, 120, 36, "DB", INFO)

# §4 — LB · 웹 둘 · 주 DB · 부 DB
x, cx = COLX[3], COLX[3] + CW // 2
d.box(cx - 60, RL, 120, 36, PAPER, RULE, 1.0, 6)
d.t(cx, RL + 23, "로드밸런서", 13, INK, KR, "middle", 600)
d.arrow([(cx, RL + 36), (cx, 212)], MUTED, "ar", 1.4)
d.box(cx - 96, 216, 192, 60, PAPER, RULE, 0.9, 6)
node(cx - 84, 224, 80, 36, "웹 1", OK)
node(cx + 4, 224, 80, 36, "웹 2", OK)
d.arrow([(cx - 62, 276), (cx - 62, 300)], MUTED, "ar", 1.4)
d.arrow([(cx + 62, 276), (cx + 62, 300)], MUTED, "ar", 1.4)
node(cx - 96, 304, 68, 36, "주 DB", INFO)
node(cx + 28, 304, 68, 36, "부 DB", INFO)
d.arrow([(cx - 26, 330), (cx + 26, 330)], ACC, "acc", 1.8)
d.t(cx, 318, "복제", 12, ACC, KR, "middle")
d.t(cx - 68, 292, "쓰기", 12, MUTED, KR, "end")
d.t(cx + 56, 292, "읽기", 12, MUTED, KR, "end")

d.legend(H - 56, [("웹 서버", OK), ("DB", INFO), ("복제", ACC)])
d.save("01-01.chapter-overview.svg")
print("ok chapter-overview")
