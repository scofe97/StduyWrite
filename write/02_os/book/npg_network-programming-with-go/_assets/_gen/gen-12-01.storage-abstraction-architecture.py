# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.12 Listing 12-2~12-4, 12-11, 12-13, 12-18
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 580
d = D(W, H, "ARCHITECTURE · STORAGE ABSTRACTION",
      "housework 명령 처리 코드와 storage 별칭 뒤의 세 저장 패키지",
      "명령 처리 코드는 storage 별칭의 Load·Flush 만 부르고, storage import 줄로 저장 패키지를 고릅니다. protobuf 로 갈 때는 housework import 도 v1 으로 바꿉니다.",
      lead="storage.Load 는 io.Reader, storage.Flush 는 io.Writer 를 받습니다.")

# 1. 상단: cmd/housework.go
d.tone(200, 100, 560, 72, INFO, 6, "14", 1.2)
d.t(480, 128, "cmd/housework.go", 14, INFO, MONO, "middle", 600)
d.t(480, 150, "list · add · complete · load · flush", 11, MUTED, KR, "middle")

# 아래 화살표
d.arrow([(480, 172), (480, 216)], c=SOFT, m="soft")
d.t(490, 196, "storage.Load(df) · storage.Flush(df, chores)", 11, MUTED, MONO, "start")

# 2. 중간: storage 계약 인터페이스
d.tone(140, 220, 680, 80, OK, 6, "14", 1.2)
d.t(480, 248, "storage 별칭 (Load · Flush)", 14, OK, KR, "middle", 600)
d.t(480, 270, "Load(r io.Reader) ([]*Chore, error)  |  Flush(w io.Writer, chores []*Chore) error", 11, INK, MONO, "middle")
d.t(480, 288, "storage \".../json\" · \".../gob\" · \".../protobuf\" 가운데 한 줄", 11, MUTED, KR, "middle")

# 아래 3분기 화살표
for x_dst in (180, 480, 780):
    d.arrow([(x_dst, 300), (x_dst, 344)], c=SOFT, m="soft")

# 3. 하단 세 엔진
# Engine 1: json
d.tone(60, 348, 240, 76, ACC, 6, "14", 1.1)
d.t(180, 374, "json/housework.go", 13, ACC, MONO, "middle", 600)
d.t(180, 394, "json.NewDecoder(r).Decode", 11, INK, MONO, "middle")
d.t(180, 410, "json.NewEncoder(w).Encode", 11, MUTED, MONO, "middle")

# Engine 2: gob
d.tone(360, 348, 240, 76, ACC, 6, "14", 1.1)
d.t(480, 374, "gob/housework.go", 13, ACC, MONO, "middle", 600)
d.t(480, 394, "gob.NewDecoder(r).Decode", 11, INK, MONO, "middle")
d.t(480, 410, "gob.NewEncoder(w).Encode", 11, MUTED, MONO, "middle")

# Engine 3: protobuf
d.tone(660, 348, 240, 76, ACC, 6, "14", 1.1)
d.t(780, 374, "protobuf/housework.go", 13, ACC, MONO, "middle", 600)
d.t(780, 394, "io.ReadAll + proto.Unmarshal", 11, INK, MONO, "middle")
d.t(780, 410, "proto.Marshal + w.Write", 11, MUTED, MONO, "middle")

# 하단 수렴 화살표 (직교 라우팅)
d.arrow([(180, 424), (180, 448), (460, 448), (460, 468)], c=SOFT, m="soft")
d.arrow([(480, 424), (480, 468)], c=SOFT, m="soft")
d.arrow([(780, 424), (780, 448), (500, 448), (500, 468)], c=SOFT, m="soft")

# 4. 저장 파일: housework.db
d.tone(340, 472, 280, 46, INFO, 6, "14", 1.1)
d.t(480, 494, "housework.db", 13, INFO, MONO, "middle", 600)
d.t(480, 509, "143 B · 105 B · 48 B", 11, MUTED, MONO, "middle")

d.legend(534, [("명령 처리·파일", INFO), ("storage 별칭", OK), ("저장 패키지", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-01.storage-abstraction-architecture.svg"
d.save(str(svg_path))
print("ok 12-01 storage-abstraction-architecture")
