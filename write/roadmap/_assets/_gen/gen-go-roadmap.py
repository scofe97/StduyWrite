# write/roadmap/go-roadmap.md §학습 순서 — Go 학습 로드맵.
#
# 이 로드맵은 보유 노트가 0편이다. write/ 어디에도 Go 카테고리가 없으므로 노드의 책 줄이
#   유일한 자료 표시다. 그래서 다른 편보다 책 줄이 촘촘하고, 빈 줄은 소장본도 없는 자리다.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다. 단계에만 배지를 달던 앞 판은 한 단계 안에서
#   무엇이 뼈대이고 무엇이 곁가지인지 말하지 못했다.
#
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다. 정독 노트 편수는 도식에 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보다. 노트 링크는 본문 단계 표가 맡는다.
#
# 대체(ACC)는 같은 자리를 두 자료가 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree — 부모(단계)에서 자식(개념)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 52
CH_W, CH_H, CH_GAP = 268, 46, 10
BUS, ROW_GAP, PHASE_GAP = 184, 44, 40
NOTE_H = 76
ELBOW = 14

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계 제목, 단계 부제, [왼쪽], [오른쪽])
#   개념 노드 = (개념, 책 챕터 — 없으면 빈 문자열, 우선순위)
stages = [
    ("1 · 문법", "빠르게 통과하되 값 의미론은 붙잡는다",
     [("개발 환경 · go 명령", "Learning Go 1장", "필수"),
      ("변수 · 상수 · 선언", "Learning Go 2장", "필수"),
      ("if · for · switch · 섀도잉", "Learning Go 4장", "필수"),
      ("함수 · 다중 반환 · defer", "Learning Go 5장", "필수"),
      ("포인터와 값 의미론", "Learning Go 6장", "필수")],
     [("array · slice · append", "Learning Go 3장", "필수"),
      ("map · struct · zero value", "Learning Go 3장", "필수"),
      ("무엇이 복사되고 무엇이 공유되는가", "Learning Go 3·6장", "필수"),
      ("작은 프로젝트로 손에 익히기", "Pocket-Sized Projects 2~5장", "대체")]),

    ("2 · 타입 설계", "상속 대신 조합, 예외 대신 값",
     [("메서드 · receiver · method set", "Learning Go 7장", "필수"),
      ("인터페이스 · 암묵 구현 · 배치", "Learning Go 7장", "필수"),
      ("embedding · 조합", "Learning Go 7장", "필수"),
      ("type assertion · type switch", "Learning Go 7장", "추천")],
     [("error value · wrapping", "Learning Go 9장", "필수"),
      ("errors.Is · errors.As", "Learning Go 9장", "필수"),
      ("제네릭 · 타입 파라미터 · 제약", "Learning Go 8장", "추천"),
      ("제네릭으로 캐시 만들기", "Pocket-Sized Projects 7장", "선택")]),

    ("3 · 관용구와 도구", "Go 답게 쓰고 도구로 검사한다",
     [("패키지 경계 · 네이밍", "Learning Go 10장", "필수"),
      ("module · MVS · workspace", "Learning Go 10장", "필수"),
      ("go build · vet · staticcheck", "Learning Go 11장", "필수"),
      ("표준 라이브러리 지도", "Learning Go 13장", "추천")],
     [("context — 취소와 값 전달", "Learning Go 14장", "필수"),
      ("slice aliasing · interface nil", "", "추천"),
      ("goroutine leak · loop variable", "", "추천"),
      ("reflect · unsafe · cgo", "Learning Go 16장", "선택")]),

    ("4 · 동시성", "공유로 통신하지 말고 통신으로 공유한다",
     [("goroutine · GOMAXPROCS · 스케줄러", "Learn Concurrent Go 2장", "필수"),
      ("메모리 공유와 경쟁 상태", "Learn Concurrent Go 3장", "필수"),
      ("mutex · RWMutex", "Learn Concurrent Go 4장", "필수"),
      ("조건 변수 · 세마포어", "Learn Concurrent Go 5장", "추천"),
      ("WaitGroup · barrier", "Learn Concurrent Go 6장", "필수")],
     [("channel · buffered · select", "Learning Go 12장", "필수"),
      ("message passing · 채널 패턴", "Learn Concurrent Go 7~9장", "필수"),
      ("pipeline · fan-in · fan-out", "Learn Concurrent Go 10장", "추천"),
      ("deadlock 회피", "Learn Concurrent Go 11장", "추천"),
      ("채널 소유권 — 닫기는 한 곳에서", "Learn Concurrent Go 7장", "필수"),
      ("sync.Once — 중복 close 막기", "", "추천"),
      ("atomic · spin lock · futex", "Learn Concurrent Go 12장", "추천"),
      ("happens-before · race detector", "", "필수")]),

    ("5 · 테스트와 성능", "추측 대신 재고 남길 테스트만 남긴다",
     [("table-driven test · test double", "Learning Go 15장", "필수"),
      ("coverage · golden file", "Learning Go 15장", "추천"),
      ("benchmark · fuzzing", "Pocket-Sized 부록 D·F", "추천")],
     [("pprof 네 축 — CPU · heap", "", "필수"),
      ("runtime/trace · 스케줄러 추적", "", "추천"),
      ("escape analysis · 할당 줄이기", "", "추천"),
      ("GC · GOGC · GOMEMLIMIT", "", "추천")]),

    ("6 · 서비스", "네트워크 현상을 직접 구현해 본다",
     [("네트워크 개요 · 주소 해석 · 라우팅", "Network Programming Go 1·2장", "필수"),
      ("TCP 스트림 · 데이터 전송", "Network Programming Go 3·4장", "필수"),
      ("UDP · 신뢰성 보강", "Network Programming Go 5·6장", "추천"),
      ("TLS 로 통신 지키기", "Network Programming Go 11장", "추천"),
      ("Unix domain socket", "Network Programming Go 7장", "선택")],
     [("HTTP 클라이언트 · 타임아웃", "Network Programming Go 8장", "필수"),
      ("HTTP 서비스 · 라우팅", "Network Programming Go 9장", "필수"),
      ("직렬화 · 로깅 · 지표", "Network Programming Go 12·13장", "추천"),
      ("복원력 · 느슨한 결합", "Cloud Native Go 8·9장", "추천"),
      ("관리성 · 관측성 · 보안", "Cloud Native Go 10~12장", "추천"),
      ("go:embed — 정적 자원 품기", "Cloud Native Go 10장", "추천"),
      ("distroless · 멀티스테이지 이미지", "", "추천"),
      ("syscall/js — Wasm 이라는 경계", "", "선택"),
      ("gRPC 서비스 만들기", "Pocket-Sized Projects 10·11장", "선택")]),

    ("7 · 터미널과 세션", "사람이 붙어 있는 연결을 다룬다",
     [("SSH 3계층 — 전송 · 인증 · 연결", "", "필수"),
      ("pty-req 와 window-change", "", "필수"),
      ("세션 채널과 애플리케이션 경계", "", "필수"),
      ("ANSI CSI 로 화면 직접 그리기", "", "추천")],
     [("rune · grapheme · 터미널 셀 폭", "", "필수"),
      ("논블로킹 알림과 신호 병합", "", "필수"),
      ("인증과 인가는 다른 문제다", "", "필수"),
      ("슬라이딩 윈도우 속도 제한", "", "추천"),
      ("세션 정리와 자원 상한", "", "추천")]),
]

