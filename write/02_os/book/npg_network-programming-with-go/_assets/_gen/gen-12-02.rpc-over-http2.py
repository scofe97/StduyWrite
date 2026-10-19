# 타입 스펙: type-sequence
# 사실 출처: gRPC PROTOCOL-HTTP2.md(POST·경로·content-type·te·5바이트 머리·트레일러), 생성 코드 RobotMaid_List_FullMethodName, 12-02 실행(Empty 0바이트, 할 일 2건 Chores 29바이트)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, MONO, KR

W, H = 940, 610
s = Seq(W, H, "SEQUENCE · RPC OVER HTTP/2",
        "gRPC 로컬 호출 추상화와 HTTP/2 프레이밍 순서",
        "호출자 코드의 client.List 가 생성된 스텁에서 POST /housework.RobotMaid/List HEADERS 와 5바이트 머리만 있는 DATA 로 나가고, "
        "Rosie.List 의 결과 Chores 29바이트가 grpc-status 0 트레일러와 함께 돌아와 *Chores 로 반환되는 순서입니다.",
        lead="함수 호출 한 번이 HTTP/2 스트림 하나가 되고, 결과는 트레일러의 grpc-status 로 정해집니다.")

s.lanes([("호출자 코드", "list()"),
         ("클라이언트 스텁", "RobotMaidClient"),
         ("gRPC 서버", "Rosie")],
        y0=104, lane_w=190)

def selfmsg_left(seq, lane, label, y, c, sub=None):
    x = seq.LX[lane]
    seq.path(f"M {x-10} {y-10} L {x-40} {y-10} L {x-40} {y+10} L {x-13} {y+10}", c, 1.4, m="ar")
    seq.t(x - 48, y - 4, label, 11, c, MONO, "end", 600)
    if sub:
        seq.t(x - 48, y + 13, sub, 11, MUTED, KR, "end")

s.msg("호출자 코드", "클라이언트 스텁", "client.List(ctx, &Empty{})", 180, INFO, "info",
      sub="평범한 메서드 호출")

s.selfmsg("클라이언트 스텁", "Empty → 0바이트", 232, ACC,
          sub="새 스트림 하나")

s.msg("클라이언트 스텁", "gRPC 서버", "HEADERS  POST /housework.RobotMaid/List", 292, OK, "ok",
      sub="content-type: application/grpc · te: trailers")

s.msg("클라이언트 스텁", "gRPC 서버", "DATA  00 00 00 00 00", 352, OK, "ok",
      sub="압축 0 · 길이 0 · 본문 없음")

selfmsg_left(s, "gRPC 서버", "Rosie.List()", 404, ACC,
             sub="mu.Lock() 뒤 r.chores 를 담아 반환")

s.msg("gRPC 서버", "클라이언트 스텁", "DATA  00 00 00 00 1d + 29바이트", 464, OK, "ok",
      sub="할 일 2건 · 트레일러 grpc-status: 0")

s.msg("클라이언트 스텁", "호출자 코드", "(*Chores, nil)", 524, INFO, "info",
      sub="29바이트를 Go 구조체로")

s.rails(548)
s.legend(H - 48, [("호출자 코드", INFO), ("HTTP/2 프레임", OK), ("직렬화와 서버 처리", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-02.rpc-over-http2.svg"
s.save(str(svg_path))
print(f"ok {svg_path.name}")
