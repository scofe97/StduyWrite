# 11-02.chapter-overview — 상호 TLS 는 직접 만든 인증서로 클라이언트도 검증하고 서버는 접속 주소를 인증서 이름과 맞춘다
# 본문 요구(11-02 「학습 목표」 개념도 문단): §1 줄은 ClientAuth 와 ClientCAs 로 서버가 클라이언트에게 인증서를 요구하는 상호 인증 원리,
#           §2 줄은 x509 템플릿과 P-256 ECDSA 키 쌍으로 자체 서명 인증서와 개인키 PEM 파일을 만드는 과정,
#           §3 줄은 GetConfigForClient 로 소켓 IP 를 얻고 VerifyPeerCertificate 로 인증서 SAN 이름과 대조하는 서버 검증,
#           §4 줄은 tls.Dial 이후 첫 I/O 에서 핸드셰이크가 완료되고 상호 인증이 통과하는 시험 검증이다.
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(10-02 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표.
# 사실 출처: 《Network Programming with Go》 Ch.11 Securing Communications with TLS (Listing 11-12~11-22),
#           crypto/tls, crypto/x509, RFC 8446.
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


d = D(W, H, "ARCHITECTURE · 11-02 OVERVIEW",
      "상호 TLS 는 직접 만든 인증서로 클라이언트를 검증하고 접속 주소를 맞춥니다",
      "11-02 의 키워드 개념도. §1 줄은 ClientAuth 와 ClientCAs 로 서버가 클라이언트에게 인증서를 요구하고 신뢰 체인을 확인하는 상호 인증 원리다. "
      "§2 줄은 x509.Certificate 템플릿과 P-256 ECDSA 키 쌍을 결합해 자체 서명 인증서와 개인키 PEM 파일을 만드는 과정이다. "
      "§3 줄은 GetConfigForClient 로 소켓 IP 를 얻고 VerifyPeerCertificate 로 역방향 DNS 및 인증서 SAN 이름을 대조하는 서버 검증이다. "
      "§4 줄은 tls.Dial 이 클라이언트 쪽 핸드셰이크를 마친 뒤 첫 Write·Read 로 서버의 판정을 받는 시험이다.",
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

# §1 상호 TLS 는 서버도 클라이언트에게 인증서를 요구한다
node(0, 0, "ClientAuth 설정", "RequireAndVerify", INFO)
node(0, 1, "인증서 요청 전송", "CertificateRequest", ACC)
node(0, 2, "ClientCAs 신뢰 풀", "클라이언트 루트 검증", OK)
harrow(0, 0, "인증서 제출 강제", ACC, "acc")
harrow(0, 1, "발급 체인 검증", OK, "ok")

# §2 x509 템플릿으로 인증서와 키 쌍을 직접 만든다
node(1, 0, "x509.Certificate", "SAN · 키 용도 템플릿", INFO)
node(1, 1, "P-256 ECDSA", "GenerateKey 비대칭키", INFO)
node(1, 2, "PEM 파일 생성", "cert.pem · key.pem", OK)
harrow(1, 0, "자체 서명 바인딩", INFO, "info")
harrow(1, 1, "DER 블록 인코딩", OK, "ok")

# §3 서버는 클라이언트 인증서를 CA 풀로 검증하고 접속 주소와 인증서 이름을 맞춘다
node(2, 0, "GetConfigForClient", "hello.Conn 소켓 IP", INFO)
node(2, 1, "LookupAddr PTR", "역방향 호스트명 조회", INFO)
node(2, 2, "Peer 인증서 검증", "SAN 호스트명 대조", OK)
harrow(2, 0, "접속 IP 추출", INFO, "info")
harrow(2, 1, "opts.DNSName 대조", OK, "ok")

# §4 시험으로 상호 인증 핸드셰이크를 끝까지 확인한다
node(3, 0, "tls.Dial 반환", "클라이언트 쪽 완료", INFO)
node(3, 1, "첫 Read", "서버 판정 수신", ACC)
node(3, 2, "에코 확인", "hello 그대로 수신", OK)
harrow(3, 0, "Write hello", ACC, "acc")
harrow(3, 1, "경고 없음", OK, "ok")

d.legend(584, [("설정 및 템플릿", INFO), ("핸드셰이크 트리거", ACC), ("검증 및 완료", OK)])
out_path = pathlib.Path(__file__).resolve().parent.parent / "11-02.chapter-overview.svg"
d.save(str(out_path))
print("ok 11-02 overview:", out_path)
