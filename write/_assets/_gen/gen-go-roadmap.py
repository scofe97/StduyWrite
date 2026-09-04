# write/go-roadmap.md §도입 — Go 언어 학습 로드맵.
# Go 는 01_language 의 문법, 02_os 의 동시성, 08_cloud 의 서비스에 걸쳐 있어 문서를 write/ 직계에 둔다.
# 판형은 network-roadmap 과 같다 — 세로 척추에 국면과 단계를 걸고 개념을 좌우로 뻗는다.
# 점선 박스는 책이 다루지 않아 공식 문서로 채울 키워드다.
# 보유하지 않은 책과 공식 문서가 섞이므로, 단계 라벨의 출처 구분은 본문 표가 맡는다.
# 단계 라벨의 연도는 낡음 점검 결과다 — 2017년 Concurrency in Go 를 7단계에서 빼고
# 같은 내용을 2023년 LCPG 8~10장으로 대체했다. 연도 근거는 본문 표에 적는다.
# 조건부 두 단계는 국면 노드 없이 절단선 아래 꼬리로 붙인다 — 국면 여섯은 type-tree 너비 5 를 넘는다.
# 타입 스펙: type-tree — 부모에서 자식으로 갈라지는 계층. coral 은 동시성 국면 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

SX = 500
NODE_W, NODE_H = 288, 48
CH_W, CH_H, CH_GAP = 236, 32, 8
BUS, ROW_GAP, PHASE_GAP = 180, 40, 36

phases = [
    ("문법과 손", "0~2단계", INFO, [
        ("0 · A Tour of Go · 공식 튜토리얼", "go.dev/tour",
         ["값 · 변수 · 제어문", "메서드와 인터페이스"], ["고루틴과 채널 맛보기"],
         ["Go 설치와 모듈 초기화", "go.dev 시작 튜토리얼 여덟"]),
        ("1 · Learning Go 2nd", "1~6장 · 2024",
         ["선언과 타입", "슬라이스와 맵", "함수와 클로저"], ["포인터와 값 의미론", "제로값 관용구"],
         ["이스케이프 분석", "go vet · staticcheck"]),
        ("2 · Learning Go 2nd", "7~9장 · 2024",
         ["구조체 임베딩", "인터페이스 암묵 구현"], ["제네릭과 타입 파라미터", "에러를 값으로 다루기"],
         ["errors.Is · As · wrap", "인터페이스 오염 피하기"]),
    ]),
    ("관용구와 도구", "3~5단계", INFO, [
        ("3 · Effective Go · Code Review Comments", "공식",
         ["이름 짓기와 패키지 경계", "관용적 에러 처리"], ["인터페이스는 쓰는 쪽에서", "동시성 관용구"],
         ["Google Go Style Guide", "gofmt 가 끝낸 논쟁"]),
        ("4 · Learning Go 2nd", "10·11·13·14장 · 2024",
         ["모듈과 최소 버전 선택", "go 툴체인"], ["표준 라이브러리", "context 의 취소와 값"],
         ["workspace 모드", "pkg.go.dev 읽는 법"]),
        ("5 · 100 Go Mistakes", "전권 · 2022",
         ["슬라이스 공유와 재할당", "인터페이스와 nil"], ["고루틴 누수", "표준 라이브러리의 함정"],
         ["race detector", "벤치마크로 확인하기"]),
    ]),
    ("동시성", "6~8단계", ACC, [
        ("6 · Learn Concurrent Programming with Go", "1~7장 · 2023",
         ["스레드와 고루틴", "메모리 공유의 위험"], ["뮤텍스와 조건변수", "웨이트그룹과 배리어"],
         ["GOMAXPROCS 와 스케줄러", "세마포어 패턴"]),
        ("7 · Learning Go 12장 · LCPG 8~10장", "2024 · 2023",
         ["채널과 select", "파이프라인"], ["fan-in 과 fan-out", "취소 전파"],
         ["errgroup", "채널 대신 뮤텍스를 고를 때"]),
        ("8 · The Go Memory Model · LCPG", "공식 · 11~12장",
         ["happens-before 관계", "데드락의 네 조건"], ["원자 연산과 스핀락"],
         ["sync.Once · atomic.Value", "false sharing"]),
    ]),
    ("테스트와 성능", "9~10단계", INFO, [
        ("9 · Learn Go with Tests · Learning Go", "무료 · 15장",
         ["테이블 주도 테스트", "인터페이스로 가짜 만들기"], ["커버리지와 벤치마크", "퍼징"],
         ["testify 를 쓸지 말지", "golden file 테스트"]),
        ("10 · pprof · trace · Learning Go", "공식 · 16장",
         ["CPU 와 힙 프로파일", "실행 추적"], ["reflect · unsafe · cgo 의 대가"],
         ["GOGC 와 GOMEMLIMIT", "할당을 줄이는 법"]),
    ]),
    ("서비스로", "11~12단계", INFO, [
        ("11 · Network Programming with Go", "1~9장 · 2020",
         ["소켓과 주소 해석", "TCP 스트림"], ["UDP 와 신뢰성", "HTTP 클라이언트와 서버"],
         ["메서드·와일드카드 라우팅", "log/slog 구조화 로깅"]),
        ("12 · Cloud Native Go 2nd", "4~13장 · 2024",
         ["클라우드 네이티브 패턴", "확장성과 느슨한 결합"], ["복원력", "관측 가능성과 보안"],
         ["OpenTelemetry Go SDK", "구조화 로깅 slog"]),
    ]),
]

