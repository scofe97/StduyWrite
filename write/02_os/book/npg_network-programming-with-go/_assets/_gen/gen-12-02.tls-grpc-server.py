# 타입 스펙: type-sequence
# 사실 출처: RFC 8446 §2·§4.3.1(ALPN 은 EncryptedExtensions), RFC 9113 §3.4(프리페이스·SETTINGS), gRPC PROTOCOL-HTTP2.md, grpc-go v1.84.0 credentials/tls.go, 12-02 실행(TLSv1.3·ALPN h2, Chores 29바이트, Response 4바이트)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, MONO, KR

W, H = 880, 780
s = Seq(W, H, "SEQUENCE · TLS GRPC SERVER FLOW",
        "TLS 1.3 ALPN 협상과 Rosie 서버 메서드 실행 순서",
        "Rosie 를 등록한 grpc.Server 가 localhost:34443 에서 TLS 1.3 핸드셰이크로 ALPN h2 를 고르고, "
        "HTTP/2 프리페이스와 SETTINGS 를 주고받은 뒤 Add 요청을 받아 Rosie.Add 를 부르는 순서입니다.",
        lead="ALPN 으로 h2 를 고른 연결에서만 HTTP/2 프리페이스와 gRPC 요청이 오갑니다.")

s.lanes([("gRPC 클라이언트", "client.go"),
         ("gRPC 서버", "localhost:34443")],
        y0=104, lane_w=220)

def selfmsg_left(seq, lane, label, y, c, sub=None):
    x = seq.LX[lane]
    seq.path(f"M {x-10} {y-10} L {x-40} {y-10} L {x-40} {y+10} L {x-13} {y+10}", c, 1.4, m="ar")
    seq.t(x - 48, y - 4, label, 11, c, MONO, "end", 600)
    if sub:
        seq.t(x - 48, y + 13, sub, 11, MUTED, KR, "end")

Y0, DY = 180, 52

def y(i):
    return Y0 + i * DY

selfmsg_left(s, "gRPC 서버", "RegisterRobotMaidServer(server, rosie)", y(0), ACC,
             sub="Serve 전에 등록")

s.msg("gRPC 클라이언트", "gRPC 서버", "ClientHello", y(1), INFO, "info",
      sub="ALPN 후보 h2 · P-256 키 공유")
s.msg("gRPC 서버", "gRPC 클라이언트", "ServerHello", y(2), INFO, "info",
      sub="TLS 1.3 · 여기부터 암호화")
s.msg("gRPC 서버", "gRPC 클라이언트", "EncryptedExtensions (ALPN: h2)", y(3), WARN, "warn",
      sub="비어 있으면 클라이언트가 끊음")
s.msg("gRPC 서버", "gRPC 클라이언트", "Certificate · CertificateVerify · Finished", y(4), INFO, "info",
      sub="cert.pem 을 RootCAs 로 확인")
s.msg("gRPC 클라이언트", "gRPC 서버", "Finished", y(5), INFO, "info")

s.msg("gRPC 클라이언트", "gRPC 서버", "PRI * HTTP/2.0 + SETTINGS", y(6), OK, "ok",
      sub="클라이언트 프리페이스")
s.msg("gRPC 서버", "gRPC 클라이언트", "SETTINGS · SETTINGS ACK", y(7), OK, "ok",
      sub="서버 프리페이스 · 양쪽이 ACK")
s.msg("gRPC 클라이언트", "gRPC 서버", "POST /housework.RobotMaid/Add", y(8), OK, "ok",
      sub="DATA 00 00 00 00 1d + Chores 29바이트")

selfmsg_left(s, "gRPC 서버", "Rosie.Add · mu.Lock()", y(9), ACC,
             sub="r.chores 에 2건 추가")

s.msg("gRPC 서버", "gRPC 클라이언트", "HEADERS · DATA · 트레일러", y(10), OK, "ok",
      sub="Response 4바이트 · grpc-status: 0")

s.rails(y(10) + 30)
s.legend(H - 48, [("TLS 핸드셰이크", INFO), ("ALPN 결정", WARN), ("HTTP/2·gRPC", OK), ("서버 안 처리", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-02.tls-grpc-server.svg"
s.save(str(svg_path))
print(f"ok {svg_path.name}")
