# 05-01.chapter-overview — 8바이트 헤더와 세션 부재로 최신 데이터를 지연 없이 방출하고, net.ListenPacket 과 ReadFrom·WriteTo 로 에코 서버를 구현하며, 단일 소켓 리스너의 제3자 패킷을 발신 주소 검증으로 걸러낸다
# 본문 요구(05-01 「학습 목표」 개념도 문단): §1 줄은 8바이트 헤더와 최신 데이터 우선(§1), §2 줄은 net.ListenPacket 과 ReadFrom·WriteTo(§2),
#           §3 줄은 단일 소켓 리스너와 제3자 패킷 및 발신 주소 검증(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자, 행 안은 가로 화살표, 행 사이는 세로 화살표 하나.
#           관계 라벨은 화살표 위(가로) 또는 오른쪽(세로)에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: 《Network Programming with Go》 Ch.5 Unreliable UDP Communication (Listing 5-1~5-5),
#           net.ListenPacket, net.PacketConn, ReadFrom, WriteTo, net.Addr, interloper.
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


d = D(W, H, "ARCHITECTURE · 05-01 OVERVIEW",
      "UDP 는 연결 없이 보내고 소켓 하나가 누구에게서든 받습니다",
      "05-01 의 키워드 개념도. 윗줄은 신뢰성 기능을 생략해 헤더가 8바이트로 작고 핸드셰이크가 없어 1 RTT 없이 최신 데이터를 방출하는 UDP 의 특성이다. "
      "가운데 줄은 Accept 없이 net.ListenPacket 으로 소켓을 열고 ReadFrom 이 반환한 주소로 WriteTo 에코를 보내는 서버 흐름이다. "
      "아랫줄은 모든 UDP 소켓이 리스너여서 제3자 패킷이 클라이언트 수신 큐에 끼어들 수 있어 발신 주소를 검증해야 한다는 원리다.",
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


def varrow(i, j, label):
    x = nx(j) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    d.arrow([(x, y1 + 2), (x, y2 - 4)], SOFT, "soft", 1.3)
    d.t(x + 10, (y1 + y2) / 2 + 4, label, 11, MUTED, kr(label), "start", 600)


for i, sec in enumerate(("§1", "§2", "§3")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12)

node(0, 0, "신뢰성 기능 생략", "8바이트 헤더 · 포트·길이·체크섬")
node(0, 1, "세션·핸드셰이크 부재", "최선형(best-effort) 전송", WARN)
node(0, 2, "최신 데이터 우선", "DNS 질의 · 기상 관측 스트리밍", OK)
harrow(0, 0, "연결 설정도 생략")
harrow(0, 1, "1 RTT 없이 바로 방출")

node(1, 0, "net.ListenPacket", "net.PacketConn 소켓 생성", INFO)
node(1, 1, "s.ReadFrom(buf)", "(n, clientAddr, err) 수신", INFO)
node(1, 2, "s.WriteTo(buf, addr)", "발신자 주소로 에코 전송", OK)
harrow(1, 0, "Accept 없이 소켓 열고")
harrow(1, 1, "돌려준 주소로")

node(2, 0, "단일 소켓 리스너", "리스너·연결 소켓 구분 없음")
node(2, 1, "제3자 (interloper)", "클라이언트 수신 큐에 끼어듦", WARN)
node(2, 2, "발신 주소 검증", "addr 비교 · 서버 응답 필터링", ACC)
harrow(2, 0, "누구에게서든 패킷 수신")
harrow(2, 1, "주소 다르면 다시 읽음")
varrow(1, 1, "클라이언트의 ReadFrom 에도")

d.legend(456, [("Go net 호출 · 구조", INFO), ("정상 전송 · 도메인 이점", OK), ("신뢰성 부재 · 방해", WARN), ("필수 주소 검증", ACC)])
d.save("05-01.chapter-overview.svg")
print("ok 05-01 overview")
