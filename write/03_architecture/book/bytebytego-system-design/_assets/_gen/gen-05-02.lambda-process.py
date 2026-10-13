# 타입 스펙: type-process — 같은 페이지 조회 로그의 건수가 배치 경로(MapReduce)와 속도 경로(Storm)를 따로 지나 두 뷰에 담기고 질의 시점에 한 값으로 합쳐진다. 칸 사이를 건너가는 것은 조회 건수 하나.
# 사실 출처: Nathan Marz, "How to beat the CAP theorem"(2011-10-13) — 마스터 데이터셋은 추가 전용, 배치 뷰는 최근 몇 시간을 뺀 전부를 미리 계산하고 실시간 뷰가 마지막 몇 시간을 메우며 질의 때 둘을 합친다(페이지 조회 수 예시, Storm). 두 시스템에 같은 로직을 두 번 구현하는 부담은 Jay Kreps, "Questioning the Lambda Architecture"(2014-07-02). 조회 건수 1,000,030·1,000,000·30 과 시각 13시·14시는 설명용 예시 값이다.
# Layout conventions: 칸 4열 — 로그 x=24 w=140, 엔진 x=272 w=140, 뷰 x=520 w=156, 질의 x=784 w=148, 열 간격 108. 행 중심 y=172(배치)·316(속도), 상자 높이 88. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 468
d = D(W, H, "BYTEBYTEGO · 05-02 §4",
      "람다 구조의 두 경로와 합산",
      "같은 조회 로그가 배치 경로와 속도 경로를 따로 지나 질의 시점에 합쳐지는 흐름입니다",
      "같은 조회 로그가 두 경로를 따로 지나 질의 때 합쳐집니다. 값은 예시입니다")

BH = 88
ROWS = {"배치": 172, "속도": 316}
COL = {"배치": INFO, "속도": WARN}
LOGX, ENGX, VIEWX, SRVX = 24, 272, 520, 784
LOGW, ENGW, VIEWW, SRVW = 140, 140, 156, 148


def fam(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


# 원본 로그 — 두 줄에 걸친 높은 상자
d.box(LOGX, 128, LOGW, 232, PAPER2, RULE, 0.9, 6)
d.t(LOGX + LOGW / 2, 164, "원본 로그", 13, INK, KR, "middle", 600)
d.t(LOGX + LOGW / 2, 188, "추가 전용", 13, MUTED, KR)
d.t(LOGX + LOGW / 2, 248, "/a 조회", 13, MUTED, KR)
d.t(LOGX + LOGW / 2, 276, "1,000,030", 13, INK, MONO, "middle", 600)

for name, cy in ROWS.items():
    c = COL[name]
    top = cy - BH // 2
    # 엔진 — 집계 코드를 두 번 구현하는 자리가 focal
    d.tone(ENGX, top, ENGW, BH, ACC, 6, "14", 1.4)
    eng, sub = ("MapReduce", "수 시간 지연") if name == "배치" else ("Storm", "건별 증분")
    d.t(ENGX + ENGW / 2, cy - 4, eng, 13, INK, MONO, "middle", 600)
    d.t(ENGX + ENGW / 2, cy + 20, sub, 13, MUTED, KR)
    # 뷰
    d.tone(VIEWX, top, VIEWW, BH, c, 6, "14", 1.2)
    view, rng, val = ("배치 뷰", "/a · 13시까지", "1,000,000") if name == "배치" else ("실시간 뷰", "/a · 14시", "30")
    d.t(VIEWX + VIEWW / 2, cy - 12, view, 13, c, KR, "middle", 600)
    d.t(VIEWX + VIEWW / 2, cy + 8, rng, 13, MUTED, fam(rng))
    d.t(VIEWX + VIEWW / 2, cy + 30, val, 13, INK, MONO, "middle", 600)
    # 로그 → 엔진: 건너가는 값
    x1, x2 = LOGX + LOGW + 4, ENGX - 4
    d.arrow([(x1, cy), (x2, cy)], c, "info" if name == "배치" else "warn", 1.6)
    chip_txt = "1,000,000" if name == "배치" else "30"
    d.chip((x1 + x2) / 2, cy - 20, chip_txt, c)
    d.t((x1 + x2) / 2, cy + 28, "13시까지" if name == "배치" else "14시", 13, MUTED, KR)
    # 엔진 → 뷰
    d.arrow([(ENGX + ENGW + 4, cy), (VIEWX - 4, cy)], c, "info" if name == "배치" else "warn", 1.6)
    # 뷰 → 질의
    d.arrow([(VIEWX + VIEWW + 4, cy), (SRVX - 4, cy)], c, "info" if name == "배치" else "warn", 1.6)

# 두 엔진을 잇는 집계 코드 2벌
cx = ENGX + ENGW / 2
d.line(cx, 216, cx, 272, ACC, 1.2, "3 4")
d.chip(cx, 244, "집계 코드 2벌", ACC, 13)

# 질의 시점 합산
d.box(SRVX, 128, SRVW, 232, PAPER2, RULE, 0.9, 6)
d.t(SRVX + SRVW / 2, 196, "질의 시점 합산", 13, INK, KR, "middle", 600)
d.t(SRVX + SRVW / 2, 244, "1,000,000 + 30", 12, MUTED, MONO)
d.t(SRVX + SRVW / 2, 276, "= 1,000,030", 13, INK, MONO, "middle", 600)

d.legend(H - 44, [("배치 경로", INFO), ("속도 경로", WARN), ("두 번 구현하는 집계", ACC)])
d.save("05-02.lambda-process.svg")
