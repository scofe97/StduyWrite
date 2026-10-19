# 타입 스펙: type-architecture
# 사실 출처: 12-02 본문 §1~§4, gRPC PROTOCOL-HTTP2.md, 생성 코드 housework_grpc.pb.go, grpc-go v1.84.0 credentials/tls.go, 12-02 실행 결과
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 630

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def nx(j):
    return COL_X + j * STRIDE

def ny(i):
    return ROW_Y + i * ROW_STRIDE

d = D(W, H, "ARCHITECTURE · 12-02 OVERVIEW",
      "gRPC 서비스 정의와 TLS 서버 및 인증서 피닝 클라이언트",
      "12-02 의 개념도입니다. §1 줄은 client.List 호출이 POST /housework.RobotMaid/List 로 가서 grpc-status 0 트레일러와 함께 *Chores 로 돌아오는 길입니다. "
      "§2 줄은 service RobotMaid 가 protoc-gen-go-grpc 로 housework_grpc.pb.go 가 되어 RobotMaidServer 와 RobotMaidClient 를 내는 모습입니다. "
      "§3 줄은 Rosie 를 등록하고 grpc.Creds(credentials.NewTLS(cfg)) 를 건 grpc.Server 가 localhost:34443 에서 ALPN h2 로 받는 모습입니다. "
      "§4 줄은 cert.pem 하나를 RootCAs 로 넘기고 grpc.NewClient 로 만든 연결이 첫 RPC 때 열려 할 일 표를 찍기까지입니다.",
      lead="줄마다 한 절이고, 화살표 위 글자는 그 단계에서 일어나는 일입니다.")

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

# §1 호출 하나가 HTTP/2 요청으로
node(0, 0, "client.List", "ctx, &Empty{}", INFO)
node(0, 1, "HTTP/2 POST", "/housework.RobotMaid/List", OK)
node(0, 2, "*Chores 반환", "트레일러 grpc-status: 0", ACC)
harrow(0, 0, "스텁이 직렬화")
harrow(0, 1, "응답과 트레일러", ACC, "acc")

# §2 service 블록에서 두 쪽 코드로
node(1, 0, "service RobotMaid", "Add · Complete · List", INFO)
node(1, 1, "protoc-gen-go-grpc", "housework_grpc.pb.go", OK)
node(1, 2, "RobotMaidServer", "클라이언트는 RobotMaidClient", ACC)
harrow(1, 0, "protoc")
harrow(1, 1, "코드 생성", ACC, "acc")

# §3 등록한 Rosie 와 TLS 자격 증명을 건 서버
node(2, 0, "Rosie", "sync.Mutex 로 목록 보호", INFO)
node(2, 1, "grpc.Server", "grpc.Creds(NewTLS(cfg))", OK)
node(2, 2, "localhost:34443", "net.Listen 그대로 Serve", ACC)
harrow(2, 0, "등록")
harrow(2, 1, "ALPN h2 로 받음", ACC, "acc")

# §4 피닝한 인증서로 첫 RPC 때 연결
node(3, 0, "cert.pem", "RootCAs 풀에 이것 하나", INFO)
node(3, 1, "grpc.NewClient", "아직 연결 없음", OK)
node(3, 2, "# [X] Description", "Add·Complete 뒤 List", ACC)
harrow(3, 0, "TLS 자격 증명")
harrow(3, 1, "첫 RPC 때 연결", ACC, "acc")

d.legend(H - 42, [("시작 값", INFO), ("중간 단계", OK), ("결과", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-02.chapter-overview.svg"
d.save(str(svg_path))
print(f"ok {svg_path.name}")
