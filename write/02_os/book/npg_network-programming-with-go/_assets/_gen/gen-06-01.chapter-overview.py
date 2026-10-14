# 06-01.chapter-overview — TFTP 패킷 네 종이 바이트로 맞물려 UDP 신뢰성을 세웁니다
# 본문 요구(06-01 「학습 목표」 개념도 문단): §1 줄은 DatagramSize 에서 헤더 4바이트를 뺀 BlockSize 로 단편화를 피하고 stop-and-wait 로 왕복하는 규약의 기본선입니다.
#           §2 줄은 ReadReq 구조체가 필드 끝마다 0x00 종단자를 두고 역직렬화할 때 ReadString(0) 으로 파싱하는 읽기 요청입니다.
#           §3 줄은 Data 구조체가 io.Reader 페이로드를 싣고 d.Block++ 로 전진하다 65,535 블록을 넘기면 33.5MB 톱니를 만나는 한계입니다.
#           §4 줄은 Ack 가 블록 번호로 수신을 확인하고 오류 시 Err 패킷으로 세션을 즉시 폐기하는 대화의 닫힘입니다.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Network Programming with Go Ch.6 Ensuring UDP Reliability (Listing 6-1~6-8, Fig 6-1~6-5),
#           RFC 1350 (The TFTP Protocol Revision 2).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 680


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 06-01 OVERVIEW",
      "TFTP 패킷 네 종이 바이트로 맞물려 UDP 신뢰성을 세웁니다",
      "06-01 의 키워드 개념도. §1 줄은 DatagramSize 516바이트에서 헤더 4바이트를 뺀 512바이트 BlockSize 와 stop-and-wait 신뢰 전송의 기준이다. "
      "§2 줄은 ReadReq 구조체가 필드마다 0x00 종단자를 두고 ReadString(0) 으로 파싱하는 요청 규격이다. "
      "§3 줄은 Data 구조체가 io.Reader 페이로드를 싣고 d.Block++ 로 번호를 전진시키다 33.5MB 톱니 한계를 만나는 전송 흐름이다. "
      "§4 줄은 Ack 가 블록 번호로 수신을 확인하며 오류 발생 시 Err 패킷으로 통신을 즉시 폐기하는 대화의 닫힘이다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 TFTP 는 UDP 위의 작은 파일 전송 규약이다
node(0, 0, "DatagramSize", "516B · 단편화 회피", INFO)
node(0, 1, "BlockSize", "512B 순수 페이로드")
node(0, 2, "stop-and-wait", "블록마다 1 RTT 대기", OK)
harrow(0, 0, "헤더 4B 빼면")
harrow(0, 1, "1 블록씩 전송")

# §2 읽기 요청은 opcode·파일명·모드를 0 바이트로 끊는다
node(1, 0, "ReadReq", "Filename · Mode", INFO)
node(1, 1, "0x00 종단자", "가변 길이 경계 구분")
node(1, 2, "ReadString(0)", "역직렬화 파싱", OK)
harrow(1, 0, "필드 끝마다 배치")
harrow(1, 1, "널 바이트까지 읽음")

# §3 데이터 패킷은 블록 번호와 최대 512바이트를 싣는다
node(2, 0, "Data", "Block · Payload io.Reader", INFO)
node(2, 1, "d.Block++", "uint16 순차 증가")
node(2, 2, "33.5MB 톱니", "0 으로 랩어라운드", WARN)
harrow(2, 0, "호출할 때마다")
harrow(2, 1, "65,535 넘으면", WARN, "warn")

# §4 ACK 와 ERROR 패킷이 대화를 닫는다
node(3, 0, "Ack(uint16)", "고정 4바이트", INFO)
node(3, 1, "수신 확인", "블록 번호 통보", OK)
node(3, 2, "Err", "세션 즉시 폐기", ACC)
harrow(3, 0, "도착 블록 회신")
harrow(3, 1, "대신 오류면", ACC, "acc")

varrow(2, 0, "블록마다 회신")

d.legend(584, [("패킷 규격", INFO), ("정상 완료", OK), ("오버플로 주의", WARN), ("예외 종료", ACC)])
d.save("06-01.chapter-overview.svg")
print("ok 06-01 overview")
