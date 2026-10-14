# 03-01.chapter-overview — 패킷 손실과 혼잡을 재전송으로 메우고, 세션은 핸드셰이크와 순서 번호로 열며, 수신 버퍼와 창 크기가 속도를 묶고, conn.Close 와 FIN·TIME_WAIT 로 닫는다
# 본문 요구(03-01 「학습 목표」 개념도 문단): 윗줄 패킷 손실과 전송 제어(§1), 둘째 줄 3-way 핸드셰이크와 순서 번호·ACK(§2),
#           셋째 줄 수신 버퍼와 슬라이딩 윈도(§3), 넷째 줄 conn.Close 와 FIN·TIME_WAIT 정상 종료(§4).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.3 Reliable TCP Data Streams, RFC 9293, RFC 793.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 648


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 03-01 OVERVIEW",
      "세션은 핸드셰이크로 열고 창으로 속도를 맞추며 FIN 으로 닫습니다",
      "03-01 의 키워드 개념도. 윗줄은 패킷 손실과 혼잡을 재전송과 전송률 조절로 극복해 결함 없는 바이트 흐름을 만드는 길이다. "
      "둘째 줄은 net.Dial 호출 뒤에서 3-way 핸드셰이크로 세션을 열고 순서 번호와 누적 ACK 로 데이터를 추적하는 흐름이다. "
      "셋째 줄은 수신 버퍼와 Window Size 로 전송 속도를 묶고 Zero Window 로 멈춰 세우는 슬라이딩 윈도다. "
      "넷째 줄은 conn.Close 로 시작하는 양방향 FIN·ACK 교환과 TIME_WAIT 대기를 거쳐 세션을 안전하게 정리하는 정상 종료다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "패킷 손실 · 혼잡", "전송 오류 · 대역폭 포화")
node(0, 1, "재전송 · 전송률 조절", "손실 감지 · 순서 재정렬", INFO)
node(0, 2, "결함 없는 바이트 흐름", "하위 결함 은닉 · 신뢰성 보장", OK)
harrow(0, 0, "확인응답 미수신 감지")
harrow(0, 1, "번호 맞춰 순서 재조립")

node(1, 0, "net.Dial", "Go 연결 수립 호출")
node(1, 1, "3-way Handshake", "SYN · SYN/ACK · ACK", INFO)
node(1, 2, "순서 번호 · 누적 ACK", "net.Conn 반환 · 전송 추적", OK)
harrow(1, 0, "커널이 핸드셰이크 은닉")
harrow(1, 1, "ESTABLISHED 수립")

node(2, 0, "수신 버퍼", "conn.Read() 로 소비")
node(2, 1, "Window Size", "ACK 에 실리는 수신 창", INFO)
node(2, 2, "Zero Window", "송신 중단 · 버퍼 차면 Write 대기", WARN)
harrow(2, 0, "ACK 에 잔여 창 통보")
harrow(2, 1, "읽기 지연 시 창 고갈")

node(3, 0, "conn.Close()", "정상 종료 절차 트리거")
node(3, 1, "양방향 FIN 교환", "FIN_WAIT_1 · CLOSE_WAIT", INFO)
node(3, 2, "TIME_WAIT", "2 × MSL 대기 후 CLOSED", OK)
harrow(3, 0, "FIN 전송 시작")
harrow(3, 1, "최종 ACK 회신 후")

d.legend(584, [("TCP 제어 · 교환", INFO), ("정상 도달 · 보장", OK), ("전송 대기", WARN)])
d.save("03-01.chapter-overview.svg")
print("ok 03-01 overview")
