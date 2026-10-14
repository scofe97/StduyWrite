# 04-01.chapter-overview — net.Conn 은 파일처럼 읽고 쓰며, 고정 버퍼·bufio.Scanner·TLV 로 메시지를 자르고, 일시적 오류는 Timeout 으로 판별해 재시도한다
# 본문 요구(04-01 「학습 목표」 개념도 문단): §1 줄 net.Conn 표준 I/O 호환, §2 줄 conn.Read 고정 버퍼 수신과 io.EOF,
#           §3 줄 bufio.Scanner 구분자 토큰화, §4 줄 TLV 고정 헤더와 MaxPayloadSize 보안 한도, §5 줄 Timeout 판별과 재시도 루프.
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자, 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표 하나.
#           관계 라벨은 화살표 위(가로) 또는 오른쪽(세로)에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: 《Network Programming with Go》 Ch.4 Sending TCP Data (Listing 4-1~4-13),
#           net.Conn, io.ReadWriteCloser, conn.Read, bufio.Scanner, MaxPayloadSize, net.Error.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 768


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 04-01 OVERVIEW",
      "TCP 는 경계가 없어 읽는 쪽이 메시지를 자릅니다",
      "04-01 의 키워드 개념도. §1 줄은 net.Conn 이 io.ReadWriteCloser 를 구현해 표준 도구와 결합하는 구조다. "
      "§2 줄은 고정 버퍼로 읽을 때 conn.Read 가 도착한 만큼만 채우므로 buf[:n] 을 슬라이싱하고 io.EOF 로 마치는 흐름이다. "
      "§3 줄은 구분자가 있는 스트림을 bufio.Scanner 와 Split 으로 잘라 온전한 토큰 단위로 추출하는 방식이다. "
      "§4 줄은 5바이트 고정 헤더와 MaxPayloadSize 로 메모리 고갈을 막고 io.ReadFull 로 페이로드를 채우는 TLV 구조다. "
      "§5 줄은 쓰기 오류 발생 시 Timeout 판별을 거쳐 10초 대기 후 최대 7회까지 재시도하는 복구 루프다.",
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


for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1: net.Conn 은 파일처럼 읽고 쓴다
node(0, 0, "net.Conn", "소켓 추상화 인터페이스", INFO)
node(0, 1, "io.ReadWriteCloser", "Read · Write · Close")
node(0, 2, "파일과 같은 인터페이스", "표준 도구에 그대로 연결", OK)
harrow(0, 0, "인터페이스 구현")
harrow(0, 1, "파일처럼 다룸")

# §2: 고정 버퍼로 읽으면 메시지 경계는 내 몫이다
node(1, 0, "conn.Read(buf)", "도착한 만큼만 반환", INFO)
node(1, 1, "buf[:n]", "유효 데이터 슬라이싱")
node(1, 2, "io.EOF", "정상 스트림 종료 신호", OK)
harrow(1, 0, "n 바이트 읽음")
harrow(1, 1, "연결 닫히면")

# §3: 구분자가 있으면 bufio.Scanner 로 자른다
node(2, 0, "bufio.NewScanner", "소켓을 감싸 버퍼링", INFO)
node(2, 1, "scanner.Split", "ScanWords 구분자 지정")
node(2, 2, "scanner.Text()", "온전한 토큰 단위 반환", OK)
harrow(2, 0, "분할 규칙 설정")
harrow(2, 1, "Scan 호출마다")

# §4: TLV 로 길이를 먼저 보내 버퍼를 알맞게 잡는다
node(3, 0, "5바이트 고정 헤더", "Type 1B + Length 4B", INFO)
node(3, 1, "MaxPayloadSize", "10MB 상한 · OOM 방어", ACC)
node(3, 2, "io.ReadFull", "페이로드 전체 반복 수신", OK)
harrow(3, 0, "길이 검증")
harrow(3, 1, "한도 안이면")

# §5: 읽기·쓰기 오류는 일시적일 수 있다
node(4, 0, "conn.Write", "네트워크 전송 오류 발생", INFO)
node(4, 1, "nErr.Timeout()", "타임아웃 여부 판별", WARN)
node(4, 2, "10초 대기 재시도", "최대 7회 루프", OK)
harrow(4, 0, "오류 발생 시")
harrow(4, 1, "타임아웃이면")

varrow(0, 0, "소켓에서 읽음")

d.legend(712, [("핵심 API · 헤더", INFO), ("정상 완료 · 해결", OK), ("타임아웃 판별", WARN), ("보안 상한", ACC)])
d.save("04-01.chapter-overview.svg")
print("ok 04-01 overview")
