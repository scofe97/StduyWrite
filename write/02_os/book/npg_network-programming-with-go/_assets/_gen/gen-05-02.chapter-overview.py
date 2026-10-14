# 05-02.chapter-overview — net.Conn 으로 상대를 고정해 제3자 패킷을 거르고, MTU 실측 예산 아래로 보내 단편화를 피한다
# 본문 요구(05-02 「학습 목표」 개념도 문단): §1 바인딩 줄 net.Dial 목적지 등록과 net.Conn, §1 필터링 줄 제3자 패킷 차단과 client.Read,
#           §2 단편화 줄 MTU 초과 분할과 단일 조각 유실 시 전체 폐기, §2 MTU 실측 줄 ping DF 플래그와 1,472바이트 상한 도출.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.5 Unreliable UDP Communication (Listing 5-6~5-10, p.113–116),
#           net.Dial("udp", addr), net.Conn, client.Read, ping -M do, Message too long, 1,472바이트 MTU.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 648


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 05-02 OVERVIEW",
      "net.Conn 으로 상대를 고정하고 MTU 아래로 보내 단편화를 피합니다",
      "05-02 의 키워드 개념도. §1 바인딩 줄은 net.Dial 로 커널에 상대 주소를 등록하고 무핸드셰이크로 net.Conn 을 얻는 흐름이다. "
      "§1 필터링 줄은 제3자의 방해 패킷을 커널이 걸러내고 에코 서버의 응답만 client.Read 로 수신하는 과정이다. "
      "§2 단편화 줄은 MTU 를 넘는 대형 데이터그램이 IP 조각으로 나뉘어 조각 하나만 잃어도 전체가 폐기되는 위험이다. "
      "§2 MTU 실측 줄은 ping DF 플래그로 경로 한계를 확인하고 28바이트 헤더를 뺀 1,472바이트 페이로드 상한을 도출하는 길이다.",
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

# §1 바인딩: net.Dial 은 핸드셰이크 없이 원격 상대를 고정한다
node(0, 0, 'net.Dial("udp", addr)', "원격 목적지 주소 고정", INFO)
node(0, 1, "커널 소켓 기록", "로컬 소켓에 상대 등록")
node(0, 2, "net.Conn", "주소 없는 Read · Write", OK)
harrow(0, 0, "패킷 전송 없이 등록")
harrow(0, 1, "net.Conn 으로 반환")

# §1 필터링: 커널이 제3자 패킷을 거르고 Read/Write 를 단순화한다
node(1, 0, "제3자 방해 패킷", "interloper 로컬 전송", WARN)
node(1, 1, "커널 소켓 필터링", "수신 큐 진입 전 폐기")
node(1, 2, "client.Read(buf)", "발신 주소 확인 생략", OK)
harrow(1, 0, "다이얼 상대와 불일치")
harrow(1, 1, "에코 서버 응답만")

# §2 단편화: MTU 초과 데이터그램은 조각나고 하나만 잃어도 전체 폐기된다
node(2, 0, "대형 데이터그램", "MTU 초과 페이로드", WARN)
node(2, 1, "IP 단편화", "1,480바이트 조각 분할")
node(2, 2, "데이터그램 전체 폐기", "부분 복구 불가 · 손실 급증", BAD)
harrow(2, 0, "링크 MTU 초과 시")
harrow(2, 1, "단일 조각 유실 시")

# §2 MTU 실측: ping DF 실측으로 1,472바이트 안전 페이로드를 도출한다
node(3, 0, "ping -M do", "DF 비트 단편화 금지 실측", INFO)
node(3, 1, "Message too long", "헤더 포함 MTU 1,500B 초과", WARN)
node(3, 2, "1,472바이트 페이로드", "MTU 1,500 경로의 상한", OK)
harrow(3, 0, "1,500바이트 초과 시")
harrow(3, 1, "헤더 28바이트 차감")

d.legend(584, [("Go API · 탐측 명령", INFO), ("안전 전송 · 도출 상한", OK), ("방해 · 분할 · 한계 초과", WARN), ("데이터그램 폐기", BAD)])
d.save("05-02.chapter-overview.svg")
print("ok 05-02 overview")
