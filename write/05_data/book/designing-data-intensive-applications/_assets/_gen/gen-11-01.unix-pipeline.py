# 11-01 §2 — Unix 로그 분석 파이프라인 단계마다 실제 데이터 스트림이 변환되는 데이터 흐름.
# 사실 출처: 11-01 본문 §2(L46~L61), DDIA 2판 Ch 11 p.4~5 ("Simple Log Analysis"). 명령과 예시 값은 원서 그대로.
# 로그 줄은 원서 p.4 의 한 줄(216.58.210.78 … /css/typography.css)만 쓰고, 나머지 줄은 IP 없이 줄였다.
# 카운트·URL 은 원서 p.5 출력(4189 /favicon.ico … 915 /css/typography.css) 그대로. 한글은 MONO 줄에 넣지 않는다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
Y1 = 156
H1 = 148
GAP_Y = 36
Y2 = Y1 + H1 + GAP_Y
H2 = 148
LEG = Y2 + H2 + 28
H = LEG + 52

d = D(W, H, "11-01 · §2 DATA FLOW", "Unix 파이프라인 단계별 데이터 변환 흐름",
      "cat, awk, sort, uniq, head로 이어지는 명령 파이프라인에서 레코드가 추출되고 정렬되며 집계되는 데이터 변환 모습을 추적한다. 정렬을 통한 동일 키 군집화가 핵심이다.",
      "표준 입출력 파이프 · 필드 추출 · 사전순 정렬 군집화 · 인접 카운트 집계 · 상위 5개 출력")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "Unix 파이프라인 원리: 단일 책임 명령들을 stdin · stdout 표준 인터페이스로 연결해 데이터 스트림을 순차 처리", 12, INK, KR, "middle", 600)

PW = 264
GAP_X = 16
X0 = 28

steps = [
    # 상단 3단계 (0, 1, 2)
    ("1단계", "cat access.log", "로그 파일 행 스트림 방출", INFO, [
        '216.58.210.78 "GET /css/..."',
        '... "GET /favicon.ico ..."',
    ]),
    ("2단계", "awk '{print $7}'", "요청 URL 필드 추출", INFO, [
        '/css/typography.css',
        '/favicon.ico',
    ]),
    ("3단계", "sort", "사전순 정렬 · 동일 키 군집", ACC, [
        '/css/typography.css',
        '/css/typography.css',
    ]),
    # 하단 3단계 (3, 4, 5)
    ("4단계", "uniq -c", "인접 동일 행 빈도 카운트", ACC, [
        ' 915 /css/typography.css',
        '4189 /favicon.ico',
    ]),
    ("5단계", "sort -r -n", "빈도수 기준 내림차순 정렬", ACC, [
        '4189 /favicon.ico',
        '3631 /2016/02/08/how-to-do...',
    ]),
    ("6단계", "head -n 5", "상위 5개 결과 추출 및 종료", OK, [
        '4189 /favicon.ico',
        ' 915 /css/typography.css',
    ]),
]

for idx, (step_num, cmd, desc, c, samples) in enumerate(steps):
    row = idx // 3
    col = idx % 3
    x = X0 + col * (PW + GAP_X)
    y = Y1 if row == 0 else Y2
    card_h = H1 if row == 0 else H2

    # 카드 외곽
    d.box(x, y, PW, card_h, PAPER2, c, 1.2)

    # 헤더: 단계 칩 + 명령어
    d.chip(x + 28, y + 20, step_num, c, 11, 4)
    d.t(x + 60, y + 24, cmd, 12, INK, MONO, "start", 600)
    d.t(x + PW / 2, y + 46, desc, 11, MUTED, KR, "middle")
    d.line(x + 10, y + 56, x + PW - 10, y + 56, RULE, 0.8)

    # 데이터 샘플 박스
    d.box(x + 8, y + 66, PW - 16, 70, PAPER, RULE, 0.8)
    d.t(x + 16, y + 84, "표준 출력 스트림:", 11, SOFT, KR, "start")
    for s_idx, sample in enumerate(samples):
        sy = y + 104 + s_idx * 20
        d.t(x + 16, sy, sample, 11, c, MONO, "start")

# 파이프 연결 화살표
# 1 -> 2
d.arrow([(X0 + PW, Y1 + H1 / 2), (X0 + PW + GAP_X, Y1 + H1 / 2)], MUTED, "ar", 1.4)
# 2 -> 3
d.arrow([(X0 + 2 * PW + GAP_X, Y1 + H1 / 2), (X0 + 2 * PW + 2 * GAP_X, Y1 + H1 / 2)], MUTED, "ar", 1.4)

# 3 -> 4 (상단 우측 -> 하단 좌측: 직각 배선)
mid_y = Y1 + H1 + GAP_Y / 2
x_from = X0 + 2 * PW + GAP_X + PW / 2
x_to = X0 + PW / 2
d.arrow([(x_from, Y1 + H1), (x_from, mid_y), (x_to, mid_y), (x_to, Y2)], MUTED, "ar", 1.4)

# 4 -> 5
d.arrow([(X0 + PW, Y2 + H2 / 2), (X0 + PW + GAP_X, Y2 + H2 / 2)], MUTED, "ar", 1.4)
# 5 -> 6
d.arrow([(X0 + 2 * PW + GAP_X, Y2 + H2 / 2), (X0 + 2 * PW + 2 * GAP_X, Y2 + H2 / 2)], MUTED, "ar", 1.4)

d.legend(LEG, [
    ("데이터 추출", INFO),
    ("정렬 및 집계", ACC),
    ("결과 필터링", OK),
])

d.save("11-01.unix-pipeline.svg")
