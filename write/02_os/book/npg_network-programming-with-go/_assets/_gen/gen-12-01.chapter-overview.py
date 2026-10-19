# 타입 스펙: type-architecture
# 사실 출처: NPG Ch.12 Data Serialization, RFC 8259, encoding/gob, protobuf.dev
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 750

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

def nx(j):
    return COL_X + j * STRIDE

def ny(i):
    return ROW_Y + i * ROW_STRIDE

d = D(W, H, "ARCHITECTURE · 12-01 OVERVIEW",
      "직렬화 흐름과 Go 의 세 직렬화 형식 JSON·Gob·protobuf",
      "12-01 의 키워드 개념도입니다. §1 줄은 Chore{…} 를 []byte 로 바꿔 보내고 받는 쪽이 복제본을 만드는 흐름입니다. "
      "§2 줄은 storage import 줄만 바꿔 저장 형식을 고르는 housework 앱입니다. "
      "§3 줄은 143 B 텍스트로 저장되지만 any 로 풀면 숫자가 float64 가 되는 JSON 입니다. "
      "§4 줄은 형식 정보를 값보다 먼저 싣는 105 B 의 Gob 입니다. "
      "§5 줄은 .proto 를 protoc 로 컴파일해 여러 언어가 같은 48 B 를 읽는 protobuf 입니다.",
      lead="화살표 위 글자는 두 단계 사이에서 일어나는 일, 왼쪽 칩은 그 줄을 다루는 절입니다.")

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

for i, sec in enumerate(("§1", "§2", "§3", "§4", "§5")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

# §1 직렬화 흐름
node(0, 0, "메모리 구조체", "Chore{…}", INFO)
node(0, 1, "바이트 열", "[]byte", OK)
node(0, 2, "받는 쪽 복제본", "같은 Chore{…}", ACC)
harrow(0, 0, "Encode·Marshal")
harrow(0, 1, "Decode·Unmarshal", ACC, "acc")

# §2 housework 저장 구조
node(1, 0, "명령 처리 코드", "list · add · complete", INFO)
node(1, 1, "storage 별칭", "Load(r) · Flush(w)", OK)
node(1, 2, "housework.db", "JSON · Gob · protobuf", ACC)
harrow(1, 0, "load · flush 호출")
harrow(1, 1, "import 줄로 선택", ACC, "acc")

# §3 JSON
node(2, 0, "공개 필드만", "Complete · Description", INFO)
node(2, 1, "JSON 텍스트", "143 B", OK)
node(2, 2, "any 로 풀 때", "숫자는 float64", ACC)
harrow(2, 0, "필드 이름 그대로")
harrow(2, 1, "number 하나", ACC, "acc")

# §4 Gob
node(3, 0, "형식 명세 2개", "13 B + 40 B", INFO)
node(3, 1, "값 메시지", "49 B", OK)
node(3, 2, "Go 디코더", "다른 언어용 아님", ACC)
harrow(3, 0, "명세 먼저")
harrow(3, 1, "105 B 파일", ACC, "acc")

# §5 Protocol Buffers
node(4, 0, "housework.proto", "필드 번호 1 · 2", INFO)
node(4, 1, "housework.pb.go", "Chore · Chores 타입", OK)
node(4, 2, "48 B 바이트", "언어별 코드가 같이 읽음", ACC)
harrow(4, 0, "protoc 컴파일")
harrow(4, 1, "proto.Marshal", ACC, "acc")

d.legend(690, [("입력·정의", INFO), ("변환 결과", OK), ("받는 쪽·결과", ACC)])
svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-01.chapter-overview.svg"
d.save(str(svg_path))
print("ok 12-01 chapter-overview")
