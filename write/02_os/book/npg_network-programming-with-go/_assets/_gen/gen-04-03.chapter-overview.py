# 04-03.chapter-overview — net.Conn 에서 TCPConn 을 꺼내고, keepalive·linger·버퍼를 제어하며, Zero Window 와 CLOSE_WAIT 를 막는다
# 본문 요구(04-03 「학습 목표」 개념도 문단): §1 줄 net.Conn 과 구체 타입 추출, §2 줄 KeepAliveConfig 와 커널 탐침,
#           §3 줄 SetLinger(0) 과 RST 강제 종료, §4 줄 SetReadBuffer 와 자동 튜닝 무력화, §5 줄 Zero Window·CLOSE_WAIT 와 defer Close.
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자, 행 안은 가로 화살표.
#           관계 라벨은 화살표 위에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: 《Network Programming with Go》 Ch.4 Sending TCP Data (Listing 4-23~4-27, p.32–38),
#           net.TCPConn, net.KeepAliveConfig, SetLinger, SetReadBuffer, Zero Window, CLOSE_WAIT.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 768


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-03 OVERVIEW",
      "TCPConn 손잡이로 소켓을 제어하고 누수 버그를 막습니다",
      "04-03 의 키워드 개념도. §1 줄은 net.Conn 에서 *net.TCPConn 구체 타입을 꺼내고 comma-ok 단언으로 이식성을 지키는 흐름이다. "
      "§2 줄은 KeepAliveConfig 로 주기와 횟수를 제어해 커널 빈 ACK 탐침으로 죽은 연결을 정리하는 L4 감지다. "
      "§3 줄은 SetLinger(0) 으로 미전송 데이터를 폐기하고 RST 세그먼트로 강제 종료하는 동작이다. "
      "§4 줄은 SetReadBuffer 호출로 커널 자동 튜닝이 꺼져 처리량이 떨어지는 위험이다. "
      "§5 줄은 별개인 두 결함을 나란히 둔다. handle() 블로킹이 부르는 Zero Window 는 수신과 처리를 나눠 피하고, Close 누락이 부르는 CLOSE_WAIT 고착은 defer c.Close() 로 막는다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1: net.Conn 아래의 TCPConn 을 꺼낸다
node(0, 0, "net.Conn", "인터페이스 추상화")
node(0, 1, "*net.TCPConn", "저수준 소켓 옵션 손잡이", INFO)
node(0, 2, "comma-ok 단언", "이식성 · 테스트 용이성 보존", OK)
harrow(0, 0, "구체 타입 추출")
harrow(0, 1, "필요한 곳만 단언")

# §2: keepalive 로 죽은 연결을 OS 가 찾게 한다
node(1, 0, "KeepAliveConfig", "Go 1.23+ 정밀 파라미터", INFO)
node(1, 1, "커널 빈 ACK 탐침", "유휴 연결 건전성 검사")
node(1, 2, "소켓 강제 정리", "죽은 연결 판정 · 파기", WARN)
harrow(1, 0, "유휴 주기 지정")
harrow(1, 1, "정한 횟수 침묵 시")

# §3: Close 뒤에 남은 데이터는 linger 가 정한다
node(2, 0, "SetLinger(0)", "강제 즉시 종료 지정", WARN)
node(2, 1, "conn.Close()", "기본값 -1 은 FIN 전송")
node(2, 2, "RST 세그먼트", "버퍼 폐기 · 상대 즉시 통보", BAD)
harrow(2, 0, "0초 지정 후 닫기")
harrow(2, 1, "FIN 대신 방출")

# §4: 수신·송신 버퍼 크기를 바꾼다
node(3, 0, "SetReadBuffer", "212992 바이트 수동 고정", INFO)
node(3, 1, "자동 튜닝 무력화", "수신 윈도 조절 중단", WARN)
node(3, 2, "처리량 급감", "고속망 BDP 미달 · 낭비", WARN)
harrow(3, 0, "호출 즉시 기능 꺼짐")
harrow(3, 1, "윈도 작게 묶이면")

# §5: 흔한 버그 둘 — zero window 와 CLOSE_WAIT
node(4, 0, "Zero Window", "수신·처리 분리로 방지", WARN)
node(4, 1, "CLOSE_WAIT", "커널 소켓 고착 · fd 고갈", BAD)
node(4, 2, "defer c.Close()", "종료 경로 무관 자원 회수", OK)
harrow(4, 0, "또 하나 · 닫기 누락")
harrow(4, 1, "시작 시 defer 등록")

d.legend(712, [("소켓 제어 API", INFO), ("안전 패턴 · 회수", OK), ("경고 · 성능 저하", WARN), ("강제 종료 · 소켓 고착", BAD)])
d.save("04-03.chapter-overview.svg")
print("ok 04-03 overview")
