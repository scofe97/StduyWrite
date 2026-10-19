# 타입 스펙: type-dp-security-matrix
# 사실 출처: NPG Ch.12, RFC 8259, protobuf.dev, encoding/gob, 실측 결과
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 1000, 640
d = D(W, H, "COMPARISON · SERIALIZATION FORMATS",
      "JSON·Gob·Protocol Buffers 의 크기와 특성 비교",
      "같은 할 일 세 건을 저장한 바이트 수와 가독성, 다른 언어 지원, 스키마 파일, Go API 를 견줍니다.",
      lead="크기는 할 일 세 건(Mop floors, Clean dishes[X], Mow the lawn)을 housework.db 에 쓴 바이트 수이고, 괄호는 JSON 대비 비율입니다.")

# 3개 컬럼 X 좌표 및 카드
cols = [
    ("JSON (텍스트)", "143 B (100%)", INFO, 180),
    ("Gob (Go 전용 이진)", "105 B (73%)", WARN, 450),
    ("Protocol Buffers (다언어)", "48 B (34%)", OK, 720)
]
CW = 240

# 상단 메트릭 카드 (크기)
for title, size_str, c, x in cols:
    d.tone(x, 110, CW, 70, c, 6, "14", 1.2)
    d.t(x + CW / 2, 134, title, 13, c, KR, "middle", 600)
    d.t(x + CW / 2, 162, size_str, 16, INK, MONO, "middle", 600)

rows = [
    ("데이터 표현",
     "UTF-8 텍스트",
     "형식 명세 + 값 (자기 기술)",
     "필드 번호 태그 + 값"),
    ("사람 가독성",
     "cat 으로 바로 읽음",
     "hexdump 필요",
     "hexdump 필요"),
    ("다른 언어",
     "대부분 언어에 공식 라이브러리",
     "Go 중심 (다른 언어용 아님)",
     "protoc 가 코드를 만드는 언어"),
    ("스키마 파일",
     "없음 (구조체 태그)",
     "없음 (명세를 함께 보냄)",
     "필수 (.proto)"),
    ("Go 인코딩 API",
     "json.NewEncoder / Decoder",
     "gob.NewEncoder / Decoder",
     "proto.Marshal / Unmarshal"),
    ("맞는 자리",
     "브라우저 · 공개 REST API",
     "Go 서비스끼리 · 로컬 저장",
     "여러 언어 서비스 · 작은 크기")
]

Y_START = 200
ROW_H = 60

for r_idx, (attr, val_json, val_gob, val_pb) in enumerate(rows):
    y = Y_START + r_idx * ROW_H
    fill = "#161B22" if r_idx % 2 == 0 else "#0D1117"
    d.box(40, y, W - 80, ROW_H - 8, fill=fill, stroke=RULE, sw=0.6)

    # 속성 라벨 (좌측 바)
    d.t(54, y + 28, attr, 11, SOFT, KR, "start", 600)

    fam = lambda v: KR if any("가" <= ch <= "힣" for ch in v) else MONO
    d.t(300, y + 28, val_json, 11, INK, fam(val_json), "middle")
    d.t(570, y + 28, val_gob, 11, INK, fam(val_gob), "middle")
    d.t(840, y + 28, val_pb, 11, INK, fam(val_pb), "middle")

d.legend(580, [("JSON", INFO), ("Gob", WARN), ("Protocol Buffers", OK)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-01.serialization-format-comparison.svg"
d.save(str(svg_path))
print("ok 12-01 serialization-format-comparison")
