# 04-02.chapter-overview — io.Copy 로 양방향 프록시를 잇고, TeeReader·MultiWriter 로 소켓을 엿보며, TCP 핸드셰이크로 핑을 대신한다
# 본문 요구(04-02 「학습 목표」 개념도 문단): §1 줄 양방향 프록시와 CloseWrite half-close, §2 줄 TeeReader·MultiWriter 트래픽 관측과 지연 방어,
#           §3 줄 net.DialTimeout 핸드셰이크 측정과 오류 판별.
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.4 Sending TCP Data (Listing 4-14~4-22),
#           net.TCPConn.CloseWrite, io.Copy, io.TeeReader, io.MultiWriter, net.DialTimeout.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 520


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-02 OVERVIEW",
      "io.Copy 로 프록시를 잇고 TeeReader 로 엿보며 TCP 핸드셰이크로 핑을 대신합니다",
      "04-02 의 키워드 개념도. 윗줄(§1)은 io.Copy 로 양방향 독립 고루틴을 엮고 CloseWrite 로 FIN 을 넘긴 뒤 conn.Close 로 안전하게 닫는 프록시다. "
      "가운데 줄(§2)은 TeeReader 와 MultiWriter 로 트래픽을 복제하고 nil 에러 반환과 버퍼 채널로 소켓 통신을 보호하는 무침습 관측이다. "
      "아랫줄(§3)은 net.DialTimeout 으로 TCP 3-way 핸드셰이크 경과 시간 dur 을 재고 Timeout 으로 오류를 판별하는 핑 대체 흐름이다.",
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


for i, sec in enumerate(("§1", "§2", "§3")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

# §1: io.Copy 양방향 프록시와 CloseWrite half-close 완성
node(0, 0, "io.Copy", "방향마다 독립 고루틴", INFO)
node(0, 1, "CloseWrite()", "단방향 FIN 전달", ACC)
node(0, 2, "Close()", "양방향 종료 후 자원 반환", OK)
harrow(0, 0, "EOF 수신 시")
harrow(0, 1, "양방향 모두 끝나면")

# §2: TeeReader·MultiWriter 무침습 관측과 블로킹·에러 방어
node(1, 0, "TeeReader · MultiWriter", "수신 복제 · 송신 분기", INFO)
node(1, 1, "nil 에러 반환", "소켓 전송 중단 방어", WARN)
node(1, 2, "버퍼 채널 비동기 기록", "로그 유실 감수 · 지연 보존", OK)
harrow(1, 0, "로깅 실패 시")
harrow(1, 1, "느려짐까지 끊으려면")

# §3: net.DialTimeout 핸드셰이크 시간 측정과 ICMP 대체 핑
node(2, 0, "net.DialTimeout", "서비스 포트 다이얼", INFO)
node(2, 1, "dur (경과 시간)", "포트 생존 · 왕복 지연 실측", OK)
node(2, 2, "Timeout()", "RST 거부와 무응답 가름", WARN)
harrow(2, 0, "핸드셰이크 완료 시")
harrow(2, 1, "실패면 err 로")

d.legend(456, [("표준 I/O 장치", INFO), ("정상 완료 · 실측", OK), ("에러 격리 · 판별", WARN), ("half-close 전달", ACC)])
d.save("04-02.chapter-overview.svg")
print("ok 04-02 overview")
