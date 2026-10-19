# 타입 스펙: type-architecture
# 사실 출처: 12-02 의 housework.proto 와 protoc 33.2·protoc-gen-go v1.36.11·protoc-gen-go-grpc 1.6.1 로 실제 생성한 housework.pb.go·housework_grpc.pb.go
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 940, 470
d = D(W, H, "ARCHITECTURE · PROTOBUF CODEGEN",
      "proto 서비스 정의와 protoc-gen-go-grpc 코드 생성",
      "housework.proto 의 service RobotMaid 를 protoc 가 두 플러그인으로 넘겨 housework.pb.go 와 housework_grpc.pb.go 를 만들고, "
      "housework_grpc.pb.go 에서 클라이언트 쪽 RobotMaidClient·NewRobotMaidClient 와 서버 쪽 RobotMaidServer·UnimplementedRobotMaidServer·RegisterRobotMaidServer 가 나옵니다.",
      lead="service 블록 하나에서 클라이언트가 부를 스텁과 서버가 채울 인터페이스가 함께 나옵니다.")

# 왼쪽: proto 정의
LX, LY, LW, LH = 40, 130, 250, 230
d.tone(LX, LY, LW, LH, INFO, 8, "10", 1.2)
d.t(LX + LW / 2, LY + 32, "housework.proto", 14, INFO, MONO, "middle", 600)
d.t(LX + LW / 2, LY + 54, "service RobotMaid", 11, MUTED, MONO, "middle")
d.line(LX + 20, LY + 70, LX + LW - 20, LY + 70, RULE, 0.8)
d.t(LX + 20, LY + 98, "rpc Add (Chores)", 11, INK, MONO, "start")
d.t(LX + 20, LY + 126, "rpc Complete (CompleteRequest)", 11, INK, MONO, "start")
d.t(LX + 20, LY + 154, "rpc List (Empty)", 11, INK, MONO, "start")
d.t(LX + 20, LY + 196, "List 의 빈 요청도 Empty", 11, MUTED, KR, "start")

# 가운데: protoc 와 두 플러그인
MX, MY, MW, MH = 350, 150, 230, 190
d.arrow([(LX + LW + 4, LY + LH / 2), (MX - 6, LY + LH / 2)], INFO, "info", 1.5)
d.tone(MX, MY, MW, MH, OK, 8, "14", 1.2)
d.t(MX + MW / 2, MY + 30, "protoc", 14, OK, MONO, "middle", 600)
d.line(MX + 16, MY + 46, MX + MW - 16, MY + 46, RULE, 0.8)
d.t(MX + 18, MY + 74, "protoc-gen-go", 11, INK, MONO, "start", 600)
d.t(MX + 18, MY + 94, "housework.pb.go", 11, MUTED, MONO, "start")
d.t(MX + 18, MY + 130, "protoc-gen-go-grpc", 11, INK, MONO, "start", 600)
d.t(MX + 18, MY + 150, "housework_grpc.pb.go", 11, MUTED, MONO, "start")

# 분기 화살표 (housework_grpc.pb.go 줄에서 갈라진다)
BX = MX + MW + 40
SY = MY + 140
d.arrow([(MX + MW + 4, SY), (BX, SY), (BX, 175), (636, 175)], ACC, "acc", 1.4)
d.arrow([(MX + MW + 4, SY), (BX, SY), (BX, 330), (636, 330)], ACC, "acc", 1.4)

# 오른쪽 위: 클라이언트 스텁
d.box(640, 120, 270, 110, stroke=ACC, sw=1.1)
d.chip(775, 135, "클라이언트 스텁", ACC, 11, 6)
d.t(660, 175, "RobotMaidClient", 11, INK, MONO, "start")
d.t(660, 205, "NewRobotMaidClient(cc)", 11, OK, MONO, "start")

# 오른쪽 아래: 서버 인터페이스
d.box(640, 255, 270, 150, stroke=ACC, sw=1.1)
d.chip(775, 270, "서버 인터페이스", ACC, 11, 6)
d.t(660, 310, "RobotMaidServer", 11, INK, MONO, "start")
d.t(660, 338, "UnimplementedRobotMaidServer", 11, INK, MONO, "start")
d.t(660, 357, "값으로 품음 · 새 메서드는 Unimplemented", 11, MUTED, KR, "start")
d.t(660, 386, "RegisterRobotMaidServer", 11, OK, MONO, "start")

d.legend(H - 48, [("proto 정의", INFO), ("protoc 와 플러그인", OK), ("생성된 Go 코드", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-02.proto-codegen.svg"
d.save(str(svg_path))
print(f"ok {svg_path.name}")
