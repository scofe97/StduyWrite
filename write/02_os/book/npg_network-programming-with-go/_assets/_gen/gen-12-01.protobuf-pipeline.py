# 타입 스펙: type-process
# 사실 출처: protobuf.dev, protoc, protoc-gen-go, NPG Ch.12 Listing 12-16~12-19
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 980, 480
d = D(W, H, "PROCESS · PROTOCOL BUFFERS PIPELINE",
      "Protocol Buffers 정의에서 48 B 파일까지",
      ".proto 정의를 protoc 와 protoc-gen-go 로 컴파일해 housework.pb.go 를 만들고, proto.Marshal 로 할 일 세 건을 48 B 로 씁니다.",
      lead="proto 패키지에는 Encoder·Decoder 가 없어 []byte 를 직접 읽고 씁니다.")

stages = [
    ("1. 메시지 정의", "v1/housework.proto",
     ["syntax = \"proto3\"", "message Chore / Chores", "complete = 1", "description = 2"], INFO),
    ("2. protoc 컴파일", "protoc-gen-go v1.36.11",
     ["--go_out=.", "--go_opt=", "paths=source_relative", "출력 housework/v1/"], INFO),
    ("3. 생성된 Go 코드", "housework.pb.go",
     ["type Chore struct", "type Chores struct", "Chores []*Chore", "DO NOT EDIT"], OK),
    ("4. 바이트 변환", "proto.Marshal",
     ["proto.Marshal(&Chores)", "proto.Unmarshal(b, &c)", "io.ReadAll · w.Write", "Encoder·Decoder 없음"], OK),
    ("5. 저장된 바이트", "housework.db · 48 B",
     ["0a 0c 12 0a 4d 6f …", "false 필드는 생략", "이름 없이 번호만", "다른 언어도 같은 .proto"], ACC),
]

BW, BH = 168, 240
Y0 = 130

for idx, (title, sub, items, c) in enumerate(stages):
    x = 26 + idx * 190
    d.tone(x, Y0, BW, BH, c, 6, "14", 1.2)
    d.t(x + BW / 2, Y0 + 28, title, 13, c, KR, "middle", 600)
    d.t(x + BW / 2, Y0 + 48, sub, 11, INK, MONO, "middle")
    d.line(x + 10, Y0 + 60, x + BW - 10, Y0 + 60, RULE, 0.8)

    y_item = Y0 + 86
    for it in items:
        d.t(x + BW / 2, y_item, it, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in it) else MONO, "middle")
        y_item += 34

    if idx < 4:
        x_arr_start = x + BW + 2
        x_arr_end = x + BW + 20
        d.arrow([(x_arr_start, Y0 + BH / 2), (x_arr_end, Y0 + BH / 2)], c=SOFT, m="soft", sw=1.3)

d.legend(410, [("정의·도구", INFO), ("생성 코드·API", OK), ("결과 48 B", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-01.protobuf-pipeline.svg"
d.save(str(svg_path))
print("ok 12-01 protobuf-pipeline")