CUT_AFTER = 2          # 3단계 뒤에 "언어" ↔ "동시성과 서비스" 절단선
NOTES = {
    2: "1~3단계는 언어를 익히는 구간이고 4단계부터가 Go 를 고르는 이유다.",
    5: "이 로드맵은 보유 노트가 0편이다. 책 줄이 유일한 자료이고, 빈 줄은 소장본도 없는 자리다.",
}


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 28


ROOT_Y = 116 + 190
y = ROOT_Y + 52 + PHASE_GAP
for i, (_t, _s, left, right) in enumerate(stages):
    y += row_h(left, right) + ROW_GAP
    if i in NOTES:
        y += NOTE_H
    if i == CUT_AFTER:
        y += 56
H = y + 84

d = D(W, H, "WRITE · GO ROADMAP",
      "Go 학습 로드맵",
      "애플리케이션이 여는 socket 에서 커널 패킷 경로로 내려간 뒤 Kubernetes 데이터패스로 다시 "
      "올라간다. 척추에 단계 여덟을 걸고 개념을 좌우로 뻗었다. 노드의 주인공은 개념이고 아래 줄은 "
      "그 개념을 다루는 책의 장이다. 점 색이 우선순위이고, 책 줄이 비면 아직 자료가 없는 자리다.",
      "노드는 개념, 아래 줄은 그 개념을 다루는 책의 장입니다")

LX, LY, LW, LH = 40, 96, 380, 190
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만"),
                                ("대체", "같은 자리 — 하나만 고릅니다")]):
    cy = LY + 54 + i * 26
    c = MARK[lab]
    d.o.append(f'<circle cx="{LX + 24}" cy="{cy}" r="5" fill="{c}"/>')
    d.t(LX + 40, cy + 4, lab, 12, c, KR, "start", 600)
    d.t(LX + 78, cy + 4, txt, 12, MUTED, KR, "start")
d.t(LX + 16, LY + 172, "책 줄이 비면 아직 자료가 없는 자리 — 개념이 먼저입니다", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("network-roadmap", "TCP · TLS · HTTP 의 프로토콜 축"),
        ("os-roadmap", "epoll · 스케줄러 · 프로파일 방법론"),
        ("Learning Go 16장", "reflect · unsafe · cgo — 필요할 때만"),
        ("Cloud Native Go 1~3장", "클라우드 네이티브 개론과 Go 소개")]):
    cy = RY + 56 + i * 33
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 52, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 32, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 52, SX, H - 120, RULE, 1.4)


def draw_stage(title, sub, left, right, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (concept, book, mark) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * ELBOW) - (CH_W if side == "left" else 0)
            c = MARK[mark]
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * ELBOW, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.o.append(f'<circle cx="{bx + 15}" cy="{cy - 8}" r="4.5" fill="{c}"/>')
            d.t(bx + 28, cy - 4, concept, 12, INK, KR, "start")
            d.t(bx + 28, cy + 14, book if book else "책 없음 — 채울 자리", 10,
                SOFT if book else MARK["선택"], MONO, "start")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, INFO, 1.2)
    d.t(SX, mid - 4, title, 14, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, KR)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


y = ROOT_Y + 52 + PHASE_GAP
for i, (title, sub, left, right) in enumerate(stages):
    y += draw_stage(title, sub, left, right, y) + ROW_GAP
    if i in NOTES:
        y += draw_note(NOTES[i], y)
    if i == CUT_AFTER:
        d.line(40, y + 12, W - 40, y + 12, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 235}" y="{y}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~3단계는 언어 · 4단계부터는 Go 를 고르는 이유", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("언어와 활용의 경계", WARN)])
d.save("go-roadmap.svg")
