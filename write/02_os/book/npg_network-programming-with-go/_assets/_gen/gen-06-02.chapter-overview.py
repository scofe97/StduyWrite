# 06-02.chapter-overview — 요청마다 고루틴과 net.Dial 로 소켓을 분리하고, 512바이트 블록마다 ACK 대기와 재전송으로 전진하며, SHA512/256 해시로 다운로드 파일의 무결성을 검증한다
# 본문 요구(06-02 「학습 목표」 개념도 문단): §1 줄 고루틴과 net.Dial 전용 소켓 분리, §2 줄 정지-대기 전송과 타임아웃 재전송 루프, §3 줄 클라이언트 다운로드와 SHA512/256 무결성 검증.
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자, 행 안은 가로 화살표.
#           관계 라벨은 화살표 위에 둔다. 열 x = 60 + j·340, 노드 216×64, 행 y = 112 + i·128.
#           왼쪽 44px 열에는 그 행을 다루는 절 칩.
# 사실 출처: 《Network Programming with Go》 Ch.6 Ensuring UDP Reliability (Listing 6-9~6-13, p.15–25),
#           RFC 1350, net.PacketConn, net.Dial, SetReadDeadline, DatagramSize, sha512.Sum512_256.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 520


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "ARCHITECTURE · 06-02 OVERVIEW",
      "소켓을 분리해 응답하고 블록마다 ACK 를 확인합니다",
      "06-02 의 키워드 개념도. §1 줄은 69번 공용 소켓에서 요청을 받아 고루틴과 net.Dial 로 전용 소켓을 여는 연결 분리다. "
      "§2 줄은 512바이트 블록을 보내고 6초 타임아웃 재전송을 거쳐 516바이트 미만까지 전진하는 정지-대기 전송이다. "
      "§3 줄은 75,352바이트 파일을 다운로드하고 SHA512/256 해시로 원본과의 일치를 확인하는 무결성 검증이다.",
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

# §1: 서버는 요청마다 새 연결로 따로 응답한다
node(0, 0, "Server", "69번 net.PacketConn 감청")
node(0, 1, "go s.handle", "요청마다 고루틴 분기", INFO)
node(0, 2, "net.Dial", "임시 포트로 상대 고정", OK)
harrow(0, 0, "ReadReq 수신 시")
harrow(0, 1, "클라이언트 주소로")

# §2: 블록 하나를 보내고 ACK 를 받을 때까지 기다린다
node(1, 0, "정지-대기 전송", "512바이트 블록 송신")
node(1, 1, "RETRY 루프", "타임아웃 시 최대 10회", WARN)
node(1, 2, "NEXTPACKET", "516B 미만 시 전송 종료", OK)
harrow(1, 0, "6초 안에 ACK 대기")
harrow(1, 1, "ACK 번호 일치 시")

# §3: 받은 파일은 체크섬으로 확인한다
node(2, 0, "test.svg 다운로드", "148블록 · 75,352바이트")
node(2, 1, "SHA512/256", "64비트 최적화 · 32바이트", INFO)
node(2, 2, "체크섬 일치", "전송 무결성 최종 검증", OK)
harrow(2, 0, "파일 해시 계산")
harrow(2, 1, "원본 payload 와 대조")

d.legend(456, [("핵심 처리 · 도구", INFO), ("정상 완료 · 검증", OK), ("타임아웃 재전송", WARN)])
d.save("06-02.chapter-overview.svg")
print("ok 06-02 overview")