tail = [
    ("13 · Learn Go with Pocket-Sized Projects", "전 12장 · 2025",
     ["CLI 와 라이브러리 만들기", "제네릭 캐시"], ["gRPC 서비스", "동시성 미로 풀이"],
     ["크로스 컴파일", "데이터베이스 연결"]),
    ("14 · Writing An Interpreter In Go", "1.7판 · 2020",
     ["렉서와 파서", "AST 순회"], ["평가기와 환경"],
     ["Writing a Compiler in Go 로 잇기"]),
]

NOTE_H = 76
NOTES = {'관용구와 도구': '문법을 알아도 관용구를 모르면 Go 로 Java 를 쓰게 된다. 이 국면이 그 간격을 메운다.', '동시성': 'Go 를 쓰는 이유의 절반이 여기 있다. 2017년 책 대신 2023년 LCPG 8~10장으로 채웠다.'}

def ph_note(name):
    return NOTES.get(name)

def row_h(left, right, extra):
    n = max(len(left), len(right) + len(extra))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 24

y = 116 + 96 + 48 + PHASE_GAP
for _n, _, _, steps in phases:
    y += NODE_H + ROW_GAP
    for s in steps:
        y += row_h(s[2], s[3], s[4]) + ROW_GAP
    y += (NOTE_H if ph_note(_n) else 0) + PHASE_GAP - ROW_GAP
y += 56
for s in tail:
    y += row_h(s[2], s[3], s[4]) + ROW_GAP
H, W = y + 76, 1000

d = D(W, H, "WRITE · GO ROADMAP",
      "Go 언어 학습 로드맵",
      "위에서 아래로 읽는 순서. 척추에 국면 다섯과 단계 열다섯을 걸고 각 단계에서 배우는 개념을 좌우로 뻗었다. "
      "실선 박스는 책과 공식 문서가 다루는 개념이고, 점선 박스는 그 밖에서 채울 키워드다. "
      "절단선 아래 둘은 목표가 생겼을 때만 여는 조건부 단계다.",
      "실선은 책과 공식 문서가 다루는 개념, 점선은 그 밖에서 채울 키워드입니다")

READ_KINDS = [('책과 공식 문서가 다루는 개념', 'book'), ('그 밖에서 채울 키워드', 'extra')]

# 좌상단 읽는 법 상자 — roadmap.sh 판형의 범례 자리
LX, LY, LW, LH = 40, 96, 320, 84
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for _i, (_txt, _kind) in enumerate(READ_KINDS):
    _cy = LY + 46 + _i * 20
    if _kind == "extra":
        d.o.append(f'<rect x="{LX + 16}" y="{_cy - 8}" width="18" height="14" rx="3" fill="{PAPER}" '
                   f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="3 3"/>')
    else:
        d.o.append(f'<rect x="{LX + 16}" y="{_cy - 8}" width="18" height="14" rx="3" '
                   f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(LX + 44, _cy + 3, _txt, 13, MUTED, KR, "start")

def draw_note(text, y):
    d.o.append(f'<rect x="120" y="{y}" width="760" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(140, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(140, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H

ROOT_Y = 116 + 96
d.box(SX - 120, ROOT_Y, 240, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 100, RULE, 1.4)

def draw_step(title, chap, left, right, extra, y):
    h = row_h(left, right, extra)
    mid = y + h / 2
    for side, items in (("left", [(v, False) for v in left]),
                        ("right", [(v, False) for v in right] + [(v, True) for v in extra])):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (label, dashed) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 36) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 36, cy, RULE, 1.0)
            if dashed:
                d.o.append(f'<rect x="{bx}" y="{cy - CH_H/2}" width="{CH_W}" height="{CH_H}" rx="6" '
                           f'fill="{PAPER}" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
                d.t(bx + CH_W / 2, cy + 5, label, 13, SOFT, KR, "middle")
            else:
                d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
                d.t(bx + CH_W / 2, cy + 5, label, 13, MUTED, KR, "middle")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, RULE, 1.0)
    d.t(SX, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 14, chap, 12, SOFT, MONO)
    return h

y = ROOT_Y + 48 + PHASE_GAP
for name, stage, color, steps in phases:
    if color is ACC:
        d.tone(SX - NODE_W / 2, y, NODE_W, NODE_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - NODE_W / 2, y, NODE_W, NODE_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, stage, 12, SOFT, MONO)
    y += NODE_H + ROW_GAP
    for s in steps:
        y += draw_step(*s, y) + ROW_GAP
    if ph_note(name):
        y += draw_note(ph_note(name), y)
    y += PHASE_GAP - ROW_GAP

d.line(40, y + 20, W - 40, y + 20, WARN, 1.4, "6 5")
d.o.append(f'<rect x="{SX - 108}" y="{y + 8}" width="216" height="22" rx="4" fill="{PAPER}"/>')
d.t(SX, y + 25, "여기부터는 목표가 생겼을 때만", 13, WARN, KR)
y += 56
for s in tail:
    y += draw_step(*s, y) + ROW_GAP

d.legend(H - 68, [("책과 공식 문서", INFO), ("가장 큰 덩어리", ACC), ("그 밖의 키워드", SOFT)])
d.save("go-roadmap.svg")
