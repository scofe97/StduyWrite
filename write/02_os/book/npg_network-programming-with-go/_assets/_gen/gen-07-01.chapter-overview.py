# 07-01.chapter-overview — Unix 도메인 소켓은 파일 경로로 묶이고 세 가지 타입이 경계를 다르게 다룹니다
# 본문 요구(07-01 「학습 목표」 개념도 문단): §1~2 줄은 파일시스템 경로를 소켓 주소로 삼아 네트워크 스택을 우회하고 os.Chmod 권한 통제와 UnlinkOnClose 자동 삭제로 수명 주기를 관리하는 기반입니다.
#           §3 줄은 unix 스트림 소켓에서 세 번 보낸 바이트가 단일 Read 로 합쳐질 수 있는 경계 없는 흐름입니다.
#           §4 줄은 unixgram 데이터그램 통신에서 서버 회신을 받으려면 클라이언트 소켓 파일 바인딩이 필수이고 패킷 경계가 보존되는 동작입니다.
#           §5 줄은 unixpacket 시퀀스 패킷 소켓이 1:1 연결 위에서 경계를 지키되 수신 버퍼를 넘긴 잔여 바이트를 즉시 버리는 성질입니다.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표 하나.
# 사실 출처: 《Network Programming with Go》 Ch.7 Unix Domain Sockets (Listing 7-1~7-12, Fig 7-1~7-3),
#           net.Listen, os.Chmod, SetUnlinkOnClose, net.Conn, net.ListenPacket, net.PacketConn.
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


d = D(W, H, "ARCHITECTURE · 07-01 OVERVIEW",
      "Unix 도메인 소켓은 파일 경로로 묶이고 세 가지 타입이 경계를 다르게 다룹니다",
      "07-01 의 키워드 개념도. "
      "§1~2 줄은 파일시스템 경로를 소켓 주소로 삼아 네트워크 스택을 우회하고 os.Chmod 권한 통제와 UnlinkOnClose 자동 삭제로 소켓 파일 수명 주기를 관리하는 기반이다. "
      "§3 줄은 unix 스트림 소켓에서 세 번 나눈 conn.Write 가 단일 Read 호출로 합쳐질 수 있는 경계 없는 동작이다. "
      "§4 줄은 unixgram 데이터그램 통신에서 서버 회신을 위해 클라이언트 소켓 파일 바인딩이 필수이고 4바이트 패킷 경계가 보존되는 흐름이다. "
      "§5 줄은 unixpacket 시퀀스 패킷 소켓이 1:1 연결형으로 경계를 지키되 버퍼보다 큰 초과 바이트를 영구 폐기하는 특성이다.",
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


for i, sec in enumerate(("§1~2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1~2 소켓 파일과 통신 원리
node(0, 0, "파일시스템 경로", "IP·포트 대신 소켓 주소", INFO)
node(0, 1, "os.Chmod(0660)", "소유자·그룹 권한 통제")
node(0, 2, "UnlinkOnClose", "스트림 Close 시 자동 삭제", OK)
harrow(0, 0, "소켓 파일 바인딩")
harrow(0, 1, "정상 종료 시")

# §3 스트림 타입 unix 로 에코 서버를 짠다
node(1, 0, '"unix" (스트림)', "순서 보장 양방향 세션", INFO)
node(1, 1, '3회 Write("ping")', "4B × 3 = 12B 연속 전송")
node(1, 2, "1회 Read(buf)", '"pingpingping" 일 수 있음', WARN)
harrow(1, 0, "conn.Write 분할 전송")
harrow(1, 1, "경계 없는 바이트 흐름", WARN, "warn")

# §4 unixgram 은 데이터그램 경계를 지키고 양쪽 모두 소켓 파일이 필요하다
node(2, 0, '"unixgram" (데이터그램)', "비연결형 독립 데이터그램", INFO)
node(2, 1, "클라이언트 파일 바인딩", "cSocket 생성 · 0622 권한", ACC)
node(2, 2, "3회 ReadFrom", "4B 데이터그램 경계 보존", OK)
harrow(2, 0, "서버 회신 주소용", ACC, "acc")
harrow(2, 1, "WriteTo 3회 전송 시")

# §5 unixpacket 은 연결형이면서 메시지 경계를 지킨다
node(3, 0, '"unixpacket" (시퀀스)', "연결형 세션 · macOS·Windows 미지원", INFO)
node(3, 1, "net.Conn 패킷 전달", "1:1 연결 위 경계 보존", OK)
node(3, 2, "초과 바이트 폐기", '2B 버퍼 시 "ng" 영구 삭제', WARN)
harrow(3, 0, "1:1 연결 수립")
harrow(3, 1, "버퍼 크기 미달 시", WARN, "warn")

varrow(0, 0, "네트워크 타입 지정")

d.legend(584, [("소켓 API · 타입", INFO), ("정상 동작 · 경계 보존", OK), ("결합 · 폐기 주의", WARN), ("필수 바인딩", ACC)])
d.save("07-01.chapter-overview.svg")
print("ok 07-01 overview")
