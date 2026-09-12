# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

W = 1000
SX = 500
TOP = 164
STRIDE = 156
STAGE_W = 300
STAGE_H = 64
SIDE_W = 300
SIDE_H = 92

stages = [
    ("1", "문법", "필수", INFO,
     ["변수 · 제어문 · 함수", "slice · map · struct", "pointer · zero value"],
     ["작은 프로그램을 패키지와", "함수로 나눠 작성합니다"]),
    ("2", "타입 설계", "필수", INFO,
     ["method · embedding", "interface · type assertion", "error · generic"],
     ["작은 인터페이스와 에러 체인을", "사용하는 쪽에서 설계합니다"]),
    ("3", "관용구와 도구", "필수", INFO,
     ["package boundary · naming", "module · workspace", "gofmt · vet · staticcheck"],
     ["Go 관용구로 코드를 구성하고", "표준 도구로 검사합니다"]),
    ("4", "동시성", "필수", ACC,
     ["goroutine · mutex · WaitGroup", "channel · select · context", "happens-before · race"],
     ["실패와 취소가 모든 고루틴에", "전파되는 구조를 만듭니다"]),
    ("5", "테스트와 성능", "필수", INFO,
     ["table test · fuzz · benchmark", "race detector · pprof", "trace · GC · allocation"],
     ["테스트와 프로파일로", "행위와 병목을 확인합니다"]),
    ("6", "서비스", "필수", OK,
     ["net · net/http · timeout", "graceful shutdown · resilience", "slog · OpenTelemetry"],
     ["종료와 관측 경계를 갖춘", "네트워크 서비스를 구성합니다"]),
]

H = TOP + STRIDE * len(stages) + 92
d = D(W, H, "WRITE · GO ROADMAP", "Go 학습 로드맵",
      "문법에서 타입 설계, 관용구, 동시성, 테스트와 성능, 네트워크 서비스로 이어지는 여섯 단계입니다.",
      "왼쪽은 핵심 키워드, 가운데는 단계, 오른쪽은 완료 기준입니다")

d.box(SX - 116, 96, 232, 44, PAPER2, RULE, 1.0)
d.t(SX, 123, "여섯 단계를 순서대로 봅니다", 14, INK, KR, "middle", 600)
d.line(SX, 140, SX, TOP + STRIDE * (len(stages) - 1) + STAGE_H, RULE, 1.4)

for index, (number, title, priority, color, keywords, completion) in enumerate(stages):
    y = TOP + index * STRIDE
    mid = y + STAGE_H / 2
    side_y = mid - SIDE_H / 2
    d.line(330, mid, SX - STAGE_W / 2, mid, RULE, 1.0)
    d.line(SX + STAGE_W / 2, mid, 670, mid, RULE, 1.0)
    d.box(30, side_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(46, side_y + 20, "핵심 키워드", 13, SOFT, KR, "start", 600)
    for line_index, keyword in enumerate(keywords):
        d.t(46, side_y + 42 + line_index * 18, keyword, 13, MUTED, KR, "start")
    if index == 3:
        d.tone(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, ACC, 6, "14", 1.4)
    else:
        d.box(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, PAPER, color, 1.2)
    d.t(SX - 128, y + 25, number, 12, color, MONO, "start", 600)
    d.t(SX + 6, y + 26, title, 15, ACC if index == 3 else INK, KR, "middle", 600)
    d.t(SX + 6, y + 49, priority, 13, color, KR)
    d.box(670, side_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(686, side_y + 20, "완료 기준", 13, SOFT, KR, "start", 600)
    for line_index, line in enumerate(completion):
        d.t(686, side_y + 48 + line_index * 20, line, 13, MUTED, KR, "start")

d.legend(H - 52, [("필수", INFO), ("추천", OK), ("학습 중심", ACC)])
d.save("go-roadmap.svg")
