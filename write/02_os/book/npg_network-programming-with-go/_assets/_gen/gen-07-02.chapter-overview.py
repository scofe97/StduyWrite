# 07-02.chapter-overview — 커널이 보증하는 피어 자격 증명으로 접속한 프로세스를 인증하고 미인가 연결을 차단합니다
# 본문 요구(07-02 「학습 목표」 개념도 문단): §1 줄은 SO_PEERCRED 로 커널 보증 신원을 확인하고 복제된 소켓 디스크립터를 통해 피어 자격 증명을 조회하는 기저입니다.
#           §2 줄은 전달받은 문자열 그룹 이름을 시스템 DB 에서 조회하여 O(1) 판정이 가능한 숫자 GID 집합으로 구축하는 인가 목록입니다.
#           §3 줄은 AcceptUnix 로 수락한 연결마다 피어의 보조 그룹 소속을 대조해 Welcome 전송 또는 즉시 차단으로 가르는 서버 루프입니다.
#           §4 줄은 netcat 으로 소켓에 접속하고 sudo -g 로 그룹을 전환하며 사용자 DB 장부 기준으로 인가가 판정되는 동작을 검증하는 시험입니다.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.7 Unix Domain Sockets — Writing a Service That Authenticates Clients (Listing 7-13~7-16),
#           Linux unix(7) SO_PEERCRED, dup(2), sudo(8).
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


d = D(W, H, "ARCHITECTURE · 07-02 OVERVIEW",
      "커널이 보증하는 피어 자격 증명으로 접속 프로세스를 인증합니다",
      "07-02 의 키워드 개념도. "
      "§1 줄은 커널이 보증하는 SO_PEERCRED 소켓 옵션을 conn.File() 과 GetsockoptUcred 로 질의해 위조 불가능한 피어 자격 증명을 얻는 기저다. "
      "§2 줄은 전달받은 문자열 그룹 이름을 user.LookupGroup 으로 조회해 빠른 판정이 가능한 map[string]struct{} 집합으로 구축하는 인가 목록이다. "
      "§3 줄은 s.AcceptUnix() 로 수락한 접속마다 auth.Allowed 로 피어 UID 가 사용자 DB 에서 속한 그룹을 대조해 Welcome 또는 연결 종료로 가르는 서버 루프다. "
      "§4 줄은 nc -U 로 소켓에 접속하고 sudo -g 로 기본 그룹을 바꿔도 그 그룹은 판정에서 빠지고 UID 의 사용자 DB 소속으로 인가가 정해지는지 시험하는 검증이다.",
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
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 커널이 접속한 프로세스의 신원을 알려 준다
node(0, 0, "SO_PEERCRED", "커널 보증 피어 자격 증명", INFO)
node(0, 1, "conn.File()", "*os.File 복제 · Close 필수", WARN)
node(0, 2, "GetsockoptUcred", "ucred.Uid 추출 · EINTR 재시도", OK)
harrow(0, 0, "조회할 fd 필요")
harrow(0, 1, "Fd() 로 질의")

# §2 그룹 이름을 그룹 ID 로 바꿔 허용 목록을 만든다
node(1, 0, "문자열 그룹 이름", "명령줄 인자 목록")
node(1, 1, "user.LookupGroup", "시스템 DB 에서 GID 조회", INFO)
node(1, 2, "map[string]struct{}", "값 0바이트 · O(1) 판정", OK)
harrow(1, 0, "시스템 DB 조회")
harrow(1, 1, "grp.Gid 등록")

# §3 접속마다 자격 증명을 보고 허용하거나 끊는다
node(2, 0, "s.AcceptUnix()", "*net.UnixConn 연결 수락", INFO)
node(2, 1, "auth.Allowed", "UID 의 DB 그룹 대조", INFO)
node(2, 2, "Welcome / 거부", "인가 시 환영 · 미인가 즉시 Close", ACC)
harrow(2, 0, "연결 넘겨 판정")
harrow(2, 1, "허용 여부 분기")

# §4 netcat 으로 서비스를 시험한다
node(3, 0, "nc -U", "/tmp/creds.sock 소켓 접속", INFO)
node(3, 1, "sudo -g", "실행 기본 그룹 변경", INFO)
node(3, 2, "UID 장부 대조", "사용자 DB 소속으로 판정", WARN)
harrow(3, 0, "-g 로 그룹 전환")
harrow(3, 1, "-g 그룹은 판정 제외")

d.legend(584, [("핵심 API · 도구", INFO), ("정상 조회 · 집합", OK), ("누수 주의 · 장부 판정", WARN), ("접근 제어 분기", ACC)])
d.save("07-02.chapter-overview.svg")
print("ok 07-02 overview")
