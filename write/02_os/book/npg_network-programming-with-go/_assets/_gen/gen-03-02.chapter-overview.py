# 03-02.chapter-overview — Listen 과 포트 0으로 리스너를 열고, Accept 루프와 defer Close 로 고루틴을 분기하며, Dial 로 핸드셰이크를 감추고, conn.Close 와 io.EOF 로 정상 종료한다
# 본문 요구(03-02 「학습 목표」 개념도 문단): 첫째 줄 net.Listen 과 포트 0(§1), 둘째 줄 listener.Accept 와 고루틴 분기(§1),
#           셋째 줄 net.Dial 과 net.Conn(§2), 넷째 줄 conn.Close 와 io.EOF(§2).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.3 Reliable TCP Data Streams (Listing 3-1~3-3),
#           net.Listen, net.Listener, listener.Accept, net.Dial, net.Conn, io.EOF.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 648


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 03-02 OVERVIEW",
      "Go 의 TCP 연결은 Listen·Accept·Dial 세 호출로 맺는다",
      "03-02 의 키워드 개념도. 1행은 net.Listen 에 포트 0을 넘겨 임시 포트를 독점 바인딩하고 실제 주소를 확인하는 리스너 생성이다. "
      "2행은 listener.Accept 로 핸드셰이크 완료를 기다려 연결마다 고루틴을 분기하고 defer c.Close 로 소켓 FD 를 회수하는 수신 루프다. "
      "3행은 클라이언트가 net.Dial 로 주소를 해석하고 3-way 핸드셰이크를 거쳐 net.Conn 양방향 소켓을 얻는 연결 수립이다. "
      "4행은 conn.Close 로 시작된 FIN 세그먼트가 서버 c.Read 에 io.EOF 정상 종료 시그널로 전달되는 세션 종료다.",
      lead="화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.")


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("§1", "§1", "§2", "§2")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "net.Listen", '"tcp", "127.0.0.1:0"', INFO)
node(0, 1, "임시 포트 할당", "운영체제 동적 배정")
node(0, 2, "listener.Addr()", "할당 포트 조회", OK)
harrow(0, 0, "포트 0 지정 시")
harrow(0, 1, "실제 주소 확인")

node(1, 0, "listener.Accept()", "3-way 핸드셰이크 대기", INFO)
node(1, 1, "go func(c net.Conn)", "비동기 요청 처리")
node(1, 2, "defer c.Close()", "소켓 FD 회수 · 누수 방지", ACC)
harrow(1, 0, "연결마다 고루틴 분기")
harrow(1, 1, "핸들러 종료 시")

node(2, 0, "net.Dial", '"tcp", address', INFO)
node(2, 1, "핸드셰이크 은닉", "3-way 교환 완료 대기")
node(2, 2, "net.Conn", "양방향 데이터 소켓", OK)
harrow(2, 0, "주소 해석 · 다이얼")
harrow(2, 1, "성공 시 반환")

node(3, 0, "conn.Close()", "클라이언트 정상 종료", WARN)
node(3, 1, "c.Read(buf)", "블로킹 대기 중 깨어남", INFO)
node(3, 2, "io.EOF", "정상 종료 시그널 수신", OK)
harrow(3, 0, "FIN 세그먼트 전송")
harrow(3, 1, "전송 완료 통지")

d.legend(584, [("Go net 호출 · 동작", INFO), ("정상 수립 · 결과", OK), ("필수 정리", ACC), ("세션 종료 트리거", WARN)])
d.save("03-02.chapter-overview.svg")
print("ok 03-02 overview")
